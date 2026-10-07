/* sa_hunt128.c — two-phase annealing hunt in the [65,127] window (128-bit masks).
 *
 * Target: cubic graphs on n in [66,126] (even). Forbidden power-of-2 lengths
 * there are {4,8,16,32,64}.
 *
 * Phase 1: minimize E = 10*#C4 + 5*#C8 + 2*#C16 (exact counts). On E=0 the
 *          graph is {4,8,16}-free — logged (notable object at these sizes).
 * Phase 2: moves constrained to keep {4,8,16}-freeness (through-edge existence
 *          checks on the two new edges); objective = #C32 counted under a node
 *          budget (cap-hit => treated as cap). On reaching budgeted count 0,
 *          run the exact MITM C32 test; if truly C32-free, print PHASE3
 *          CANDIDATE (g6) and exit 43 — the supervisor then runs the external
 *          C64 oracle (Glasgow). C128 does not fit below n=128.
 *
 * Usage: sa_hunt128 n seed [max_moves]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;
#define MAXV 128

static u128 adj[MAXV];
static int N;
static u64 rng_s[2];

static u64 xr(void)
{
    u64 s0 = rng_s[0], s1 = rng_s[1];
    u64 r = s0 + s1;
    s1 ^= s0;
    rng_s[0] = ((s0 << 55) | (s0 >> 9)) ^ s1 ^ (s1 << 14);
    rng_s[1] = (s1 << 36) | (s1 >> 28);
    return r;
}
static int rnd(int m) { return (int)(xr() % (u64)m); }

static inline int ctz128(u128 x)
{
    u64 lo = (u64)x;
    if (lo) return __builtin_ctzll(lo);
    return 64 + __builtin_ctzll((u64)(x >> 64));
}
static inline int pop128(u128 x)
{
    return __builtin_popcountll((u64)x) + __builtin_popcountll((u64)(x >> 64));
}
static inline u128 bit128(int i) { return (u128)1 << i; }

/* ---- exact cycle counting with optional node budget ---- */
static long cnt;
static int Lt;
static int dist_s[MAXV];
static u128 allowed;
static long node_budget;        /* <0: unlimited */
static int budget_hit;

static void bfs(int src)
{
    int q[MAXV], qh = 0, qt = 0;
    u128 seen = bit128(src);
    for (int u = 0; u < N; u++) dist_s[u] = 1 << 20;
    dist_s[src] = 0;
    q[qt++] = src;
    while (qh < qt) {
        int u = q[qh++];
        u128 nb = adj[u] & allowed & ~seen;
        while (nb) {
            int w = ctz128(nb);
            nb &= nb - 1;
            seen |= bit128(w);
            dist_s[w] = dist_s[u] + 1;
            q[qt++] = w;
        }
    }
}

static int second_v;
static void dfs_count(int u, int depth, u128 onpath, int s)
{
    if (budget_hit) return;
    if (node_budget >= 0 && --node_budget < 0) { budget_hit = 1; return; }
    if (depth == Lt - 1) {
        if ((adj[u] & bit128(s)) && second_v < u) cnt++;
        return;
    }
    u128 nb = adj[u] & allowed & ~onpath;
    while (nb && !budget_hit) {
        int w = ctz128(nb);
        nb &= nb - 1;
        if (dist_s[w] <= Lt - depth - 1)
            dfs_count(w, depth + 1, onpath | bit128(w), s);
    }
}

/* count cycles of length L; if budget >= 0 and exceeded, returns >= cap marker */
static long count_cycles_b(int L, long budget)
{
    if (L > N) return 0;
    cnt = 0;
    Lt = L;
    node_budget = budget;
    budget_hit = 0;
    for (int s = 0; s < N && !budget_hit; s++) {
        allowed = 0;
        for (int i = s; i < N; i++) allowed |= bit128(i);
        bfs(s);
        u128 nb = adj[s] & allowed;
        while (nb && !budget_hit) {
            int w = ctz128(nb);
            nb &= nb - 1;
            if (dist_s[w] <= L - 1) {
                second_v = w;
                dfs_count(w, 1, bit128(s) | bit128(w), s);
            }
        }
    }
    if (budget_hit) return cnt + 1000000;     /* "at least this many" marker */
    return cnt;
}
static long count_cycles(int L) { return count_cycles_b(L, -1); }

static long energy1(void)
{
    return 10 * count_cycles(4) + 5 * count_cycles(8) + 2 * count_cycles(16);
}

/* ---- through-edge existence of C_L using edge (a,b): path a..b of length L-1 */
static int exist_found;
static int target_b, plen_need;
static void dfs_exist(int u, int depth, u128 onpath)
{
    if (exist_found) return;
    if (depth == plen_need) {
        if (u == target_b) exist_found = 1;
        return;
    }
    u128 nb = adj[u] & ~onpath;
    while (nb && !exist_found) {
        int w = ctz128(nb);
        nb &= nb - 1;
        if (dist_s[w] <= plen_need - depth)
            dfs_exist(w, depth + 1, onpath | bit128(w));
    }
}
static int cycle_through_edge(int a, int b, int L)
{
    /* distances to b avoiding nothing (upper-bound-free prune) */
    allowed = 0;
    for (int i = 0; i < N; i++) allowed |= bit128(i);
    bfs(b);
    if (dist_s[a] > L - 1) return 0;
    exist_found = 0;
    target_b = b;
    plen_need = L - 1;
    dfs_exist(a, 0, bit128(a));
    return exist_found;
}
static int edge_makes_small_p2(int a, int b)
{
    return cycle_through_edge(a, b, 4) || cycle_through_edge(a, b, 8) ||
           cycle_through_edge(a, b, 16);
}

/* ---- exact MITM C32 (128-bit masks) ---- */
typedef struct { u128 mask; } pr;
static pr *bk[MAXV];
static int bc[MAXV], bcap_[MAXV];
static void push(int w, u128 m)
{
    if (bc[w] == bcap_[w]) {
        bcap_[w] = bcap_[w] ? 2 * bcap_[w] : 64;
        bk[w] = realloc(bk[w], bcap_[w] * sizeof(pr));
        if (!bk[w]) { fprintf(stderr, "OOM\n"); exit(2); }
    }
    bk[w][bc[w]++].mask = m;
}
static void ep(int u, int depth, u128 onpath, int h)
{
    if (depth == h) { push(u, onpath); return; }
    u128 nb = adj[u] & allowed & ~onpath;
    while (nb) {
        int w = ctz128(nb);
        nb &= nb - 1;
        ep(w, depth + 1, onpath | bit128(w), h);
    }
}
static int has_c32_exact(void)
{
    if (N < 32) return 0;
    for (int s = 0; s < N; s++) {
        allowed = 0;
        for (int i = s; i < N; i++) allowed |= bit128(i);
        for (int w = 0; w < N; w++) bc[w] = 0;
        ep(s, 0, bit128(s), 16);
        for (int w = s + 1; w < N; w++) {
            u128 both = bit128(s) | bit128(w);
            for (int i = 0; i < bc[w]; i++)
                for (int j = i + 1; j < bc[w]; j++)
                    if ((bk[w][i].mask & bk[w][j].mask) == both) return 1;
        }
    }
    return 0;
}

/* ---- graph6 (n <= 126 fits the 1-byte + padding case? no: n>62 needs the
 * 4-byte form: 126 then 3 sextets) ---- */
static void print_g6(FILE *f)
{
    if (N <= 62) fputc(N + 63, f);
    else {
        fputc(126, f);
        fputc(63 + ((N >> 12) & 63), f);
        fputc(63 + ((N >> 6) & 63), f);
        fputc(63 + (N & 63), f);
    }
    int bits = 0, acc = 0;
    for (int j = 1; j < N; j++)
        for (int i = 0; i < j; i++) {
            acc = (acc << 1) | (int)((adj[i] >> j) & 1);
            if (++bits == 6) { fputc(acc + 63, f); bits = 0; acc = 0; }
        }
    if (bits) fputc((acc << (6 - bits)) + 63, f);
    fputc('\n', f);
}

static void random_cubic(void)
{
    int stubs[3 * MAXV];
    for (;;) {
        for (int i = 0; i < 3 * N; i++) stubs[i] = i / 3;
        for (int i = 0; i < N; i++) adj[i] = 0;
        for (int i = 3 * N - 1; i > 0; i--) {
            int j = rnd(i + 1), t = stubs[i];
            stubs[i] = stubs[j]; stubs[j] = t;
        }
        int ok = 1;
        for (int i = 0; i < 3 * N && ok; i += 2) {
            int a = stubs[i], b = stubs[i + 1];
            if (a == b || (int)((adj[a] >> b) & 1)) ok = 0;
            else { adj[a] |= bit128(b); adj[b] |= bit128(a); }
        }
        if (ok) return;
    }
}

static int pick_nbr(int v)
{
    int k = rnd(pop128(adj[v]));
    u128 t = adj[v];
    while (k--) t &= t - 1;
    return ctz128(t);
}

int main(int argc, char **argv)
{
    N = atoi(argv[1]);
    u64 seed = argc > 2 ? strtoull(argv[2], 0, 10) : 1;
    long maxmoves = argc > 3 ? atol(argv[3]) : 5000000;
    rng_s[0] = seed ^ 0x9E3779B97F4A7C15ULL;
    rng_s[1] = seed * 0xBF58476D1CE4E5B9ULL + 1;
    if (N % 2 || N < 66 || N > 126) { fprintf(stderr, "n must be even, 66..126\n"); return 2; }

    random_cubic();
    int phase = 1;
    long E = energy1(), bestE = E, best2 = 1L << 60;
    double T = 20.0;
    long stall = 0;
    for (long mv = 0; mv < maxmoves; mv++) {
        if (mv % 500000 == 0 && mv)
            fprintf(stderr, "[n=%d seed=%llu] mv=%ldk phase=%d E=%ld bestE=%ld best2=%ld T=%.2f\n",
                    N, (unsigned long long)seed, mv / 1000, phase, E, bestE,
                    best2 >= (1L << 60) ? -1 : best2, T), fflush(stderr);
        if (mv % 2000 == 0) {
            T *= 0.995;
            if (T < 0.3) T = 0.3;
        }
        int a, b, c, d, tries = 0;
        u128 sav_a, sav_b, sav_c, sav_d;
        do {
            a = rnd(N); b = pick_nbr(a);
            c = rnd(N); d = pick_nbr(c);
            if (++tries > 200) break;
        } while (a == c || a == d || b == c || b == d ||
                 (int)((adj[a] >> c) & 1) || (int)((adj[b] >> d) & 1));
        if (a == c || a == d || b == c || b == d ||
            (int)((adj[a] >> c) & 1) || (int)((adj[b] >> d) & 1)) continue;
        sav_a = adj[a]; sav_b = adj[b]; sav_c = adj[c]; sav_d = adj[d];
        adj[a] &= ~bit128(b); adj[b] &= ~bit128(a);
        adj[c] &= ~bit128(d); adj[d] &= ~bit128(c);
        adj[a] |= bit128(c); adj[c] |= bit128(a);
        adj[b] |= bit128(d); adj[d] |= bit128(b);

        if (phase == 2) {
            /* must preserve {4,8,16}-freeness: only the new edges can create */
            if (edge_makes_small_p2(a, c) || edge_makes_small_p2(b, d)) {
                adj[a] = sav_a; adj[b] = sav_b; adj[c] = sav_c; adj[d] = sav_d;
                continue;
            }
            long E2 = count_cycles_b(32, 2000000);
            if (E2 <= E || exp((E - E2) / T) * 4294967296.0 > (double)(xr() & 0xFFFFFFFFu)) {
                E = E2;
                if (E < best2) {
                    best2 = E;
                    stall = 0;
                    fprintf(stderr, "[n=%d seed=%llu] phase2 best #C32=%ld\n",
                            N, (unsigned long long)seed, E);
                    if (E == 0 && !has_c32_exact()) {
                        fprintf(stderr, "*** PHASE3 CANDIDATE: {4,8,16,32}-free cubic n=%d — needs external C64 check ***\n", N);
                        print_g6(stdout);
                        fflush(stdout);
                        return 43;
                    }
                }
            } else {
                adj[a] = sav_a; adj[b] = sav_b; adj[c] = sav_c; adj[d] = sav_d;
            }
        } else {
            long E2 = energy1();
            if (E2 <= E || exp((E - E2) / T) * 4294967296.0 > (double)(xr() & 0xFFFFFFFFu)) {
                E = E2;
                if (E < bestE) {
                    bestE = E;
                    stall = 0;
                    if (E == 0) {
                        fprintf(stderr, "[n=%d seed=%llu] PHASE 1 COMPLETE: {4,8,16}-free cubic graph found — logging, entering phase 2\n",
                                N, (unsigned long long)seed);
                        print_g6(stdout);
                        fflush(stdout);
                        if (getenv("P2_PHASE1_ONLY")) return 44;
                        phase = 2;
                        E = count_cycles_b(32, 2000000);
                        best2 = E;
                        T = 6.0;
                        fprintf(stderr, "[n=%d seed=%llu] phase2 start #C32=%ld\n",
                                N, (unsigned long long)seed, E);
                    }
                }
            } else {
                adj[a] = sav_a; adj[b] = sav_b; adj[c] = sav_c; adj[d] = sav_d;
            }
        }
        if (++stall > 1500000) {
            random_cubic();
            phase = 1;
            E = energy1();
            T = 20.0;
            stall = 0;
        }
    }
    fprintf(stderr, "[n=%d seed=%llu] done: phase=%d bestE=%ld best2=%ld\n",
            N, (unsigned long long)seed, phase, bestE,
            best2 >= (1L << 60) ? -1 : best2);
    return 0;
}

/* sa_hunt.c — simulated-annealing hunt for cubic Erdős–Gyárfás counterexamples.
 *
 * State: a simple cubic (3-regular) graph on n vertices (n even, 34 <= n <= 62).
 * Energy: E = 10*#C4 + 5*#C8 + #C16  (exact counts, canonical enumeration).
 * Move:  random 2-edge rewiring preserving 3-regularity and simplicity.
 * When E = 0: test C32 exactly (meet-in-the-middle). If also C32-free, the graph
 * is a genuine counterexample (n < 64 so no further power-of-2 length fits):
 * print it loudly and exit 42.
 *
 * Usage: sa_hunt n seed [max_moves]
 * Reports best energy reached; writes zero-E-but-C32 graphs to stdout as g6
 * (interesting extremals: no C4/C8/C16).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

typedef uint64_t u64;
#define MAXV 64

static u64 adj[MAXV];
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

/* ---- exact cycle counting (canonical: min vertex root, dir by 2nd<last) ---- */
static long cnt;
static int Lt;
static int dist_s[MAXV];
static u64 allowed;

static void bfs(int src)
{
    int q[MAXV], qh = 0, qt = 0;
    u64 seen = 1ULL << src;
    for (int u = 0; u < N; u++) dist_s[u] = 1 << 20;
    dist_s[src] = 0;
    q[qt++] = src;
    while (qh < qt) {
        int u = q[qh++];
        u64 nb = adj[u] & allowed & ~seen;
        while (nb) {
            int w = __builtin_ctzll(nb);
            nb &= nb - 1;
            seen |= 1ULL << w;
            dist_s[w] = dist_s[u] + 1;
            q[qt++] = w;
        }
    }
}

static int second_v;
static int cap_path[64];        /* current DFS path (vertices) */
static int cap_cycle[64];       /* reservoir-sampled cycle of length Lt */
static int cap_have;
static void dfs_count(int u, int depth, u64 onpath, int s)
{
    cap_path[depth] = u;
    if (depth == Lt - 1) {
        if ((adj[u] & (1ULL << s)) && second_v < u) {
            cnt++;
            if ((long)(xr() % (u64)cnt) == 0) {   /* reservoir: keep with prob 1/cnt */
                cap_path[0] = s;
                for (int i = 0; i < Lt; i++) cap_cycle[i] = cap_path[i];
                cap_have = 1;
            }
        }
        return;
    }
    u64 nb = adj[u] & allowed & ~onpath;
    while (nb) {
        int w = __builtin_ctzll(nb);
        nb &= nb - 1;
        if (dist_s[w] <= Lt - depth - 1)
            dfs_count(w, depth + 1, onpath | (1ULL << w), s);
    }
}

static long count_cycles(int L)
{
    if (L > N) return 0;
    cnt = 0;
    Lt = L;
    cap_have = 0;
    for (int s = 0; s < N; s++) {
        allowed = 0;
        for (int i = s; i < N; i++) allowed |= 1ULL << i;
        bfs(s);
        u64 nb = adj[s] & allowed;
        while (nb) {
            int w = __builtin_ctzll(nb);
            nb &= nb - 1;
            if (dist_s[w] <= L - 1) {
                second_v = w;
                cap_path[0] = s;
                dfs_count(w, 1, (1ULL << s) | (1ULL << w), s);
            }
        }
    }
    return cnt;
}

static long energy(void)
{
    return 10 * count_cycles(4) + 5 * count_cycles(8) + count_cycles(16);
}

/* ---- MITM C32 existence (exact) ---- */
typedef struct { u64 mask; } pr;
static pr *bk[MAXV];
static int bc[MAXV], bcap_[MAXV];
static void push(int w, u64 m)
{
    if (bc[w] == bcap_[w]) {
        bcap_[w] = bcap_[w] ? 2 * bcap_[w] : 64;
        bk[w] = realloc(bk[w], bcap_[w] * sizeof(pr));
    }
    bk[w][bc[w]++].mask = m;
}
static void ep(int u, int depth, u64 onpath, int h)
{
    if (depth == h) { push(u, onpath); return; }
    u64 nb = adj[u] & allowed & ~onpath;
    while (nb) {
        int w = __builtin_ctzll(nb);
        nb &= nb - 1;
        ep(w, depth + 1, onpath | (1ULL << w), h);
    }
}
static int has_c32(void)
{
    if (N < 32) return 0;
    for (int s = 0; s < N; s++) {
        allowed = 0;
        for (int i = s; i < N; i++) allowed |= 1ULL << i;
        for (int w = 0; w < N; w++) bc[w] = 0;
        ep(s, 0, 1ULL << s, 16);
        for (int w = s + 1; w < N; w++) {
            u64 both = (1ULL << s) | (1ULL << w);
            for (int i = 0; i < bc[w]; i++)
                for (int j = i + 1; j < bc[w]; j++)
                    if ((bk[w][i].mask & bk[w][j].mask) == both) return 1;
        }
    }
    return 0;
}

/* ---- graph6 out ---- */
static void print_g6(FILE *f)
{
    fputc(N + 63, f);
    int bits = 0, acc = 0;
    for (int j = 1; j < N; j++)
        for (int i = 0; i < j; i++) {
            acc = (acc << 1) | ((adj[i] >> j) & 1);
            if (++bits == 6) { fputc(acc + 63, f); bits = 0; acc = 0; }
        }
    if (bits) fputc((acc << (6 - bits)) + 63, f);
    fputc('\n', f);
}

/* ---- random cubic graph via pairing until simple ---- */
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
            if (a == b || (adj[a] >> b & 1)) ok = 0;
            else { adj[a] |= 1ULL << b; adj[b] |= 1ULL << a; }
        }
        if (ok) return;
    }
}

int main(int argc, char **argv)
{
    N = atoi(argv[1]);
    u64 seed = argc > 2 ? strtoull(argv[2], 0, 10) : 12345;
    long maxmoves = argc > 3 ? atol(argv[3]) : 2000000;
    rng_s[0] = seed ^ 0x9E3779B97F4A7C15ULL;
    rng_s[1] = seed * 0xBF58476D1CE4E5B9ULL + 1;
    if (N % 2 || N < 8 || N > 62) { fprintf(stderr, "bad n\n"); return 2; }

    random_cubic();
    long E = energy(), bestE = E;
    double T = 20.0;
    long stall = 0;
    for (long mv = 0; mv < maxmoves; mv++) {
        if (mv % 1000000 == 0 && mv) {
            fprintf(stderr, "[n=%d seed=%llu] mv=%ldM E=%ld bestE=%ld T=%.2f\n",
                    N, (unsigned long long)seed, mv / 1000000, E, bestE, T);
            fflush(stderr);
        }
        if (mv % 2000 == 0) {
            T *= 0.995;
            if (T < 0.3) T = 0.3;
        }
        /* pick two disjoint edges; targeted mode rips an edge off a live C16 */
        int a, b, c, d, tries = 0;
        int targeted = 0;
        u64 sav[4];
        if (cap_have && rnd(10) < 7) {
            int k = rnd(16);
            int ta = cap_cycle[k], tb = cap_cycle[(k + 1) % 16];
            if (adj[ta] >> tb & 1) { targeted = 1; a = ta; b = tb; }
        }
        do {
            if (!targeted) a = rnd(N);
            u64 nb = adj[a];
            b = __builtin_ctzll(nb >> rnd(3) ? nb : nb);      /* rough pick */
            if (!targeted) {   /* uniform neighbor pick */
                int k = rnd(__builtin_popcountll(adj[a]));
                u64 t = adj[a];
                while (k--) t &= t - 1;
                b = __builtin_ctzll(t);
            }
            c = rnd(N);
            {
                int k = rnd(__builtin_popcountll(adj[c]));
                u64 t = adj[c];
                while (k--) t &= t - 1;
                d = __builtin_ctzll(t);
            }
            if (++tries > 3) targeted = 0;
            if (++tries > 200) break;
        } while (a == c || a == d || b == c || b == d ||
                 (adj[a] >> c & 1) || (adj[b] >> d & 1));
        if (a == c || a == d || b == c || b == d ||
            (adj[a] >> c & 1) || (adj[b] >> d & 1)) continue;
        sav[0] = adj[a]; sav[1] = adj[b]; sav[2] = adj[c]; sav[3] = adj[d];
        /* rewire ab, cd -> ac, bd */
        adj[a] &= ~(1ULL << b); adj[b] &= ~(1ULL << a);
        adj[c] &= ~(1ULL << d); adj[d] &= ~(1ULL << c);
        adj[a] |= 1ULL << c; adj[c] |= 1ULL << a;
        adj[b] |= 1ULL << d; adj[d] |= 1ULL << b;
        long E2 = energy();
        if (E2 <= E || exp((E - E2) / T) * 4294967296.0 > (double)(xr() & 0xFFFFFFFFu)) {
            E = E2;
            if (E < bestE) {
                bestE = E;
                stall = 0;
                if (E == 0) {
                    fprintf(stderr, "[n=%d seed=%llu] E=0 (no C4/C8/C16)! testing C32...\n",
                            N, (unsigned long long)seed);
                    if (!has_c32()) {
                        fprintf(stderr, "*** COUNTEREXAMPLE CANDIDATE (no C4/C8/C16/C32, cubic, n=%d) ***\n", N);
                        print_g6(stdout);
                        fflush(stdout);
                        return 42;
                    }
                    fprintf(stderr, "  ...has C32; recording extremal, continuing\n");
                    print_g6(stdout);
                    fflush(stdout);
                    /* keep hunting: perturb strongly */
                    T = 4.0;
                }
            }
        } else {
            adj[a] = sav[0]; adj[b] = sav[1]; adj[c] = sav[2]; adj[d] = sav[3];
        }
        if (++stall > 400000) {         /* restart */
            random_cubic();
            E = energy();
            T = 8.0;
            stall = 0;
        }
    }
    fprintf(stderr, "[n=%d seed=%llu] done: bestE=%ld finalE=%ld\n",
            N, (unsigned long long)seed, bestE, E);
    return 0;
}

/* p2check.c — exact power-of-two cycle analysis for graph6 input (n <= 64).
 *
 * For the Erdős–Gyárfás campaign: a graph is a counterexample iff it has
 * min degree >= 3 and contains no simple cycle of length 4, 8, 16, 32, or 64
 * (only lengths <= n can occur).
 *
 * Modes (graph6 lines on stdin):
 *   -s            spectrum: per graph, print "<n> <m> mindeg=<d> :" then for each
 *                 power-of-two L <= n whether a C_L exists (L:1 / L:0)
 *   -f            filter: print graph6 of graphs containing NO power-of-two cycle
 *                 (candidate counterexamples if mindeg>=3; combine with -d3)
 *   -F L1,L2,..   filter on a custom forbidden set: print graphs with none of C_Li
 *   -d D          additionally require min degree >= D in filter modes
 *   -c            count only: total read, and how many are power-of-2-cycle-free
 *   -M            use meet-in-the-middle verification for L in {16,32,64} as a
 *                 cross-check on the DFS result (slower; abort on any mismatch)
 *
 * Exit code 0 normally; any graph passing -f with mindeg>=3 is echoed to stdout
 * and also reported loudly on stderr (potential counterexample).
 *
 * Cycle existence: canonical-rooted DFS. A simple cycle of length L has a
 * unique minimal vertex s; we search paths s=v0,v1,...,v_{L-1} with all vi>s
 * for i>0, closing with an edge v_{L-1}~s. Pruning: precomputed BFS distance
 * to s inside the allowed vertex set; a path at depth d (edges used) from
 * vertex u can only close into an L-cycle if dist(u,s) <= L-d. Exact and
 * complete: no cycle is missed, no non-cycle is reported.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t u64;

#define MAXV 64

static u64 adj[MAXV];
static int N;

/* ---------- graph6 ---------- */
static int read_graph6(const char *line)
{
    const unsigned char *p = (const unsigned char *)line;
    int n, i, j, k, bitpos;
    if (*p == '>') {            /* optional >>graph6<< header */
        const char *h = strstr(line, "<<");
        if (!h) return -1;
        p = (const unsigned char *)h + 2;
    }
    if (*p == 126) {            /* extended sizes */
        p++;
        if (*p == 126) {        /* 6-byte size: n >= 258048 — unsupported */
            return -1;
        }
        n = 0;
        for (k = 0; k < 3; k++) n = (n << 6) | (p[k] - 63);
        p += 3;
    } else {
        n = *p - 63;
        p++;
    }
    if (n < 1 || n > MAXV) return -1;
    N = n;
    for (i = 0; i < n; i++) adj[i] = 0;
    bitpos = 0;
    for (j = 1; j < n; j++) {
        for (i = 0; i < j; i++) {
            int ch = p[bitpos / 6];
            if (ch == 0 || ch == '\n') return -1;
            if ((ch - 63) & (1 << (5 - bitpos % 6))) {
                adj[i] |= 1ULL << j;
                adj[j] |= 1ULL << i;
            }
            bitpos++;
        }
    }
    return n;
}

/* ---------- BFS distances within an allowed set ---------- */
static void bfs_dist(int src, u64 allowed, int *dist)
{
    int queue[MAXV], qh = 0, qt = 0, u;
    u64 seen;
    for (u = 0; u < N; u++) dist[u] = 1 << 20;
    dist[src] = 0;
    seen = 1ULL << src;
    queue[qt++] = src;
    while (qh < qt) {
        u64 nb;
        u = queue[qh++];
        nb = adj[u] & allowed & ~seen;
        while (nb) {
            int w = __builtin_ctzll(nb);
            nb &= nb - 1;
            seen |= 1ULL << w;
            dist[w] = dist[u] + 1;
            queue[qt++] = w;
        }
    }
}

/* ---------- exact-length simple cycle, canonical-rooted DFS ---------- */
static int L_target;
static int dist_to_s[MAXV];
static u64 allowed_mask;
static int found;

static void dfs_cycle(int u, int depth, u64 onpath, int s)
{
    u64 nb;
    if (found) return;
    if (depth == L_target - 1) {
        if (adj[u] & (1ULL << s)) found = 1;
        return;
    }
    nb = adj[u] & allowed_mask & ~onpath;
    while (nb && !found) {
        int w = __builtin_ctzll(nb);
        nb &= nb - 1;
        /* need to get back to s in exactly L-depth-1 more edges from w */
        if (dist_to_s[w] <= L_target - depth - 1) {
            dfs_cycle(w, depth + 1, onpath | (1ULL << w), s);
        }
    }
}

static int has_cycle_dfs(int L)
{
    int s;
    if (L > N) return 0;
    L_target = L;
    for (s = 0; s < N; s++) {
        u64 all = 0;
        int i;
        for (i = s; i < N; i++) all |= 1ULL << i;   /* s is min vertex */
        allowed_mask = all;
        bfs_dist(s, all, dist_to_s);
        found = 0;
        {   /* start DFS at s; first step into any neighbor > s */
            u64 nb = adj[s] & all & ~(1ULL << s);
            while (nb && !found) {
                int w = __builtin_ctzll(nb);
                nb &= nb - 1;
                if (dist_to_s[w] <= L - 1)
                    dfs_cycle(w, 1, (1ULL << s) | (1ULL << w), s);
            }
        }
        if (found) return 1;
    }
    return 0;
}

/* ---------- meet-in-the-middle existence for even L (cross-check) ----------
 * A cycle of length L=2h with minimal vertex s splits at s and the opposite
 * vertex w into two internally-disjoint s->w paths of length h, using only
 * vertices >= s. Enumerate all simple h-edge paths from s (vertices > s except
 * s itself), bucket by endpoint, and test pairs for mask-disjointness
 * (intersection exactly {s, w}).  Exact, no heuristics. */
typedef struct { u64 mask; } pathrec;

static pathrec *bucket[MAXV];
static int bcount[MAXV], bcap[MAXV];

static void push_path(int w, u64 mask)
{
    if (bcount[w] == bcap[w]) {
        bcap[w] = bcap[w] ? 2 * bcap[w] : 64;
        bucket[w] = (pathrec *)realloc(bucket[w], bcap[w] * sizeof(pathrec));
        if (!bucket[w]) { fprintf(stderr, "OOM\n"); exit(2); }
    }
    bucket[w][bcount[w]++].mask = mask;
}

static void enum_paths(int u, int depth, u64 onpath, int h, int s)
{
    if (depth == h) { push_path(u, onpath); return; }
    u64 nb = adj[u] & allowed_mask & ~onpath;
    while (nb) {
        int w = __builtin_ctzll(nb);
        nb &= nb - 1;
        enum_paths(w, depth + 1, onpath | (1ULL << w), h, s);
    }
}

static int has_cycle_mitm(int L)
{
    int s, w, i, j, h = L / 2;
    if (L > N || (L & 1)) return has_cycle_dfs(L);
    for (s = 0; s < N; s++) {
        u64 all = 0;
        for (i = s; i < N; i++) all |= 1ULL << i;
        allowed_mask = all;
        for (w = 0; w < N; w++) bcount[w] = 0;
        enum_paths(s, 0, 1ULL << s, h, s);
        for (w = s + 1; w < N; w++) {
            u64 both = (1ULL << s) | (1ULL << w);
            for (i = 0; i < bcount[w]; i++)
                for (j = i + 1; j < bcount[w]; j++)
                    if ((bucket[w][i].mask & bucket[w][j].mask) == both)
                        return 1;
        }
    }
    return 0;
}

/* ---------- helpers ---------- */
/* primary existence test: DFS for short lengths, MITM for L >= 32 (the DFS
 * can wander exponentially hunting long cycles in large-girth graphs; the
 * MITM path-join is exact and fast on sparse graphs) */
static int has_cycle(int L)
{
    return (L >= 32) ? has_cycle_mitm(L) : has_cycle_dfs(L);
}

static int min_degree(void)
{
    int v, d, md = MAXV + 1;
    for (v = 0; v < N; v++) {
        d = __builtin_popcountll(adj[v]);
        if (d < md) md = d;
    }
    return N ? md : 0;
}

static int edge_count(void)
{
    int v, m = 0;
    for (v = 0; v < N; v++) m += __builtin_popcountll(adj[v]);
    return m / 2;
}

int main(int argc, char **argv)
{
    int mode_spectrum = 0, mode_filter = 0, mode_count = 0, use_mitm = 0;
    int req_mindeg = 0;
    int custom[8], ncustom = 0;
    long total = 0, passed = 0;
    char line[4096];
    int a;

    for (a = 1; a < argc; a++) {
        if (!strcmp(argv[a], "-s")) mode_spectrum = 1;
        else if (!strcmp(argv[a], "-f")) mode_filter = 1;
        else if (!strcmp(argv[a], "-c")) mode_count = 1;
        else if (!strcmp(argv[a], "-M")) use_mitm = 1;
        else if (!strcmp(argv[a], "-d") && a + 1 < argc) req_mindeg = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-F") && a + 1 < argc) {
            char *tok = strtok(argv[++a], ",");
            mode_filter = 1;
            while (tok && ncustom < 8) { custom[ncustom++] = atoi(tok); tok = strtok(NULL, ","); }
        }
        else { fprintf(stderr, "unknown option %s\n", argv[a]); return 2; }
    }
    if (!mode_spectrum && !mode_filter && !mode_count) mode_count = 1;

    while (fgets(line, sizeof line, stdin)) {
        int n = read_graph6(line);
        int L, bad = 0;
        if (n < 0) { fprintf(stderr, "bad graph6 line: %.40s\n", line); return 2; }
        total++;
        if (mode_spectrum) {
            printf("%d %d mindeg=%d :", n, edge_count(), min_degree());
            for (L = 4; L <= n; L *= 2) {
                int hd = has_cycle(L);
                if (use_mitm && L == 16) {
                    int hm = has_cycle_mitm(L);
                    if (hm != hd) {
                        fprintf(stderr, "MITM/DFS MISMATCH n=%d L=%d dfs=%d mitm=%d g6=%s",
                                n, L, hd, hm, line);
                        return 3;
                    }
                }
                printf(" %d:%d", L, hd);
            }
            printf("\n");
        } else {
            if (req_mindeg && min_degree() < req_mindeg) continue;
            if (ncustom) {
                int k;
                for (k = 0; k < ncustom && !bad; k++)
                    if (custom[k] <= n && has_cycle(custom[k])) bad = 1;
            } else {
                for (L = 4; L <= n && !bad; L *= 2) {
                    int hd = has_cycle(L);
                    if (use_mitm && L == 16 && !hd) {
                        int hm = has_cycle_mitm(L);
                        if (hm != hd) {
                            fprintf(stderr, "MITM/DFS MISMATCH n=%d L=%d g6=%s", n, L, line);
                            return 3;
                        }
                    }
                    if (hd) bad = 1;
                }
            }
            if (!bad) {
                passed++;
                if (mode_filter) {
                    fputs(line, stdout);
                    fflush(stdout);
                    if (!ncustom && min_degree() >= 3)
                        fprintf(stderr, "*** SURVIVOR (no power-of-2 cycle, mindeg>=3): %s", line);
                }
            }
        }
    }
    if (mode_count || mode_filter)
        fprintf(stderr, "p2check: read=%ld passed=%ld\n", total, passed);
    return 0;
}

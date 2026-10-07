/* cycscan.c — exact simple-cycle presence/absence at given lengths, graph6
 * input, arbitrary degrees, n <= 4096.  Generalizes p2check.c's method
 * (canonical-rooted DFS + BFS-distance pruning) beyond the 64-vertex bitmask.
 *
 * Usage: cycscan [-F 4,8,16] [-t] [-c] [file]
 *   -F list   lengths to test (default 4,8,16)
 *   -t        vertex-transitive mode: root every search at vertex 0 only,
 *             with no vertex-order restriction (valid iff the input graph is
 *             vertex-transitive; ~n x faster)
 *   -c        print only summary counts
 * Output per graph:  n=<n> m=<m> C4=1/0 C8=1/0 ...  spectrum bits
 * (1 = at least one such cycle exists).  Graphs with all-zero bits are
 * echoed to stderr as SURVIVOR lines.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 4096
#define MAXD 16

static int n, m;
static int deg[MAXN];
static int adj[MAXN][MAXD];

static int readg6(const char *s) {
    const unsigned char *p = (const unsigned char *)s;
    long nn;
    if (*p == ':') return -3;
    if (*p == '~') {
        if (p[1] == '~') { nn = 0; for (int i = 2; i < 8; i++) nn = (nn << 6) | (p[i] - 63); p += 8; }
        else { nn = 0; for (int i = 1; i < 4; i++) nn = (nn << 6) | (p[i] - 63); p += 4; }
    } else { nn = *p - 63; p += 1; }
    if (nn < 1 || nn > MAXN) return -1;
    n = (int)nn; m = 0;
    memset(deg, 0, sizeof(int) * n);
    int bit = 0; unsigned char cur = 0;
    for (int v = 1; v < n; v++)
        for (int u = 0; u < v; u++) {
            if (bit == 0) { cur = *p++ - 63; bit = 6; }
            bit--;
            if ((cur >> bit) & 1) {
                if (deg[u] >= MAXD || deg[v] >= MAXD) return -2;
                adj[u][deg[u]++] = v; adj[v][deg[v]++] = u; m++;
            }
        }
    return 0;
}

static int dist[MAXN];
static unsigned char on[MAXN];
static int L_target, root, vt_mode;
static int queue_[MAXN];

/* BFS distances from root among allowed vertices (>= root unless vt_mode) */
static void bfs(void) {
    for (int i = 0; i < n; i++) dist[i] = 1 << 29;
    dist[root] = 0;
    int qh = 0, qt = 0;
    queue_[qt++] = root;
    while (qh < qt) {
        int u = queue_[qh++];
        for (int k = 0; k < deg[u]; k++) {
            int w = adj[u][k];
            if ((vt_mode || w >= root) && dist[w] > dist[u] + 1) {
                dist[w] = dist[u] + 1;
                queue_[qt++] = w;
            }
        }
    }
}

/* DFS for a simple cycle of length L_target through root with all vertices
 * allowed (>= root unless vt_mode).  Returns 1 if found. */
static int dfs(int u, int depth) {
    if (depth == L_target - 1) {
        for (int k = 0; k < deg[u]; k++) if (adj[u][k] == root) return 1;
        return 0;
    }
    for (int k = 0; k < deg[u]; k++) {
        int w = adj[u][k];
        if ((vt_mode || w > root) && !on[w] && dist[w] <= L_target - depth - 1) {
            on[w] = 1;
            if (dfs(w, depth + 1)) { on[w] = 0; return 1; }
            on[w] = 0;
        }
    }
    return 0;
}

static int has_cycle(int L) {
    L_target = L;
    int rmax = vt_mode ? 1 : n;
    for (root = 0; root < rmax; root++) {
        bfs();
        memset(on, 0, n);
        on[root] = 1;
        /* start with first edge root->w, w > root (or any w in vt mode);
         * to avoid finding each cycle twice we would order the two neighbors,
         * but presence-only does not care. */
        for (int k = 0; k < deg[root]; k++) {
            int w = adj[root][k];
            if ((vt_mode || w > root) && dist[w] <= L - 1) {
                on[w] = 1;
                if (dfs(w, 1)) return 1;
                on[w] = 0;
            }
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    int Ls[16], nL = 0, count_only = 0;
    const char *fname = NULL;
    for (int a = 1; a < argc; a++) {
        if (!strcmp(argv[a], "-F") && a + 1 < argc) {
            char *tok = strtok(argv[++a], ",");
            while (tok && nL < 16) { Ls[nL++] = atoi(tok); tok = strtok(NULL, ","); }
        } else if (!strcmp(argv[a], "-t")) vt_mode = 1;
        else if (!strcmp(argv[a], "-c")) count_only = 1;
        else fname = argv[a];
    }
    if (nL == 0) { Ls[0] = 4; Ls[1] = 8; Ls[2] = 16; nL = 3; }
    FILE *f = fname ? fopen(fname, "r") : stdin;
    if (!f) { perror("open"); return 2; }
    static char line[600000];
    long total = 0, surv = 0;
    while (fgets(line, sizeof line, f)) {
        size_t len = strlen(line);
        while (len && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = 0;
        if (!len) continue;
        if (readg6(line) < 0) { fprintf(stderr, "skip bad line: %.40s\n", line); continue; }
        total++;
        int any = 0;
        int have[16];
        for (int i = 0; i < nL; i++) {
            have[i] = (Ls[i] <= n) ? has_cycle(Ls[i]) : 0;
            any |= have[i];
        }
        if (!any) {
            surv++;
            fprintf(stderr, "SURVIVOR n=%d m=%d g6=%s\n", n, m, line);
        }
        if (!count_only) {
            printf("n=%d m=%d", n, m);
            for (int i = 0; i < nL; i++) printf(" C%d=%d", Ls[i], have[i]);
            printf(" g6=%.120s\n", line);
        }
        if (total % 1000 == 0) fprintf(stderr, "...%ld done (%ld surv)\n", total, surv);
    }
    fprintf(stderr, "cycscan: %ld graphs, %ld with none of the tested lengths\n",
            total, surv);
    return 0;
}

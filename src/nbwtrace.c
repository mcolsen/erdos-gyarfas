/* nbwtrace.c — exact traces of powers of the Hashimoto (non-backtracking)
 * matrix for graph6 input, arbitrary degrees, n <= 4096.
 *
 * tr(H^L) = number of cyclically-non-backtracking closed L-walks (dart-rooted).
 * Facts used downstream:  tr(H^L) >= 2L * #C_L;  tr(H^L)=0 ==> no C_d, d|L.
 *
 * Usage: nbwtrace [-L 4,8,16,32] [file.g6]
 *   per input line prints:  n=<n> m=<m> tr4=<..> tr8=<..> ...  (decimal u128)
 *
 * Exact: u128 accumulators; per-dart counts are bounded by 2^L in subcubic
 * graphs (max outdeg of H = maxdeg-1); overflow impossible for L<=64, deg<=3.
 * For safety with higher degrees, a saturating check aborts on overflow.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;

#define MAXN 4096
#define MAXD 8

static int n, m;
static int deg[MAXN];
static int adj[MAXN][MAXD];

/* graph6 reader (short and long n forms) */
static int readg6(const char *s) {
    const unsigned char *p = (const unsigned char *)s;
    long nn;
    if (*p == ':') { fprintf(stderr, "sparse6 unsupported\n"); return -1; }
    if (*p == '~') {
        if (p[1] == '~') { /* 36-bit */
            nn = 0; for (int i = 2; i < 8; i++) nn = (nn << 6) | (p[i] - 63);
            p += 8;
        } else {
            nn = 0; for (int i = 1; i < 4; i++) nn = (nn << 6) | (p[i] - 63);
            p += 4;
        }
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

static void print_u128(u128 x) {
    char buf[44]; int i = 0;
    if (x == 0) { putchar('0'); return; }
    while (x) { buf[i++] = '0' + (int)(x % 10); x /= 10; }
    while (i) putchar(buf[--i]);
}

/* darts: for vertex u, slot k (k < deg[u]) -> dart id du[u]+k pointing u->adj[u][k].
 * rev of dart (u,k): dart (v,k') with adj[v][k']=u matching the same edge.
 * Simple graphs: the unique k' with adj[v][k']==u. */
static int du[MAXN + 1];
static int dhead[2 * MAXN * MAXD / 2 + 8]; /* head vertex of dart */
static int drev[2 * MAXN * MAXD / 2 + 8];

static int build_darts(void) {
    int D = 0;
    for (int u = 0; u < n; u++) { du[u] = D; D += deg[u]; }
    du[n] = D;
    for (int u = 0; u < n; u++)
        for (int k = 0; k < deg[u]; k++) {
            int v = adj[u][k];
            dhead[du[u] + k] = v;
            int kk = -1;
            for (int j = 0; j < deg[v]; j++) if (adj[v][j] == u) { kk = j; break; }
            drev[du[u] + k] = du[v] + kk;
        }
    return D;
}

int main(int argc, char **argv) {
    int Ls[16], nL = 0, Lmax = 0;
    const char *fname = NULL;
    for (int a = 1; a < argc; a++) {
        if (!strcmp(argv[a], "-L") && a + 1 < argc) {
            char *tok = strtok(argv[++a], ",");
            while (tok && nL < 16) { Ls[nL++] = atoi(tok); tok = strtok(NULL, ","); }
        } else fname = argv[a];
    }
    if (nL == 0) { Ls[0] = 4; Ls[1] = 8; Ls[2] = 16; Ls[3] = 32; nL = 4; }
    for (int i = 0; i < nL; i++) if (Ls[i] > Lmax) Lmax = Ls[i];
    if (Lmax > 64) { fprintf(stderr, "L>64 unsupported (overflow)\n"); return 2; }
    FILE *f = fname ? fopen(fname, "r") : stdin;
    if (!f) { perror("open"); return 2; }
    static char line[600000];
    static u128 vec[2][2 * MAXN * MAXD / 2 + 8];
    while (fgets(line, sizeof line, f)) {
        size_t len = strlen(line);
        while (len && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = 0;
        if (!len) continue;
        if (readg6(line) < 0) { fprintf(stderr, "skip bad line\n"); continue; }
        int D = build_darts();
        u128 tr[16]; for (int i = 0; i < nL; i++) tr[i] = 0;
        for (int s = 0; s < D; s++) {
            u128 *cur = vec[0], *nxt = vec[1];
            memset(cur, 0, sizeof(u128) * D);
            cur[s] = 1;
            for (int step = 1; step <= Lmax; step++) {
                memset(nxt, 0, sizeof(u128) * D);
                for (int d = 0; d < D; d++) {
                    u128 c = cur[d];
                    if (!c) continue;
                    int v = dhead[d], r = drev[d];
                    for (int k = 0; k < deg[v]; k++) {
                        int d2 = du[v] + k;
                        if (d2 != r) nxt[d2] += c;
                    }
                }
                u128 *t = cur; cur = nxt; nxt = t;
                for (int i = 0; i < nL; i++)
                    if (Ls[i] == step) tr[i] += cur[s];
            }
        }
        printf("n=%d m=%d", n, m);
        for (int i = 0; i < nL; i++) {
            printf(" tr%d=", Ls[i]);
            print_u128(tr[i]);
        }
        printf(" g6=%.90s\n", line);
        fflush(stdout);
    }
    return 0;
}

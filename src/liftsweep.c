/* liftsweep.c — voltage-config sweep engine for one base + many groups.
 *
 * Job file (text):
 *   base <id> <nslot> <kinds: string of c/l/s>
 *   words <L> <nwords>            (levels in increasing L; L in {1,2,4,8,16})
 *   w <tok...L ints> <npairs> <i j ...>
 *   group <name> <order>
 *   mul <o*o ints> / inv <o ints>
 *   gensets <nmax> <o u32 masks>  (per element: bitmask of maximal subgroups containing it; 0 masks = skip GEN check)
 *   reps0 <count> <elements>      (slot-0 value restriction; empty = all)
 *   run
 *   (more group sections ...)
 *
 * Per config over slot domains (c: all; l: g!=e, g*g!=e; s: g!=e, g*g==e):
 *   GEN kill (config values all inside one maximal subgroup -> redundant),
 *   then per level: for each word: net voltage; if identity:
 *     L<=4: kill;  L in {8,16}: degeneracy check (pairs i,j: prefix_i ==
 *     prefix_j means the walk is not a simple cycle); non-degenerate -> kill.
 *   Survivor -> "SURV base=<id> group=<name> vals=<...>".
 * Stats per group to stderr.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXO 64
#define MAXSLOT 8
#define MAXW 200000
#define MAXL 16

static int baseid, nslot;
static char kinds[MAXSLOT + 2];
typedef struct { int L, n, off; } Level;
static Level levels[8];
static int nlevels;
static unsigned char wtok[MAXW * MAXL];       /* tokens per word, padded to L */
static int wpairs_off[MAXW + 1];
static unsigned char wpair_buf[MAXW * 240];   /* i,j byte pairs (<=120 pairs/word) */
static int wcount_total;

static unsigned char mul[MAXO * MAXO], inv_[MAXO];
static int order_, ident;
static uint32_t genmask[MAXO];
static int ngensets;
static int reps0[MAXO], nreps0;
static char gname[128];

static long long stat_cfg, stat_gen, stat_kill[5], stat_surv;

static int dom[MAXSLOT][MAXO], domn[MAXSLOT];

static void build_domains(void) {
    for (int s = 0; s < nslot; s++) {
        domn[s] = 0;
        for (int g = 0; g < order_; g++) {
            int gg = mul[g * MAXO + g];
            if (kinds[s] == 'c') dom[s][domn[s]++] = g;
            else if (kinds[s] == 'l') { if (g != ident && gg != ident) dom[s][domn[s]++] = g; }
            else { if (g != ident && gg == ident) dom[s][domn[s]++] = g; }
        }
        if (s == 0 && nreps0 > 0 && kinds[0] == 'c') {
            /* intersect slot-0 domain with reps (abelian orbit reps) */
            int nd = 0;
            for (int i = 0; i < domn[0]; i++)
                for (int j = 0; j < nreps0; j++)
                    if (dom[0][i] == reps0[j]) { dom[0][nd++] = dom[0][i]; break; }
            domn[0] = nd;
        }
    }
}

static inline int eval_word(const unsigned char *tok, int L, const int *vals,
                            unsigned char *pref) {
    int p = ident;
    pref[0] = ident;
    for (int i = 0; i < L; i++) {
        unsigned char t = tok[i];
        if (t != 255) {
            int v = vals[t >> 1];
            if (t & 1) v = inv_[v];
            p = mul[p * MAXO + v];
        }
        pref[i + 1] = p;
    }
    return p;
}

static void run_group(void) {
    build_domains();
    for (int s = 0; s < nslot; s++)
        if (domn[s] == 0) {
            fprintf(stderr, "STAT base=%d group=%s cfg=0 (empty domain)\n", baseid, gname);
            return;
        }
    stat_cfg = stat_gen = stat_surv = 0;
    memset(stat_kill, 0, sizeof stat_kill);
    int idx[MAXSLOT] = {0};
    int vals[MAXSLOT];
    unsigned char pref[MAXL + 1];
    for (;;) {
        for (int s = 0; s < nslot; s++) vals[s] = dom[s][idx[s]];
        stat_cfg++;
        /* GEN: all values inside a common maximal subgroup? */
        int alive = 1;
        if (ngensets > 0) {
            uint32_t common = 0xffffffffu;
            for (int s = 0; s < nslot; s++) common &= genmask[vals[s]];
            if (common) { stat_gen++; alive = 0; }
        }
        if (alive) {
            for (int lv = 0; lv < nlevels && alive; lv++) {
                int L = levels[lv].L, nw = levels[lv].n, off = levels[lv].off;
                for (int w = 0; w < nw; w++) {
                    const unsigned char *tok = &wtok[(off + w) * MAXL];
                    int net = eval_word(tok, L, vals, pref);
                    if (net != ident) continue;
                    if (L <= 4) { alive = 0; stat_kill[lv]++; break; }
                    /* degeneracy: any pair i<j with equal base vertex and
                     * equal prefix -> walk not a simple cycle */
                    const unsigned char *pp = &wpair_buf[wpairs_off[off + w] * 2];
                    int np = wpairs_off[off + w + 1] - wpairs_off[off + w];
                    int degen = 0;
                    for (int q = 0; q < np; q++)
                        if (pref[pp[2 * q]] == pref[pp[2 * q + 1]]) { degen = 1; break; }
                    if (!degen) { alive = 0; stat_kill[lv]++; break; }
                }
            }
            if (alive) {
                stat_surv++;
                printf("SURV base=%d group=%s vals=", baseid, gname);
                for (int s = 0; s < nslot; s++) printf("%d%c", vals[s], s + 1 < nslot ? ',' : '\n');
            }
        }
        /* odometer */
        int s = nslot - 1;
        while (s >= 0 && ++idx[s] == domn[s]) idx[s--] = 0;
        if (s < 0) break;
    }
    fprintf(stderr, "STAT base=%d group=%s cfg=%lld gen=%lld", baseid, gname, stat_cfg, stat_gen);
    for (int lv = 0; lv < nlevels; lv++)
        fprintf(stderr, " killL%d=%lld", levels[lv].L, stat_kill[lv]);
    fprintf(stderr, " surv=%lld\n", stat_surv);
    fflush(stdout);
}

int main(int argc, char **argv) {
    FILE *f = argc > 1 ? fopen(argv[1], "r") : stdin;
    if (!f) { perror("open"); return 2; }
    char cmd[64];
    int pair_top = 0;
    while (fscanf(f, "%63s", cmd) == 1) {
        if (!strcmp(cmd, "base")) {
            if (fscanf(f, "%d %d %8s", &baseid, &nslot, kinds) != 3) return 3;
            nlevels = 0; wcount_total = 0; pair_top = 0;
        } else if (!strcmp(cmd, "words")) {
            int L, n;
            if (fscanf(f, "%d %d", &L, &n) != 2) return 3;
            levels[nlevels].L = L; levels[nlevels].n = n; levels[nlevels].off = wcount_total;
            nlevels++;
        } else if (!strcmp(cmd, "w")) {
            /* need current level L = levels[nlevels-1].L */
            int L = levels[nlevels - 1].L;
            unsigned char *tok = &wtok[wcount_total * MAXL];
            memset(tok, 255, MAXL);
            for (int i = 0; i < L; i++) { int t; fscanf(f, "%d", &t); tok[i] = (unsigned char)t; }
            int np; fscanf(f, "%d", &np);
            wpairs_off[wcount_total] = pair_top;
            for (int q = 0; q < np; q++) {
                int i, j; fscanf(f, "%d %d", &i, &j);
                wpair_buf[(pair_top + q) * 2] = (unsigned char)i;
                wpair_buf[(pair_top + q) * 2 + 1] = (unsigned char)j;
            }
            pair_top += np;
            wcount_total++;
            wpairs_off[wcount_total] = pair_top;
        } else if (!strcmp(cmd, "group")) {
            fscanf(f, "%127s %d", gname, &order_);
        } else if (!strcmp(cmd, "mul")) {
            for (int i = 0; i < order_; i++)
                for (int j = 0; j < order_; j++) { int x; fscanf(f, "%d", &x); mul[i * MAXO + j] = (unsigned char)x; }
            /* identity */
            for (int e = 0; e < order_; e++) {
                int ok = 1;
                for (int j = 0; j < order_; j++) if (mul[e * MAXO + j] != j) { ok = 0; break; }
                if (ok) { ident = e; break; }
            }
        } else if (!strcmp(cmd, "inv")) {
            for (int i = 0; i < order_; i++) { int x; fscanf(f, "%d", &x); inv_[i] = (unsigned char)x; }
        } else if (!strcmp(cmd, "gensets")) {
            fscanf(f, "%d", &ngensets);
            for (int i = 0; i < order_; i++) { unsigned int x; fscanf(f, "%u", &x); genmask[i] = x; }
        } else if (!strcmp(cmd, "reps0")) {
            fscanf(f, "%d", &nreps0);
            for (int i = 0; i < nreps0; i++) fscanf(f, "%d", &reps0[i]);
        } else if (!strcmp(cmd, "run")) {
            run_group();
        }
    }
    return 0;
}

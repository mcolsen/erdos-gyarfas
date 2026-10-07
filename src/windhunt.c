/* windhunt.c — winding-vector analysis of closed cyclically-NBW L-walks on
 * the five 2-vertex cubic bases, for the trace-32-hole hunt over abelian
 * (esp. cyclic) voltage groups.
 *
 * For base B with r free slots, every closed NBW L-walk has a winding vector
 * c in Z^r (signed slot-usage counts).  Over Z_m with voltages t in Z_m^r the
 * identity-voltage walk count (= tr(H_lift^L)/m) is
 *     Sigma_c mult_L(c) * [c . t == 0 mod m].
 * So tr(H_lift^L) = 0  iff  c.t != 0 mod m for every c with mult_L(c) > 0.
 * If mult_L(0) > 0 the base is dead for ALL abelian groups at length L.
 *
 * Bases (darts: tail head rev slot sign; slot<0 = tree/identity):
 *   0 theta     : 3 parallel edges u-v; tree edge #3; slots e1,e2
 *   1 dumbbell  : loops a,b + bridge (tree); slots la,lb
 *   2 loopsemi  : loop at u, 2 semis at v, bridge (tree); slots l,s1,s2
 *   3 semis4    : 2 semis each end, bridge (tree); slots s1,s2,s3,s4
 *   4 dubsemi   : double edge u-v (one tree, one slot) + semi each; e,s1,s2
 *
 * Modes:
 *   windhunt table <L>          — per base: |W_L|, mult_L(0), sample stats
 *   windhunt val <base> <m> <L> <t0,t1,..>  — winding-sum walk count (for
 *                                  cross-validation against nbwtrace)
 *   windhunt hunt <base> <L> <mlo> <mhi>    — for each m, sample t's; report
 *                                  first (m,t) with all c.t != 0, if any
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct { int nd, r; int tail[8], head[8], rev[8], slot[8], sign[8]; const char *name; } BaseT;

/* dart tables.  Proper edge -> darts d (slot,+1), d^1 (slot,-1).
 * loop -> darts d,d+1 rev-paired, slot +1/-1.  semi -> single dart rev=self. */
static BaseT BASES[5];

static void init_bases(void) {
    /* 0: theta — e1(s0), e2(s1), e3(tree) between u=0,v=1 */
    BaseT *b = &BASES[0]; b->name = "theta"; b->nd = 6; b->r = 2;
    int t0[6] = {0,1,0,1,0,1}, h0[6] = {1,0,1,0,1,0}, r0[6] = {1,0,3,2,5,4};
    int s0[6] = {0,0,1,1,-1,-1}, g0[6] = {1,-1,1,-1,1,-1};
    memcpy(b->tail,t0,sizeof t0); memcpy(b->head,h0,sizeof h0); memcpy(b->rev,r0,sizeof r0);
    memcpy(b->slot,s0,sizeof s0); memcpy(b->sign,g0,sizeof g0);
    /* 1: dumbbell — loop at 0 (s0), loop at 1 (s1), bridge tree */
    b = &BASES[1]; b->name = "dumbbell"; b->nd = 6; b->r = 2;
    int t1[6] = {0,0,1,1,0,1}, h1[6] = {0,0,1,1,1,0}, r1[6] = {1,0,3,2,5,4};
    int s1[6] = {0,0,1,1,-1,-1}, g1[6] = {1,-1,1,-1,1,-1};
    memcpy(b->tail,t1,sizeof t1); memcpy(b->head,h1,sizeof h1); memcpy(b->rev,r1,sizeof r1);
    memcpy(b->slot,s1,sizeof s1); memcpy(b->sign,g1,sizeof g1);
    /* 2: loopsemi — loop at 0 (s0), semis at 1 (s1,s2), bridge tree */
    b = &BASES[2]; b->name = "loopsemi"; b->nd = 6; b->r = 3;
    int t2[6] = {0,0,1,1,0,1}, h2[6] = {0,0,1,1,1,0}, r2[6] = {1,0,2,3,5,4};
    int s2[6] = {0,0,1,2,-1,-1}, g2[6] = {1,-1,1,1,1,-1};
    memcpy(b->tail,t2,sizeof t2); memcpy(b->head,h2,sizeof h2); memcpy(b->rev,r2,sizeof r2);
    memcpy(b->slot,s2,sizeof s2); memcpy(b->sign,g2,sizeof g2);
    /* 3: semis4 — semis s1,s2 at 0; semis s3,s4 at 1; bridge tree */
    b = &BASES[3]; b->name = "semis4"; b->nd = 6; b->r = 4;
    int t3[6] = {0,0,1,1,0,1}, h3[6] = {0,0,1,1,1,0}, r3[6] = {0,1,2,3,5,4};
    int s3[6] = {0,1,2,3,-1,-1}, g3[6] = {1,1,1,1,1,-1};
    memcpy(b->tail,t3,sizeof t3); memcpy(b->head,h3,sizeof h3); memcpy(b->rev,r3,sizeof r3);
    memcpy(b->slot,s3,sizeof s3); memcpy(b->sign,g3,sizeof g3);
    /* 4: dubsemi — edges e1(tree), e2(s0) between 0,1; semi at 0 (s1), semi at 1 (s2) */
    b = &BASES[4]; b->name = "dubsemi"; b->nd = 6; b->r = 3;
    int t4[6] = {0,1,0,1,0,1}, h4[6] = {1,0,1,0,0,1}, r4[6] = {1,0,3,2,4,5};
    int s4[6] = {-1,-1,0,0,1,2}, g4[6] = {1,-1,1,-1,1,1};
    memcpy(b->tail,t4,sizeof t4); memcpy(b->head,h4,sizeof h4); memcpy(b->rev,r4,sizeof r4);
    memcpy(b->slot,s4,sizeof s4); memcpy(b->sign,g4,sizeof g4);
}

#define LMAX 32
#define BOX (2 * LMAX + 1)

/* W_L via DP: for each start dart, propagate (dart, winding) -> counts.
 * winding coords in [-L, L], packed base-BOX.  r <= 4: BOX^4 = 17.9M states
 * per dart — with u32 counts: 6*17.9M*4B = 430 MB * 2 layers.. too fat for
 * r=4 with counts; use u64 total via hashing instead?  Simpler: r<=4 uses
 * offset-packed arrays but only ACTIVE windings via sparse expansion per
 * step (walk of length t reaches <= C(t) windings).  We use a dense array
 * limited to coords in [-L/1, L/1] but int32 counts and r<=3 dense; r=4
 * (semis4) uses reduced box [-L/2..] since each semi step is +1 only mod 2?
 * Pragmatic: for r=4 semis, windings count usage mod nothing — usage of
 * each semi <= L; box [0..L]^4 too big; but semis4 walks alternate
 * bridge/semi so each semi usage <= L/2 = 16: box 17^4 = 83k. fine dense.
 * We keep it simple: dense box per base chosen by slot kinds. */
static int boxlo[4], boxhi[4], dims[4];
static long long nstates;

static long long widx(const int *c) {
    long long ix = 0;
    for (int i = 0; i < 4; i++) ix = ix * dims[i] + (i < 4 ? (c[i] - boxlo[i]) : 0);
    return ix;
}

typedef uint32_t cnt_t;

static int dump_mode = 0, dump_base = -1;

int cmd_table(int L) {
    for (int bi = 0; bi < 5; bi++) {
        BaseT *b = &BASES[bi];
        if (dump_mode && bi != dump_base) continue;
        /* per-slot usage bounds: proper/loop slots: |c| <= L; semi: 0..L/2;
           tighten: any slot appears <= L times; loops consume 1 step each use;
           windings bounded by L. use lo=-L hi=L for sign-able slots, 0..L for semis. */
        /* exact boxes: each step changes one coord by +-1, so intermediate
         * and final windings lie in [-L, L] (signed slots) / [0, L] (semis,
         * always +1).  No clipping can occur with these bounds. */
        for (int s = 0; s < 4; s++) { boxlo[s] = 0; boxhi[s] = 0; dims[s] = 1; }
        for (int s = 0; s < b->r; s++) {
            int has_neg = 0;
            for (int d = 0; d < b->nd; d++)
                if (b->slot[d] == s && b->sign[d] < 0) has_neg = 1;
            boxlo[s] = has_neg ? -L : 0;
            boxhi[s] = L;
            dims[s] = boxhi[s] - boxlo[s] + 1;
        }
        nstates = 1;
        for (int i = 0; i < 4; i++) nstates *= dims[i];
        long long tot = nstates * b->nd;
        cnt_t *cur = calloc(tot, sizeof(cnt_t)), *nxt = calloc(tot, sizeof(cnt_t));
        long long *wmult = calloc(nstates, sizeof(long long));
        if (!cur || !nxt || !wmult) { fprintf(stderr, "OOM base %d\n", bi); return 2; }
        long long clipped = 0;
        for (int start = 0; start < b->nd; start++) {
            memset(cur, 0, tot * sizeof(cnt_t));
            /* take the first step: dart=start */
            {
                int c[4] = {0, 0, 0, 0};
                if (b->slot[start] >= 0) c[b->slot[start]] += b->sign[start];
                int ok = 1;
                for (int i = 0; i < b->r; i++) if (c[i] < boxlo[i] || c[i] > boxhi[i]) ok = 0;
                if (ok) cur[start * nstates + widx(c)] = 1;
            }
            for (int step = 2; step <= L; step++) {
                memset(nxt, 0, tot * sizeof(cnt_t));
                for (int d = 0; d < b->nd; d++) {
                    cnt_t *cd = &cur[(long long)d * nstates];
                    for (long long ix = 0; ix < nstates; ix++) {
                        cnt_t v = cd[ix];
                        if (!v) continue;
                        /* unpack */
                        int c[4]; long long rem = ix;
                        for (int i = 3; i >= 0; i--) { c[i] = (int)(rem % dims[i]) + boxlo[i]; rem /= dims[i]; }
                        for (int e = 0; e < b->nd; e++) {
                            if (b->tail[e] != b->head[d] || e == b->rev[d]) continue;
                            int c2[4] = {c[0], c[1], c[2], c[3]};
                            if (b->slot[e] >= 0) c2[b->slot[e]] += b->sign[e];
                            int ok = 1;
                            for (int i = 0; i < b->r; i++)
                                if (c2[i] < boxlo[i] || c2[i] > boxhi[i]) { ok = 0; break; }
                            if (!ok) { clipped += v; continue; }
                            nxt[(long long)e * nstates + widx(c2)] += v;
                        }
                    }
                }
                cnt_t *t = cur; cur = nxt; nxt = t;
            }
            /* closures: darts d with start in succ(d): head[d]==tail[start], start != rev[d] */
            for (int d = 0; d < b->nd; d++) {
                if (b->head[d] != b->tail[start] || start == b->rev[d]) continue;
                cnt_t *cd = &cur[(long long)d * nstates];
                for (long long ix = 0; ix < nstates; ix++)
                    if (cd[ix]) wmult[ix] += cd[ix];
            }
        }
        long long nw = 0, m0 = 0, total = 0;
        for (long long ix = 0; ix < nstates; ix++)
            if (wmult[ix]) {
                nw++; total += wmult[ix];
                if (dump_mode) {
                    int c[4]; long long rem = ix;
                    for (int i = 3; i >= 0; i--) { c[i] = (int)(rem % dims[i]) + boxlo[i]; rem /= dims[i]; }
                    printf("c");
                    for (int i = 0; i < b->r; i++) printf(" %d", c[i]);
                    printf(" mult %lld\n", wmult[ix]);
                }
            }
        {
            int z[4] = {0, 0, 0, 0};
            m0 = wmult[widx(z)];
        }
        printf("base %d %-9s r=%d L=%d |W|=%lld total_rooted=%lld mult0=%lld clipped=%lld%s\n",
               bi, b->name, b->r, L, nw, total, m0, clipped,
               m0 == 0 && clipped == 0 ? "  <-- ZERO-FREE: abelian trace-hole possible!" : "");
        free(cur); free(nxt); free(wmult);
    }
    return 0;
}

int main(int argc, char **argv) {
    init_bases();
    if (argc >= 3 && !strcmp(argv[1], "table")) return cmd_table(atoi(argv[2]));
    if (argc >= 4 && !strcmp(argv[1], "dump")) {
        dump_mode = 1; dump_base = atoi(argv[2]);
        return cmd_table(atoi(argv[3]));
    }
    fprintf(stderr, "usage: windhunt table <L> | dump <base> <L>\n");
    return 1;
}

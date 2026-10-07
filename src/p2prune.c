/* p2prune.c — PRUNE plugin for nauty's geng.
 *
 * Compile geng with -DPRUNE=p2_prune and link this file. geng builds graphs by
 * adding one vertex at a time (vertex n-1, adjacent only to earlier vertices),
 * so every cycle created at this step passes through vertex n-1 (a simple cycle
 * uses at most two edges at n-1, and all new edges are incident to n-1).
 * Inductively, if every ancestor level was pruned with the same length set,
 * any cycle of a forbidden length in the current graph goes through n-1.
 * A C_L through v=n-1 exists iff two distinct neighbors a,b of v are joined by
 * a simple path of length L-2 in G - v. Supergraphs keep their subgraph's
 * cycles, so pruning is sound (never loses a completion that would survive)
 * and complete (output graphs contain no forbidden cycle).
 *
 * Forbidden lengths from env P2_LENGTHS (default "8,16"); geng's -f flag
 * already handles C4 natively (P2_LENGTHS may include 4 to do it here instead).
 *
 * Exact-length path search: DFS from each neighbor a with conservative pruning
 * by multi-source BFS distance to the remaining target neighbors.
 */

#include "gtools.h"
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t u64;
#define PMAXV 64

static int p2_lengths[8];
static int p2_nlen = -1;        /* -1: not initialised */

static u64 padj[PMAXV];
static int pn;

static void p2_init(void)
{
    const char *env = getenv("P2_LENGTHS");
    char buf[128], *tok;
    p2_nlen = 0;
    if (!env) env = "8,16";
    strncpy(buf, env, sizeof buf - 1);
    buf[sizeof buf - 1] = 0;
    for (tok = strtok(buf, ","); tok && p2_nlen < 8; tok = strtok(NULL, ","))
        p2_lengths[p2_nlen++] = atoi(tok);
}

/* BFS distances from every vertex of 'targets' simultaneously (in G - v),
 * i.e. dist[u] = min over t in targets of d(u,t). */
static void p2_bfs_multi(u64 targets, u64 excl, int *dist)
{
    int queue[PMAXV], qh = 0, qt = 0, u;
    u64 seen = targets;
    for (u = 0; u < pn; u++) dist[u] = 1 << 20;
    {
        u64 t = targets;
        while (t) {
            int w = __builtin_ctzll(t);
            t &= t - 1;
            dist[w] = 0;
            queue[qt++] = w;
        }
    }
    while (qh < qt) {
        u64 nb;
        u = queue[qh++];
        nb = padj[u] & ~seen & ~excl;
        while (nb) {
            int w = __builtin_ctzll(nb);
            nb &= nb - 1;
            seen |= 1ULL << w;
            dist[w] = dist[u] + 1;
            queue[qt++] = w;
        }
    }
}

static int p2_found;
static int p2_plen;             /* required path length in edges (= L-2) */
static u64 p2_targets;          /* neighbors of v usable as endpoint b */
static u64 p2_excl;             /* the vertex v itself */
static int p2_dist[PMAXV];

static void p2_dfs(int u, int depth, u64 onpath)
{
    u64 nb;
    if (p2_found) return;
    if (depth == p2_plen) {
        /* endpoint must be a target (b != a guaranteed: a cleared from targets) */
        if (p2_targets & (1ULL << u)) p2_found = 1;
        return;
    }
    nb = padj[u] & ~onpath & ~p2_excl;
    while (nb && !p2_found) {
        int w = __builtin_ctzll(nb);
        nb &= nb - 1;
        if (p2_dist[w] <= p2_plen - depth - 1)
            p2_dfs(w, depth + 1, onpath | (1ULL << w));
    }
}

/* Does G contain a cycle of exact length L through vertex v? */
static int p2_cycle_through(int v, int L)
{
    u64 nbrs = padj[v], a_iter;
    if (L - 2 < 1) return 0;
    if (__builtin_popcountll(nbrs) < 2) return 0;
    p2_plen = L - 2;
    p2_excl = 1ULL << v;
    a_iter = nbrs;
    while (a_iter) {
        int a = __builtin_ctzll(a_iter);
        a_iter &= a_iter - 1;
        /* only pair a with strictly larger neighbors: each cycle counted once */
        p2_targets = nbrs & ~(((1ULL << a) << 1) - 1);   /* bits > a */
        if (!p2_targets) break;
        p2_bfs_multi(p2_targets, p2_excl, p2_dist);
        p2_found = 0;
        if (p2_dist[a] <= p2_plen)
            p2_dfs(a, 0, (1ULL << a) | p2_excl);  /* mark v via excl anyway */
        if (p2_found) return 1;
    }
    return 0;
}

int p2_prune(graph *g, int n, int maxn)
{
    int i, j, k, v;
    (void)maxn;
    if (p2_nlen < 0) p2_init();
    if (n < 3) return 0;
    pn = n;
    for (i = 0; i < n; i++) {
        setword row = g[i];
        u64 m = 0;
        for (j = 0; j < n; j++)
            if (row & ((setword)1 << (WORDSIZE - 1 - j))) m |= 1ULL << j;
        padj[i] = m;
    }
    v = n - 1;                  /* the newly added vertex */
    for (k = 0; k < p2_nlen; k++) {
        int L = p2_lengths[k];
        if (L <= n && p2_cycle_through(v, L)) return 1;
    }
    return 0;
}

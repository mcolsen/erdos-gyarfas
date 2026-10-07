Erdos-Gyarfas power-of-2-cycle sweep of Conder's symmcubic10000 census
Date: 2026-07-27.  Scope: all 3815 census entries (796 with n<=2048 used as
validation set + re-swept; 3019 with 2048 < n <= 10000 = the new sweep range).

PIPELINE
1. Parsed symmcubic10000list.txt + the six relations files (3815 presentations;
   metadata cross-agreement between the two sources verified per entry;
   |Aut| = n * |H| verified per entry, |H| = 3*2^(t-1)).
2. Reconstructed every graph as the coset graph of the vertex-stabilizer
   H = <type's stabilizer generators> in G = <presentation>, adjacency
   xH ~ yH iff x^-1 y in H a H, via custom C HLT Todd-Coxeter (tc.c) with
   coincidence processing; graph = orbit closure of base edge {H, Ha} under
   the right-multiplication action (mkgraph.py).
   sympy's coset enumeration was tried first and was correct
   but too slow (258 s at n=4944 vs 0.03-2 s for tc.c); it was retained as a
   cross-validator: standardized coset tables byte-identical on 21/21 sampled
   entries spanning all six types, n = 4..3072.
3. Validation gates:
   (a) all 796 reconstructions with n<=2048 isomorphic to Conder's packaged
       graphs (nauty labelg canonical forms): 796/796 PASS.
   (b) for all 3815: vertex count, cubic, simple, connected, girth == census,
       bipartite == census: 3815/3815 PASS, zero mismatches.
   (c) cycle-checker (cycheck.c) validated against the previously
       brute-force-validated p2check.c on 5500 random cubic graphs
       (n=12..24 incl. girth>=5 sets): C4/C8/C16 flags, girth, bipartiteness
       all agree; zero failures.
4. Sweep tests (exact integer logic only):
   C4/C8: exact canonical-rooted DFS for simple cycles of that exact length
   (BFS-distance + parity pruning). C16 on {4,8}-free graphs: exact DFS,
   PLUS the closed cyclically-non-backtracking-16-walk dart search whenever
   girth >= 9 (2g > 16 makes it equivalent) - the two independent engines
   agreed on every one of the 2125 girth>=9 graphs (and NBW-8 vs cyc-8
   agreed on every girth>=5 graph).
5. Survivors: Glasgow subgraph solver (independent code) with C_L patterns;
   every positive mapping re-verified edge-by-edge as a simple cycle.

RESULTS
- {4,8,16}-free graphs: 689 of 3815 (23 with n<=2048, 666 in 2048<n<=10000).
  Full list: survivors_4_8_16_free.txt.  Girths: 7 (x9, all non-bipartite:
  C2030.1, C3276.4, C3584.13, C4060.1, C4060.2, C4060.10, C5740.1, C6622.2,
  C6622.3), 10 (x21), 11 (x4), 12 (x310), 13 (x1), 14 (x125), 15 (x14),
  17 (x3), 18 (x187), 19 (x6), 20 (x9).
- EVERY one of the 689 contains C32 AND C64 AND C128 (2067 witness cycles
  found by Glasgow, all verified; tarball survivor_pow2_witnesses.tar.gz).
  Zero timeouts, zero graphs needed the 256+ ladder.
- Therefore NO census graph on <= 10000 vertices avoids all powers of two:
  no counterexample to Erdos-Gyarfas in this family.
- Independent confirmation of C16-freeness by Glasgow on ground-truth files
  for all 23 survivors with n<=2048 (plus C4/C8), positive controls included,
  and on a 48-graph sample of sweep-range survivors (all girth<=8 survivors
  + 40 random): see work dir c16_xcheck_results.txt.

ERRATA vs the 2026-07-24 campaign report: that report claimed only 3
{4,8,16}-free graphs in the n<=2048 census (C2030.1, C1458.10, C1458.11).
The 3 are genuine (their properties re-verified here: C2030.1 girth 7
non-bipartite; C1458.10/11 girth 12 bipartite, no C16), but the count is
wrong: there are 23 such graphs with n<=2048, confirmed independently with
the Glasgow solver on Conder's own packaged adjacency lists (e.g. C1050.1,
girth 12, no C4/C8/C16).  REPORT.md now records the corrected count;
the "census clean" conclusion itself still stands (all 23
contain C32/C64/C128).

FILES (this directory)
- symmcubic10000_pow2_sweep.csv   per-entry results (3815 rows)
- survivors_4_8_16_free.txt       689 survivors w/ C32/C64/C128 status
- survivor_pow2_witnesses.tar.gz  witness cycles (689 x {C32,C64,C128})
- sweep_results.json, survivor_powers.json, recon_status.tsv  raw data
Code + intermediates: ../work (tc.c, cycheck.c, mkgraph.py, parsers,
runners, coset tables, adjacency lists, g6, validation logs).

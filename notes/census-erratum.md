# Erratum: the phase-1 Conder-census claim, corrected

REPORT.md §2c states: "Conder cubic symmetric census ≤ 2048 | 796 | 3
survivors (C2030.1, C1458.10, C1458.11)". **The survivor count and coverage
label are wrong; the tooling was not.**

## What actually holds (this worktree's sweep, 2026-07-27)

Full census to 10000 vertices (3,815 graphs, reconstructed from Conder's
group presentations via coset enumeration, validated by isomorphism against
Conder's packaged adjacency lists on the ≤2048 range and by metadata
(order/girth/bipartiteness) on all 3,815):

- **689 graphs are {4,8,16}-free** — exactly 23 with n ≤ 2048 (20 missed by
  phase 1: C1050.1, C1134.3–5, C1140.4, C1248.1, C1344.1/5, C1458.1,
  C1512.3, C1728.8, C1792.1, C1824.3, C1944.3/4/6, C1950.1, C2016.1,
  C2024.2/4 — plus the three already known). Survivor girths: 7×9, 10×21,
  11×4, 12×310, 13×1, 14×125, 15×14, 17×3, 18×187, 19×6, 20×9.
- **Every one of the 689 contains C32, C64, and C128** (2,067 Glasgow
  witness cycles, verified edge-by-edge; zero timeouts, zero inconclusive
  entries; C16 decisions triple-engined: exact DFS + non-backtracking dart
  search + Glasgow, zero disagreements). The census is clean: no
  counterexample below 10,000 vertices in the arc-transitive world.
- Artifacts archived in `results/census10000/` (per-graph CSV, survivor
  list, witness cycles, methodology README).

## Root cause

796 is the size of the Conder–Dobcsányi *768-vertex* (extended Foster)
census, not the ≤2048 census (~1,150 entries). Phase 1 evidently swept the
768 file under a ≤2048 label, plus the three separately-known large objects
(the phase-1 census scripts are not in the repo, so this is inference, not
autopsy — the count itself is what is certain).
Independent re-verification here: Glasgow absence proofs on Conder's own
packaged adjacency (not our reconstruction) confirm e.g. C1050.1 and C1458.1
have no C16, with positive control C1458.2 (has C16) and known survivor
C1458.10 (does not). `checker.py` agrees with Glasgow on C1050.1
(SURVIVOR at --limit 16) — the phase-1 checker is exonerated. The 11
archived SA specimens (n = 82–126) were also re-verified with Glasgow:
all genuinely {4,8,16}-free. No phase-1 result other than the census row
is affected.

## What the corrected picture buys

- The girth-7 fat-hole mechanism is not one sporadic miracle: the census
  holds a whole **Macbeath–Hurwitz family** (C2030.1 = non-orientable {7,3}
  map skeleton of PSL(2,29); siblings C182.3-adjacent, C364.*, C4060.1/2/10,
  C5740.1, C6622.2/3 across p = 13, 29, 41, 43) plus ~20 sub-2048 girth-10/12
  trace-hole objects (C1050.1, C1458.1, …) for the mechanism study.
- Smallest known cubic AT graph with no C16 drops from 1458 to **1050**
  (C1050.1, girth 12; the vertex-transitive record from the algebra
  worktree's PSV sweep is 630).

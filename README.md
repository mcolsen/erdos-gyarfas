# The Erdős–Gyárfás conjecture: a computational campaign

## Author's Note

Inspired by several vibe math results and the fact that I was not reliably using my full subscription allotments, I asked Claude Fable and GPT 6 Pro to find a counterexample to the Erdős–Gyárfás conjecture. They were not successful but apparently did find some interesting graphs. This paragraph is the only human-authored content in this repository. I have not reviewed the findings but am making them available for the next agent with a user who has tokens to burn.

## Introduction

> **Conjecture (Erdős–Gyárfás, mid-1990s).** Every graph with minimum degree
> at least 3 contains a simple cycle whose length is a power of two.

This repository is the durable, curated record of a July–August 2026
computational campaign and a subsequent GPT Pro investigation of the conjecture —
[problem #64](https://www.erdosproblems.com/64) on
erdosproblems.com, for which Erdős offered \$100 for a proof and \$50 for a
counterexample (he reportedly expected it to be *false*).

**Outcome: no counterexample exists on fewer than 36 vertices, any cubic
counterexample needs at least 50 vertices, none occurs in either symmetric
census through the stated limits, and the campaign's margin analysis explains
why every search lane failed in the same direction.** The conjecture won on
points. The full narrative, with per-run methods and times, is in
[REPORT.md](REPORT.md); a draft mathematical note is in
[paper/](paper/erdos-gyarfas-note.tex).

## Reading the archive

The repository contains two stages of AI-assisted research:

- **Original campaign (July–August 2026, with Claude):** the bounds summarized
  below, with methods and evidence in [REPORT.md](REPORT.md) and
  [REPORT-other-approaches.md](REPORT-other-approaches.md).
- **GPT Pro continuation (archive compiled October 6, 2026):** [chat/](chat/README.md)
  contains a curated account of the conversation, five runnable experiment
  bundles, graphs, certificates, and verification logs. Start with its
  [findings](chat/FINDINGS.md), [corrections](chat/CORRECTIONS.md), and
  [provenance](chat/PROVENANCE.md). The compilation date is not a date for every
  experiment, and the archive is not a verbatim transcript.

The continuation produced cubic graphs on **370 vertices avoiding C₄, C₈, C₁₆,
and C₃₂** and **26,550 vertices also avoiding C₆₄**,
plus interface constructions and obstruction arguments. Those two graphs
contain C₆₄ and C₁₂₈, respectively; **no counterexample was found**.
Its [search-status ledger](chat/SEARCH_STATUS.md) distinguishes completed
finite exclusions from interrupted or undecided searches. The earlier
campaign's lower bounds and the continuation's constructions are separate
results.

For consolidated claims, use the campaign reports and the continuation's
findings and corrections. Dated drafts, interim snapshots, and experiment
notes retain the scope and intermediate frontiers of their respective stages.

## Headline results

| # | claim | method | where |
|---|---|---|---|
| 1 | No counterexample on **n ≤ 21** | pure isomorph-free enumeration (no SAT); n=21 certified by **two** independent complete partitions, ~900 CPU-h | REPORT §2b |
| 2 | No counterexample on **n ≤ 32**, assumption-free | SAT modulo symmetries (SMS) + Glasgow propagator | REPORT §2b |
| 3 | **Any counterexample needs ≥ 36 vertices** | sound minimum-order structural chaining on top of #2 | REPORT §2b |
| 4 | Any **cubic** counterexample needs **≥ 50** vertices | SMS ladder n = 32..48, all zero; n=48 closed by separate monolith and cube-partition executions of the validated stack | REPORT §2a |
| 5 | Any **bipartite** counterexample needs **≥ 57** vertices | 2-colored SMS ladder n = 33..56, all zero | REPORT §2b |
| 6 | **≥ 2/3 of a minimal counterexample is cubic** (strengthens Carr's 4/7) | one-line proof from Carr's own corollaries | [verification/](verification/carr-2605.22844-verification.md) |
| 7 | **Δ ≤ ⌊(n−1)/2⌋** for every C₄-free graph with δ ≥ 3 | elementary; no minimality needed | [verification/](verification/carr-2605.22844-verification.md) |
| 8 | Both cubic symmetric censuses are **clean**: all 3,815 arc-transitive graphs ≤ 10,000 and all 111,360 vertex-transitive graphs ≤ 1,280 satisfy the conjecture | exact spectra; 689 + 100 {C₄,C₈,C₁₆}-free survivors **all** contain C₃₂ | REPORT §2c |
| 9 | Smallest cubic graph with no C₄/C₈/C₁₆ has **between 50 and 82 vertices** | SMS lower bound + 11 verified specimens at n = 82–126 | REPORT §2f, [results/](results/) |
| 10 | **Trace-hole Moore bound**: a cubic graph with tr(H^L) = 0 has n ≳ 2^{L/2−1} — walk-certified constructions cannot reach C₆₄ below 2.1×10⁹ vertices | Ihara–Bass analysis; believed novel | [notes/trace-moore-bound.md](notes/trace-moore-bound.md) |
| 11 | EG is false iff an **α-block** exists; no α-block has **n ≤ 32** | block-cut reduction + validated SMS ladder over the larger one-degree-2 space | REPORT §2g, [notes/block-program.md](notes/block-program.md) |

Two 2026 non-peer-reviewed inputs were independently adjudicated and both
found sound: [Carr, arXiv:2605.22844](https://arxiv.org/abs/2605.22844)
(verified, then strengthened — #6 above) and
[Balaji's SMS frontier n ≤ 31](https://github.com/ArjunBalaji79/erdos-gyarfas-min-degree-3)
(design audit + full replication + count-exact cross-validation).

## Repository map

```
REPORT.md         the campaign log: every method, every number, every correction
REPORT-other-approaches.md
                  detailed alpha-block, census, lift, and arithmetic lane record
STATUS.md         archival stopping state of the interrupted alpha-block runs
paper/            draft mathematical note (LaTeX)
chat/             GPT Pro continuation: topic notes, five experiment bundles,
                  retained graphs, corrections, and certificate verifiers
src/              toolchain: geng PRUNE plugin, exact cycle checkers (C + Python),
                  SAT encodings, annealers, drivers — built via src/build.sh
verification/     adjudication of Carr arXiv:2605.22844 + the 2/3 and Δ-cap proofs
results/          graph artifacts (graph6), census survivors, and compact run
                  certificates including the final n=48 two-path evidence
notes/            algebraic, block-program, regime, and correction notes
```

Both former worktree histories are merged into `main`. The other-approaches
lane contains the α-block equivalence program (EG is false iff an α-block
exists; exhaustive ladder empty through n = 32), the corrected Conder census
sweep to 10,000 vertices, the cyclic-lift closure through 127 vertices, and the
regime analysis. Its interrupted higher-rung state is preserved in
[STATUS.md](STATUS.md); those partial runs establish no additional verdict.

## Methodology

The standing rule was to use disjoint stacks or runs where feasible and,
otherwise, to validate every ingredient count-exactly on nonzero controls.
The nauty/`geng` stack and the SMS stack — disjoint codebases, disjoint
algorithms — agreed on five gates before the SMS stack was trusted alone; the
exact cycle checker was validated against brute force on all 13,591 graphs with n ≤ 8; the
enumeration reproduced Markström's published counts before extending them;
and the n = 21 capstone was enumerated twice via independently sliced
partitions. The n=48 cubic rung likewise agrees between a full monolith and a
complete recursive cube partition after the cubing machinery reproduced a
known positive count exactly. Two self-corrections are part of the public
record, both caught by this discipline before any claim rested on them: a res/mod splitting
subtlety (REPORT §2b — cross-modulus refinement of `geng` work classes is
**unsound**; single-modulus partitions are exact) and a census coverage
erratum (REPORT §2c).

## Reproducing

Everything was run on one 48-thread workstation (Fedora). Rough recipe:

1. `src/build.sh` — builds the C tools against [nauty 2.8.9](https://pallini.di.uniroma1.it/).
2. SMS ([Kirchweger–Szeider](https://github.com/markirch/sat-modulo-symmetries))
   and the Glasgow subgraph solver, built from source at the commits pinned in
   Balaji's repo; Python venv with `networkx`, `python-sat`, `pysms`.
3. Per-run command lines, shard layouts, and wall/CPU times are documented
   inline in REPORT.md; drivers in `src/` (`run_shards.sh`, `sms_frontier.sh`,
   `sa_fleet.sh`).

Heed the res/mod warning in REPORT §2b if you distribute `geng` runs.

## Provenance

The repository history is the timestamp record:

| date (2026) | commit | event |
|---|---|---|
| 07-24 | `4405c4b` | campaign start |
| 07-24 | `be3ef56` | toolchain + adjudications + **the 2/3 strengthening** (#6) |
| 07-25 | `07b4abc`… | bipartite ladder, [65,127] window, extremal bracket |
| 07-27 | `18ebb32` | res/mod method correction (public self-erratum) |
| 07-29 | `38006a9` | n = 21 settled (complete mod-256 partition, zero) |
| 07-30 | `ff2ab64` | n = 21 cross-certified (complete mod-16 partition, zero) |
| 07-30 | `530f21d` | census erratum folded into main (corrected sweeps) |
| 07-30 | `6f8ae56` | α-block ladder through n = 32, all zero |
| 07-31 | `de749f2` | cubic n = 46 rung zero |
| 08-04 | archived in final merge | cubic n = 48 closed by two paths; frontier ≥ 50 |
| 08-08 | final history merge | algebra and other-approaches histories reconciled on `main` |

The 2/3 bound (#6) was independently observed in a post by user *jul059* on
the erdosproblems.com problem-64 forum dated **2026-07-26**; commit `be3ef56`
above records this repository's proof on **2026-07-24**.

## Citing

```bibtex
@misc{olsen2026eg,
  author = {Olsen, Maria},
  title  = {Computational and structural bounds for the
            Erd\H{o}s--Gy\'arf\'as conjecture},
  year   = {2026},
  note   = {Code, data, research notes, and verification artifacts in this repository.}
}
```

## Acknowledgments & license

The original campaign was designed and executed in collaboration with Claude
(Anthropic); the continuation in `chat/` was developed with GPT Pro / ChatGPT
(OpenAI). Prior art this work builds on: Markström (2004), Royle (c. 2004),
Carr (2026), Balaji (2026), and the nauty / SMS / CaDiCaL / Glasgow tool
authors.

No repository-wide license has been specified. See also the continuation's
[license and attribution note](chat/LICENSE-NOTE.md).

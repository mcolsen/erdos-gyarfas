# Claude session audit and campaign closure

This note records the 2026-08-08 review of the Claude transcripts associated
with this repository and reconciles their unfinished-looking messages with the
committed record. It is a provenance map, not a new search result.

## Sessions reviewed

- `a14ef79b-70db-4db3-a343-dc053ee8e021`: phase-1 campaign, correction,
  archive, README, and draft-paper work. Its mathematical outcomes are backed
  by the phase-1 commits merged into `main`.
- `e397a738-ce4d-43e7-a8c4-3397853029a5`: algebraic-program validation,
  trace-Moore work, exact lift and census sweeps, trace-hole census, n=46, and
  the n=48 cube-and-conquer run. Commits through `34f4b5d` preserve the work up
  to the 2026-08-01 interim snapshot.
- `f17f05c3-6fb4-4896-bd91-d502d0079c30`: worktree-local continuation and
  post-run notifications. The decisive n=48 outputs landed after Claude access
  failed, so no Claude turn folded them into git.
- `861ff342-c435-47d6-8a57-0bf3eedbcd99`: setup only; no mathematical result
  or unpreserved experiment.
- Subagents `agent-a9e49c75dc71dd7e5` and `agent-a3afdf4936106e92c`:
  independent trace-Moore/Foster verification and literature/census-source
  audit. Their conclusions are distilled in `trace-moore-bound.md` and
  `algebraic-program-validation.md`.

The raw JSONL transcripts were not copied into git: they mostly duplicate
commits, contain large tool chatter and machine-specific temporary paths, and
are not the reproducibility artifacts. The durable record is the source,
notes, graph witnesses, correction history, and compact final certificates.

## Reconciled outcomes

- The phase-1 n=21 enumeration is complete through two pure single-modulus
  partitions, both zero. The earlier cross-modulus refinement idea is recorded
  as unsound and was not used for a claim.
- The corrected Conder census and complete PSV census are recorded with their
  final survivor counts; all survivors satisfy the conjecture.
- The stochastic and CEGAR searches concluded negative. Text saying they were
  running was stale status, not an unfinished promised result.
- The scoped algebraic program completed: full PSV census, all bases through
  six vertices including semi-edges, loopless eight-vertex bases, the stated
  group library, and the parameterized two-vertex winding searches. The
  proposal note is retained but marked superseded by its validation report.
- The n=48 cubic rung is zero by two completed paths: the monolith and the full
  recursive cube partition. `results/n48_final_20260804.tar.gz` and its
  checksum preserve the final evidence. The cubic frontier is at least 50 and
  the {C4,C8,C16}-free extremal bracket is [50,82].
- The direct top-level cube-0 worker was only a redundant third path. It was
  stopped after final archival on 2026-08-08; no campaign process remains.
- The separate other-approaches history is now merged into `main`: α-block
  equivalence and the B0 ladder through n=32, the corrected Conder census,
  cyclic-lift closure, arithmetic assessment, implementation, and compact
  artifacts are all retained. Its last ignored shepherd snapshot
  (2026-08-03T05:33:26Z) is distilled in `STATUS.md`: n=33 stopped at 520/522
  race cubes, n=34 at five complete shards plus 411/1,360 per-cube jobs, and
  capped n=46 at one of four shards. None of those partial runs yielded a
  verdict.

## Scope boundaries

- No n=50 rung was attempted.
- Eight-vertex bases with semi-edges and some exotic group families were not
  swept; the exact lift claim is limited accordingly.
- Larger-base trace-32 winding lattices, anti-Ramanujan constructions, and
  C2030-style exact cycle-hole constructions were not resolved by the campaign.
- The interrupted n=33, n=34, and capped-cell jobs are preserved as scoped
  partial attempts, not pending promises or mathematical results. No process
  from that lane remained active at the 2026-08-08 audit.
- The draft paper is an archival account of the campaign, with its
  bibliographic limitations recorded in the source.

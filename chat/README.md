# Erdős–Gyárfás: chat research archive

A curated record of the computational and structural investigation in Maria Olsen's research conversation with **GPT Pro / ChatGPT (OpenAI)**. Compiled **2026-10-06** from the visible chat and retained artifacts, and incorporated into this repository as `chat/`. The earlier July–August campaign is documented in the [repository README](../README.md) and [campaign report](../REPORT.md).

**No counterexample was found.** The archive contains successful partial constructions, mathematical obstruction arguments, scoped computational exclusions, exploratory runs that remain unresolved, and the corrections needed to interpret them correctly.

## Start here

Read [FINDINGS.md](FINDINGS.md) for the result index, [CHRONOLOGY.md](CHRONOLOGY.md) for the progression of the investigation, and [CORRECTIONS.md](CORRECTIONS.md) before citing early claims. [REPRODUCING.md](REPRODUCING.md) explains what can be checked independently and how. [PROVENANCE.md](PROVENANCE.md) describes the source material, recovered artifacts, and editorial history; this is a research archive rather than a verbatim transcript.

## Latest retained state

| Object / result | What is established | Essential limit |
|---|---|---|
| 190-vertex cubic graph | No C4/C8/C16; exactly **178,077 C32s** | Contains C32; no order-minimality claim |
| 370-vertex cubic graph | No C4/C8/C16/C32; no cycles 16–32; exactly 43 C33s | Explicit C64 witness |
| 26,550-vertex cubic graph | No C4/C8/C16/C32/C64; no cycles 16–64; exactly 630 C65s | Explicit C128 witness |
| Theta(2,3,4) phase interfaces | Exact-one rule removes the dyadic length from a selected expanded cycle family at every dyadic scale | Boundary examples still have degree-two terminals |
| Constructed 554-cell catalogue | **468 uniform transmitters; 86 explicit local escapes** | Not all possible cells; uniform reductions do not exclude arbitrary mixtures |
| All-T7/T15 obstruction | Such assemblies on **any connected simple cubic core**, including cores with bridges, contain a dyadic cycle | Specific templates, not arbitrary seven-/fifteen-vertex cells |
| Joint synthesis | 13,486 checked routing schemas across retained runs | All synthesis verdicts remain UNKNOWN or UNKNOWN_SOLVER |
| Terminal identification | 6,087 degree-complete rejected candidates; 67,272 checked guarded cycle clauses | No identification search domain was exhausted |

Central graph files and their measured metadata are indexed in [data/graphs/README.md](data/graphs/README.md). The theorem notes distinguish unbounded arguments from finite regression checks; none is presented as proof-assistant formalization or peer-reviewed publication.

## Repository layout

```text
docs/                    discrete topic notes: early searches, constructions,
                         proofs, interfaces, synthesis, and remaining scope
experiments/
  01-gadget-compression/  exact cell compression, n190 search, and n370 construction
  02-gap64/              26,550-vertex construction and structural checks
  03-phase-interfaces/   exhaustive 181-cell domain, phase rings, repair certificates
  04-interface-filters/  554-cell catalogue, routing oracle, completion/motif witnesses
  05-joint-synthesis/    all-scale profiles, joint learning, guarded identification
legacy/                  retained early sources, graphs, incidence table, cap summary
data/graphs/             central copies and explicitly reconstructed graph checkpoints
provenance/              source notes, input hashes, extraction and reconstruction maps
verification/packaging/  checks actually rerun while preparing this archive
tools/                   archive checks, verifier runner, and legacy reconstruction
MANIFEST.sha256          outer file-integrity manifest
```

The five experiment directories preserve the runnable layout, source code, data, certificates, and logs of the original bundles. Their narrative notes received an archival edit; manifests describe the current files. Historical notes and logs may contain obsolete `/mnt/data/...` scratch paths; the current documentation maps retained files to portable repository paths and does not imply that every historical scratch file exists. See [PROVENANCE.md](PROVENANCE.md) for the distinction between original packaging checks and current file integrity.

## Verification

From `chat/`, using the packaging environment (Python 3.13.5 and NetworkX 3.6.1):

```sh
python -m pip install -r requirements-verify.txt
python tools/check_archive.py
python tools/run_verifiers.py
```

The default runner invokes certificate verifiers, **not the optimization searches**. Do not use `python -O`: the retained checkers use assertions. Compiler-dependent direct counters and solver-dependent search programs are optional and documented separately.

During packaging, all five input manifests matched and all nine selected retained verification programs passed again. Twenty-one central graph files also received fresh structural checks; direct power-length counts were rerun where practical. The 26,550-vertex absence claim was checked by its exact structural verifier, not by brute-force enumeration of all long cycles. These checks do not recover lost early search ledgers or prove literature novelty.

## Attribution and publication status

This is preliminary AI-assisted research by Maria Olsen with GPT Pro / ChatGPT. Existing work and external theorem references are identified in [REFERENCES.md](REFERENCES.md). No new software license or publication-priority claim is assigned here; see [LICENSE-NOTE.md](LICENSE-NOTE.md).

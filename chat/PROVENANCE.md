# Provenance and preservation

## Source layers

This archive combines three evidence layers from Maria Olsen's conversation with GPT Pro / ChatGPT (OpenAI): substantive reports in the visible conversation; graph/source/note artifacts retained from those reports; and five runnable research bundles. It is not a raw message export. The earlier campaign is preserved in the [parent repository](../README.md).

`provenance/input_archives.json` records each input ZIP's SHA-256, original internal top directory, packaged experiment directory, and file count. At initial packaging, each internal member was copied without edits; only its outer directory name changed. The original bundle manifests were verified against all 312 listed member entries; the five manifests themselves brought the preserved experiment member total to 317 files.

The five research notes were also copied to `provenance/`. Thematically split notes in `docs/` use their section text with a scope/source wrapper. `provenance/topic_extraction_map.json` gives the original section numbers. Earlier unbundled findings were transcribed into notes 01–04 with explicit historical-evidence labels.

## Repository editorial history

Commit `eee4ebd` imported the packaged archive into `chat/` on 2026-10-06.
The subsequent archival edit removed planning and correspondence reminders,
replaced upload instructions with repository navigation, and recast useful
unfinished-work descriptions as limits of the retained evidence. This includes
the narrative notes in `experiments/` and their copies in `provenance/`.
Original source code, graphs, certificates, and run logs were preserved.

The outer and nested file manifests describe the edited tree. Input ZIP hashes
and `verification/packaging/` logs describe the original packaging operation;
they are historical records, not hashes or fresh verification logs for the
edited prose. Git history preserves the imported wording and original manifests.

## Recovered graphs

The 219,531 graph is fully specified by `legacy/replay/edge_counts_219531.tsv`: its first two columns list every edge. The 220,225 graph is recovered from a literal base64 payload preserved in a user-visible code cell in the chat; that payload is saved separately. The three recorded surgeries recover 216,687, 216,367 and 216,246. The final 216,246 bytes match the later gadget bundle's input exactly.

`tools/reconstruct_legacy_graphs.py` reproduces these recoveries. They reconstruct explicit saved data, not guessed graphs with matching counts. All recovered graphs received new direct cycle counts. The lost 224,547 graph has no comparable recovery record.

The 61-vertex graph's original graph6 bytes are preserved. Its central DIMACS copy is a representation conversion using NetworkX, not a new specimen. Central copies of later graphs are byte-identical to their experiment originals.

## Timestamps

The packaging date is 2026-10-06. Stage numbers represent conversation order. Original log/environment files retain their own metadata, but those are not replaced with invented dates. Random seeds that resemble dates are not treated as experiment timestamps. Historical runtime claims are not used as evidence that background work actually persisted after a response.

## Integrity versus scientific validity

The outer and nested manifests verify current file integrity. Executed verifier logs establish that the included finite certificate checkers accepted their inputs in the observed packaging environment. Those facts are distinct from exhaustive discovery, a general mathematical theorem, or an independent literature review.

The package is intentionally conservative about missing material. `data/missing_artifacts.json` identifies important absent checkpoints and raw ledgers; `CORRECTIONS.md` distinguishes withdrawn claims from merely unrecoverable ones.

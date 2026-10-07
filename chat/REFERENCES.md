# Sources and external references

This document records sources used or cited in the conversation. No fresh literature search was performed for the documentation task; current conjecture status, priority and bibliographic details beyond the retained source record are not independently established here.

## Primary research record

The authoritative evidence for this continuation is the explicit data, code and certificates in the five `experiments/` directories. Their original prose notes are preserved in `provenance/`, and topic notes link to them by relative path. Earlier claims without corresponding artifacts are labelled historical in notes 01–04.

Maria Olsen's original repository, supplied by the user: `https://github.com/mcolsen/erdos-gyarfas`. Its README and reports were read earlier in the conversation. The background results in note 01 belong to that campaign and are not reproduced wholesale in this archive.

## Matching-polytope theorem used in the charge arguments

Jack Edmonds, *Maximum matching and a polyhedron with 0,1-vertices*, Journal of Research of the National Bureau of Standards, Section B, 69(1–2), 125–130 (1965). DOI: `10.6028/jres.069b.013`.

The retained joint note also cites a primary-source restatement: Guoli Ding, Lei Tan, Wenan Zang, *When Is the Matching Polytope Box-Totally Dual Integral?*, Mathematics of Operations Research 43(1), 64–99, online 2017. DOI: `10.1287/moor.2017.0852`.

The local turn-charge identities, interval deductions, and leaf-component extension are presented in this archive as derived arguments. Their use of the matching theorem is explicit; no independent novelty claim is made.

## Background mentioned in the upstream campaign

The source record refers to Markström's 2004 computation, Royle's earlier enumeration, Carr's `arXiv:2605.22844`, and Balaji's `erdos-gyarfas-min-degree-3` repository. Those bibliographic references are carried forward as context; their full texts are not supplied here and their original claims were not re-adjudicated during packaging.

The upstream experiment record also attributes nauty/geng, SAT modulo symmetries, CaDiCaL and the Glasgow subgraph solver. This archive includes later Python/C/C++ research sources, not distributions of those tools.

## Named bases and data provenance

The gap constructions use explicit LCF specifications and saved edge lists. Those files, rather than an unstated external graph name or remote download, define the reproducible graphs. The small-graph atlas controls use NetworkX. Historical exploration consulted Sage's graph-generation source; no correctness claim here depends on a graph name without retained edges.

## Citation guidance

When citing a finding, state its precise domain and link its topic note plus graph/certificate. Treat finite tests as verification of concrete ingredients, not as proof of an unbounded theorem. Use [CORRECTIONS.md](CORRECTIONS.md) to avoid quoting a superseded count or an early unsupported interpretation. This archive does not assign a DOI or arXiv identifier to itself.

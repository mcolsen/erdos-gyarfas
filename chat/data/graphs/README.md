# Central graph inventory

These are real retained or explicitly reconstructed files. All use one-based DIMACS edge lists. Counts below are fresh direct counts except the n26,550 gap, which is certified by exact structural verification. Full hashes, source provenance, degree distributions, and check outputs are in [index.json](index.json).

| File | n | m | Degree distribution | Selected counts / witness |
|---|---:|---:|---|---|
| [n032_phase_boundary.edge](n032_phase_boundary.edge) | 32 | 40 | 2: 16, 3: 16 | C4=0, C8=0, C16=0, C32=0 |
| [n040_phase_boundary.edge](n040_phase_boundary.edge) | 40 | 50 | 2: 20, 3: 20 | C4=0, C8=0, C16=0, C32=0 |
| [n061_one_deficiency_c16_8.edge](n061_one_deficiency_c16_8.edge) | 61 | 91 | 2: 1, 3: 60 | C4=0, C8=0, C16=8, C32=176980 |
| [n064_phase_boundary.edge](n064_phase_boundary.edge) | 64 | 80 | 2: 32, 3: 32 | C4=0, C8=0, C16=0, C32=0, C64=0 |
| [n181_noncubic_c32_831828.edge](n181_noncubic_c32_831828.edge) | 181 | 273 | 3: 180, 6: 1 | C4=0, C8=0, C16=0, C32=831828 |
| [n183_noncubic_c32_819153.edge](n183_noncubic_c32_819153.edge) | 183 | 276 | 3: 180, 4: 3 | C4=0, C8=0, C16=0, C32=819153 |
| [n183_uncapped_c32_296418.edge](n183_uncapped_c32_296418.edge) | 183 | 273 | 2: 3, 3: 180 | C4=0, C8=0, C16=0, C32=296418 |
| [n184_c32_492309.edge](n184_c32_492309.edge) | 184 | 276 | 3: 184 | C4=0, C8=0, C16=0, C32=492309 |
| [n186_c32_279630.edge](n186_c32_279630.edge) | 186 | 279 | 3: 186 | C4=0, C8=0, C16=0, C32=279630 |
| [n186_c32_476415.edge](n186_c32_476415.edge) | 186 | 279 | 3: 186 | C4=0, C8=0, C16=0, C32=476415 |
| [n190_c32_178077.edge](n190_c32_178077.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=178077 |
| [n190_c32_216246.edge](n190_c32_216246.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=216246 |
| [n190_c32_216367.edge](n190_c32_216367.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=216367 |
| [n190_c32_216687.edge](n190_c32_216687.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=216687 |
| [n190_c32_219531.edge](n190_c32_219531.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=219531 |
| [n190_c32_220225.edge](n190_c32_220225.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=220225 |
| [n190_c32_446643.edge](n190_c32_446643.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=446643 |
| [n190_checkpoint_claimed303008.edge](n190_checkpoint_claimed303008.edge) | 190 | 285 | 3: 190 | C4=0, C8=0, C16=0, C32=303008 |
| [n26550_c4c8c16c32c64free.edge](n26550_c4c8c16c32c64free.edge) | 26550 | 39825 | 3: 26550 | C4=C8=C16=C32=C64=0; C65=630 (structural); C128 witness |
| [n294_c16_122.edge](n294_c16_122.edge) | 294 | 441 | 3: 294 | C4=0, C8=0, C16=122 |
| [n370_c4c8c16c32free.edge](n370_c4c8c16c32free.edge) | 370 | 555 | 3: 370 | C4=0, C8=0, C16=0, C32=0, C33=43 |

No entry is a counterexample. Degree distribution `2:32, 3:32`, for example, means 32 vertices have degree two and 32 have degree three. A boundary graph can be power-free and still fail the minimum-degree requirement.

The original graph6 seed and old sources remain in [legacy](../../legacy/). Missing or withdrawn claims are listed in [missing_artifacts.json](../missing_artifacts.json) and [CORRECTIONS.md](../../CORRECTIONS.md).

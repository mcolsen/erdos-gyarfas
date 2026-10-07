# U11 variable-factor transmission and final catalogue classification

**Scope/status:** Final classification of the 554 supplied objects: 468 uniform transmitters and 86 explicit local escapes. U11 is not the earlier G11.

**Retained source:** [eg_joint_research_note.md](../provenance/eg_joint_research_note.md).

**Executable evidence:** [experiments/05-joint-synthesis](../experiments/05-joint-synthesis/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 3. Resolve the remaining catalogue cell: U11

Do not confuse this cell with the earlier G11 having chords 0-2 and 5-7. Here

    U11 = C11 + {0-2, 4-9},

with vertices 0,...,10 and terminals (1,3,5,6,7,8,10). It is catalogue `cell0095`.

Its inclusion-minimal contribution supports, in the certificate's index order, are

    0: {2,6,10,11}
    1: {3,5,9,10}       = B
    2: {3,7,8,9,10}
    3: {4,5,8}          = D
    4: {4,6,7,10,11}
    5: {4,8,9}
    6: {5,7,8,9,10}
    7: {6,7,8,9}.

Every actual turn support contains at least one of these minimal supports. There are 330 multisets of four minimal supports. Exactly one fails to realize a total of 32:

    B,D,D,D.

For every other multiset, an explicit choice summing to 32 is retained.

### Variable-factor transmission theorem

For every r divisible by four, and every sequence of r turns in U11, the expanded spectrum contains either 4r or 8r. Consequently every dyadic quotient cycle transmits a dyadic cycle.

**Proof.** Partition the selected minimal supports into blocks of four. Call a block bad only if it is BDDD. Two bad blocks can be repartitioned into BBDD and DDDD, both good. A bad block together with any partner block other than DDDD can also be repartitioned into two good blocks. `u11_variable_dilation.json` supplies and verifies all 329 such finite repartition identities.

Repeated repairs therefore remove every bad block unless the entire sequence has one B and r-1 Ds. In the nonexceptional case, choose contribution 32 from each good block, totaling 8r. In the exceptional case, choose 3 from B, 5 from one D, and 4 from each other D, totaling

    3 + 5 + 4(r-2) = 4r.

Enlarging a chosen minimal support to the original actual support cannot remove these paths. QED.

The exception is real, not merely a gap in the method: BDDD...D cannot make 8r. The low B choices are too small, whereas B=9 or 10 requires deficits one or two from the maximum-eight D choices. D permits only deficits zero, three, or four.

Together with the previous pentagon theorem, this leaves **468 uniformly transmitting catalogue cells and 86 with explicit power-free four-turn witnesses**. All prior cell graphs/path sets and four-turn certificates were rechecked this turn. This classification concerns the supplied 554 objects only; it is not a classification of all possible interfaces.

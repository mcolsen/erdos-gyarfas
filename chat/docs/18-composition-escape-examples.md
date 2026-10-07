# Parity, odd-divisor and narrow-band composition escapes

**Scope/status:** Local cycle-family escapes, not complete minimum-degree-three graphs.

**Retained source:** [eg_interface_filters_note.md](../provenance/eg_interface_filters_note.md).

**Executable evidence:** [experiments/04-interface-filters](../experiments/04-interface-filters/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 3. Three explicit interfaces that escape the common mechanism

### 3.1 Hexagon: a parity-twisted cycle family

A C6 has contribution supports, according to terminal distance 1,2,3,

    {2,6}, {3,5}, {4}.

On any simple r-cycle, take opposite terminals at r-1 visits and a distance-two turn at one visit. The *entire* expanded cycle family is

    {4r-1,4r+1}.

Both lengths are odd. Therefore neither is a power of two. This is an all-r statement about the selected turn pattern, not a claim that all cycles in a larger assembly receive that pattern.

### 3.2 Heptagon: an odd-divisor cycle family

For C7, terminal distance two gives internal paths of lengths 2 and 5, hence contributions

    {3,6}.

Using this turn at every visit yields exactly

    {3r,3r+3,...,6r}.

Every length is divisible by three, so every power of two is absent, for any r. The cell itself only contains its internal 7-cycle and is safe. It still has five unused terminals per visited cell.

### 3.3 A narrow interval, not a gapped spectrum

Define G11 as C11 on vertices 0,...,10 plus chords 0–2 and 5–7. Its seven terminals are

    {1,3,4,6,8,9,10}.

Its internal cycle polynomial is

    2x^3 + x^9 + 2x^10 + x^11,

so it is internally power-free. The terminal pair (3,8) has exact internal path support {4,5,6}, or contributions {5,6,7}.

Repeating that turn on a dyadic r-cycle produces the complete interval

    [5r,7r],

which lies strictly between the consecutive powers 4r and 8r.

This corrects an overly narrow design intuition: an interface need not have holes in its individual path support. A sufficiently narrow, appropriately positioned interval can escape inheritance too. What matters is the composed support around a cycle, together with the feasibility of completing all other terminals.

# All-T7/T15 obstruction for cubic cores with bridges

**Scope/status:** Extends the specific-template obstruction to all connected simple cubic cores. Includes the local necessary mixed-cell inequality.

**Retained source:** [eg_joint_research_note.md](../provenance/eg_joint_research_note.md).

**Executable evidence:** [experiments/05-joint-synthesis](../experiments/05-joint-synthesis/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 6. Remove the bridge exception from the T7/T15 obstruction

### Theorem

An assembly using only T7 and T15 on **any connected simple cubic core**, with any terminal orientations, contains a power-of-two simple cycle. The core is not required to be bridgeless.

This is a theorem about these explicit templates, not arbitrary seven- or fifteen-vertex graphs, and not arbitrary interfaces or noncubic cores.

### Charges and the bridgeless case

Each turn has a complete interval of contributions [l,u]. A core cycle therefore expands to every length in [L,U]. If this interval avoids all powers of two, it fits in [2^k+1,2^(k+1)-1], hence 2L-U>=3.

Assign each turn charge w=2l-u. For T7 the three charges are (-1,-1,+1), whose sum s is -1. For T15 they are (-7,-7,-3), whose sum is -17.

The following standard consequence of Edmonds's matching-polytope theorem is used: a bridgeless loopless cubic multigraph has a probability distribution on perfect matchings with every edge marginal 1/3. Indeed, x_e=1/3 has vertex sums one, and every odd cut has at least three edges, so it lies in the perfect-matching polytope. Complementary two-factors therefore use each turn with probability 1/3.

In a bridgeless core, the expected charge of a complementary two-factor is (sum_v s_v)/3<0. But if all expanded cycles were power-free, each component cycle would have charge at least three, so every two-factor would have total charge at least three. Contradiction.

### Leaf bridge-component argument

Suppose the core has bridges. Delete them, and choose a leaf component B of the resulting component tree. It cannot be a singleton: a singleton in a cubic core would meet three bridges, not one. Within B exactly one vertex w has degree two; every other vertex has degree three. B is bridgeless.

Suppress w, replacing its two-edge path by one distinguished edge e. The result H is a bridgeless loopless cubic multigraph; parallel edges are allowed. Use the perfect-matching distribution above and lift its complementary two-factors back to B. For every v other than w, each turn is used with probability 1/3. Vertex w is used precisely when e belongs to the two-factor, with probability 2/3. Its one available turn has charge c_w<=1.

If the complete expanded graph were power-free, every cycle of every such lifted two-factor would have charge at least three. Its total charge would therefore be at least three. Taking expectations instead gives

    (sum_{v in B, v!=w} s_v + 2 c_w)/3
       <= (-(|B|-1)+2)/3
        = (3-|B|)/3
        < 3,

a contradiction. QED.

For mixed T3/T7/T15 cores the same argument gives the useful **local necessary condition**

    sum_{v in B, v!=w} s_v + 2 c_w >= 9

for every leaf bridge component, with s=3 for T3. It does not exclude every mixed construction.

### External theorem reference

Jack Edmonds, *Maximum matching and a polyhedron with 0,1-vertices*, Journal of Research of the National Bureau of Standards, Section B 69(1–2), 125–130 (1965), DOI: 10.6028/jres.069b.013. A primary-source restatement of the matching-polytope inequalities is given in the abstract of Guoli Ding, Lei Tan, Wenan Zang, *When Is the Matching Polytope Box-Totally Dual Integral?*, Mathematics of Operations Research 43(1), 64–99, online 2017, DOI: 10.1287/moor.2017.0852. The charge identities and bridge extension above are derived here; no literature novelty claim is made.

# Heptagon turn-count profiles at every dyadic scale

**Scope/status:** All-orders proof with 11,304 finite regression cases; selected simple quotient cycles only.

**Retained source:** [eg_joint_research_note.md](../provenance/eg_joint_research_note.md).

**Executable evidence:** [experiments/05-joint-synthesis](../experiments/05-joint-synthesis/). Internal code/data paths in the extracted research text below are relative to that experiment directory. The section text is preserved from the source note; later corrections and superseding claims are indexed in [CORRECTIONS.md](../CORRECTIONS.md).

---

## 2. Exact heptagon turn profiles at every dyadic scale

For a C7 cell, terminal separations one, two, and three give contribution supports

    A = {2,7},   B = {3,6},   C = {4,5}.

Let r=2^k, k>=2, be a simple quotient-cycle length, and let a,b,c count its A,B,C turns. Thus a+b+c=r. Its complete expanded spectrum is

    2a+3b+4c + {5x+3y+z : 0<=x<=a, 0<=y<=b, 0<=z<=c}.

All lengths lie between 2r and 7r, so the only possible dyadic lengths are 2r and 4r. The former occurs exactly for the all-A pattern. The latter occurs exactly when

    5x+3y+z = 2a+b                                      (H)

has a solution in the stated bounds.

### Theorem

The expanded family is power-free exactly for the following three profiles:

| Exponent k | Safe (a,b,c) profiles |
|---|---|
| k even | (0,r,0), (r-1,1,0), (r-2,0,2) |
| k odd | (0,r,0), (r-2,2,0), (r-1,0,1) |

The order of the turns is irrelevant for this one-cycle calculation. It is a necessary-and-sufficient statement for these selected simple-quotient-cycle families, not a sufficient condition for a complete assembly to be a counterexample. Additional cycles, including repeated cell visits, still matter.

For example, at r=8 the safe profiles are (0,8,0), (6,2,0), and (7,0,1). At r=16 they are (0,16,0), (15,1,0), and (14,0,2).

### Proof of completeness

Set D=2a+b and M=5a+3b+c. We solve (H) by cases. An interval of at least five consecutive integers remains an interval after adding the choices {0,5}; an interval of at least three remains an interval after adding {0,3}. This supplies the simple induction steps below.

* If c>=4, start with [0,c], add all a choices {0,5}, then all b choices {0,3}. The entire interval [0,M] is present, so D is present.
* If c=3 and b>=1, the choices for y,z first fill [0,3b+3], after which the five-steps fill [0,M]. If b=0, the attained residues modulo five are 0,1,2,3. The target 2r-6 has excluded residue four only when r is divisible by five, impossible for a power of two. The selected quotient and remainder respect the bounds.
* If c=2 and b>=1, the choices for y,z fill [0,3b+2], of width at least six; adding five-steps fills [0,M]. If b=0, the attained residues are 0,1,2 modulo five. The target 2r-4 fails precisely for r congruent to plus or minus one modulo five, equivalently even k. This is (r-2,0,2).
* Suppose c=1. If a=0, D=b=r-1 is zero or one modulo three; choose z that residue and y=(b-z)/3. If b=0, the allowed residues are zero and one modulo five, so D=2r-2 fails exactly for odd k. If a>=1,b=1, the allowed residues are 0,1,3,4 modulo five; D=2r-3 misses only when r is divisible by five. If a>=1,b>=2, the sumset contains [3,M-3]. The base (a,b)=(1,2) contains every integer 3 through 9; additional three- or five-steps preserve the claimed interval. D lies inside it.
* Finally suppose c=0. If a=0, the all-B contributions are multiples of three and neither 2r nor 4r is available. If b=0, all-A has the forbidden 2r. If a=1, choose x=0 when r is two modulo three, or x=1 when r is one modulo three; the resulting y is in [0,b]. For a>=2,b=1, the available residues modulo five are 0,3; D=2r-1 fails exactly for even k. For a>=2,b=2, the available residues are 0,3,1; D=2r-2 fails exactly for odd k. For a>=2,b=3, the residues are 0,3,1,4; D=2r-3 would fail only if five divided r. Finally, for a>=2,b>=4 the sumset contains [8,M-8]. The base (2,4) contains all integers 8 through 14, and adding three- or five-steps proves the interval by induction. D lies inside it.

For the residue arguments, r=2^k is plus or minus one modulo five exactly when k is even, and plus or minus two exactly when k is odd. Nonnegative bounded solutions in the listed small cases follow directly from the quotient/remainder choices; the r=4 cases are included. These cases exhaust all nonnegative a,b,c. QED.

`certificates/heptagon_profiles.json` records all 11,304 turn-count profiles for r=4,8,16,32,64,128. Discovery uses polynomial-support bitsets; verification uses an independent bounded-Diophantine test. The finite check is a regression of the proof, **not its extension to untested r**.

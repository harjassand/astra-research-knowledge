# A mean-complete boundary record and the memory it deliberately forgets

29 October 2026, Brisbane. Independent construction/challenge of the root's
boundary principle. Ordinary finite proofs and exact rational controls;
no unknown source, physical assay, or historical priority claim.

## 1. Contract and the inherited Schur identity

Let a finite reversible continuous-time source have positive unnormalised
weights `w`, generator `Q`, and symmetric conductance Laplacian
`L=-diag(w)Q`. Thus `L 1=0`; a common positive scaling of `L,w` changes no
generator. Split its states into nonempty resolved boundary B and interior
I. Every connected interior component must meet B, so `G=L_II` is positive
definite. Empty interiors use zero-size matrices and zero residuals.

Put

```
H = -G^-1 L_IB,
S = L_BB-L_BI G^-1 L_IB,
b = w_B+H^T w_I,
c = w_I^T G^-1 w_I,
mu = sum(w).
```

The M-matrix inverse is entrywise nonnegative, `H>=0`, `H 1=1`,
`S 1=0`, `b>0`, and `sum(b)=mu`. Hence for this CLOSED module total mass
is redundant mathematically, although retaining it is a useful integrity
check. This differs from an arbitrary grounded source-response problem,
where its source mass need not be determined by its boundary Gram record.

For any nonempty A contained in B with V\A nonempty, write R=B\A. The killed mean from
the equilibrium law conditioned outside A is exactly

```
T_A = [c+b_R^T S_RR^-1 b_R] / [mu-sum_{a in A} w_a].       (1)
```

Proof: solve the killed Poisson equation `L_CC h_C=w_C`, C=V\A.
Elimination gives `h_R=S_RR^-1 b_R` and
`h_I=G^-1 w_I+H_IR h_R`. Pairing with `w_C` gives the numerator in (1).
Division is by the actual source mass outside A. All inverse matrices are
positive definite under connectedness and nonempty A. Formula (1) is NOT
a replacement of a singleton by a coarse indicator in a full-generator
Green formula: it is the actual killed equation.

This algebra is already present in Astra N798's source-aware composition
and conventional static condensation. Its new uses here are the exact
query-family equivalence below, the precise memory information that can
be forgotten for that family, and an explicit extension to unions of
regions. Neither a low-dimensional boundary nor cheap acquisition follows
from the identity.

## 2. Exact equivalence for passive exterior mean queries

Fix the same labelled boundary B and same known total module mass mu.
The exterior may attach any known finite reversible network to B, may
contain a nonempty absorbing ground, and may carry additional positive
state masses. It must not touch the eliminated I. Source preparation for
each query is the full resulting live-state weight law divided by its
total live mass; it is not an arbitrary common initial state.

**Theorem.** Two modules have the same mean for every such passive
exterior query if and only if their triples `(S,b,c)` are equal, in the
same mass/conductance calibration. Equality is sufficient by block
elimination of the exterior: its reduced conductance, effective load,
residual, and mass add to those of the module, with no source double count.

Here is a physically allowed family proving necessity. Connect every
boundary node to absorbing ground by the same fixed conductance t>0.
At boundary i, attach a pendant live node of weight z_i>0 by a known
conductance g_i>0. If z_i=0, omit that node. These are passive graph
attachments; no arbitrary SPD matrix with nonphysical off-diagonal signs
is needed. The pendant nodes contribute exactly

```
S_ext=0, b_ext=z, c_ext=sum_i z_i^2/g_i, mu_ext=sum_i z_i.
```

After subtracting their known residual, the measured mean obeys

```
F(z) := (mu+sum z) T(t,z)-sum_i z_i^2/g_i
      = c+(b+z)^T M(b+z),  M=(S+tI)^-1.                 (2)
```

Equality of T for z in any open positive orthant yields equality of
these quadratic polynomials. Their quadratic coefficients give M and
therefore S; their linear coefficients give `2Mb` and therefore b;
their constants give c. A single fixed t suffices. This proves exact
task equivalence, not a minimum bit count or a precision-free acquisition
algorithm.

There is also an explicit finite discrimination family. Values at
`0,e_i,2e_i,e_i+e_j` use `(k+1)(k+2)/2` queries for k=|B|. Recover

```
M_ii = [F(2e_i)-2F(e_i)+F(0)]/2,
M_ij = [F(e_i+e_j)-F(e_i)-F(e_j)+F(0)]/2,
d_i  = F(e_i)-F(0)-M_ii,
b = M^-1 d/2, S=M^-1-tI, c=F(0)-b^T M b.
```

These queries themselves ask for consequential means. Their acquisition,
precision, elapsed time and conditioning can be expensive. Their finite
number establishes identifiability in the stated query family, not an
efficient physical interface. A common scaling of an entire assembled
network is a harmless gauge; independently rescaling one module while
leaving calibrated external conductances fixed is not.

**Native-hazard correction.** This equivalence fixes exterior CONDUCTANCES,
not arbitrary native jump or killing rates. A killing hazard kappa_i at
port i contributes conductance `w_i kappa_i`; its compilation additionally
needs the boundary mass vector `w_B`. That vector is already needed for
the conditional denominator in (1). It must therefore remain in any
interface supporting native hazards or arbitrary boundary target subsets.

The distinction is necessary. A one-port module with port mass x, leaf
mass 2-x and edge conductance `(2-x)^2`, 0<x<2, always has
`mu=2,S=0,b=2,c=1`. Killing at the port at the same NATIVE hazard kappa
gives mean `1/2+2/(x kappa)`. At kappa=1, x=1 and x=1/2 give means 5/2
and 9/2, despite equal triples. Thus the stronger clock-calibrated record
is `(S,b,c,w_B)`, subject to the declared common scale and known exterior
interface. The root's native-excursion construction retains `w_B=s/lambda`
and is not defeated by this counterexample.

## 3. The record is a selected zero-frequency jet, not all memory

Let D=diag(w), and define the boundary dynamical Schur function

```
K(s)=L_BB+sD_B-L_BI(G+sD_I)^-1 L_IB.
```

It is analytic near s=0. Direct differentiation and `H1=1` give

```
K(0)=S,
K'(0)=D_B+H^T D_I H,
K'(0)1=b,
-(1/2)1^T K''(0)1=c.                                  (3)
```

Thus this mean query family needs the full zero-order matrix, a
first-derivative row sum and one second-derivative scalar. It does not
need the full frequency function. These are selected derivatives of the
eliminated memory, rather than a claim that the memory vanishes.

### The entire first jet can miss an arbitrarily large mean

Take weights `(1,1,1)`, boundary B={0,1}, and edges 0--1 of conductance
1 and 0--2 of conductance d>0. Then, for every d,

```
S=[[1,-1],[-1,1]], b=(2,1), mu=3,
K'(0)=diag(2,1), c=1/d.
```

All boundary-started means of hitting the other boundary state are fixed:
`E_0 tau_1=2`, `E_1 tau_0=1`. Nevertheless

```
E_{w(.|{0,2})} tau_1 = 2+1/(2d),
```

which is unbounded as d decreases. The stationary initial state has a
fixed chance to begin inside a long-lived pendant trap. The equilibrium
residual clock is indispensable even when the first boundary derivative
and all these boundary-started means are known exactly. This does not
claim identical raw boundary trajectories for different d.

### Same complete mean record, different survival law

One port of mass 1 with one leaf of mass 1 and edge conductance 1 has
`mu=2,S=0,b=2,c=1`. A second module has one port of mass 1, two leaves
of mass 1/2 each, and edge conductances 1 and 1/3. It has the same record.
Their expansions are respectively

```
K_1(s)=2s-s^2+s^3+O(s^4),
K_2(s)=2s-s^2+(5/4)s^3+O(s^4).
```

They therefore have exactly equal equilibrium-source means in EVERY
allowed passive exterior. With just conductance 1 from port to ground,
both means are 5/2, but their second hitting-time moments are 13 and 53/4.
Indeed their Poisson fields are `(2,3)` and `(2,5/2,7/2)`, and

```
E tau^2 = (2/mu) h^T D h.
```

The survival laws consequently differ. This gives a positive separation:
one can forget real dynamical distinctions exactly for a specified
consequence, while those distinctions remain necessary for another.

## 4. Unions of whole regions are a legitimate macroscopic query family

Partition the microscopic states into disjoint nonempty modules C_j.
In each module retain B_j containing EVERY endpoint of an edge to another
module. Its interior I_j=C_j\B_j has no cross-module edge. The module's
closed Laplacian includes its internal edges only and the original state
weights. Compute its `(S_j,b_j,c_j,mu_j)`.

For a nonempty proper target union A of whole modules, discard those
modules entirely. On the remaining ports assemble K_A from the surviving
S_j, all inter-module edges joining two live modules, and a grounding
diagonal for each edge from a live port to a target port. Let b_A be the
concatenation of surviving b_j. Then

```
T_A = [sum_live c_j+b_A^T K_A^-1 b_A]/sum_live mu_j.      (4)
```

Proof: restrict the actual global Laplacian to all live nodes. Its
interior block is block diagonal because all cross-module edges are on
retained ports. Elimination adds the live module Schur triples; crossing
edges into A retain their diagonal contribution and lose their absorbed
column, precisely producing K_A. The source outside A is exactly the
concatenation of live module weights. The grounded system is positive
definite if every live component can reach A.

The target may contain many microscopic configurations. Its entire
interior need not become a resolved boundary: first entry into a target
module already occurs at one of its retained ports. This resolves the
set-query identity issue for a DECLARED modular geometry. It does not
show that arbitrary scientific basins have small separators, that these
separators are known, or that a coarse milestone label is a sufficient
state. Native acquisition must respect the internal-versus-cross edge
rates at ports; reflecting a port or resetting an entrance distribution
is a changed interface unless justified and charged.

## 5. Comparators, sources and actual addition

Ordinary direct killed solves are exact and inexpensive in the controls
below. Sparse direct elimination, Krylov methods and conventional static
condensation can use precisely the same boundary record. No runtime
superiority over these methods is established. Exact milestoning already
uses resolved entrance information and short-trajectory kernels to obtain
means; its first-hit distribution obligation cannot be erased by naming
a boundary.

Primary sources consulted:

- Dörfler and Bullo, *Kron Reduction of Graphs with Applications to
  Electrical Networks*, arXiv:1102.2950, especially equations (1.2),(2.1)
  and Lemma 2.1. https://arxiv.org/pdf/1102.2950
- Aristoff, Bello-Rivas and Elber, *A Mathematical Framework for Exact
  Milestoning*, MMS 14(1), 301–322 (2016), sections 2 and 3.2, Theorem 3.3,
  and the numerical-error conditions in section 5.
  https://www.math.colostate.edu/~aristoff/milestoning.pdf
- Wang et al., *Approximating First Hitting Point Distribution in
  Milestoning for Rare Event Kinetics* (2023), abstract and its explicit
  initial-distribution obligation. https://arxiv.org/abs/2302.08098

Astra N798's current capsule was retrieved through ALL TEN continuation
pages at input version
`9301bf5171d4110151e38e5ddebeb1212f593a1c14f7751e019e9a8264a3b8ef`,
revision `d6672151ce8e86d4af3e74b3b880abcdc82ae304`. Its governing
`updates/FG/synthesis/compact/derived/SOURCE_SCHUR_COMPOSITION_THEOREM.txt`
was read in full (177 lines; SHA256
`f9e5e00beb57a1da2a931e6faec3554439147b6214e33b21530385bf4320888c`).
It already contains source-aware Schur composition and the warning that
unknown boundary/source loads and coverage are separate obligations. Its
current notices retain physical context-clock invariance, global component
weights, source coverage and precision as open acquisition boundaries.
No inherited review status is upgraded here and no prior dependency is
re-audited.

The addition is an exact task-equivalence characterization using genuinely
passive probes, its finite distinguishing family, the selected memory-jet
interpretation and counterexamples, and the explicit whole-region target
compiler. The acquisition bridge and finite confidence construction are
owned by the root and acquisition collaborator; this note does not assume
their success.

## 6. Executable scope

`check_passive_equivalence.py` uses rational arithmetic to check ordinary
Schur identities and finite passive-query recovery, compare the two
mean-equivalent memory examples, and compile every nonempty proper target
union in a four-module 16-state graph against its full killed solve.
The source generators are supplied to this control. There are no source
observations, physical preparations or hidden-law estimates. Its JSON
receipt reports exact values and check counts; numerical execution is a
supplement to the proofs above, not their generality argument.

## Appendix: a proved moment hierarchy, without making it the destination

The same algebra gives a precise statement for higher moments, which helps
separate task equivalence from full process equivalence. For a known
grounded boundary matrix R with S+R positive definite, put

```
b(s)=w_B-L_BI(G+sD_I)^-1 w_I=K(s)1/s,
c(s)=w_I^T(G+sD_I)^-1 w_I
    =[s mu-1^T K(s)1]/s^2.
```

The apparent singularities are removable at zero. The full equilibrium
survival Laplace transform is exactly

```
F_R(s)=integral_0^infinity exp(-st) P_w(tau>t) dt
      =[c(s)+b(s)^T(K(s)+R)^-1 b(s)]/mu.               (5)
```

To verify the two identities, use `G1=-L_IB1` and
`1^T L_BI=-1^T G`; no stationarity approximation is used. To verify (5),
apply block elimination to `L+E_B R E_B^T+sD`. In finite dimension the
grounded operator is positive, so the transform is analytic near zero.
For r>=1, its coefficient obeys

```
E_w tau^r = (-1)^(r-1) r! [s^(r-1)] F_R(s).
```

Writing `K(s)=sum_j K_j s^j`, a sufficient selected jet for all such
r-th-moment queries consists of full `K_0,...,K_(r-1)`, the vector
`K_r 1`, and the scalar `1^T K_(r+1)1` (and the consistent total mass).
Indeed inverse-series terms through degree r-1 need K only through
degree r-1; b terms need K_1 1 through K_r 1; c terms need contracted
K_2 through K_(r+1). All lower terms are contained in that record.
No minimality theorem is asserted for r>1, and derivatives are not
counted as acquired measurements. Known exteriors with additional masses
or interiors add their own known dynamic Schur data before the same
calculation. The r=1 case is exactly the main theorem, and the pair above
shows why its record does not automatically predict r=2.

# Coherent return stratification for one polynomial map

Status: complete proof candidate; internal mathematical check only. One focused independent internal mathematical check found no gap or counterexample. External/formal validation and priority remain unresolved. The proof below is the actual proposed mechanism, not a consequence inferred from generic rational observability. It aims at a primitive-recursive bound uniform in dimension. It does **not** provide an elementary bound uniform in dimension.

## 1. Input and target

Let K be an algebraically closed field, F:K^n -> K^n a polynomial map of maximum coordinate degree d>=1, and h in K[x_1,...,x_n] a nonconstant polynomial of degree e>=1. For a specified initial point a, define

L(a)=min{t>=0: h(F^t(a)) != 0},

with L(a)=infinity if no such t exists. This is the number of initial zero terms, not the largest index of an arbitrary zero and not a Skolem decision procedure.

For a computational consequence, coefficients and initial point are rational, in characteristic zero, with integers in binary and polynomials explicitly represented (dense or sparse, with the encoding specified). The geometric bound below does not depend on coefficient heights. Evaluating the resulting finite prefix exactly has primitive-recursive bit cost in the input encoding, although the bound is extremely large. No polynomial-time or practical algorithm is claimed.

## 2. Proposed bound

Put Delta_0=e and T_0=1. For i=0,...,n-1 define

T_{i+1}=(Delta_i+1) T_i,
Delta_{i+1}=Delta_i^(n+2) d^((n+1) T_i).

Candidate theorem: if L(a) is finite, then

L(a) <= T_n - 1.

Hence testing h(F^t(a))=0 for t=0,...,T_n-1 would certify all-time zeroness. The iteration depth in this recurrence is n. It is primitive recursive jointly in n,d,e, but its tower height grows with n.

## 3. Return devices: the induction invariant

Fix V=V(h). A return device on an algebraic subset W of V assigns to each irreducible component C of W either a SAFE label, or:

- a positive integer tau_C<=T;
- a closed subset D_C = C intersect F^(-tau_C)(W);
- for every x in D_C, F^s(x) belongs to V for 0<=s<=tau_C;
- for every x in C minus D_C, the actual orbit exits V at some time s<=T.

SAFE means every point of C stays in V forever. These are semantic statements about the original map F, including all intermediate times. The map attached to C is exactly F^tau_C. It is never an independently selectable transition.

A non-SAFE component is good if D_C=C and bad otherwise. For each good C, the irreducible image closure of F^tau_C(C) is contained in some irreducible component of W; select one as its successor. An edge always carries a positive integer time and a complete intervening-survival guarantee.

## 4. Dimension-lowering lemma

Suppose W has m irreducible components and a return device of budget T. Let

E = union of D_C over the bad components C.

Each D_C is a proper closed subset of C. Therefore dim E < dim W whenever W is nonempty (with dim empty=-1).

### 4.1 Access from W

Follow the selected component successors at good components. A path reaching SAFE is safe. A cycle made only of good components is also safe: each entire component is sent into the next by a positive power of the SAME F, and every intervening iterate remains in V. Iterating the cycle covers an unbounded sequence of original times with no gaps in the survival guarantee.

Any eventually escaping orbit must therefore reach a bad component after at most m-1 good jumps. At that point either it lies in D_C, hence in E, or it exits V within at most T additional original steps. Thus, from any eventually escaping point of W, within at most mT original steps there is an exit or a visit to E.

No arbitrary first-return choice has been introduced. A selected jump is valid on the whole component and is a power of F; an apparent identity cycle actually proves indefinite survival under the original F.

### 4.2 Construct a device on E

Let A be an irreducible component of E. Since E is a finite union of closed D_C, choose a bad C with A subset D_C. First apply its prescribed jump F^tau_C. This is valid on all of A and lands in W. The image closure is irreducible and lies in some component of W. If that component is good, follow its fixed successor jump. Continue through good components.

If the component path reaches SAFE or repeats a good component, every point of A is SAFE. Otherwise it reaches a bad component B after an initial jump and at most m-1 good jumps. Let Q=F^q be the composed map. Then 1<=q<=mT, Q(A) subset B, and every point of A stays in V throughout the q original steps.

Define D'_A = A intersect Q^(-1)(E).

For x in D'_A, the actual orbit stays in V up to q and returns to E at q. For x in A minus D'_A, Q(x) lies in B minus E. In particular Q(x) is not in D_B, because D_B is one of the sets included in E. The old device then guarantees exit from V within T more steps. Thus the exit budget is at most (m+1)T.

Attach tau'_A=q and D'_A to A. This is a valid new return device, of budget T'=(m+1)T, and its domain has exactly the required form A intersect F^(-q)(E). Good and bad classification can now be repeated.

Crucially, the construction does not require F to preserve dimension, be injective, or be dominant. Images may collapse into lower-dimensional subsets of components. Only irreducibility of image closures is used.

## 5. Start and stop

Initially W_0=V. Give every irreducible component C the time tau_C=1 and domain D_C=C intersect F^(-1)(V). Survival and exit statements are immediate. Thus T_0=1.

Apply the dimension-lowering lemma repeatedly, stopping as soon as the set is empty. Since dim V<=n-1, at most n restrictions are needed. Unused terms of the numerical recurrence remain harmless upper bounds. Write m_i for the actual number of components of W_i and T_i for any valid budget. An eventual escape from W_0 takes at most

sum_{i=0}^{n-1} m_i T_i

steps: at each level there is an exit or a visit to the next level within m_i T_i; at the last level there is no next-level point. The safe cycles never contain an eventually escaping point.

## 6. Degree budget

Use total geometric degree: sum of projective degrees of all irreducible components, including components of different dimensions. Let deg W<=Delta.

Two standard algebraic facts, with elementary geometric justifications:

1. W can be defined set-theoretically by polynomials of degree at most Delta. For each p outside W and each k-dimensional irreducible component C, take its projective closure and a projection to projective (k+1)-space whose center avoids the join of p with that closure. The projected component is a hypersurface of degree at most deg C and does not contain the projected p. Pulling back its equation separates p from C; multiply these separators over the components. Taking a basis of the finite-dimensional space I(W) intersect K[x_1,...,x_n]_{<=Delta} gives a finite defining family. This is a statement about the reduced set, not a bound for generators of its full ideal.
2. If C has degree delta and Z is defined by polynomials of degree at most E>=1, then deg(C intersect Z)<=delta E^(n+1). To see a conservative bound, repeatedly take a generic linear combination of the defining equations which does not vanish identically on any current component not contained in Z. Such components drop dimension. After at most n+1 cuts no unwanted component remains. Bézout bounds each cut by a factor E. Components already contained in Z are retained and are included in the total-degree accounting.

For each bad component C, its return domain is C intersect F^(-tau_C)(W), with tau_C<=T. Pullback of a degree-Delta defining equation has degree at most Delta d^T. Therefore

deg D_C <= deg C (Delta d^T)^(n+1).

Summing over bad C gives

deg E <= Delta^(n+2) d^((n+1)T).

Also m<=Delta. These are precisely the advertised Delta and T recurrences. Finally

sum Delta_i T_i = sum (T_{i+1}-T_i)=T_n-1.

## 7. Why this does not extend to arbitrary input words

With multiple unrelated transition maps, a cycle for one selected succession of inputs does not guarantee survival for every input word. The SAFE inference in Section 4.1 would be invalid for the all-words zeroness problem. Here all jumps are powers of one fixed map, so the intermediate-orbit guarantees concatenate along the unique actual orbit. This is the proposed structural escape from the general polynomial-automaton Ackermann barrier.

## 8. Boundary cases and obligations

- If h is identically zero, all orbits are zero. If h is a nonzero constant, L=0.
- Constant F can be handled directly; d is replaced by max(1,deg F).
- Reducible, non-equidimensional, and singular W are included through total geometric degree and irreducible components.
- Return domains are exact closed preimages. Replacing them by arbitrary hypersurface supersets would invalidate the induction.
- No generic initial-point assumption, nonzero denominator, or field-of-observables substitution is used.
- One focused independent internal check covered the device induction, degree bookkeeping, and endpoint accounting without finding a gap. This is not external validation or a formal proof-assistant verification.
- Priority is unestablished. Component graphs and dimension reduction occur in earlier discrete multiplicity and difference-Nullstellensatz work. The unrestricted specified-orbit conclusion must be compared, not inferred new from the absence of an exact phrase in a search.

## 9. Consequences and explicit scope limits

### 9.1 A simple tower majorant

Let A=max(16,n+2,d,e). The recurrence admits a rough majorant by a power tower of base A and height 2n+1. Indeed, if Delta_i,T_i<=W and W>=A, then both next values are at most 2^(W^4), which is at most A^(A^W). Iterating this two-exponential majorant n times proves the assertion. This is a finite-height tower for each fixed n, and a primitive-recursive function when n varies. It is not one fixed-height elementary function of all parameters.

### 9.2 Exact bit computation

The geometric theorem does not require computing components in order to use its uniform decision bound. Over Q, calculate T_n, then evaluate the first T_n scalar outputs exactly. With sparse integer/rational coefficient encoding in binary, one polynomial update increases a common numerator/denominator bit-height by at most a factor polynomial in d and adds a term bounded by the input description. Iterating a primitive-recursively bounded number of times gives a primitive-recursive bit-cost bound. This says nothing about practical feasibility.

Equivalence of two autonomous polynomial recurrences reduces to zeroness by taking their product state and the difference of their outputs. Coordinate outputs are the special case e=1.

### 9.3 Quantitative autonomous observability

Apply the theorem to the product map (x,y) -> (F(x),F(y)) and output h(x)-h(y). Equality of the two scalar output windows through the resulting bounded horizon implies equality at every later time, for every pair of initial points, including singular points. This yields a primitive-recursive finite observation cutoff for one autonomous map. It does not assert a polynomial observation algebra, a regular rational update at every quotient point, or a time-uniform approximation guarantee.

### 9.4 No transfer to arbitrary controls or partial rational maps

Arbitrary adaptively chosen input words are not covered. A specified polynomial closed-loop controller may be included as part of one enlarged autonomous state, but this is a different contract from arbitrary feedback policies.

A rational map merely promised to avoid poles along the selected orbit is also not covered by the present proof: its return domains need not be closed in one fixed affine state variety. No claim about the full ratrec-to-simple-ratrec conjecture or the general Skolem problem follows.

### 9.5 Certificate extraction is finite

At the root there are no SAFE labels. All later SAFE labels are derived from a finite good-component cycle or an already justified SAFE component. Every map is an explicitly composed positive power of F. Every return-domain equation is a closed preimage in the same affine space. Inclusions, decompositions and dimensions can be checked by finite algebraic algorithms; the semantic SAFE property is therefore not an extra oracle assumption. The proof above uses it as a convenient label for conclusions established by previous finite steps.

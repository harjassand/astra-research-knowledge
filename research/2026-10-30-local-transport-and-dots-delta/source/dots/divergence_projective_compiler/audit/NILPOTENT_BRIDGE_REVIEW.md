# Independent adversarial review: strong-nilpotence decoder bridge

**Scope/status.** Reviewed `STRONG_NILPOTENT_DECODER.md` and `ACQUIRED_CHART_THEOREM.md` mathematically. The strong-nilpotence inverse-circuit theorem is valid over Q as stated. The added implementation review below accepts only the specifically hashed source and receipts identified there. Independent exact symbolic controls are in `nilpotent_adversarial_controls.py` and its saved JSON. No matched numerical speed advantage or historical novelty has been established.

## 1. The actual theorem is sound

Write the normalized acquired chart as F=Id+N, with N(0)=0 and JN(0)=0. Let A be the Q-span of all coefficient matrices of JN. If all products of l matrices of A vanish, then the fixed-point iteration G_0(z)=z, G_(k+1)(z)=z-N(G_k(z)) stabilizes by G_(l-1). Thus the draft's looser bound of at most l iterations is safe.

For clarity, set Delta_k=G_k-G_(k-1). The divided-difference matrix B(u,v)=integral_0^1 JN(v+t(u-v))dt belongs to the scalar extension of A. Delta_1=-B(z,0)z, and Delta_(k+1)=-B(G_k,G_(k-1))Delta_k. Therefore Delta_l=0. This implies F(G_(l-1))=Id.

The other composition need not be guessed from a Jacobian determinant. In the polynomial ring, F(u)-F(v)=(I+B(u,v))(u-v), and B(u,v)^l=0. Hence I+B has its finite Neumann inverse. Substitute u=G(F(x)) and v=x to obtain G(F(x))=x. This proves both global identities without invoking the Jacobian conjecture or an unverified injectivity assumption.

A shared multi-output DAG for N can be cloned once per fixed-point step. With the earlier G outputs referenced rather than expanded/copied as trees, this gives O(l(size(N)+n)) new gates, plus normalization. It is a genuine circuit-size conclusion, not a sparse-polynomial support conclusion.

The equivalence between strong Jacobian nilpotence and constant linear triangularizability is classical: van den Essen and Hubbers, Theorem 1.6, with the coefficient-matrix formulation in Lemma 2.1. This must not be presented as newly discovered mathematics. [Primary paper](https://www.cs.ru.nl/E.Hubbers/pubs/strnil.pdf).

## 2. Flag acquisition and soundness

V_0=Q^n and V_(k+1)=sum_(M in basis A) M V_k is descending. A nonzero stable subspace remains stable forever; a successful chain strictly drops until zero, so l<=n.

A sampled matrix span is not automatically the full coefficient space. Either acquire the exact coefficient matrices, verify symbolic span membership, or verify a **universal flag** directly: JN(X)V_k is contained in V_(k+1) for every k. Using exact bases and annihilators, the latter consists of polynomial identity checks. It suffices even if the sampled A is not complete. A few pointwise nilpotence checks, or the universal same-point identity (JN(X))^n=0, do not suffice.

If random PIT is used, candidate acquisition and certification must use fresh independent randomness, bound residual formal degrees, and union-bound all checks and all adaptive attempts. An observed numerical zero is not exact acceptance. Random integer evaluation over Q also has arithmetic-height cost. Modular verification needs bad-prime handling; a denominator invertible mod p does not alone guarantee every nonzero rational residual remains nonzero modulo p.

The source-size bound is conditional on a compact **acquired** chart circuit. It does not itself bound the cost of finding that chart, evaluating jets, normalizing, choosing bases, or testing identities. Expanded coefficient extraction and expanded global inverse compositions can reinstate the exponential bottleneck. Those costs must be measured separately or avoided by genuine circuit certificates.

## 3. Exact adversarial controls now saved

The independent script imports no producer code and asserts the following.

### 3.1 Invertible does not imply strong, even in two variables

F=(x+y^2, y+(x+y^2)^2) has inverse

    G=(u-(v-u^2)^2, v-u^2).

Both compositions are checked exactly, and det JF=1. But tr J(F-Id)=4y(x+y^2), which is not identically zero. Thus the strong test must reject it without claiming it is noninvertible.

### 3.2 Pointwise nilpotence is an unsound replacement

For variables x,y,z,w, take

    N=(y w^3-x^2 w^2,
       z w^3+2xy w^2-2x^3 w,
       -y^2 w^2+2x^2 y w-x^4,
       0).

N is homogeneous of degree four and JN(0)=0. The script verifies (JN)^4=0 identically. Yet at a=(0,0,0,1), b=(1,0,0,1),

    JN(a) JN(b) JN(a) JN(b)
      = [[28,-8,-6,12],[16,-4,-4,8],[0,0,0,0],[0,0,0,0]],

so it is not strong. This is a homogenization of the perturbation in Campbell's Example 4; the normalization and mixed witness above are independently checked, not taken on citation. [Campbell 1999](https://arxiv.org/pdf/math/9907157).

### 3.3 A compact inverse genuinely outside the strong subclass

The smaller map

    N=(z(x+zy)^2, -(x+zy)^2, 0)

has N(0)=0, JN(0)=0, (JN)^3=0, and JN*N=0. It is not strong: at a=(1,0,0), b=(1,0,1),

    JN(a) JN(b) JN(a) = [[0,0,0],[8,0,-4],[0,0,0]].

Nevertheless F=Id+N has inverse G=Id-N. Both compositions pass exact symbolic checks. This is a polynomial specialization of Campbell's Example 3, an established quasi-translation mechanism. [Campbell 1999, Example 3](https://arxiv.org/pdf/math/9907157).

This suggests a cheap, honest extension rather than treating strong-nilpotence rejection as the end of decoder acquisition. Try G_1=Id-N and test its global identities, or certify JN*N=0. The latter is sufficient: the derivation D=N dot grad has D(N_i)=0, so D^2(x_i)=0; Leibniz makes D locally nilpotent on polynomials, and exp(tD)x=x+tN(x). Its inverse is exp(-tD), giving Id-N at t=1. It strictly enlarges the admitted family, but is itself classical and introduces no superiority over an equally informed standard symbolic method.

## 4. Exponential output cost is not cured

For the quadratic chain F_i=x_i+x_(i+1)^2, F_n=x_n, the inverse degree is 2^(n-1). At target z=(0,...,0,2), the first output is -2^(2^(n-1)) (n>=2), requiring exactly 2^(n-1)+1 magnitude bits. The script checks this at n=2,3,4,6,8,12,16. Thus a small inverse circuit cannot imply polynomial-time exact rational output in the input dimension alone.

Floating-point evaluation can represent large magnitudes compactly, but error criteria matter. Along this ray the absolute derivative has magnitude d*2^(d-1), d=2^(n-1). Uniform fixed absolute error can therefore demand exponentially many precision bits. Relative error on this particular ray is much better conditioned (relative amplification d, logarithm n-1). Neither favorable nor unfavorable conditioning is universal.

The linear evolution also incurs matrix-exponential conditioning, coordinate/basis conditioning, projective denominator separation, and the inverse circuit's value/roundoff amplification. A time-independent gate count is not a time/accuracy-independent bit complexity theorem. Near a genuine pole the original real flow may not exist across the requested time.

## 5. Equally informed conventional comparison

Ordinary fixed-point inversion with the same acquired chart is literally the proposed algorithm. Constant-basis triangular backward substitution is also available once the same flag is known. Newton or a symbolic system can exploit those certificates; the comparison cannot withhold the chart/flag from the conventional method. The proved benefit is removal of degree-enumeration/monomial-expansion overhead for a certified subclass, **not** a lower bound against ordinary symbolic inversion or projective recognition.

The consequential completed obligation is therefore: *an acquired strong flag is enough to manufacture a compact original-state decoder without assuming an inverse or enumerating its exponential degree.* The useful additional lead is the independent quasi-translation admission rule. Practical scientific advantage, robustness to nonexact inputs, and a generic compact-decoder acquisition theorem remain open.

## 6. Added implementation review and independent replay

Inspected `strong_decoder.py`, including its subsequently added quasi-translation path. The front end `raw_chart(raw,x)` accesses only raw coefficients and coordinates; `strong_decoder(chart,x)` and `quasi_decoder(chart,x)` access only the acquired chart and coordinates. The hidden constructor is separate and is not called by those routines. The source implements complete coefficient extraction, exact flag construction, and actual shared-DAG substitution. The final affine normalization is in the correct direction, including nonzero offsets.

`DAG.substitute` snapshots the old topologically ordered prefix, maps old variable gates to shared replacement roots, and creates one remapped gate per old gate. It does not recursively duplicate each occurrence of a substituted expression. During the fixed-point loop the substituted roots are the original N roots, so the snapshot has fixed original size. The final affine substitution processes the accumulated graph once. Dead nodes still consume memory and must be charged, even when the final live subgraph is smaller.

The independent script `strong_decoder_replay.py` loads only the serialized raw fields and acquired chart/matrix results, then reacquires from the raw fields. It imports the producer to manufacture the certificate/DAG, but all certificate checks and the rational/symbolic DAG interpreters are separately written. It does not call `hidden_family` and does not use the hidden chart to certify acquisition.

**Passed:**

- 22 exact projective closure component identities across strong raw n=2,3,4,5 and quasi raw n=3.
- The reacquired chart and matrix match every saved raw-input record.
- 14 independent universal flag identities Q_(k+1) JN(X) V_k=0, together with full column ranks and the zero terminal space, for the strong cases.
- The quasi raw case has exact JN*N=0 and is independently rejected by the strong route.
- 70 two-way exact rational point tests evaluated by the independent DAG interpreter. These are test coverage, not substitutes for global identity certificates.
- 16 expanded global inverse component identities for strong n=2,3 and quasi n=3. Expansion was intentionally **not run** for strong n=4,5; their admission is the exact universal flag plus the audited fixed-point construction.
- Both expanded inverse compositions for an additional nonzero-offset, nontrivially output-mixed chart.
- The degree-four homogeneous 4D same-point-nilpotent control is rejected by both strong and quasi admission.

The source and result hashes at this replay were:

    strong_decoder.py
    faed35d2f6c9cdaedfe62a11ec29835e2ed79568b6f00e3514f84452e257d6fe
    strong_decoder_results.json
    14fa0af90f4e67ee83ff6ca7baf2f8854ec7128ce6e5cfef0f890faeb961af66
    circuit_jets.py
    3a313bf630fdc1e8840c6d6d54015aad29ba6bafbc23d442a39ff72af155ac12

The full machine-readable receipt, including the replay-script hash, is `strong_decoder_replay.json`.

An additional direct allocation inspection found these `(n,total allocated nodes,final reachable nodes,peak stage reachable nodes)` tuples for the decoder-only chain tests:

    (4,25,14,17), (8,95,30,57), (12,213,46,121), (16,379,62,209).

These support polynomial graph construction but prevent interpreting the final 62 live nodes as the complete n=16 build memory. The n=4,8,12,16 chain scaling records are **decoder-only**, not raw-field acquisition records. The raw front end still expands input polynomials and uses coefficient arithmetic, so no general raw-circuit polynomial-time implementation follows from these runs.

**Verdict:** accept the narrowly scoped acquisition/certificate/compact-decoder implementation at the hashes above and the theorem-backed strong/quasi admission mechanisms. Do not promote this to an unrestricted polynomial-inversion algorithm, an end-to-end bit-complexity theorem, a practical speed result, or a novel result about strong nilpotence/quasi-translations.

The implementation replay was rerun successfully after the metrics-only addition of `inverse_total_allocated_nodes`; the displayed hashes above are refreshed to that run.

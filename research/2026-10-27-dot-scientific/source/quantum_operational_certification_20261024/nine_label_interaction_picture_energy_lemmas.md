# Interaction-picture energy lemmas for noise-adapted sampled filters

2026-10-27. Exact partial progress, NOT a full nine-label p^-2 receiver theorem. Root and continuation worker independently derived the single-Hamiltonian lemma; branch-energy extension below is algebraic. Independent receipt requested.

## Setup

Use the received pure-isometry plus arbitrary-reset source. Let Q=I_A tensor VV*, let Phi_j be any of the nine known input-Weyl rotations of Phi_V, and write

 D=I_A tensor[p VV*/3+2q tau/3],
 H_j=p Phi_j-D=4T_j-6omega.

All these operators act on A tensor B. The density programs satisfy the useful operator dominations

 omega<=D/2, T_j<=D.

Indeed omega=pQ/9+q I_A tensor tau/3=D/2-pQ/18, and
 T_j=pPhi_j/4+pQ/12+q I_A tensor tau/3
 <=pQ/3+q I_A tensor tau/3<=D.

## 1. Exact operator-valued energy bound inside one ideal classifier

Let X be any data effect,0<=X<=I, and let U be ANY ideal coherent circuit made from controlled functions of ONE H_j and ancilla-only gates. This includes finite QPE, reversible majority classification, copying its decision bit, and compute/uncompute. Fresh ancillary dimensions may be arbitrarily large.

In an H_j eigenbasis the circuit has form

 U=sum_lambda Pi_lambda tensor U_lambda,

with the same ancillary unitary on every vector in a degenerate eigenspace. Set

 Z=U*(I_anc tensor X)U.

Then0<=Z<=I. For any unit ancillary vector v, R_v=<v|Z|v> is a data effect whose diagonal in the H_j eigenbasis equals that of X. Therefore

 Tr(H_j R_v)=Tr(H_j X),
 Tr(D R_v)=p Tr(Phi_j R_v)-Tr(H_j X)
           <=p-Tr(H_j X)<=p+Tr(DX).

Equivalently, as an OPERATOR inequality on the entire ancillary space,

 Tr_data[(I_anc tensor D) Z]
 <=[p-Tr(H_j X)] I_anc
 <=[p+Tr(DX)] I_anc.

The weighted partial trace is positive because D acts on data only; it equals the partial trace with D^(1/2) on both sides. By the program dominations the same upper bound applies to T_j, and half that bound to omega. This is independent of phase-register dimension. It does not merely bound an unconditioned scalar trace.

If a positive backward observable selects a classical branch, it is bounded above by the corresponding unconditional effect before selection. Hence this energy bound can be applied to an unconditional positive majorant, but that replacement must be tracked in any later error accounting.

## 2. Turning weighted partial traces into square bounds

Let sigma be any density program and0<=Z<=I a joint ancilla-data effect satisfying

 Tr_data[(I tensor sigma) Z]<=w I_anc.

Then

 (I tensor sigma) Z (I tensor sigma)<=w I.

Proof: in a sigma eigenbasis with eigenvalues s_k, set R_k=sqrt(s_k)<k|Z^(1/2). Then R_k R_k*=s_k Z_kk<=sum_l s_l Z_ll<=wI, so each ||R_k||²<=w. For any joint vector v,

 ||(I tensor sigma)Z^(1/2)v||²
 =sum_k s_k ||R_k v||²<=w||v||².

Taking adjoints gives the displayed positive-square bound. In particular, for a projector Pi this gives ||sigma Pi||²<=w. The usual commutator positive-square bounds therefore need no ancillary-dimension multiplier. This lemma alone does not yet establish the full local DME-versus-ideal transported-observable inequality.

## 3. Ideal branch-to-branch energy transport

An ideal accepted OR rejected finite classifier branch has data Kraus operators K_l=f_l(H_j), with effect

 E=sum_l K_l* K_l<=I.

Its data CP map Psi is trace-nonincreasing AND subunital, since every K_l is normal and all commute. Moreover Psi(H_j)=H_j E. Consequently

 Psi(D)-D
 =p[Psi(Phi_j)-Phi_j]+H_j(I-E)
 <=2p I.

Here Psi(Phi_j)<=Psi(I)<=I; since E commutes with H_j, H_j(I-E)<=(H_j)_+<=pI. Thus for every positive backward effect X,

 Tr[D Psi*(X)]<=Tr(DX)+2p TrX,
 Tr Psi*(X)<=TrX.

After k ideal branch maps, an initial effect of trace at most r and D-energy E0 retains trace at most r and has D-energy at most E0+2kpr. This is valid across different labels H_j, because their D is common. Branch selection need not preserve trace exactly.

## What remains open

The received single-label p^-2 proof used exact cancellation of first-order population drift for its own spectral projector. A multi-label proof must instead compare each actual collision to IDEAL transport, use the energy bounds above for its backward observable, and charge all positive majorant terms against the actual selected earlier history. Simply telescoping uniform diamond errors on reset still loses p and yields p^-3 relative-error training.

In particular, the common span of the nine chi_j is generally NOT invariant under H_j. The finite-matrix diagnostic `nine_label_span_cancellation_obstruction.py/.txt` gives nonzero span commutators even for tiny coherent-reset overlap. This refutes a naive reuse of the old commuting-sector argument, not the interaction-picture route.

No full-throughput p learner, reusable program bank, or finite-batch amortization theorem is established here. The received combined guarantee remains p/9 throughput, Delta of order p², and p0^-2 consumed-program training per data attempt.

## 4. Controlled collision: isolate the attenuation rather than dropping cancellations

Let C=|1><1| be the control projector and sigma the density program. The exact controlled partial-SWAP channel has principal Kraus operator

 K=I+(cos h-1) C tensor I-i sin h C tensor sigma,

and the remaining CP map is

 sin²h |1><1| tensor[ sigma Tr(X_11)-sigma X_11 sigma ].

The bracket is CP: its Choi matrix is sigma tensor I-|vec(sigma)><vec(sigma)|, positive by the rank-one Schur test and Tr sigma=1, with support restriction if sigma is singular. This decomposition follows by expanding the00,01,10,11 control blocks; it retains the cancellation between control dephasing and data loss.

For a positive joint target effect Z with weighted partial trace <=wI, the residual CP map contributes at most w sin²h to target population. The principal K differs from the ideal controlled exp(-ih sigma) by O(h²). In particular, the leading discrepancy includes the control attenuation -(h²/2) C tensor(I-sigma²), which is not bounded by the small target weight alone.

For a Z-projector-orthogonal input and zero target weight, this attenuation creates only O(h^4) population, not automatically O(h²); separate off-diagonal control dephasing terms can overestimate the effect because diagonal loss cancels them. However cross terms for general inputs prevent simply inferring the stationary bound (1+Ch²)Z+Ch²wI. A source-weighted or structured majorant estimate is still needed. This is an exact decomposition, not closure of the multi-label receiver.

## 5. Decisive failure of an unqualified transported-projector inequality

A small operator-valued program weight alone does NOT imply

 K_pair^*(Pi)<=(1+Cdelta²) U_ideal^* Pi U_ideal+Cdelta² w I

with a universal constant C for arbitrary transported Pi. Explicit example, with data dimension3 and0<p<1/5:

 sigma=diag(2p,3p,1-5p), rho=diag(p,p,1-2p),
 H=4sigma-6rho=diag(2p,6p,-2-8p).

Let Q=|0><0|+|1><1| and Xcode=|0><1|+|1><0|. On one control and the data set

 Pi=[I_control tensor Q+X_control tensor Xcode]/2.

This is a rank-two projection. It really is a transported I_control tensor|+><+|: controlled exp[iH pi/(4p)] supplies a controlled code Z up to a known control phase, and an ancillary Hadamard gives the displayed Pi. Weighted partial traces are(5p/2)I for sigma and pI for rho, so w=5p/2 tends to zero.

Take v=|+>_control tensor|->_code, so Pi v=0, and choose the input to be U_ideal* v. Its ideal target population is exactly zero. For a signed pair with angles4delta,-6delta, its actual target population tends as p decreases to zero to

 [1-cos(4delta)cos(6delta)]²/4>0

for generic fixed nonzero delta. Therefore its ratio to delta²w diverges. The floor is order delta^4, arising from principal-Kraus control attenuation; it is not an order-delta² false-population jump. Exact finite matrices are corroborated in `transported_projection_attenuation_counterexample.py/.txt`.

This counterexample excludes the unrestricted operator inequality above. It does not exclude a source-weighted inequality, a bound with additional attenuation terms, or a theorem requiring step size to shrink with p. In particular it is not a counterexample to the received stationary single-target receiver or to a not-yet-proved full-throughput construction.

### Small linked steps do not alone rescue the uniform inequality

The same example can use delta=p tending to zero. In the code |+> direction, take the ideal final control state sqrt(p)|+>+sqrt(1-p)|-> and precompose the input with the inverse ideal controlled evolution. Its ideal target population is r=p. In the p-to-zero limit the principal pair attenuates the control1 amplitude by

 c=cos(4delta)cos(6delta)=1-26delta²+O(delta^4).

This creates a positive interference contribution of leading size26delta² sqrt(p), whereas the proposed right-hand excess is Cdelta²(r+w)=3.5Cdelta²p. The program replacement corrections are only O(pdelta²), and the remaining terms are smaller along delta=p. Thus the ratio diverges as p^(-1/2). Direct finite-matrix ratios for p=delta=10^-2,10^-3,10^-4,10^-5 are respectively75.4,237.6,746.0,2352.4.

Therefore merely tying the collision step to p does not establish the unrestricted relative-population operator inequality. One must exploit the actual source/CQ structure or change the estimate. The coherent test input here is not claimed to arise as the dominant reset history of the proposed receiver.

## 6. A concrete principal-pair CQ estimate (partial cone step)

This subsection addresses only the principal Kraus term; residual CP jumps and complete branch iteration must still be accounted for separately. It does not establish the receiver.

For source programs sigma=T_j and rho=omega, put a=4delta,b=-6delta,c=cos(a)cos(b), and let

 L=(cos(b)I-i sin(b)rho)(cos(a)I-i sin(a)sigma),
 E=L-c exp(-i delta H_j).

For |delta|<=1/10, the following conservative data-operator inequality holds:

 E E*<=4096 delta^4 D.

To verify it, expand E into four pieces: the sigma coefficient -i cos(b)[sin(a)-a cos(a)], the rho coefficient -i cos(a)[sin(b)-b cos(b)], the product -sin(a)sin(b)rho sigma, and the exponential remainder -c[exp(-i delta H_j)-I+i delta H_j]. Their squared coefficients are bounded respectively by(64/3)^2 delta^6,72^2 delta^6,576delta^4, and the final remainder square. Since sigma,rho<=D and are densities, sigma²,rho²,rho sigma² rho<=D. Also ||H_j||<=2/3 and H_j²<=8D, so the exponential remainder square is at most(8/9)delta^4D. Bounding the square of four terms by four times their individual squares gives less than4096delta^4D.

Now let a positive joint state be CQ in the H_j eigenbasis,

 R_CQ=sum_lambda R_lambda tensor|lambda><lambda|,
 R_anc=sum_lambda R_lambda.

Then R_CQ<=R_anc tensor I and Tr R_anc=Tr R_CQ. The pair's principal controlled Kraus is

 K=A U_ideal+C tensor E,
 A=|0><0|+c|1><1|,
 U_ideal=controlled exp(-i delta H_j), C=|1><1|.

A U_ideal maps CQ states to CQ states and is contractive on each ancillary block. Write R0=A U_ideal R_CQ U_ideal* A*. The positive-square cross-term inequality with parameter delta² yields

 +/-[K R_CQ K*-R0]
 <=delta² R0+8192delta²(C R_anc C) tensor D.

The bound is dimension-free because Tr R_anc equals the original CQ mass, rather than the ancillary dimension. Finally D=H_-+pPhi_j-H_+<=H_-+pPhi_j. Hence the right-hand error consists of a CQ contribution plus a positive trace-O(pdelta²) remainder, with explicit ancillary trace accounting.

This explains why the source-CQ route can evade the transported-projector counterexample: the dangerous arbitrary coherent input is excluded from its dominant part, and the arbitrary remainder has only trace O(p). It remains necessary to prove an analogous complete selected-branch estimate, handle residual CP jumps, and propagate the weighted errors through the actual repeated/multiple-label circuit. Those steps are not asserted here.

### Residual CP jumps can also be charged to D with bounded ancillary trace

For a single controlled collision with density sigma, its residual jump map is bounded above by

 sin²a (C Tr_data(R) C) tensor sigma.

For the two-collision pair applied to R_CQ, separate the residual output as the full second collision applied to the first jump, plus the second jump applied to the first principal output. The first jump is at most sin²a(CR_anc C) tensor sigma.

For any positive ancillary S and density sigma<=D, the second collision with rho maps S tensor sigma to at most

 [2 B S B+3sin²b C S C] tensor D,
 B=|0><0|+cos(b)|1><1|.

This follows by splitting its principal Kraus B tensor I-i sin(b)C tensor rho into two terms and using twice the two positive squares; rho sigma rho<=rho²<=D, and its residual replacement term is at most sin²b C S C tensor D. The bracket's trace is at most5TrS. The second jump on the first principal output has ancillary trace at most sin²b TrR_CQ, because principal Kraus evolution is trace-nonincreasing.

As sin²a<=16delta² and sin²b<=36delta², the TOTAL residual output is bounded by

 delta² S_jump tensor D, with Tr S_jump<=116 Tr R_CQ.

Combining this with the principal estimate proves a complete signed-pair cone inequality:

 +/-[C_pair(R_CQ)-R0]
 <=delta²R0+delta² S_error tensor D,
 Tr S_error<=8308 Tr R_CQ.

The lower inequality remains valid because the residual output is positive; the same larger upper bound works on both signs. This is a complete local channel statement, with arbitrary ancillary correlations in the CQ blocks, not merely a reduced-data calculation.

Ancilla-only outcome selection preserves CQ structure and decreases the positive remainder's trace. However R0 uses control attenuation, not the ideal classification circuit, and comparing its SELECTED outcomes to ideal selected outcomes still requires bookkeeping. In particular A R_lambda A* need not be below R_lambda in Loewner order, despite decreasing its trace. Do not drop that distinction when propagating a selected-branch error.

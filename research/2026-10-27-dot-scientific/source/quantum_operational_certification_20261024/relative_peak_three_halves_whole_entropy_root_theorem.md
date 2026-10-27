# Whole entropy order below relative peak 3/2

27 October 2026. Root proof using the independently reconstructed finite-support pencil mechanism. Independent receipt requested. This is a whole-source theorem, not an integration of top scores along an unreceived clipping path.

## Theorem

Let N=W3 tensor id_R, W3(B)=(Tr(B)I-B^T)/2, and E(X)=I3/3 tensor Tr_A X. The reference is any finite-dimensional space. Let X>=0 and tau=E(X). Suppose

 X <= (3/2) tau.

Define the homogeneous deficit

 Delta(X)=D(X||tau)-2D(NX||tau).

All three positive operators have the same trace, so the linear terms in the homogeneous relative entropy cancel. On the actual product support of tau, let P0 be the kernel projection of X. Then

 Delta(X) >= (1/2) Tr(P0 tau) >=0.                 (1)

Equality Delta(X)=0 holds exactly when X=E(X), including the zero source. In particular every singular X on its faithful actual marginal support has strictly positive deficit. No lower spectral bound, ordinary condition-number bound, finite reference-size bound, entropy whitening, or clipping-preservation assumption is used.

This does not resolve the unrestricted conjecture: sources with relative peak exceeding3/2 remain outside the theorem.

## 1. An eigenvector pencil lemma without topness or effect bounds

Let U>=0, B>0, U psi=psi, ||psi||=1, and U<=(3/2)B. Neither U nor B need be effects, and psi need not be a maximal eigenvector. Put mu=<psi,Bpsi> and C=(U+3B)/4. Then

 <psi,(logB-2logC)psi> >= (1/2)(1-mu).            (2)

The right side is allowed to be negative. The key is not to impose mu<=1 before summing over the original source spectrum.

First take U faithful. Define

 q(t)=<psi,Pi_+(tB-U)psi>, q0(t)=1_(t>1),
 h(s)=<psi,log(U+sB)psi>.

The received renormalized positive-part derivation gives

 h(s)=integral_0^infinity s q(t)/[t(t+s)] dt,
 integral_0^infinity q(t)/t^2 dt=mu.

Its only eigenvector premise is Upsi=psi: <logU>=0, and the diagonal Frechet-log derivative at eigenvalue1 equals <B>. There is no use of U<=I, B<=I, or maximality. Positivity receives the same-pencil identities for arbitrary finite positive operators.

Faithfulness makes q vanish near zero. The actual order U<=1.5B makes q(t)=1 for t>1.5. Thus q-q0 is compactly supported away from zero. Subtracting the reference identity h0(s)=log(1+s), then taking s to infinity, gives <logB>=integral(q-q0)/t. At s3 the same identity yields

 j:=<logB-2logC>
   =integral [(t-3)/(t(t+3))](q-q0) dt.           (3)

Let r(t)=t(3-t)/(t+3). Exactly,

 r(t)-1/2=-(t-1)(2t-3)/[2(t+3)].

Consequently r<=1/2 below1 and r>=1/2 between1 and1.5. Above1.5 the integrand difference vanishes. Since q>=0 and1-q>=0,

 j >=(1/2)[integral_1^1.5 (1-q)/t^2
                    -integral_0^1 q/t^2]
   =(1/2)(1-mu).

This proves(2), including mu>1. The signs are not obtained by assuming q is monotone.

For singular U, use U_e=(U+eI)/(1+e), B_e=(B+eI)/(1+e). These preserve U_e psi=psi and U_e<=1.5B_e. B and C are already faithful because B>0, so their logarithmic limits are ordinary finite-dimensional limits. This proves the lemma on every positive eigendirection of a singular U.

## 2. Apply the lemma to EVERY original positive eigenvalue

Restrict to C3 tensor supp(Tr_A X); tau is faithful there. Let X psi_i=lambda_i psi_i with lambda_i>0. Apply the lemma to

 U_i=X/lambda_i, B_i=tau/lambda_i.

These may have eigenvalues greater than one. That causes no problem by Section1. Since N^2X=(X+3tau)/4, (2) reads

 log(lambda_i)+<psi_i,[logtau-2log(N^2X)]psi_i>
 >=(1/2)[1-<psi_i,tau psi_i>/lambda_i].          (4)

The original channel is unital, completely positive and Hilbert-Schmidt self-adjoint. Operator-log Jensen gives

 N(log NX)<=log(N^2X).

Therefore the ACTUAL entropy-gradient compression

 g_i=log(lambda_i)+<psi_i,logtau psi_i>
                  -2<psi_i,N(log NX)psi_i>

is at least the left side of(4). For singular NX, apply Jensen to NX+eI and pass to supported limits: NP_i<=NX/lambda_i ensures the individual weighted logarithms are finite on the required support.

Multiply(4) by lambda_i and sum ONLY over the positive spectrum. The exact source identities give

 sum_i lambda_i g_i=Delta(X),
 sum_i lambda_i=TrX=Trtau,
 sum_i <psi_i,tau psi_i>=Tr(P_suppX tau).

Thus Delta(X)>=(1/2)[Trtau-Tr(P_suppX tau)]=(1/2)Tr(P0 tau), proving(1). The kernel term must not be discarded by summing nonexistent zero-eigenvalue normalizations.

This is a direct spectral trace identity at one fixed source and its ORIGINAL marginal. It does not clip the source, change its marginal, or apply a free reference congruence.

## 3. Equality

If X is singular on the faithful actual marginal support, Tr(P0 tau)>0, so equality is impossible. Suppose X is faithful and Delta(X)=0. Every eigenvalue-weighted Jensen defect and calibrated pencil remainder is nonnegative, and their sum is zero. Hence each pencil has zero remainder.

The scalar calibration weights are strictly positive on(0,1) and(1,1.5). Zero remainder implies q=0 almost everywhere below1 and q=1 almost everywhere between1 and1.5. Take sequences approaching1 from both sides. Continuity of the positive and negative parts of tB-U shows that psi is annihilated by both (B-U)_+ and (B-U)_-. Therefore (B-U)psi=0. Since Upsi=psi, Bpsi=psi.

Applying this to every source eigenvector gives tau psi_i=lambda_i psi_i, hence X=tau. Conversely, if X=EX then NX=X and both relative entropies vanish. The zero source is immediate.

## Scope and preserved failures

The earlier effect/top-vector statement remains valid, but its effect bounds were unnecessary for the calibrated inequality itself. The exact spectral-clipping counterexample remains valid and is bypassed, not repaired. Relative-peak-to-local-variance counterexamples also remain valid: this proof uses the finite support of the original positive-part pencil instead of any local variance cap. The unrestricted entropy order, arbitrary channel-pair comparison, and operational recovery claims require their separate theorems.

The companion shared-pencil quantitative refinement can strengthen(1) for a smaller peak k<3/2; it is separate from this canonical proof.

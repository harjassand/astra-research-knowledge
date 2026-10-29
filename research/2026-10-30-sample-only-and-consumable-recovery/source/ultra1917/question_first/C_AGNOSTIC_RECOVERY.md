# Learning an approximately recoverable channel in one shared compressed frame

30 October 2026. C proof, paired with B's spectral-filter
acquisition. This is an ideal quantum algorithm, not hardware access.
The N1291 accepted compression/recovery inputs remain frozen. This file
extends their actual competitor argument; it does not reopen acceptance.

## 1. Metrics, inputs and the actual output task

Write d_half(A,B)=||A-B||_diamond/2. Entanglement fidelity Fe is the
Bell-target probability for the NORMALIZED k-dimensional Choi state.
The source is one unknown, fixed, memoryless CPTP channel N:k -> D.
Forward calls permit entangled logical inputs. Outputs, references and a
later payload can be held coherently and processed jointly. No unknown
Stinespring circuit, channel adjoint, environment, original-frame decoder
or source model is provided.

For one fixed projector P on the output define the trace-preserving flagged
filter J_P(X)=PXP + Tr[(I-P)X]|fail><fail|. The failure flag is orthogonal
to the success space. Let F=J_P N, and let d bound its common output-support
dimension. Filter implementation errors are charged separately against
this ONE ideal F; physical noise in N is never replaced by a perfect
source on every program carrier.

The target is a physical one-batch decoded logical channel, uniformly on
all payload states and adjoining references. The learned small decoder
belongs to this batch; no reusable original-D or streaming decoder follows.

## 2. Agnostic approximate-competitor theorem

Suppose some mathematical CPTP R0 has Fe(R0 F)>=1-zeta. It need not be
known, implemented, unique or a perfect recovery. Let the N1291 finite
tomography/affine-repair/ridge procedure estimate the actual small F with
d_half(Fhat,F)<=delta on its good event. Here 0<=delta<=1. The corrected
all-accepted inverse floor, physical depolarizing fallback and finite
rational feasibility decision from the completed review are mandatory.

For the learned Petz recovery Rhat at I_k/k, Barnum--Knill Theorem3/Eq13
applied to the singleton ensemble gives

 Fe(Rhat Fhat) >= max(0,1-zeta-delta)^2.

Indeed the same R0 has fidelity at least 1-zeta-delta on Fhat. Transferring
Rhat back to F changes the Bell-test probability by at most delta. Hence

 Fe(Rhat F) >= max(0,1-zeta-delta)^2-delta
             >= 1-2zeta-3delta.                         (1)

The final inequality also holds when zeta+delta>1, because its right side
is then nonpositive. The normalized-Choi trace-distance inequality and
the k-dimensional Choi-to-diamond bound give, on every good latent/data
pair,

 d_half(Rhat F,id_k) <= min(1,k sqrt(2zeta+3delta)).      (2)

The reference-safe joint compression has the exact all-joint-input
identity, not merely a product-state statement. For any unknown isometry
W identifying the actual rank-d output support, it turns all training
Choi programs and the payload into an integral over ONE common U in U(d).
Conditional on U the training programs are IID Choi states of U F_small U*,
independent of the payload/reference; conjugating R0 supplies a competitor
with the SAME fidelity. Thus a uniform tomography failure probability beta
and total implemented-processor half-diamond error gamma imply

 d_half(decoded,id_k) <= k sqrt(2zeta+3delta)+beta+gamma. (3)

This is precisely the N1291 proof with its perfect competitor replaced
by an approximate one. No original adjoint or recovery SDP is used.
The arbitrary-channel compression identity is the reason this replacement
is valid. Approximate filtering/compression/control errors contribute to
gamma by a hybrid bound; they are distinct from the physical source noise.

## 3. A Bell-target filter bound without a fourth-root loss

The following stronger generalization was independently proposed and
derived by root after C's exact-reversible-model argument below.
Suppose Fe(R0 N)>=1-kappa for SOME CPTP R0. Put

 t=Tr[(I-P)N(I_k/k)].

Extend R0 to the failure flag by any fixed state. Purify the actual encoded
Choi state and apply a Stinespring isometry of R0. Write the resulting
unit vector as psi, and let B=|Phi_k><Phi_k| tensor I_environment. Thus
||B psi||^2>=1-kappa. Conjugating the success projector through the
isometry gives a projector M on its range, with ||(I-M)psi||^2=t.
Its extension off the range does not matter. The success contribution
to the recovered Bell probability is ||B M psi||^2. Set A=I-M, Q=I-B.
Then

 ||B M psi||^2
 =||Bpsi||^2-2 Re<Bpsi,Apsi>+||BApsi||^2
 >=1-kappa-2t+2 Re<Qpsi,Apsi>
 >=1-kappa-2t-2sqrt(kappa*t)
 >=1-2kappa-3t.                                         (4)

The failure branch is positive and can only add Bell probability.
Consequently (3) applies with zeta<=2kappa+3t, yielding

 d_half(decoded,id_k)<=k sqrt(4kappa+6t+3delta)+beta+gamma. (5)

This separates approximate correctability from effective output rank.
No exact reversible model is needed for (4)--(5). Its input promises may
be mathematically warranted or separately qualified; they are not supplied
by the word "noise" or by a small observed sample alone.

For the more restrictive but convenient promise d_half(N,N0)<=eta with
N0 exactly reversible, C obtained the sharper coefficient

 zeta<=2t+3eta.                                         (6)

Proof: in a purification of N0's decoded Choi state, the entire vector lies
in the Bell-target subspace. If t0 is its filter rejection probability,
the projected success vector retains overlap 1-t0 with the original unit
vector. Its Bell probability is therefore at least (1-t0)^2. Applying the
same filter and R0 to N costs at most eta in Bell probability, and t0<=t+eta.
Hence Fe(R0 F)>=1-2t0-eta>=1-2t-3eta. This proof requires neither access
to N0 nor a supplied purification.

## 4. Effective rank, not exact supports of the physical source

Let A=N(I_k/k). Assume the sum of its eigenvalues after the largest d0
is at most tau. For a spectral threshold a<=b<=2a, P=1_[b,infinity)(A)
has rank at most 1/a, and

 t<=tau+2d0*a.                                          (7)

This follows by separating at most d0 eigenvalues below the threshold
from the remaining spectral tail. No eigenvector is given to the learner.
The flag raises the common support bound by one.

Together (5) and (7) yield the agnostic promise bound

 d_half(decoded,id_k)
 <=k sqrt(4kappa+6tau+12d0*a+3delta)+beta+gamma.           (8)

If A0=N0(I/k) has rank at most d0 and d_half(N,N0)<=eta, the Ky Fan
tail bound tau<=eta and (6) instead yield

 d_half(decoded,id_k)
 <=k sqrt(10eta+8d0*a+3delta)+beta+gamma.                 (9)

These bounds are uniform in D and in the smallest nonzero eigenvalue of
A0. They do not remove dependence on effective rank, k, error tolerance,
source coherence, ambient storage or trusted controls.

## 5. Finite acquisition costs inherited at their actual scope

Put h=kd, choose rational delta>0 and e=delta/(10 k h^2), a_ridge=4he.
Use h^2 Choi settings and m copies per setting, with integer L satisfying
2^L>=2h^2/beta and m=ceil[L/(2e^2)]. Training calls are N=h^2 m.
The affine/ridge estimator and acceptance test are exact rational
operations. Every accepted estimate has

 S=Fhat(I/k) >= k a_ridge I/[2(1+2h a_ridge)],
 ||S^(-1/2)||^2 <=5h/delta+4d.

Physical recovery is synthesized from learned finite Kraus matrices.
There is no inverse-spectrum promise about the unknown A or junk state.
The output rank d grows with 1/a: the fixed-d GT enumeration in the
governing predecessor alone does NOT pay uniform polynomial control cost.
C_UNIFORM_TWIRL.md supplies the separate growing-d port. B owns the
random-threshold spectral gap and source-copy implementation of filtering.

The original-D outputs of all N programs plus the payload must be kept
coherent until their ONE joint compression. The payload remains protected
during tomography and finite decoder synthesis. A batch of later payloads
requires its own justified extension; no independent repeated-release or
streaming consequence is asserted.

## 6. Strong ordinary alternatives and scientific boundary

Barnum--Knill approximate reversal is the controlling ordinary theorem,
not a new C result. Gilyen--Lloyd--Marvian--Quek--Wilde's Petz circuit
algorithm (arXiv2006.16924v2, Assumptions and Theorem1) additionally has
an implementation of the unknown channel's Stinespring unitary and its
inverse, plus block encodings/conditioning. That is a stronger access
model than the opaque forward CPTP source here. Once the small channel
is learned, either their known-matrix circuit or generic finite dilation
synthesis is an admissible ordinary decoder implementation.

Equally informed optimal-recovery SDP after small-space tomography is
also admissible. It may improve the dimension/fidelity conversion or
attain a better all-input risk. This proof does not claim Petz is the
strongest optimizer, a new approximate-QEC principle, a practical quantum
advantage or a reusable decoder. The intended changed operation is
learning the ACTUAL approximately recoverable, effectively low-rank
channel in a common latent frame, rather than comparing every noisy
program with an ideal one and incurring an N*eta error.

This is the fully derived BATCH fallback, not an exclusivity claim.
Subsequent direct primary screening found Utsumi etal.2509.03619v3's
forward-only Petz construction, with explicit ambient/conditioning costs,
and the stronger random-dilation programme2512.21260v2. The completed
C_STRONG_ORDINARY_ROUTE.md composes the latter with general Petz
machinery and B's filter into a finite consumable program acquired BEFORE
the payload. The original batch-only timing restriction is therefore not
promoted into a fundamental barrier under the full paid access model.

## Source paths actually read

At pinned Astra85048ae0abfe1c1ac932afb7d233993c3553df2a:
source_entry/C_N1291_GOVERNING.md and C_N1291_REVIEW.md (complete).
The latter includes the load-bearing accepted-estimate floor and fidelity
range corrections. Primary Barnum--Knill quant-ph/0004088v2, SectionIV,
Eq12/Theorem3/Eq13; Gilyen et al.2006.16924v2, definitions, Assumptions,
Theorem1 and inverse-Stinespring implementation were directly read.

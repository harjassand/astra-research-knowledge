# Independent review: isotropic rotation programs to a valid noisy Choi resource

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`. **Decision: accepted at the exact conditional scope below.** Scope: the root's fixed four-output transducer, two independent isotropic input programs, one retained output marginal, and the channel-factorization consequence for standard product-resource port-based teleportation. No purification cost or PBT compiler/fidelity theorem is imported by this review.

## Equivariance proof

Write f(q)=vec(R(q))^tensor2 and g(q)=q^tensor4. Rank35 of the coefficient matrix M gives S=span{f(q):q real} dimension35. Unit quaternion left/right multiplication is an orthogonal four-dimensional action Q; it induces an orthogonal nine-dimensional action D on vecR, because R(a q b)=R(a)R(q)R(b). On the spanning vectors, T D^tensor2 f(q)=T f(Qq)=g(Qq)=Q^tensor4 T f(q). Thus T intertwines on S.

The exact certificate B=(MMᵀ)^-1M has kernel equal to ker M=S-perp; J merely repeats monomials, so T=JB vanishes on S-perp. Orthogonality of the input representation and invariance of S imply invariance of S-perp. Hence T D^tensor2=Q^tensor4 T on the ENTIRE input space, including noisy components outside the clean-program span. This step is essential: checking only pure ideal programs would not justify a noisy covariance claim.

At identity frame, conjugating quaternions fixes their scalar component and rotates the three imaginary components. The commutant on this complexified representation has a scalar1D block and a scalar3D block. Therefore the retained one-program output is isotropic around the identity quaternion. Left multiplication alone moves that quaternion to any desired real unit q, and the full intertwiner transports the identity-frame result to every R. A quaternion sign changes no program density matrix. No unknown frame is supplied to the controller.

The independent exact code also checks all six infinitesimal left/right quaternion generators against their input/output tensor representations. These generate the connected unit-quaternion left/right action, providing an algebraic check independent of orientation fitting.

## Exact transfer and parameter conventions

For tau_v=(1-v)P_c+v(I-P_c)/8, its pair is a quadratic polynomial in v. Independent full81-dimensional pair matrices at three rational v values determine the exact quadratic retained marginal; this reproduces

O(v)=diag((216v²-453v+256)/432, v(62-9v)/864, v(62-9v)/864, v(62-9v)/864).

Consequently

p(v)=(405v²-720v+512)/864,
w(v)=3v(62-9v)/(405v²-720v+512),

and the conditional output is (1-w)P_q+w(I-P_q)/3. The small-v coefficient is93/256. At v=0 one recovers success16/27 and pure output; at v=8/9 one obtains success2/9 and I4/4. The formula assumes TWO independent identical tau_v inputs. A correlated pair with the same marginals need not obey it.

The root now explicitly limits its convex depolarizing interpretation to0<=v<=8/9, implying0<=w<=3/4. The exact matrix formula is also valid on0<=v<=1, but outside that restricted range one must not describe the identity/depolarizing expression as a convex mixture.

The known Bell-basis unitary sends P_q to the normalized Choi projector of V and preserves I4. The retained state is therefore exactly Choi(E), with

E=(1-4w/3) U_V+(4w/3) D_2.

Its input marginal is exactly I2/2, checked independently. Here w is Choi infidelity, equivalently total nonidentity Pauli-error probability; the identity/depolarizing MIXTURE coefficient is4w/3, not w. Half-diamond(E,U_V)=w: the Choi test gives the lower bound w, and the representation as identity with probability1-w plus three Pauli errors of weightw/3 gives upper boundw by the triangle inequality. This is an exact channel resource, not just a state close to a Choi vector.

## Why product-resource PBT pays this noise once

Let the resource be N independent copies of Choi(E)=(id_A tensor E_B)(Phi_AB). Let M_i be any Alice-only CP measurement branch on the payload and all A halves; a standard PBT branch selects B_i, traces the other B halves and relabels B_i as output. Each E_B commutes with M_i because it acts on a disjoint subsystem. Trace preservation removes all E_Bj on discarded ports j≠i. The remaining output map is exactly E composed with that branch's ideal-Bell-resource map. Summing branches gives E composed with Gamma_N, where Gamma_N is the corresponding ideal-product-resource PBT channel. This applies with arbitrary payload/reference entanglement.

Thus an independently established bound half-diamond(Gamma_N,id)<=delta_N yields half-diamond(E composed Gamma_N,U_V)<=delta_N+w, not delta_N+Nw. No claim about a specific delta_N, port count, optimal resource or efficient measurement compiler follows from this calculation. The argument uses selection/relabeling only on Bob's side; unaccounted Bob-side correction gates or errors require separate treatment.

Taking all four outputs of one noisy successful transduction does NOT establish independent ports. In fact the joint output is supported in Sym^4(C4), whereas a mixed full-rank marginal's fourfold product would have full support; they generally cannot coincide. One retained marginal from each independent acquisition/conversion batch supplies the required product resource. Correlations through source memory, common stopping events or postselection must be accounted for before claiming that interface. The whole output-noise-once claim is conditional on that product-Choi assumption.

## Boundaries and evidence

The complete matrix transfer and covariance are exact finite-dimensional arithmetic. No physical preparation, source-noise-to-label reduction, finite-cap state law, noisy control implementation, purification resource cost or PBT native execution is certified here. A shared finite cap can correlate completed batches and change their accepted states; a separately proved flagged-instrument truncation bound may transfer the ideal reference protocol, but cannot be silently replaced by an IID assumption.

The original four-program source certificate and its independent review remain dependencies. The reviewer's separate symmetrized two-output construction is not used or self-accepted. No novelty or conventional-controller advantage is claimed.

Primary comparison inspected2026-10-29: Pereira, Banchi and Pirandola, *Characterising port-based teleportation as a universal simulator of qubit channels*, https://arxiv.org/abs/1912.10374, documents general resource-to-channel PBT processing. The exact noise-once identity above is derived directly from local CP-map commutation and trace preservation rather than assumed from a numerical resource-state result.

Executed independent evidence: `independent_covariance_fast.py` completed all six exact generator identities, reconstructed the quadratic output from three complete rational pair inputs, and checked the exact Choi marginal. Its JSON is the completed computational evidence. The older dense implementation is retained only as a slow prototype and is not needed by this receipt.

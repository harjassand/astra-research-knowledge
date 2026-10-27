# Dimension-free mixed-flag heralding from the physical-flat deficit

## Operational theorem

For the actual TP channel

 E(rho)=p rho⊗sigma+q (I3/3)⊗eta, p+q=1,

allow arbitrary finite-dimensional, mixed and noncommuting logical states sigma,eta. An output isometry can be undone first when present. Define its normalized WH3 deficit Delta and the optimal logical Bayes discrimination error

 e=(1-||p sigma-q eta||_1)/2.

Then

 **Delta >= e^2/5.**                                      (1)

Consequently the actual optimal binary logical measurement, followed by discarding the logical system while retaining its classical outcome, gives a heralded instrument within

 **2e <= 2 sqrt(5 Delta)**                                (2)

in diamond norm of the ideal instrument whose success map is p id3 and failure map is q times the maximally mixed qutrit reset. The estimate is dimension-free and preserves arbitrary input entanglement. It is a decoding/instrument guarantee, not an assertion that the unmeasured logical output states themselves become orthogonal at the same rate.

## 1. Exact positive-mixture source receiving

Set X=p sigma and Y=q eta/9, and let

 Q(t)=Tr(tX-Y)_+, t>=0.

The positive-mixture theorem in white_noise_stability_operator_bath_lifting_theorem.md applies to the ACTUAL source

 A=Phi3⊗X+I9⊗Y.

Let mu be the positive Stieltjes derivative of Q', including its right-derivative atom at zero. The theorem gives

 Delta=integral_[0,infinity) h(s) dmu(s),
 h(s)=Delta(Phi3+s I9),
 mu([0,infinity))=TrX=p,
 Q(t)=integral(t-s)_+ dmu(s).                            (3)

Moreover Q(t)>=t TrX-TrY, since Tr Z_+>=TrZ. Therefore

 integral min(t,s) dmu(s)=t p-Q(t)<=TrY.

Monotone convergence gives

 integral s dmu(s)<=TrY=q/9,
 integral(1+9s)dmu(s)<=1.                               (4)

No invertibility, commutation, individual eigenvector tracking or unproved moment equality is used.

The Helstrom formula gives exactly

 e=p-Tr(X-9Y)_+=p-9Q(1/9)
  =integral min(1,9s)dmu(s).                            (5)

Thus both the entropy resource and the operational Bayes error are integrated against the SAME source-derived positive measure.

## 2. Scalar payment with an explicit universal constant

For f(x)=x logx the isotropic scalar curve is

 h(s)=f(1+s)-4f(s)-6f(s+1/3)+9f(s+1/9).

The matrix proof's scalar derivative, integrated in the success weight, gives the exact positive formula

 h(s)=integral_0^1 log(1+4xs/(x+3s)^2) dx.               (6)

Using log(1+u)>=u/(1+u),

 h(s)>=integral_0^1 4xs/[(x+s)(x+9s)] dx
     >=2s/[(1+s)(1+9s)]
     >=(1/5) min(1,9s)^2/(1+9s).                        (7)

For the final step: if s<=1/9, the ratio of the middle expression to min(1,9s)^2/(1+9s) is2/[81s(1+s)]>=1/5; if s>=1/9 the ratio is2s/(1+s)>=1/5. The endpoint s=0 is continuous.

Cauchy–Schwarz, then(4), yields

 e^2 <= [integral min(1,9s)^2/(1+9s)dmu]
        [integral(1+9s)dmu]
     <=5 Delta.

This proves(1). The constant5 is a convenient explicit certificate, not optimized.

## 3. Actual heralded instrument

Take the Helstrom success effect M=1_(0,infinity)(p sigma-q eta), with any optimal convention on its zero eigenspace. Put

 alpha=p Tr[(I-M)sigma], beta=q Tr[M eta], alpha+beta=e.

After measuring the actual logical output and discarding it, the two qutrit maps are

 J_success=(p-alpha) id3+beta R0,
 J_failure=alpha id3+(q-beta)R0,
 R0(rho)=Tr(rho)I3/3.

The ideal pair is(p id3,q R0). The difference has two opposite classical blocks, so

 ||J-J_ideal||_diamond
 =2||beta R0-alpha id3||_diamond<=2(alpha+beta)=2e.

This proves(2), with no postselection in the norm statement. Constructing M requires access to p,sigma,eta (or a separately learned discrimination model); the entropy value alone does not identify that measurement. If p>e, then actual success probability is at least p-e; its normalized successful output, including an entangled input, differs from the input by at most2e/(p-e). As usual a useful conditional recovery bound requires a nonvanishing success denominator.

## 4. Equality and lineage

Equation(1) shows Delta=0 forces e=0, hence orthogonality of the supports of p sigma and q eta. Conversely orthogonal supports or p q=0 give exact generalized-erasure/reset/reversible equality. This independently receives the equality classification.

The positive-value class itself was already covered by the earlier operator-bath lifting theorem. The short matrix multiplicative-convexity proof in physical_flat_mixed_reset_noncommuting_theorem.md is an independent proof, NOT new class coverage. The newly extracted result here is the dimension-free Bayes-error and actual heralded-instrument capability.

No assertion is made for arbitrary physically nonflat mixed reset tau; pure-reset extremum and physical-twirl monotonicity both fail there, as separately preserved.

## 5. The square-root instrument exponent is sharp, even for arbitrary decoders

Take a one-dimensional logical system, so sigma=eta=1 and

 E_p(rho)=p rho+(1-p)Tr(rho)I3/3.

For p<=1/2, its Helstrom error is e=p. Direct expansion of the exact isotropic spectra gives

 Delta(E_p)=2p^2+O(p^3) as p tends to zero.                (8)

Moreover E_p is entanglement-breaking for0<=p<=1/4. This can be verified without a threshold citation: Haar averaging pure product states gives

 integral P_psi⊗P_bar(psi) dpsi=(I9+3Phi3)/12,

which is exactly its normalized Choi state at p=1/4. For smaller p, the Choi state is a convex combination of this separable state and I9/9.

Any instrument applied only to E_p's actual output therefore has a separable positive successful normalized-Choi block C_s (possibly subnormalized). For any such block,

 Tr[(I9/3-Phi3) C_s]>=0,

because every product vector has squared overlap with normalized Phi3 at most1/3. The ideal successful map p id3 has Choi block pPhi3 and witness expectation -2p/3. Since ||I9/3-Phi3||_infinity=2/3, trace duality gives

 ||C_s-pPhi3||_1>=p.                                    (9)

The full instrument diamond distance from the ideal success/failure instrument is at least this normalized-Choi block distance, hence at least p. Equations(8)-(9) exclude a universal error bound C Delta^a for any a>1/2, even if the receiver may choose an arbitrary physical-output decoder rather than the stated logical Helstrom measurement. The target success probability remains the actual p; changing that target is not the claimed capability.

### Sharpness also holds at fixed nonzero success probability

The preceding obstruction is not only a vanishing-success-probability artifact. Fix any0<p<1, q=1-p, and use a logical qubit with

 sigma_r=diag(1-r,r), eta=diag(0,1), r tending to zero.

Logical sector0 carries reversible success mass p(1-r). Logical sector1 carries the actual subnormalized channel pr id3+q R0. The deficit is reference-direct-sum additive, so

 Delta=(q+pr) Delta(E_(pr/(q+pr)))
      =2p^2r^2/q+O(r^3),
 e=pr for sufficiently small r.

The sector1 channel is entanglement-breaking when pr/(q+pr)<=1/4. Under ANY actual output instrument, its successful Choi contribution is therefore separable and has nonnegative expectation against W=I9/3-Phi3. The sector0 successful contribution has trace at most p(1-r), hence witness expectation at least -(2/3)p(1-r). The ideal total successful Choi block pPhi3 has expectation -2p/3. Trace duality therefore again gives instrument diamond error at least pr.

In particular p=q=1/2 stays fixed, Delta=r^2+O(r^3), and every receiver has error at least r/2. Thus the square-root exponent is sharp even with success probability bounded away from both endpoints and logical rank only two. The disappearing scale is a logical overlap eigenweight, not the global success probability.

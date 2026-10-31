# Robust backward reference weights on the actual source generator

Status: ROOT candidate, UNREVIEWED. Companion to BACKWARD_CONTROLLED_OBSERVABLE_ADMISSION_CANDIDATE.md (f2d89255727d94d8a4e1a4af08c906e1e39c7fbff6149c40ee72b0f54b4d3a3c). Same fixed-patch, initialized-field, source-blind local-control and product-commutation premises. The exact theorem is not changed.

Let the actual source-only generator G be constant during the location. Choose any positive reference rate r and let

  J(t)=G^*K(t)+rK(t), ||K(t)||<=c,
  d_J>=integral_location ||J(t)||dt.

No exact source eigenspace is assumed. Let C_{s<-t} be just the prescribed IDEAL DATA control/instrument evolution, including local retained records, without any source evolution. Define the reference analysis weight

  B0(t)=2 integral_t^b exp[-r(s-t)] C_{s<-t}^* K(s) ds.

It is Hermitian, ||B0(t)||<=2c/r, B0(b)=0, and

  (partial_t+i ad_H0-r)B0=-2K,
  B0_before=C^* B0_after at a local instrument.

Because the ACTUAL constant source generator commutes with every source-blind data control/instrument,

  F(t):=(G^*+r)B0(t)
    =2 integral_t^b exp[-r(s-t)] C_{s<-t}^* J(s) ds.

Unital CP contraction and nonnegative Fubini give

  integral_a^b ||F(t)||dt <= (2/r) integral_a^b ||J(s)||ds
                          <=2d_J/r.

The proof evolves the actual generator throughout. The scalar decay kernel in B0 is an analysis reference and is NOT a changed physical generator or an uncharged simulation/preparation service.

With V=I+Im(z)B0 and q=2Rc/r<=1/2, the actual weighted generator is the exact theorem's quadratic term plus Im(z)F. Its integrated extra squared-norm exponent is at most

  (R/(1-q)) integral ||F|| <=4R d_J/r.

The same product proof, endpoint factor1+q, local instrument equality and inclusive Cauchy extraction therefore yield

  ||E(S)||<=eta_J(R)^|S|,
  eta_J(R)=sqrt(1+2Rc/r)
           exp[4R^2 c^2 tau/r+2R d_J/r]/(R-1),
  1<R<=r/(4c).

This does not charge derivative or bandwidth of ideal source-blind controls, but it DOES charge actual bias and source-model error. For a source-independent unwanted term K0, G^*K0=0, so its residual is rK0; the resulting d_J/r includes its integrated ordinary strength. Increasing r cannot hide it.

Likewise a uniform residual ||J||<=epsilon*r*c gives d_J/r<=epsilon*c*tau. At high r the residual term alone leaves a sufficient-radius expression exp(hR)/(R-1), h=2epsilon*c*tau. For h>0 its unconstrained minimum is h exp(1+h) at R=1+1/h. This is a floor of this sufficient certificate, not a universal physical lower bound for all mismatches. A source-independent data bias provides a genuine worst-case unsuppressed operation; a detuning error need not do so.

To acquire the known-model certificate, one can compute the actual generator action on all supplied coupling coefficients and bound J with exact rational arithmetic. For a real unknown apparatus the uniform model/action error still has to be calibrated. The corollary does not infer such a bound from samples of a single state or from a measured two-point covariance.

If G varies with time, G_t^* need not commute through the future integral acting on K(s). The formula above is NOT transferred to time-varying generators without an additional receiving argument. This restriction prevents silently treating a reference decay fit as an actual generator certificate.

# Fixed-control mass-metric repair

Principal follow-up, candidate proof for independent checking; not frozen initial. No priority claim.

Let A,C>=0 be self-adjoint matrices in one Hilbert space. Suppose |<v,(C-A)w>|<=d <v,Av>^(1/2)<w,Aw>^(1/2), and M>0 satisfies ||M-I||<=d<1. Put B=M^(-1)C. Proposed gap-free bound:

sup_(t>=0)||exp(-tA)-exp(-tB)|| <=8d/(1-d).

For z outside |arg z|<pi/3, scalar spectral calculus gives ||(z-A)^-1||<=2/(sqrt3 |z|), ||A^(1/2)(z-A)^-1||<=|z|^-1/2, ||A(z-A)^-1||<=2/sqrt3. Write H=M^-1/2 C M^-1/2. Then ||(zM-C)^-1||<=2/[sqrt3(1-d)|z|] and ||(zM-C)^-1 C^1/2||<=1/[sqrt(1-d)sqrt(|z|)]. Since C>=(1-d)A, replace C^1/2 on the right by A^1/2 at cost (1-d)^-1/2. These estimates hold also on the left by adjunction.

Resolvent identity:
(z-B)^-1-(z-A)^-1=(zM-C)^-1[(C-A)-(M-I)A](z-A)^-1.

The two terms are bounded by d/[(1-d)|z|] and 4d/[3(1-d)|z|], hence total <=3d/[(1-d)|z|].

For t>0 use Dunford contour rays arg z=+/-pi/3, |z|>=1/t joined by the LEFT arc |z|=1/t, pi/3<=arg z<=5pi/3. Close at large radius in the right sector, beyond all (finite) eigenvalues, then pass to infinity. This contour encloses nonnegative spectra including zero. Small arc contributes <=(2e/3)*3d/(1-d). Rays contribute <=3d/[pi(1-d)] times integral_1^infinity exp(-r/2)/r dr; this integral is <1 (e.g. 1/r<=1 for r>=1 yields bound 2exp(-.5)>1, so need split or use direct value <.56). Thus total <8d/(1-d). At t=0 trivial. No gap/inverse A is used. This is likely standard analytic-semigroup perturbation; novelty UNKNOWN.

## Reversible-chain application
True positive generator A is self-adjoint in L2(pi), learned generator B in L2(pihat). Define M=diag(pihat/pi), C=M B. Its quadratic form uses learned conductances pihat(x) qhat(x,y). If pointwise relative mass error <=d_m and edge-rate relative error <=d_q, form error <=d_m+d_q+d_m*d_q. Apply the lemma with d at least this and d_m, if d<1. Forecast error for |g|<=1 and initial density f is <=||f||_L2(pi)*8d/(1-d), plus source/numerical error. This repairs changed equilibrium weights for FROZEN control, not arbitrarily switched estimated metrics.

## Acquisition implication requiring physical checking
For energy U(k)+sum_r W_r(microblock), conditional Gibbs mu_(r,k) is independent of U. Acquire positive bare coarse rates a_r^+(k),a_r^-(k) by count-clamped conditional mixing then local rate probes (avoid noisy full-count inversion). Detailed balance implies Z_r(k)a_r^+(k)=Z_r(k+1)a_r^-(k+1). Positive estimates define what_r(0)=1, what_r(k+1)/what_r(k)=ahat_r^+(k)/ahat_r^-(k+1). The future learned generator with rates ahat_r^+/-(k_r) exp[-beta Delta_r U/2] is exactly reversible in pihat_U proportional exp(-beta U) product_r what_r(k_r).

If all bare rates have relative error eta<=1/2, log ratio errors <=4eta. With N=sum_r m_r, unnormalized log weight error <=4Neta and normalized |log(pihat_U/pi_U)|<=8Neta, UNIFORMLY in the new U. Thus d_m<=exp(8Neta)-1, giving fixed-control all-time error O(W Neta), polynomial precision eta=O(epsilon/(WN)) instead of 1/T. Must derive polynomial conditional mixing, local-rate measurement/noise conditioning, state preparation and all costs. No arbitrary strongly interacting shell promise is granted. For growing number of blocks, a full coarse matrix still has exponentially many count states; ordinary simulation remains O(T). Only fixed block number can use polynomial-log(T) matrix evaluation.

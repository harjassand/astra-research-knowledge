# Preferred two input Bell receiver protocol

## Encoding and distinct channel

Use two classical inputs i=+1,-1 and prepared qubit outputs sigma_+=(I+aX)/2, sigma_-=(I+aY)/2. The preferred choice is a=9/10, with erasure reveal q=9/20. A fixed local output rotation takes the two states to sigma_i=(I+bZ+i bX)/2, where b=a/sqrt(2). This is a classical-input preparation channel, not a coherence-preserving qubit-input channel.

Draw label ell and input i independently and uniformly from {+1,-1}. The reference state conditioned on them is

tau_(ell,i) = [[1, ell i t],[ell i t,delta]]/(1+delta),

with delta=1/10 and t=3/10. Equivalently the label-conditioned classical/reference state has blocks (B_i+ell t H_i)/(1+delta), where B_i=diag(1,delta)/2 and H_i=i X/2. Each is faithful because delta-t²=1/100>0. Both reference marginals are diag(1,delta)/(1+delta), so the erased branch has no label information. These states are separable across the classical/reference cut.

The alphabet has two active inputs. If embedded in a three-input alphabet with an unused symbol, it is not full rank on that enlarged alphabet. A sufficiently small common positive third block preserves a strict gap by continuity, but changes the exact fixture; no such regularization is silently applied here.

## Fixed Bell receiver and source optimum

Let lambda_+=(1+b)/2 and lambda_-=(1-b)/2. In output tensor reference order, the raw average state is diag(lambda_+,lambda_-) tensor diag(1,delta), and the raw tangent is (b/2) X tensor X. The optimal estimator observable O solves A O+O A=2tH. Its only nonzero entries are

O_(00,11)=O_(11,00)=t b/(lambda_+ +delta lambda_-),
O_(01,10)=O_(10,01)=t b/(lambda_- +delta lambda_+).

The four Bell vectors diagonalize O for every a and delta. Thus the measurement basis is fixed; only its eigenvalue scores vary. Equivalently, put r=6/11 and z=9/11. The scores are

Phi+ and Phi-: +br/(1+bz) and -br/(1+bz),
Psi+ and Psi-: +br/(1-bz) and -br/(1-bz).

For the preferred design their magnitudes are approximately 0.22826853 and 0.72421501. The source reveal branch measures reference X and reports i times (6/11) times the measurement outcome. The source erase branch reports zero. Its receiver is optimal for the specified encoding.

The Bell measurement is an established joint measurement. Local X measurements already attain the minimum binary 0–1 error in the rotated basis because the difference of the two target hypotheses is proportional to X tensor X. Bell refinement and its different posterior magnitudes matter to quadratic-MMSE, not to a claimed necessity of entangled measurement for guessing the label.

## Exact risks and ordering

Write c=a²/2. The reference-free SLD/MMSE erasure threshold is c; the complete threshold for this TWO-input family is c/(1-c). At a=9/10 these are 81/200 and 81/119. The reveal q=9/20 is between them. The full three-axis family has a different complete threshold, 54/73, and is not substituted here.

For the stated finite encoding,

MMSE_source = 524/605,
MMSE_target = 14723/17639,
Delta = MMSE_source-MMSE_target = 335421/10671595
      approximately 0.03143119655496671.

The all-parameter derivation is in proofs/ANALYTIC_FAMILY.md. Independently solving the full target Sylvester equation and directly evaluating conditional losses reproduces these values. This is a finite balanced-binary identity, not an infinitesimal Fisher approximation. It is an achieved protocol, not a globally optimal encoding or memory frontier.

## IID evaluation counts and their meaning

The exact loss variances are 145719/366025 for the source and 2359666496016/5488098288119 for the target. Their sum is below v=829/1000. Exact spectral bounds give target estimator norm below 3/4; the source norm is 6/11. Each arm's loss range has width at most M=3. The true gap exceeds g=157/5000=0.0314.

With n independent IID trials per arm, independent balanced label draws, and fixed correctly calibrated preparation and receivers, let D_hat be mean source loss minus mean target loss. Bernstein applied to all 2n independent centered arm variables gives

Pr(D_hat-Delta <= -x) <= exp[-n x²/(2(v+M x/3))].

M bounds each individually centered arm loss; it is not a bound assigned to a centered paired difference. The two-sided bound adds a factor two.

- 5,229 trials per arm suffice for wrong empirical ordering probability below 5%.
- 25,283 trials per arm suffice for a two-sided 95% error radius g/2=0.0157. On its coverage event the resulting interval has a strictly positive lower endpoint because Delta>g.

The first guarantee is not a confidence-interval procedure or a separate null-hypothesis significance guarantee. These are sufficient model-based counts, not minimal sample complexities. They exclude receiver fitting, training/calibration data, preparation errors, unequal detection efficiencies, correlated drift, and postselection. The exact checks also certify count sufficiency using rational upper bounds on the relevant logarithms, so floating-point rounding is not the certification basis.

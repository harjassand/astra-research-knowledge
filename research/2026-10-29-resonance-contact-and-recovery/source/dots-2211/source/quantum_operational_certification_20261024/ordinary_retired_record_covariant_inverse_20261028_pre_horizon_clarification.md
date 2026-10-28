# An acquired inverse whose retired-record complete error is quadratic

28 October 2026. New candidate; separate internal review required. This is a constructive companion to ordinary_coherent_inverse_record_retaining_lower_bound_20261028.md. It does not change that lower bound's metric or the general retained-memory fallback theorem.

## 1. Resources and the distinction that enables the construction

The calibration family is the independently restarted one-qubit source Ad_Vtheta composed with Z dephasing of known or unknown fixed p<1/2, where Vtheta=exp(-i theta Z). Write a=1-2p>0. Every probe is |+>, every readout is an ordinary equatorial two-outcome measurement; no coherent calibration reference is needed. The learner need not know a to compute its angle. A quantitative cost bound depends on a.

All training records and the learned angle/program must be inaccessible to the subsequent service controller and source. The service source memory is independent of the calibration record conditional on the actual fixed theta, as supplied by independent restarts or by an actual isolated new source instance. A private classical controller may use the learned angle to implement the decoder, but neither its program nor historical records are outputs of the compared channel. This is a physical restriction, not a mathematical choice to forget a record that a future interaction can recover.

The conclusion below compares the record-AVERAGED actual decoder with the true inverse in diamond norm. It therefore applies to any subsequent source A:P M->P M' followed by the same Vtheta, including coherent error amplitudes, provided the training record is independent of this joint service input/source. It does not assume A is a Pauli CP instrument. It does not cover a source whose continuing memory is correlated with training records, or free reuse of the same random decoder over an arbitrary long adaptive computation.

## 2. Finite actual ordinary estimator

Choose a power of two K>=4. On every one of N fresh probes choose an independent uniform integer L in {0,...,K-1}, set phi=2pi L/K, and measure cos(phi)X+sin(phi)Y. The outcome Y in {+1,-1} has

 E[Y|phi]=a cos(2theta-phi).

The actual estimator is the unit complex number

 r = S/|S|, S=sum_t Y_t exp(i phi_t).

If S=0, choose r independently and uniformly among the K roots of unity. All possible S and r are algebraic; K is finite and only log2 K random bits per probe are needed. The decoder is a phase rotation Uhat whose adjoint action corresponds to exp(+i hat_alpha Z/2), where exp(i hat_alpha)=r. It can be specified directly by algebraic square roots of r, so no free transcendental angle oracle is required; the irrelevant common phase is fixed consistently for implementation. Gate synthesis, basis preparation/readout and private program storage retain actual finite approximation costs.

For analysis only define m=2S/(aN) and u=exp(i2theta). Since K>=4, root-of-unity averaging gives

 E[m]=u, E|m-u|^2=(4/a^2-1)/N=:v/N.               (1)

Normalization obeys |r-u|<=2|m-u| when m!=0. At m=0, |r-u|<=2=2|m-u|, so the same bound holds. Hence

 E sin^2((hat_alpha-2theta)/2) <= v/N.             (2)

This is an acquired estimator using actual ordinary outcome records, not an imposed symmetric error distribution.

## 3. Exact finite-group symmetry on the angle grid

First suppose theta=pi j/K. Relabeling L by L-j shifts the observations to the theta=0 law and rotates r by exp(i2theta). Reflection L->-L conjugates r in the theta=0 law. The independent uniform tie rule has both symmetries. Thus

 lambda=E[r exp(-i2theta)] is REAL,
 b=(1-lambda)/2=E sin^2((hat_alpha-2theta)/2)<=min(1,v/N).

After all records/program labels are traced from the accessible interface, the actual residual decoder channel is EXACTLY

 E_y[ D_y composed Ad_Vtheta ]=(1-b) id+b Ad_Z.    (3)

Therefore its half-diamond error from identity is b, and composition after ANY independent joint service source preserves the upper bound b. Coherent retained error flags do not invalidate (3): the random calibration error was averaged before its independent action on the joint service, not incorrectly decomposed inside an unknown coherent native source. No CP domination relative to the record-resolved ideal process is asserted.

Equation (3) also makes the distinction from the lower-bound note precise: E_y of conditional complete errors may be order N^-1/2 while the complete norm of the genuinely record-retired averaged channel is order N^-1.

## 4. Arbitrary continuous theta with finite operations

The grid is an analysis device, not an assumption about the unknown angle. Choose nearest theta_0=pi j/K modulo pi, so |theta-theta_0|<=pi/(2K). For the SAME estimator and actual finite measurement choices, the fresh-probe root-fidelity argument from the lower-bound note gives

 TV(P_theta,P_theta0)<=sqrt(N) |theta-theta_0|.

Mixing the same CPTP decoders with two classical laws changes their half-diamond norm by at most that TV. Composing the two nearby exact V rotations adds at most |theta-theta_0|. Using (3) at theta_0 yields, uniformly for every theta,

 half || E_(Ptheta) D_y Ad_Vtheta -id ||diamond
 <= min(1, v/N + pi(sqrt(N)+1)/(2K)).             (4)

Take K to be the smallest power of two at least max(4,pi N(sqrt(N)+1)). The second term is <=1/(2N); K=O(N^(3/2)), and log2 K=O(log N). Thus the ordinary-call cost for fixed a>0 and desired record-retired complete error epsilon is O(a^-2/epsilon), plus explicitly paid finite control/implementation precision. Every probe uses one source call and one binary readout; finite roots and algebraic normalization may have substantial bit cost, and no fast arithmetic implementation is claimed here.

Independent preparation/readout, random-choice and decoder synthesis errors transfer through a whole-protocol diamond/record-TV debit nu, giving RHS(4)+nu. It is not legitimate to reuse ideal symmetry while ignoring a biased control implementation. A sufficient per-probe complete error O(nu/N), and decoder error O(nu), can be charged by an ordinary hybrid. This is a finite accuracy prescription, not hardware qualification.

## 5. Consequence and limitations

This is a scoped explicit mechanism avoiding the inverse-square cost for the WEAKER retired-record metric, while retaining coherent service memory. It does not improve the arbitrary record-retaining fallback by algebra alone. The price is genuinely private retirement, independence of training from service memory, the known one-axis mixer structure, stationary calibration contrast and the finite precision/random-control bill.

The strongest conventional learner has the same probes, measurements, estimator and resources; this is a constructive representation/interface distinction, not an asserted advantage over conventional estimation. The extension to calibration-correlated retained memory, many uses of the same random inverse under feedback, general noncommuting mixers and practical resources remains open. Historical novelty has not been established.

# Exact collective killing scale with replenishment

30 October 2026. Candidate completion using the root multiplicative forcing witness and COLLECTIVE_BIRTH_SEED_GREEN.md. Both dependencies must be read with their exact contracts and any binding review completions. No whole chemical theorem is asserted.

Root source read: collective_forcing/ROOT_PRODUCT_FORCING.md, SHA bb211c7b7d0b8b8ffac258e0b62386e74ee171468fd48c13edbd4111172d4816. Its progress subevent must change only the designated label, or make additional changes that are all safe. The product proof gives threshold c n T^L and failure exp(-c n T^L), not the earlier variance-loss exponent.

Under the constant positive immigration, bounded seed-deletion, kill-comparison and surviving-label contract in COLLECTIVE_BIRTH_SEED_GREEN.md, put

    alpha=m/(Lm+1).

The exact local upper scale is

    E tau^j <= C_j n^(-j alpha),
    E integral_0^tau f_s(A_t)dt <= C_s n^-alpha f_s(A_0),
    E[f_(s+p)(A_out); kill]
       <=C_(s,p) n^[-alpha p/(2p+m)] f_s(A_0).       (E)

No epsilon loss or logarithmic block factor is needed.

## 1. Constant-success blocks, not superpolynomial single-block survival

Let initial population be n and fix T=C n^-alpha. Stop at sigma, the first time the actual population falls below n/2; set sigma=infinity if no deletions are possible. Until sigma, every block starts with N>=n/2 labels.

Apply the virtual-label midpoint proof at that starting state, with the SAME block length T. Root product forcing supplies M=floor(c N T^L) virtual targets at the midpoint, except with probability exp(-c N T^L). Cohort adverse-touch and excessive seed-count errors are exp(-c M). On their complement the integrated kill hazard over the remaining half-block is at least

    c T M^m >= c' N^m T^(Lm+1)
              >= c'' C^(Lm+1),

for n large. Since N T^L>=c C^L n^[1/(Lm+1)], all error terms vanish uniformly in N>=n/2. Choose fixed C sufficiently large so the hazard survival term is at most1/4; then choose n sufficiently large so the other errors sum to at most1/4. Thus conditional survival through any block beginning above n/2 is at most1/2. This assertion concerns the actual kill, including possible seeds inside the block; the virtual comparison pays them as in the preceding note.

Set eta=tau wedge sigma. Conditional restart while eta has not occurred gives

    P(eta>jT)<=2^-j,
    E eta^j<=C_j T^j.

Dropping below n/2 before killing requires at least floor(n/(2d)) seed marks, because births only increase population and each seed deletes at most d. The actual mark-ratio estimate therefore gives

    P(sigma<tau)<=C exp(-c n).

For d=0 or c=0 this event is absent. The independently earned uniform replenishment/head bound applies at sigma; its constants do not grow with the current state. Hence

    E tau^j <= C_j T^j + C_j exp(-c n),

which proves the moment assertion in (E). This is precisely where the genuine replenishment proof, rather than geometric seed counts alone, is indispensable.

More explicitly, writing R=tau-sigma on the low-population branch,

    P(tau>t)
      <=P(eta>t/2)+P(sigma<tau,R>t/2)
      <=2^(-floor(t/(2T)))+C exp(-c n)exp(-c' t/2).

Thus integral_0^infinity P(tau>t)^(1/2)dt<=C T. Combine this with the killed incoming-grade bound from the preceding note to obtain graded occupation in (E). The actual kill compensator and the extra-output-grade split then give its terminal bound with delta replaced by alpha. Terminal same-grade preservation is unchanged.

## 2. The time power cannot be improved uniformly in this abstract class

Take n initial labels all at rank L, independent one-step progress clocks q, no adverse events, no safe extras, and no seeds. Keep constant immigration lambda>0. Kill at rate kappa(A)_m. Before the first immigration, the un-killed target count at time t is Binomial(n,p(t)), p(t)=P(Pois(qt)>=L). Therefore

    P(tau<=t)
      <=lambda t + kappa integral_0^t (n)_m p(u)^m du
      <=lambda t + C n^m t^(Lm+1),

using p(u)<=(qu)^L/L!. The first term simply pays the event that any immigration occurred; it does not condition the kill law incorrectly. For t=c0 n^-alpha with fixed sufficiently small c0, this probability is <=1/2 for all n large. Consequently E tau^j>=c_j n^(-j alpha) in this example.

Together with (E), this proves sharpness of the population POWER of the local killing-time scale for the stated abstract class. It does not identify sharp leading constants, optimal chemical Lyapunov powers, or recurrence for a new raw network. Ordinary clock/Filonov machinery still needs the actual full section costs and signed reward.

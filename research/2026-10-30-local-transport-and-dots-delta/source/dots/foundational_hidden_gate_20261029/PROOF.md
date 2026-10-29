# Boundary thermodynamic tomography: construction and decisive failure

29 October 2026. Private research. Producer derivation and finite diagnostic,
not independent acceptance, novelty clearance, physical measurement or apparatus.
Astra reference revision: 95c99ce592a48d4505dd4bfcc0925d7ebad0efdd.

## Result first

I investigated one broad opening: recover hidden nonequilibrium kinetics and
energy dissipation from experimentally accessible boundary control, rather than
assume the response, heat or microscopic-state oracle. Full success would turn
opaque physical devices into experimentally certified predictive/control models;
that would change how dissipative materials and energy-conversion mechanisms are
discovered. This document DOES NOT achieve that objective.

There is a concrete finite-time reconstruction for a favorable common-gate
model. More importantly, a four-state rational construction proves that even
arbitrary entry/exit control at a degree-one gateway cannot distinguish an
exact equilibrium device from devices with arbitrarily large entropy production.
The hidden jump activities stay uniformly bounded, stationary masses stay away
from zero, and the entire baseline spectrum is unchanged. Thus this is not just
insufficient samples, a tiny signal or a slow-mixing obstruction.

The broad single-port tomography opening is not justified as Astra's flagship.
It fails before scaling: physical access and thermodynamic identifiability must
be changed. This is a decision made from construction, not an opportunity ranking.

## 1. Exact input/output/cost contract

Use row-generator conventions. A CTMC has observed gateway 0 and m hidden states.
Only Y=1_{X=0} is continuously observed; hidden transitions are never observed.
Let K be an m by m irreducible internal generator, K1=0. Let c_i>=0 be rates
from hidden i to gateway, D=diag(c), and a_i>=0 be rates gateway to hidden i.
Write s=sum a_i>0 and p=a/s. The baseline full generator is

    Q = [ -s       s p ]
        [  c      K-D ].

A COMMON-BARRIER control x>0 multiplies BOTH directions of every edge incident
to the gateway, with internal K unchanged. The outgoing gateway holding rate is
xs; the conditional entrance distribution p is unchanged. During an excursion
the killed hidden generator is

    T_x = K-xD.

This is an actual CONTROL premise. Local detailed balance does not establish it.
A state-energy shift with fixed transition-state barriers typically changes only
rates OUT of that state. Such a shift leaves hidden T unchanged and provides no
new excursion information; it merely retimes gateway waits. The first exploratory
phrase 'gateway energy modulation' was physically insufficient and is withdrawn.
Root identified this error before the final construction. All code now uses
common-barrier scaling, not the erroneous energy shorthand.

The required measurements are independent regenerative excursions starting when
the observed gateway is left. The strong Markov property supplies fresh entrance
law p; it is not a hidden-state reset. For a programmed word w=(a_1,...,a_l), each
control level lasts tau until the observation window ends or the process returns.
The bounded report is whether no return occurred. Its exact probability is

    h(w)=p M_{a_1}...M_{a_l}1,
    M_a=exp(tau T_{x_a}).                                  (1)

Acquisition must pay return/wait time, missed-transition detection, latency,
control fidelity and trial count. An iid Bernoulli estimate with absolute radius
eta for J settings costs at most ceil(log(2J/delta)/(2 eta^2)) trials PER setting
by a union Hoeffding bound. This is a sufficient schedule, not a lower bound.
No fixed practical cost follows from finite state dimension.

## 2. Finite scalar-data reconstruction in the favorable class

Take x0!=x1. Let m be known, c_i pairwise distinct, and suppose the m by m matrix

    H_ij=h(0^(i+j)),  i,j=0,...,m-1                     (2)

is invertible. Define

    H^(a)_ij=h(0^i a 0^j),  A_a=H^{-1}H^(a),
    z_i=h(0^i), b=H^{-1}z, alpha_j=h(0^j).             (3)

These use O(m^2) survival settings, at most 2m-1 time intervals per setting.
Let R have rows p M0^i and C have columns M0^j1. Then H=RC and
H^(a)=R M_a C. Since H is invertible, both R and C are invertible and

    A_a=C^{-1}M_a C,  b=C^{-1}1, alpha=p C.            (4)

Assume a WARRANTED no-alias bound: tau ||T_xa||_infinity < pi for a=0,1.
Every eigenvalue of tau T_xa lies in the principal-log strip, so

    L_a=log(A_a)/tau=C^{-1}T_xa C,
    Dbar=(L_0-L_1)/(x1-x0)=C^{-1}D C.                 (5)

Let V contain eigenvectors of Dbar, and let c_hat be its diagonal eigenvalue list.
Distinct c_i imply V=C^{-1} P B for a permutation P and an invertible diagonal B.
Set

    S=V diag(V^{-1}b).

Since b=C^{-1}1 and P^{-1}1=1, S=C^{-1}P. Consequently

    K_hat=S^{-1}L_0 S+x0 diag(c_hat)=P^{-1} K P,
    p_hat=alpha S=pP.                                (6)

A single finite gateway holding-time probability r(t)=exp(-x0 s t) gives
s=-log r(t)/(x0 t). Equations (5)-(6) recover Q up to hidden permutation.
Steady-state entropy production then follows from actual recovered rates:

    sigma=sum_{i<j}(pi_i q_ij-pi_j q_ji)
                    log[(pi_i q_ij)/(pi_j q_ji)].      (7)

There is no supplied matrix oracle in this construction. The only data are
finite scalar survival and holding probabilities. However, exact probabilities
are mathematical inputs; finite trials require stability margins below.

This is ordinary switched-system/Hankel realization plus diagonal basis recovery,
not a claimed new general realization theorem. Petreczky--van Schuppen (2010/2011)
is a strong constructive predecessor. The useful model-specific statement is
which physical gate difference would provide a basis reference.

### What the invertibility assumption hides

It is not automatic at a chosen baseline. When p_i>0 and all c_i are distinct,
the controllability and observability determinants for T_x are nonzero
polynomials in x: their leading coefficients are nonzero Vandermonde products
of c, multiplied by product p_i on the row side. Thus all but finitely many
x have full Krylov rank. A sufficiently unaliased exponential preserves that
rank. This generic exact statement supplies NO lower bound on singular values.

All of the following affect statistical/bit cost: sigma_min(H), log conditioning,
minimum |c_i-c_j|, eigenvector conditioning, small p_i and control separation.
The number of states itself is an input; a hidden-order upper bound cannot be
certified from finite noisy data without a separation promise. Near-degenerate
models can mimic a smaller realization arbitrarily closely.

## 3. Exact three-state algebra check

For m=2, denote rates q01=a,q02=b,q10=c,q12=d,q20=e,q21=f. At gate x, the hidden
first-return Laplace transform is

    L_x(z) = [x R z + x^2 P+x Q]
             /[z^2+(x C+D)z+x^2 P+x Q],              (8)

where S=a+b, C=c+e, P=ce, D=d+f, Q=cf+de, R=(ac+be)/S.
Two distinct x values recover C,D,P,Q,R from the coefficient functions.
The roots of z^2-Cz+P are c,e. If c!=e,

    a=S(R-e)/(c-e), b=S-a,
    d=(Q-cD)/(e-c), f=D-d.                           (9)

The exact Fraction test uses (a,b,c,d,e,f)=(2,1,1,3,4,2), x=1,2, and recovers
every rate exactly. This is an algebra sanity check; it does not claim the
Laplace coefficients themselves have been acquired for free. Equation (2) is
the finite-probability acquisition construction actually tested next.

## 4. Execution and equally informed incumbent

experiment.py separates a hidden forward instrument from the receiver. Only
scalar h(w) and gateway survival are exposed. The receiver is not passed K,c,p.
The fixed three-hidden-state specimen has c=(.25,1.5,4), p=(.25,.4,.35), s=1.7,
x=(.6,1.8), tau=.35. Its actual norm bound meets tau||T||_infinity<=2.94<pi.

15 survival settings (including the deterministic empty word), maximum five
intervals, and one gateway setting reconstruct the model with aligned parameter
error 1.18e-11. True sigma=.733343066564; reconstructed sigma=.733343066567.
This is floating arithmetic using exact model probabilities, NOT a physical
experiment or outward-rounded numerical certificate.

Hankel condition number is about 20016; sigma_min is 8.51e-5. Fixed perturbation
radii 1e-12,1e-10,1e-8,1e-6 yield parameter errors about 1.4e-7,6.9e-6,.0038,.47.
At 1e-6 the reconstruction already has a negative offdiagonal rate.

The sampling diagnostic draws binomial COUNTS, not 140 million explicitly
simulated trajectories or laboratory excursions. At 100,000 and 10,000,000
trials per each of 14 nontrivial settings, the spectral receiver is unphysical.
The latter means a prospective 140 million excursions, not a measured runtime.

The equally informed comparator receives the SAME counts, settings, gate law,
known m and exact s. It performs conventional positive constrained weighted
nonlinear least squares (NOT maximum likelihood), with three fixed random
initializations that never use ground truth. It yields physical models but
in this diagnostic inferred sigma values 4.38 and 3.48 versus true .733. It is
not a certified global optimizer and no superiority over stronger fitting,
experimental design, Bayesian or profile-likelihood methods is established.
The unfavorable result is retained, not replaced by a tuned favorable specimen.

## 5. Stronger exact failure at a physical degree-one gateway

Let m=3, gateway 0 connect ONLY to hidden state 1, with baseline rates one in
both directions. Thus c=(1,0,0), p=(1,0,0), s=1. At baseline set

    K_0 = [ -3   1   2 ]
          [  1  -4   3 ]
          [  2   3  -5 ].

For 0<=r<r_star=(sqrt(37)-1)/6, define

    S_r = [ 1     0      0 ]
          [ 0    1+r    -r ]
          [ 0     0      1 ],

    K_r=S_r^{-1}K_0S_r
       = [ -3             1+r             2-r ]
         [ (1+2r)/(1+r)   3r-4     (3-r-3r^2)/(1+r) ]
         [  2             3+3r            -5-3r ].     (10)

All offdiagonal rates are positive on the stated interval, K_r1=0, S_r1=1,
S_r D=D S_r and p S_r=p. Thus for EVERY x

    K_r-xD=S_r^{-1}(K_0-xD)S_r.                      (11)

Equation (1) is therefore identical for every word, every interval duration,
and every control waveform, not merely for finitely many checked settings.

In fact allow the two gateway edge rates to be independently controlled:
q01=A(t)>0 and q10=B(t)>0. Extend S_r to diag(1,S_r) on all four states. It fixes
the gateway vector, total-ones vector, observation projectors and both boundary
edge matrices. The entire controlled generator family is simultaneously similar.
All binary observation laws therefore agree, including initial gateway starts.
With baseline stationary starts, use pi_r=pi_0 diag(1,S_r), which has the same
visible law and also transforms all observation products correctly.

For feedback, condition on previous visible history and controller randomness.
While away, the future boundary schedule is fixed until return; the killed
propagator has the same scalar survival law by (11). On the gateway, the same
A determines the holding law. Induction over excursions establishes equality
for arbitrary common nonanticipating bounded or locally bounded nonexplosive
boundary feedback. This is stronger than an open-loop finite-word ambiguity.

### Entropy production is nevertheless unbounded

At baseline A=B=1 the full stationary law is

    pi_r=(1,1,1+r,1-r)/4.                             (12)

The gateway carries zero stationary current. On the internal oriented cycle
1->2->3->1 the current is J=-r/4 and the forward/reverse rate-product ratio is

    R(r)=2(3-r-3r^2)/[3(2-r)(1+2r)].                  (13)

Hence the full stationary entropy production is

    sigma(r)=(r/4) log[3(2-r)(1+2r)/(2(3-r-3r^2))].  (14)

At r=0, Q is symmetric and sigma=0. At r=1/10, the affinity ratio is 287/342
and sigma=.00438321303257. As r approaches r_star from below, sigma diverges.

All jump rates and exit activities remain uniformly bounded. The smallest
stationary mass stays at least (1-r_star)/4>0.038. The full baseline generators
are similar, so their spectra are identical. The divergence is instead the
unbounded affinity of a reverse hidden edge whose rate tends to zero. A warranted
hidden affinity/rate-floor bound would be a genuinely new premise, not data
acquired from these observations. No universal entropy upper bound is inferable.

The script verifies exact symbolic similarity, row sums, positivity and the
rational r=1/10 affinity; 127 finite survival words agree within 4.44e-16.
The all-waveform proof is the algebra above, not the finite check.

## 6. The even simpler repeated-hazard failure

If D=cI, then for every waveform x(t),

    h=exp[-c integral x(t)dt] p exp(Kt)1
     =exp[-c integral x(t)dt].

All K are invisible. Uniform entrance and a three-state hidden directed cycle
with clockwise u, counterclockwise v gives sigma = [s/(s+c)](u-v)log(u/v).
Equilibrium u=v and arbitrarily dissipative u/v therefore have exactly the same
complete observed controlled law. This also makes plain why distinct diagonal
hazards were doing the real work in Section 2.

## 7. Astra connection, primary comparison, and selection decision

Exact current machinery was read, not just titles:
* N1298 PROOF.md: a distributed onsite nonlinear pulse references hidden physical
  coordinates, but one-port-only nonlinear actuation is gauge-equivariant and
  fails. The proposed distributed actuator is not physically acquired.
* N1248 QUANTITATIVE_CONTROL_FROM_STATIC_INFORMATION.md: controlled prediction
  consumes complete phase coordinates AND a warranted physical entropy upper
  bound. Neither bound nor sensing is obtained from a static fit alone.
* N1252 ACQUIRED_HIDDEN_RESPONSE_CANCELLATION.md: cross-operation reversible-loop
  Grams can synthesize useful memory-blind visible operations. Its objective is
  controlled observable laws, not recovering arbitrary dissipative hidden rates.
* N507 packet: passive reversal symmetry/CP tests do not universally establish
  hidden equilibrium; source status remains unreviewed and is not used as a
  theorem premise here. The new elementary CTMC algebra is independent.

The exact sources/paths and hashes are in SOURCES.json. This work does not
replace their claims, acceptance states, researchers or independent objectives.

Strong existing constructive alternatives are switched-system realization
(Petreczky--van Schuppen), positive likelihood/phase-type fitting and
entropy-minimization over compatible hidden models (Ehrich), and transition
waiting-time thermodynamic inference (van der Meer--Ertel--Seifert). They receive
the same control records. The Hankel mathematics here is not a new field.
The distinction between vertex-energy and symmetric-barrier perturbations is
standard and explicit in Aslyamov--Esposito and Owen--Gingrich--Horowitz.

No feasible material specimen with calibrated all-hazard-distinct common gating
has been acquired. A degree-one tunable aperture, the natural physically local
case, has the exact failure above. Model-order, Markov, detector and gate-law
qualification are not inferred from fitting the same records. Sparse gateways
usually leave repeated zero hazards, precisely where the inverse collapses.

The conclusion is not 'collect more data' or 'write a stronger theorem'. The
sustained foundational target would have to change physical information access
or target only a certifiable intervention-relative quotient. In that latter
direction N1252 is already the stronger source-bound opening, not a result to
rename. This branch therefore retains a useful construction and a decisive
negative result, but does NOT nominate itself as the global maximum.

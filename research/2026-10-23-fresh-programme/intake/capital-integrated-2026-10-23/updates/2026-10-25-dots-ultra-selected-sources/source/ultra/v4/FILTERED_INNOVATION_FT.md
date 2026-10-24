# Continually injected non-Gaussian classical noise: a circuit all-set bound

Owner: retained persistent/non-Gaussian bath Sol. 2026-10-25.

This is a new, separate construction after the initial-state results in
LOCAL_GAUSSIAN_ENVELOPE.md and SOFT_JOINT_ENERGY.md. It does not modify them.
The scientific question is whether continually arriving non-Gaussian fluctuations
with stable memory admit an all-set fault bound without replacing the initial
state of an ever-growing source by a Gaussian state at an exponential cost.

The answer below is affirmative for an exogenous CLASSICAL source, with a
precise conditional unitary circuit interface. It is not a theorem for an
interacting quantum bath, backaction, or an anharmonic quantum field. Its
probability tools, filter models, and fault-tolerance receiver are conventional;
the owned operation is their explicit composition and resource boundary.

## 1. Exact circuit and source contract

Fix finitely many physical circuit locations l=1,...,L, ordered in time
(simultaneous disjoint gates may be ordered arbitrarily). Each location has a
bounded-size data/ancilla support and an ideal unitary G_l. Include idle slots,
ancilla preparations, readout dilations, recovery controls, and reset dilations
among the locations if they are noisy. Measurement records and entropy sinks
can be retained as environment registers; later discarded registers are not
silently ideal correctors.

The classical source supplies a real angle theta_l to each fixed location.
For every realization the actual full operation is a unitary U_l(theta_l), on
that location and its declared dilation registers, with

    ||U_l(theta_l)-G_l|| <= min(2, |theta_l|).                 (1)

The full source law is independent of the unknown logical/reference input.
It can have arbitrarily long classical temporal correlations. It is not
changed by the quantum device. The theorem applies to this exogenous law,
not to an inferred classical description of a backacting quantum bath.

A sufficient physical gate model for (1) is a finite slot with angular-frequency
Hamiltonian K_l(t)=K_l,ideal(t)+theta_l f_l(t) S_l(t), where S_l is Hermitian,
||S_l(t)||<=1, and integral_slot |f_l(t)|dt<=1. Duhamel's identity gives (1)
even when the ideal control and the error operator do not commute. Equivalently,
U_l=e^{-i theta_l P_l}G_l with ||P_l||<=1 is an exact special case. A generic
time-varying process is not reduced to one integrated angle by this statement.
One must derive this sufficient model or independently establish (1).

Angles theta_l and the constants below are dimensionless. If a classical
angular-frequency offset xi_l is constant over a slot of duration t0, then
theta_l=t0 xi_l. No missing factor of hbar occurs: K=H/hbar.

The slot schedule and the source-to-slot weights are fixed in advance.
Classical feedforward is allowed through a fixed-slot coherent dilation only
when (1) and the same source law hold uniformly over its control branches.
Changing the sampling times/filter weights using observations of the source
requires a new, policy-uniform joint bound. An unconditional bound for fixed
times does not supply such an adaptive guarantee. Conditioning on a future
syndrome or postselection is not included.

## 2. Exact full marked-path factorization

Set F_l(theta_l)=U_l(theta_l)-G_l and expand the full circuit into G_l+F_l.
For a specified set F of r marked locations, sum ALL fault paths that have a
factor F_l at every location in F, allowing either factor at every other
location. Multilinearity makes this sum exactly

    A_F(theta) = V_L(theta) ... V_1(theta),
    V_l = F_l(theta_l) if l in F, and U_l(theta_l) otherwise. (2)

Thus all unmarked noisy operations remain present and unitary. In particular,
there is no omission of error evolution between the marked slots. Equation
(1), submultiplicativity, and unitarity imply

    ||A_F(theta)|| <= product_{l in F} min(2,|theta_l|)
                   <= product_{l in F} |theta_l|.           (3)

This exact discrete circuit identity, rather than a Gaussian bath expansion,
is the key interface. No Pauli twirl or observed error label is used.

Purify the entire classical source into an orthogonal environment label.
For any normalized logical/reference input, the squared norm of the full
marked bad vector is bounded by

    ||Psi_bad(F)||^2 <= E product_{l in F} theta_l^2.         (4)

The labels need not be independent across slots. Equation (4) is a coherent
fault-path statement, not a claim that individual faults are independent
Bernoulli events or physically observed Kraus outcomes.

## 3. A joint sub-Gaussian hypothesis and its all-set consequence

For every finite marked set F let theta_F be centered and suppose a positive
semidefinite matrix K_F satisfies, for every real vector u,

    E exp(u^T theta_F) <= exp(u^T K_F u/2),
    ||K_F|| <= R,              Tr K_F <= r V.              (5)

R,V are uniform over the complete circuit family, its duration, its size, and
the choice of F. They have units angle squared. A covariance bound by itself
does not establish (5). The trace and norm controls have different roles:
the latter pays for coherent memory/shared fluctuations among many slots.

Theorem. Under (1) and (5), for every marked set F,

    ||Psi_bad(F)|| <= epsilon_cl^r,
    epsilon_cl^2 = 2(R+V)/sqrt(e).                          (6)

Proof. For t>=0 and 2tR<1, introduce an independent standard Gaussian vector
z only as a mathematical integration device. Tonelli and (5) give

    E exp(t ||theta_F||^2)
      = E_z E_theta exp(sqrt(2t) z^T theta_F)
      <= E_z exp(t z^T K_F z)
      = det(I-2t K_F)^(-1/2)
      <= exp(t r V/(1-2tR)).                              (7)

The last inequality follows by diagonalizing K_F and using
-log(1-x)<=x/(1-x_max) for 0<=x<=x_max<1.
For x>=0, x^r<= [r/(e t)]^r exp(t x); also AM-GM gives
product theta_l^2 <= (||theta_F||^2/r)^r. If V>0 take
t=1/[2(R+V)]; (7) is at most exp(r/2). Therefore

    E product theta_l^2 <= [2(R+V)/sqrt(e)]^r.              (8)

If V=0, (5) forces every theta_l=0 almost surely and the result is direct.
Combining (4) and (8) proves (6). The Gaussian z in (7) is not a physical
Gaussian bath and no Wick rule for the physical noise has been invoked.

A conventional local-coherent/non-Markovian circuit threshold theorem can
receive (6), provided epsilon_cl is below its specified threshold and its
locality, fresh-ancilla, complete-circuit, and good-gadget hypotheses hold.
This note supplies no better decoder, threshold value, overhead, or native
syndrome hardware than that receiver. A source or control error absent from
the declared locations remains outside the theorem.

## 4. Stable filtering produces the required joint bound

Let eta_j, j in the integers, be independent centered innovations satisfying

    E exp(u eta_j) <= exp(sigma^2 u^2/2) for every real u.   (9)

For a real causal filter h=(h_0,h_1,...) with sum |h_j|<infinity define

    theta_t = sum_{j>=0} h_j eta_{t-j}.                    (10)

The infinite sum exists in L2; it can be obtained as the limit of finite
sums. For any finitely supported vector u on slot indices, independence
first for finite sums, then Fatou with the uniform bounds, gives

    E exp(sum_t u_t theta_t)
        <= exp[(sigma^2/2) ||H^T u||_2^2],                 (11)

where H is convolution by h. The same holds for all finite subsets by
zero-extending u. Young's convolution inequality and the diagonal entries
of HH^T give the valid uniform parameters

    R = sigma^2 ||h||_1^2,
    V = sigma^2 ||h||_2^2.                                (12)

This also extends to a spatial/temporal convolution kernel whose absolute
sum over all offsets is finite. That sum, not just a single-channel temporal
fit, must then be used in R. One scalar source broadcast to an increasing
number of sites need not have size-uniform R.

The bi-infinite stationary construction in (10) is a mathematical source
premise. A finite-time device may start from a specified filter state; its
initial transient must be included as an additional source or removed with a
paid equilibration/error bound. Source memory is not initialized for free.

For the stationary AR(1) process theta_t=a theta_{t-1}+eta_t, |a|<1,

    R = sigma^2/(1-|a|)^2,
    V = sigma^2/(1-a^2).                                  (13)

For 0<=a<1 this makes

    epsilon_cl^2 = 4 sigma^2/[sqrt(e)(1-a)^2(1+a)]
                 = 4 V/[sqrt(e)(1-a)].                   (14)

In physical units sigma=t0 sigma_xi if the innovation is an angular-frequency
offset held fixed over a slot. Interpreting a=exp(-Delta/tau_c) requires the
actual sampling interval Delta and the stated AR(1) source model. Slow memory
has a real price: the bound diverges as a approaches 1 at fixed V. An exactly
quasistatic common angle has ||K_F|| growing with r and is not certified by
uniform (5), despite its finite one-slot variance.

## 5. An explicit unbounded non-Gaussian input class

Take independent symmetric innovations with density

    p(eta) = c exp[-eta^2/(2 sigma^2) - u eta^4], u>0.      (15)

For a centered Gaussian G of variance sigma^2, the likelihood ratio between
the |eta| and |G| densities is a decreasing function of their argument. Its
single crossing (the densities integrate to the same value) implies
P(|eta|>x)<=P(|G|>x) for every x>=0. Since cosh(t x) is increasing in x>=0,
symmetry yields E exp(t eta)=E cosh(t|eta|)<=E cosh(t|G|)=
exp(sigma^2 t^2/2). Hence (9) holds although eta is unbounded and non-Gaussian.
With (10), new non-Gaussian noise keeps entering at positive rate. The proof
has no global initial-state comparison constant growing with that rate/time.

A classical coordinate with energy k x^2/2+gamma x^4, gamma>0, at temperature T
has (15) for eta=c_x x, with sigma^2=c_x^2 k_B T/k and
u=gamma/(k_B T c_x^4). This only identifies a one-sample equilibrium law.
It does NOT establish independent refreshes or an AR source from a measured
temperature. The physical relaxation, sample independence, bandwidth, entropy
flow, coupling to the qubit, and switching/control errors remain required
inputs for an actual source/device.

For a deliberately injected numerical source, a standard Gaussian proposal
accepted with probability exp(-u G^4) samples (15). Its expected proposals per
accepted innovation are 1/E exp(-u G^4), finite at fixed u,sigma. A finite
circuit requires a fresh source draw and a filter update per clock step.
This is not an exact finite-bit sampler of an arbitrary real number. Finite
precision, finite tails/overflow and random-bit generation need their own
error and entropy budgets. An empirical PSD or a finite noise record cannot
certify the all-real-u inequality (9) or the all-subset assertion (5).

## 6. Control, initialization, acquisition, and failure boundaries

1. This is a noise-tolerance theorem, not a cancellation/control protocol.
   The strongest matched standard QEC scheme may use the same knowledge and
   filter model. No reset/measurement of each noise output is required by this
   theorem, but actual ancilla resets and syndrome acquisition are still paid.
2. A finite-bit injection apparatus, calibration circuit, clock, amplifier,
   filter, control electronics, entropy sink, and readout add physical noise.
   To make a complete computer claim, bound their errors in the same receiver
   model. The mathematical source law does not acquire these operations.
3. A deterministic locationwise unitary implementation error delta_l can be
   included by another local fault expansion. If it is bounded uniformly by
   delta, all mixed selected tails obey the same triangle/binomial argument,
   giving a conservative combined amplitude strength epsilon_cl+delta. This
   applies only when the bounded perturbation is genuinely local and the
   classical law and original (1) remain valid for the comparison circuit.
   A global probability of source overflow gives an additive failure floor;
   it is not silently converted to an all-set local error strength.
4. Independent fresh bits are a source resource, not a consequence of using
   a deterministic PRNG. Likewise stationary classical noise can be simulated
   efficiently while still being an unvalidated description of a device.
5. Quantum backaction, noncommuting source operators, adaptive resampling
   correlated with the quantum history, anharmonic bath evolution, and a
   generic nonunitary SchWARMA process are not covered by (2)-(4).
6. A persistent rare shared high-amplitude branch can obey small marginal
   moments while violating uniform (5). This is why the former failed
   marginal-energy-to-all-set argument is not resurrected here.

## 7. Equally informed conventional comparison and actual contribution

The probability step is standard sub-Gaussian quadratic-form analysis; the
Gaussian-auxiliary method is explicit in Hsu, Kakade and Zhang, Theorem 1,
Remark 2 and its proof. We derived the product-moment constant (8) directly
above rather than claiming a new concentration theorem.

Schultz, Quiroz, Titum and Clader's SchWARMA already models correlated quantum
circuit errors using classical ARMA signals, permits non-Gaussian innovations,
and gives precisely random Z rotations in Eq. (9). It is the direct incumbent
for the architecture/model, not merely a distant citation. The inspected paper
develops simulation/characterization and examples of QEC; it does not supply
the explicit general joint-sub-Gaussian all-set bound (6) as stated here.
This is not a priority determination.

Ng-Preskill supplies a stronger genuinely quantum-bath theorem when its free
Gaussian/linear-field premises apply. It does not literally require the
classical exogeneity assumption used here. Conversely, the unbounded quartic
innovation in (15) has no finite worst-case angle norm and is not itself a
Gaussian field, so neither a bounded-noise-strength premise nor Wick closure
alone states this classical-source result. The present bridge is an ordinary
fault-path factorization plus conventional concentration. It establishes a
useful complete noise-model-to-receiver interface, not an exclusive computing
capability, practical advantage, new QEC architecture, or device validation.

Primary sources actually opened/read in this phase:

- Hsu, Kakade, Zhang, *A tail inequality for quadratic forms of subgaussian
  random vectors*, Theorem 1 / Remark 2 / proof,
  https://arxiv.org/html/1110.2842 .
- Schultz et al., *SchWARMA: A model-based approach for time-correlated noise
  in quantum circuits*, PR Research 3, 033229 (2021), Secs. I-III, Eq. (5) and
  Eq. (9); https://arxiv.org/pdf/2010.04580 .
- Ng and Preskill, *Fault-tolerant quantum computation versus Gaussian noise*,
  PRA 79, 032318 (2009), Eq. (9), Eq. (27), Sec. VI,
  https://arxiv.org/html/0810.4953 .

No external novelty or physical-acceptance status is claimed. The already
reviewed initial-state comparison theorem and this exogenous classical-source
theorem solve different contracts; neither covers continued non-Gaussian
quantum injection with feedback onto a persistent memory.

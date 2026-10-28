# A decisive failure of energy-only entropy truncation

28 October 2026. Ordinary continuation derivation; no historical novelty claim.
This next test prevents a false transfer from the finite-excursion SLD cutoff
to unrestricted Umegaki relative-entropy order.

## Fixed energy, vanishing omitted weight, fixed entropy defect

Take A=C^2 and reference levels |0>,|1>,|L> with energies0,1,L. Fix rational
0<s<1 and compare strictly positive rational POVMs

    P_+ = P_- = I/2,
    Q_+ = (I+sX)/2, Q_- = (I-sX)/2,

where X is Pauli X. Fix E>=1,L>2E,p=2E/(L+1), and define

    alpha = |0_A,1_R><0_A,1_R|,
    Phi = (|0_A,1_R>+|1_A,L_R>)/sqrt(2),
    beta = (1-p)(I_A/2) tensor |0><0| + p |Phi><Phi|.

Alpha has reference energy1 and beta has reference energyE. The discarded
reference probability is p/2=E/(L+1), tending to zero; alpha has none.

For the constant-output POVM,

    D(P_R(alpha)||P_R(beta)) = log(2/p).

The two Q beta output blocks on reference span{|1>,|L>} equal(p/2)Q_+^T and
(p/2)Q_-^T. Alpha gives each outcome probability1/2 and reference vector|1>.
Since

    <0|log Q_+|0> = <0|log Q_-|0>
       = -log2 + (1/2)log(1-s^2),

we obtain

    D(Q_R(alpha)||Q_R(beta))
       = log(2/p) - (1/2)log(1-s^2).

The two-channel entropy defect is therefore the fixed positive constant

    Delta_D = -(1/2)log(1-s^2).

Now reset level L to ground0, retaining all lower reference levels and the
physical A marginal, as in Gamma_Lambda in FINITE_EXCURSION_SLD.md. At reference
level1 the new beta block is(p/2)|0_A><0_A|. Both Q and P relative entropies then
equal log(2/p), so the defect is0.

For s=1/2, the original defect is approximately0.143841, independent of the
discarded tail. This analytically refutes a uniform vanishing-tail estimate
for unrestricted entropy defect based only on the two mean-energy bounds.

It does not itself establish energy-constrained fixed-accuracy undecidability:
the witness uses three reference levels and is explicit. It kills this
truncation mechanism. A denominator sector of vanishing beta weight remains
fully occupied by alpha, retaining finite conditional information.

## A sufficient replacement: paid preparation-ratio control

Suppose both state pairs obey the same two-sided operator ratio condition

    C^-1 beta <= alpha <= C beta,
    C^-1 beta' <= alpha' <= C beta',        C>=1.

Then

    |D(alpha||beta)-D(alpha'||beta')|
       <= log(C)||alpha-alpha'||_1
          +(C-C^-1)||beta-beta'||_1/2.       (1)

Proof: linearly interpolate both states. The ratio bounds persist. On a common
faithful support the derivative is

    dD/dt = Tr[(alpha'-alpha)(log alpha_t-log beta_t)]
       -Tr[(beta'-beta) T_{beta_t}(alpha_t)],

where T_B is the positive Frechet derivative of log, satisfying T_B(B)=I.
Operator monotonicity gives -log(C)I<=log alpha_t-log beta_t<=log(C)I, and
positivity gives C^-1I<=T_beta(alpha)<=CI. Since Tr(beta'-beta)=0, subtract
(C+C^-1)I/2 from that coefficient. Trace Holder and integration prove(1).
Singular common supports follow by common regularization and a limit; the
ratio bounds prevent divergent relative entropy.

Channels and reference compression preserve the ratio condition. For two
channels and endpoint trace errors at mostdelta,

    |Delta_D(original)-Delta_D(compressed)|
       <=[2log C+C-C^-1]delta.

Combining delta<=2sqrt(E/Lambda)+E/Lambda gives an effective cutoff for this
restricted entropy problem. The counterexample violates the ratio condition.

One physical way to enforce a ratio is to randomize the hypotheses:
alpha_t=(1-t)alpha+t beta and beta_t=t alpha+(1-t)beta for0<t<=1/2. Then
C=(1-t)/t. This changes the experiment and can discard its useful contrast;
it is not a free repair of unrestricted entropy order.

## Scope

The positive bound combines standard operator monotonicity, the logarithm's
Frechet derivative and energy truncation. It is a sufficient resource contract,
not a new information divergence or a practical advantage theorem. The
negative result is the load-bearing lesson: derivative-score control and mean
energy control do not acquire denominator-relative preparation control.

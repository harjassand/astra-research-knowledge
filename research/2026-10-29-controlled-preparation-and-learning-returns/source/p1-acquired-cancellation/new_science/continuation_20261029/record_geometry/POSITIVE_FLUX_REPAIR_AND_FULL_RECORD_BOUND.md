# Positive flux repair and complete adaptive-record bounds

29 October 2026. Complementary construction within continuing Astra P1. This is
an ordinary mathematical candidate, not an independent audit or a physical
experiment. Lumpability, transport repair and Markov comparison are established
machinery; the candidate bridge is the acquired-defect receiving connection.

## 1. Actual interface and positive projection

Let (X,pi) be standard Borel with a finite noninvasive readout partition A_a,
a=1,...,k, of positive masses. Set P=E_pi[.|Y]. This P is POSITIVE, unlike a
generic signed predictive feature projection. Each actual fixed call T_j is
reversible for mu_j(dx)=w_j(Y(x))pi(dx)/pi(w_j), where the positive weights are
known and bounded. All mu_j have the same conditional hidden laws
pi_a=pi(.|A_a). Their visible equilibria and kinetics may differ.

The actual kernel/switching interface, complete microscopic reversibility,
baseline calibration preparation and known visible weights remain premises.
No hidden dimension, hidden mixing or generator bound is imposed. The theorem
only covers specified calls and endpoint records.

Write in H_j=L2(mu_j):

    R_j=(I-P)T_jP,  ||R_j||<=epsilon_j,
    m_j(a)=mu_j(A_a),
    c_j(a,b)=integral T_j 1_b d pi_a.

C_j=(c_j(a,b)) is a genuine stochastic matrix. With actual label features,

    G_j=diag(m_j),
    K_j(a,b)=<1_a,T_j1_b>_mu_j,
    D_j(b,c)=<1_b,T_j^2 1_c>_mu_j,
    D_j-K_j^T G_j^-1 K_j=<R_j1_b,R_j1_c>_mu_j.

Thus C_j=G_j^-1 K_j and epsilon_j are acquired by the predecessor one- and
two-call chronological Gram experiments. Baseline pi preparation followed by
known initial weight w_j(Y_0)/pi(w_j) suffices; no fresh preparation of mu_j or
microscopic copy is used. Independent actual calls define T_j^2. Finite data
require simultaneous confidence intervals and genuine positive mass bounds.
An empirical zero is not exact closure.

## 2. Nonnegative marginal repair

If a finite nonnegative measure F on A x B has mass M and marginals alpha,beta,
and target marginals alpha',beta' also have mass M, there exists F' with those
target marginals and

    ||F'-F||_1<=||alpha'-alpha||_1+||beta'-beta||_1.       (L)

Here ||.||_1 is total mass variation, twice TV for equal-mass probability laws.
Proof: define alpha wedge alpha' using the densities of alpha and alpha'
relative to the dominating measure alpha+alpha', taking their pointwise
minimum. Trim F in its first coordinate by d(alpha wedge alpha')/dalpha,
removing t1=||alpha-alpha'||_1/2. This does not assume alpha' is absolutely
continuous with respect to alpha. Apply the same common-submeasure trimming
to the remaining second marginal and beta', removing
t2<=||beta-beta'||_1/2. Both remaining marginals lie below their targets.
If t=t1+t2>0, add the product of their deficits divided by t. If t=0, add
nothing. Removed and added masses are each t, giving(L).
If F and the target marginals are symmetric, symmetrize F'; the distance does
not increase. Standard Borel disintegrations suffice. This repair need not
preserve microscopic support or conserved sectors: it is a comparison object.

## 3. A reversible exactly lumpable comparator

For one operation form its symmetric equilibrium flux
F_j(dx,dy)=mu_j(dx)T_j(x,dy). On block A_a x A_b its mass is
M_ab=m_j(a)c_j(a,b)=m_j(b)c_j(b,a). Prescribe marginals

    alpha'_ab=c_j(a,b) mu_j restricted to A_a,
    beta'_ab=c_j(b,a) mu_j restricted to A_b.

Apply(L), use the transpose repair on paired blocks, and symmetrize diagonal
blocks. The assembled flux is symmetric and has marginal mu_j. Disintegrate
to obtain a genuine reversible kernel T_j^0 with

    T_j^0(x,A_b)=c_j(a,b) for x in A_a, mu_j-a.e.         (1)

It is strongly lumpable, and starting from pi_a then conditioning on next
label b leaves pi_b. The last assertion follows from detailed balance and(1).
Because all mu_j have the SAME pi_a, any history-selected sequence of repaired
kernels retains X_t|visible history ~pi_(Y_t), provided it starts from a mixture
of pi_a. No commutation of kernels is needed.

Write r_j,b=R_j1_b and d_j,ab=integral_(A_a)|r_j,b|dmu_j. For the chosen repair,

    delta_j,a=integral TV(T_j(x,.),T_j^0(x,.)) d pi_a(x)
       <=sum_b(d_j,ab+d_j,ba)/(2m_j(a)).                 (2)

A bound using only the acquired operator norm is

    delta_j,a<=epsilon_j [sqrt(k-1)+sqrt(1-m_j(a))]
                            /(2sqrt(m_j(a))).          (3)

Indeed R_j1=0 gives sum_b||r_j,b||_2^2
<=epsilon_j^2(1-sum_b m_j(b)^2). Hence sum_b d_j,ab
<=sqrt(k m_j(a))epsilon_j sqrt(1-sum_bm_j(b)^2)
<=epsilon_j sqrt((k-1)m_j(a)). Also sum_b d_j,ba
=||r_j,a||_1<=epsilon_j sqrt(m_j(a)(1-m_j(a))). Insert in(2).
Let Delta be max_j,a of any valid bounds(2)/(3), capped at1. Small cell masses
are a real conditioning cost. Local residual Grams can improve(2).

## 4. The complete record, including a mathematical copy of X_0

Fix any causal policy selecting operations from the entire visible history
and independent keys. Let L_x be its actual n-call endpoint-record law from x,
and L_a^0 its genuine k-state C_j record law beginning with label a. A fresh
initial read is allowed. The repaired process has law L_(Y(x))^0 from every x.

Start the true and repaired processes with the SAME mu_ref, any positive
visible reweighting of pi. Standard path telescoping, with repaired prefixes
and true suffixes, gives

    TV(Law_true(X_0,record),Law_repaired(X_0,record))
          <=min(1,nDelta),                              (4)

because under every repaired prefix the hidden state conditional on the
public history is pi_(current label). The averaged one-step discrepancy is
therefore <=Delta. The common suffix is a causal channel and contracts TV.
The mathematical inclusion of X_0 does not change this average; X_0 is not
measured and the policy is not allowed to use it. Consequently

    integral TV(L_x,L_(Y(x))^0)dmu_ref(x)<=min(1,nDelta).  (5)

This is a full adaptive transcript claim, not a final marginal claim. It is
uniform over policies by construction; no count of policies is used.

## 5. A receiving bound without exponential branching

For any event A set f_A(x)=L_x(A), g_A(x)=L_(Y(x))^0(A). Then g_A lies in V,
both functions lie in[0,1], and orthogonal projection plus(5) gives

    ||(I-P)f_A||_2^2<=||f_A-g_A||_2^2
                  <=integral|f_A-g_A|dmu_ref<=nDelta.

Together with the usual centered-event cap,

    eta_n<=min(1/2,sqrt(nDelta)).                        (6)

A fresh initial observation is INCLUDED; there is no additional sqrt(k)
factor. This improves horizon dependence only for the POSITIVE partition
projection, at the expense of a square root in epsilon and cell-mass factors.
It does not replace the generic signed-feature theorem at unchanged premises.

Insert(6) into FINITE_ERROR_PREDICTIVE_PREPARATION.md with its actual W,
kappa,e,m and genuine joint initial bound K_joint:

    TV(actual prepared service, actual reference service)
     <=min{1,sqrt(K_joint^2-1)[b_m/2+min(1/2,sqrt(nDelta))]},
    b_m=kappa^m+e(1-kappa^m)/(1-kappa).                  (7)

The reference in(7) is the ACTUAL physical source initialized at mu_ref.
The artificial repair was only used in the proof. It is never executed.
The preparation floor and warranted initial-information condition remain.

## 6. A positive model and conventional control

For actual initial density q relative to mu_ref and coarse initial label law
rho(Y), equation(5) gives

    TV(actual record, coarse C_j record)
       <=min{1,B nDelta,K sqrt(nDelta)},                (8)

using whichever actual bound q<=B or ||q||_2<=K is warranted. The second
bound follows from Cauchy--Schwarz and TV(L_x,L_Y^0)^2<=TV(L_x,L_Y^0).
For the entire old record Z with E_Z||q_Z||_2^2<=K_joint^2, use the same
Z-selected policy and coarse initial Y|Z distribution; the joint bound is
min(1,K_joint sqrt(nDelta)). An unconditional density ceiling alone does not
supply the B bound for arbitrary Z-selected policies.

A fitted positive coarse matrix with per-row TV error zeta adds n zeta.
A uniform record bound xi gives at most 2xi+planning_slack regret for any
[0,1] full-record objective optimized by ordinary finite-state methods. This
is standard control transfer, not a claim to invent dynamic programming.

## 7. Limits and close predecessors

The finite partition condition is substantial. A generic future-feature span
is not a lattice or positive conditional expectation. A separately warranted
finite measurable refinement is possible, but finite data do not prove exact
hidden sharp indicators. No favorable partition, small leakage, affordable
calibration or useful actuation is guaranteed. A naive bounded-moment estimate
of epsilon^2 can require O(epsilon^-4) samples. Asking eta accuracy over n
stages via(6) can therefore give O(n^4 eta^-8) scaling before weights,
conditioning and constants. Polynomial need not mean practical.

Hidden spaces can be infinite, continuous, nonmixing or have frozen sectors.
Transport repair can mix those sectors but is not physically claimed. The
smoothing obstruction survives because actual residuals remain nonzero. The
fixed-call statement excludes unobserved between-call paths, new durations,
clock records and unmodeled apparatus memory. Actual preparation still uses
only the acquired physical menu and actual adjoints.

Relevant primary work (priority not settled):

* P. Buchholz, Exact and ordinary lumpability in finite Markov chains,
  Journal of Applied Probability31(1),59--75(1994),
  https://doi.org/10.2307/3215235 . Includes near lumpability and aggregation
  bounds; lumpability itself is established machinery.
* G. Bian and A. Abate, On the Relationship between Bisimulation and Trace
  Equivalence in an Approximate Probabilistic Context(2017),
  https://arxiv.org/abs/1701.04547 . Full finite-horizon trace TV from
  pointwise approximate bisimulation; our input is an equilibrium L2 defect.
* Formal Error Bounds for the State Space Reduction of Markov Chains,
  https://arxiv.org/abs/2403.07618 , published Performance Evaluation167,
  102464(2025), https://doi.org/10.1016/j.peva.2024.102464 . Reduced transient
  error and relationships to exact/ordinary lumpability.
* J. Tian and D. Kannan, Lumpability and Commutativity of Markov Processes,
  https://people.nmsu.edu/jtian/publications/2006-3.pdf . Classical constant
  block-row-sum criterion explicitly stated.

The possible addition is the physical acquired-defect/completeness/positive
receiving connection. The transport lemma, Markov criterion, telescoping and
finite-state optimizer are not claimed new. This note needs focused review.

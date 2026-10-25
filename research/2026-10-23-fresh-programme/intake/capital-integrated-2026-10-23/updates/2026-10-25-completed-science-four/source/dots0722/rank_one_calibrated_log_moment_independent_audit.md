# Independent hostile audit: complete rank-one-lower coherence budget

2026-10-25. Audits `rank_one_calibrated_log_moment_complete_budget.md` and the receiving interface `rank_one_spectral_filter_scalar_upper_interface.md`. The scalar proof, arbitrary-rank-noise extension, zero atom, two-source quantum transfer, strictness, and receiving scope were checked independently.

## Verdict

**PASS.** For every finite positive block B=[[a,z],[z*,x]] with rank(x)<=1 and every PSD lower noise b,

    2C([[a,-z/2],[-z*/2,x/4+3b/8]])-C(B)
       <= (1/2)log(32/27) Tr(x-3b/2)_+.

The proof retains arbitrary finite upper dimension and every upper Schur remainder. It does not require b to be rank one, x and b to commute, a pure graph input, a finite-atom capacity optimizer, or an optimization sweep.

The constant is sharp on the orthogonal/noiseless face. For a fixed normalized lower pair with 0<q<1, the stronger pair-dependent strict capacity gap follows as stated. The proof does **not** establish the coherence budget for rank(x)>=2 or the full WH3 target.

The zero-atom extension should be stated directly: the two-point proof is valid with u=0 whenever the logarithmic shift R>0. The author has incorporated that clarification; no calibration-preserving approximation is necessary.

## 1. The two-point scalar calculation

For 0<=u<1<v, the unique probability law satisfying E[1/(1+T)]=1/2 has

    p=(v-1)(1+u)/(2(v-u)),
    1-p=(1-u)(1+v)/(2(v-u)),
    m=ET=(1+u+(1-u)v)/2.

These weights are positive, sum to one, and satisfy the calibration exactly. Also m-1=(1-u)(v-1)/2>=0.

Let H be the right side minus left side of

    2E log(R+T)<=2log(R+1)+log[(R+4m)/(R+4)].

For fixed u and R>0, H(1)=0, and differentiation independently gives

    H'(v)/(1-u)=2/(R+4m)
       +(1+u)log[(R+v)/(R+u)]/(v-u)^2
       -(1+v)/[(R+v)(v-u)].

The coefficient multiplying the logarithm is positive. Substituting log z>=2(z-1)/(z+1) therefore gives a lower, not upper, bound. Its numerator is exactly

    N=2R^2+R(v-3)+2
       +u[(4v-2)R+2(v^2-v+1)].

Its useful decomposition is

    N=2(R-1/2)^2+3/2+R(v-1)
       +u[(4v-2)R+2(v^2-v+1)]>0.

All denominators are positive. Hence H'(v)>0 and H(v)>0 for every nontrivial pair. This holds directly for u=0 when R>0. For R=0 and u>0 the same calculation also works.

There is no mistaken sign from differentiating the pair weights or from the logarithmic lower bound. Seven independent exact symbolic checks, including u=0, passed.

## 2. The flux decomposition is a genuine probability mixture

For an arbitrary calibrated law on T>=0, separate its restrictions below and above one. Put

    d(u)=(1-u)/(1+u),     e(v)=(v-1)/(1+v).

Calibration gives the common flux L=integral d dmu_-=integral e dmu_+. If L=0, the entire law is the point mass at one. Otherwise define the pair-mixing measure

    sigma(du,dv)=[d(u)+e(v)]mu_-(du)mu_+(dv)/L.

Within each pair choose probabilities e/(d+e) and d/(d+e). The lower marginal is exactly mu_- because integral e dmu_+=L; the upper marginal is similarly mu_+. The total pair mass is mu_-(R)+mu_+(R), and the original atom at one completes it to a probability mixture.

The component means average to the original finite mean m. Every component mean is at least one. Thus log(R+4m_component) is bounded below and integrable above, and concavity of log may be applied to the full component mixture, including the atom at one. This proves the stated inequality for every finite-mean calibrated law.

For R>0, all logarithmic expectations are finite: the lower bound is log R and the positive part is controlled by the finite mean. Fubini and Jensen therefore introduce no undefined signed integrals. The R=0 statement follows by decreasing R to zero after subtracting the integrable upper bound log(1+T). An atom at zero then simply gives a negative-infinite logarithmic expectation.

For a nonconstant calibrated law, L>0 and every component pair has strictly positive H. Integrating preserves strictness for every R>0. Jensen adds nonnegative slack; it cannot cancel that strict pairwise gap.

## 3. Entropy integration and all scalar factors

Let S>=0 satisfy ES=1/4 and E[q/(q+4S)]=1/2 with q>0. Set T=4S/q and R=4r/q. Then ET=1/q and the logarithmic inequality becomes exactly

    E log(r+S)<=log(r+q/4)+(1/2)log[(r+1)/(r+q)].

All factors of four and q cancel correctly. For h(r,s)=(r+s)log(r+s)-rlog r-slog s, define

    U_r=2E h(r,S)-h(r,1),
    D(r)=2h(r,q/4)-h(r,q)-U_r.

Differentiating for r>0 gives precisely twice the preceding logarithmic gap, so D'(r)>=0. Differentiation is dominated locally by log(1+S/r)<=S/r. No S log S moment is needed.

At r=0, every h term vanishes continuously. In particular 0<=E h(r,S)<=h(r,ES) by concavity in S, so D(0)=0. Therefore

    U_r<=2h(r,q/4)-h(r,q)=q f0(r/q)<=kq.

The last step uses the already verified scalar maximum of f0(a)=2h(a,1/4)-h(a,1), uniquely at a=1/8, with k=(1/2)log(32/27). This scalar conclusion includes S=0 atoms and all r>=0.

## 4. Exact spectral law for arbitrary PSD noise

Normalize x=uu*, ||u||=1, and put y=x/4+3b/8. Since y>=x/4, u belongs to the support of y. The rank-one order criterion on that support gives

    (1/4)<u|y^+|u><=1.

For each positive eigenvalue s_i of y define pi_i=|<u,e_i>|^2/(4s_i). These weights sum to at most one. Add the missing probability at s=0. This is a mathematical probability completion, not a claim that a new physical noise eigenmode was prepared.

The completed probability law obeys

    ES=sum pi_i s_i=1/4,
    E[S/(S+t)]=(1/4)<u|(y+tI)^(-1)|u>.

Thus it exactly represents the actual output resolvent kernel, including arbitrary noise rank. The zero atom contributes zero to this kernel.

Now H=2x-4y=x-3b/2 is a rank-one positive perturbation of a negative semidefinite matrix, so it has at most one strictly positive eigenvalue. If q=Tr H_+>0, then q is that eigenvalue, 0<q<=1, and the rank-one secular equation is

    1=2<u|(qI+4y)^(-1)|u>.

This follows directly from the positive eigenvector equation; qI+4y is invertible even if y is singular. Including the zero probability atom gives

    E[q/(q+4S)]
       =1-sum_i pi_i 4s_i/(q+4s_i)
       =1-<u|(qI+4y)^(-1)|u>=1/2.

Omitting the missing atom would break this identity. Its explicit inclusion is correct and load-bearing.

## 5. Spectral Jensen has the correct direction, including s=0

For the actual input B, positivity and rank-one x give its exact scalar Schur resolvent g(t), with 0<=g<=1. The function -log(1-gh) is convex in h. Therefore the actual coherence-difference integrand is at most the average obtained by replacing its output kernel by S/(S+t).

Each resulting integral is exactly

    2C(D_s B D_s)-C(B),     D_s=diag(I,sqrt(s)I).

Consequently

    F_actual(B)<=2E C(D_S B D_S)-C(B).

For s=0 the filtered coherence is zero, while its weighted term still contributes -C(B) inside the averaged difference. Because the completed weights sum to one, the input coherence coefficient remains exactly -1. No missing-mass term has been lost.

Values s>1 are permissible positive congruences in this mathematical identity. They are not asserted to be trace-nonincreasing physical filters or free postselection operations.

## 6. The quantum receiving expression is exactly balanced

Factor B=Q Q* and split Q into its upper and lower row blocks Q_U,Q_L. On the common environmental space let

    A=Q_U*Q_U,     X=Q_L*Q_L.

Their nonzero spectra match those of a,x, while A+X matches B. In particular Tr X=Tr x=1. Filtering replaces X by sX, and hence

    C(D_s B D_s)=S(A)+S(sX)-S(A+sX).

The spectral-Jensen upper expression becomes

    Psi(A,X)=S(A)+2E S(SX)-S(X)-2E S(A+SX)+S(A+X).

Its source coefficients balance separately:

    A: 1-2+1=0,
    X: 2ES-1-2ES+1=0.

This explicitly includes the zero atom and requires no commutation or proportionality of A and X. The construction retains the original upper matrix and all its Schur slack.

### The accepted binary transfer applies with exactly these hypotheses

For faithful A,X, the testing curve Tr(A-tX)_+ has a positive second-derivative measure with mass Tr X and first moment Tr A. It reproduces the positive and negative trace of every real pencil in A,X. The relative-entropy integral then represents every balanced two-source entropy expression by its scalar counterpart. Applied here, the scalar integrand is precisely U_r.

I checked the external ingredient directly at the primary source: Frenkel's Theorem 6 states the relative-entropy formula for PSD matrices with unequal traces, including its trace correction. That correction and the reference logarithm cancel under the two balance identities above. Source: [Frenkel, arXiv:2208.12194v4, Theorem 6](https://arxiv.org/html/2208.12194).

Thus Psi(A,X)<=kq Tr X=kq. For singular environmental sources, apply the balanced inequality to A+epsilon I and X+epsilon I while keeping the spectral probabilities and q fixed, then take epsilon to zero. The scalar inequality is valid for every pair of nonnegative scalar source masses, so this regularization does not need to preserve rank(X). Finite-dimensional entropy continuity and Tr(X+epsilon I)->Tr X finish the transfer.

This is an abstract trace-entropy representation, not a common measurement, classical simulation, simultaneous diagonalization, or physical compression. No ternary scalar transfer is being used.

## 7. Zero positive part, homogeneity, and endpoint equality

If q=0, then 2x-4y<=0, so y>=x/2. Consequently the actual output kernel obeys h_y(t)<=1/(2+4t). This implies 2h_y(t)<=1/(1+t), and

    (1-h_y g)^2-[1-g/(1+t)]
       =g[1/(1+t)-2h_y]+h_y^2g^2>=0.

The exact difference integrand is nonpositive. Thus the bound is zero, attained by z=0. No limiting reciprocal moment at q=0 is needed.

For arbitrary nonzero rank-one x=w uu*, divide all input and noise blocks by w. Coherence and the trace positive part are homogeneous, so the normalized result rescales exactly. For x=0, positivity forces z=0 and the statement is trivial. The sign of the output off-diagonal is removed by a block unitary and does not affect coherence.

At q=1, a unit positive eigenvector of x-3b/2 with eigenvalue one must be u and must have zero b expectation. PSD b therefore satisfies bu=0. Orthogonal noise is decoupled, and the usual scalar pure graph with upper weight 1/8 attains k. This establishes sharpness for the full arbitrary-noise class.

## 8. Fixed-pair strictness and actual receiving scope

For 0<q<1 the completed finite spectral law cannot be constant: its mean would force S=1/4, and its reciprocal moment would then force q=1. The strict scalar logarithmic inequality gives D'(r)>0 and D(r)>0 for every r>0. Hence U_r<kq at every positive r, while U_0=0<kq.

The physical spectral law is finite. Thus U_r is continuous and

    U_r=(2ES-1)log r+O(1)=-(1/2)log r+O(1)

at infinity, also with a zero atom. Its supremum is attained at a finite r and is strictly below kq. Therefore the actual capacity has a strict pair-dependent gap. This argument does not need actual capacity attainment or a uniform gap over changing lower pairs.

Combining this coherence theorem with the accepted diagonal two-source budget and the exact deficit identity is valid when rank(x)<=1, b is arbitrary PSD, and c=alpha x+beta b with alpha,beta>=0. The diagonal contribution pays k Tr(x-3b/2)_+, and the coherence cost is no larger. This closes that stated full invariant-channel class, including c=0.

Neither arbitrary c outside that cone nor rank(x)>=2 is covered. No purification, pinching, or decomposition argument removing those restrictions has been established. The full WH3 problem therefore remains open.

## 9. Independent checks and costs

Companions: `rank_one_calibrated_log_moment_independent_audit.py` and `.json`.

Seven exact scalar identities passed. One predetermined 75-digit fixture used a three-dimensional full-rank noncommuting noise matrix and three upper spectral atoms with total Schur mass 11/20, so its upper Schur remainder is genuinely nonzero. It verified the completed spectral moments, spectral-Jensen direction, purification identity, and scalar comparison. The added zero-atom mass was approximately 0.18954248; moment errors were below 2.8e-76, and the purification identity error was below 1.3e-75. These are consistency checks, not premises of universality or interval-certified inequalities.

Recorded script cost: 0.314 seconds wall time, 0.452 seconds process user CPU, 0.048 seconds system CPU, maximum RSS 49,856 KiB. One primary-source web read checked the relative-entropy theorem. There was no optimization, parameter sweep, purchase, publication, or external outreach.

No counterexample or remaining gap in the rank-one-lower/arbitrary-PSD-noise proof was found.

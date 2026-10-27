# Entropy-only polar-erasure recovery for arbitrary coherent reset

Status: new consequence, pending independent receipt. Depends on the received arbitrary-pure-main VALUE proof's e2 clock, the earlier scalar-anchor endpoint comparison, and the received original positive-spectrum polar operation. No GLS comparison or mixed-main channel claim.

Let E(rho)=p V rho V*+q Tr(rho)tau, V:C3->R isometric, p+q=1, and Delta be the normalized original WH3 deficit. Assume source parameters known. There is an explicit received-system decoder with erased rejection whose complete instrument differs from (p id,q erasure) in diamond norm by at most

min{2p,45 sqrt[5(p+3q) Delta]} <= min{2p,45 sqrt(15 Delta)}.       (1)

The decoder is the positive-spectrum polar decoder below, or always-erasure, whichever has the smaller certified bound. This is a whole two-branch operation, not a normalized nonlinear accepted map; source calibration, noiseless implementation and finite-dimensional systems are assumed.

## 1. A scalar anchor paid by the original deficit

Put d=p/3,Y=q tau/3,B=||Y||. The p=0 and q=0 cases are immediate. The new whole theorem gives
K(s)=d V*(Y+sI)^-1V,
h(s)=sqrt(e2(K(s))/3)=integral_[0,B] nu(dt)/(s+t),
nu([0,B])=d,
Delta>=integral F(h(s)I3)ds.

Define ell as the unique positive root h(ell)=1 if h(0+)>1, and ell=0 otherwise. Since h(s)<=d/s, 0<=ell<=d. Set e0=3(d-ell).

The scalar endpoint-chord proof in `pure_success_coherent_reset_scalar_anchor_value_theorem.md` sections1-4 applies directly to this positive scalar measure, with no auxiliary dimension or reset-trace limit: for ell>0 the moment integral nu(dt)/(ell+t)=1 selects endpoint mass fraction r=(d-ell)(B+ell)/(dB) on B. The endpoint clock is h_ext(s)=d[1-r B/(B+s)]/s. The scalar chord gives h<=h_ext below ell and h>=h_ext above ell. Both clocks lie above1 below ell and below1 above it. Since the derivative of F(xI3) is negative for x>1 and positive for 0<x<1, pointwise F(hI)>=F(h_ext I).

If ell=0, h(0+)<=1 and h(s)>=d/(B+s), with B>=d; both clocks are below1, giving the same comparison with r=1. If ell=d, the moment inequality forces the measure to be d delta0. All integrals converge by the whole theorem's fixed mass/support domination. The endpoint is the actual finite physically-flat source of mass T=3d+9B, whose received Bayes-error payment gives

 e0^2 <=5 T Delta <=5(p+3q) Delta.                         (2)

This comparison does not assert that the original matrix clock has a scalar anchor.

## 2. Scalar anchor controls the actual third positive eigenvalue

Let lambda3 be the smallest positive eigenvalue of dVV*-Y, padded by zero if fewer than three are positive, and e=3(d-lambda3). We prove e<=5e0.

If z=ell/d<=4/5, then e<=p=3d<=5e0. Otherwise z>4/5 and K(ell)<=I/z with e2(K(ell))=3. If its smallest eigenvalue is m_actual, the other two are at most1/z, hence
3<=1/z^2+2m_actual/z,
so m_actual>=m=(3z^2-1)/(2z)>0.

C(s)=K(s)^-1 obeys C'(s)>=I/d. Indeed for R=(Y+sI)^-1, compression Cauchy-Schwarz gives V*R^2V >=(V*RV)^2. Therefore C(ell)<=I/m and
C(s0)<=I,  s0=ell-d(1/m-1)>0.
The claimed positivity of s0 is explicit: s0/d=z+1-1/m has the sign of 3z^3+3z^2-3z-1. This polynomial is7/125 at z=4/5 and has derivative9z^2+6z-3>0 thereafter. Thus s0 is an admissible positive resolvent argument. Birman-Schwinger inertia yields three eigenvalues of dVV*-Y at least s0. Consequently
 e/e0 <=(1/m-z)/(1-z)=3z(1+z)/(3z^2-1)<=5,
where the last inequality is equivalent to12z^2-3z-5>=0 for z>=4/5. At z=1 use continuity, or K(d)=I forced by e2=3 and K(d)<=I, which implies YV=0. This also proves the zero-deficit exact recovery endpoint directly.

## 3. Actual original-source decoder and charged error

Use `pure_success_coherent_reset_positive_spectrum_erasure_lemma.md`. If lambda3>0, let P+ be the positive spectral projector of dVV*-Y, M=V*P+V and J=P+V M^-1/2. Measure {P+,I-P+}, decode acceptance by J*, and replace rejection by an orthogonal flag. The complete instrument error is at most9e (the sharper spread subtraction remains available). If fewer than three positive eigenvalues, always erase, whose error is exactly2p and is still bounded by9e. Always-erasure is available in all cases.

Combine e<=5e0 with (2) to obtain(1). All maps act on the actual received output and preserve arbitrary untouched reference systems. No hidden success/reset label is measured, and no auxiliary scalar bath is implemented. The scalar bath only pays an analytic lower bound on the original entropy deficit.

## 4. Fixed inverse filter: stronger error and constant acceptance

The received `coherent_reset_inverse_filter_heralded_channel.md` gives a stronger operational option, without changing the entropy argument. For rank-three P+, let kappa=lambda_min(M) and use the received-system success Kraus operator
Kf=sqrt(kappa) M^-1 V*P+.
It is a contraction and Kf V=sqrt(kappa)I3. The accepted branch is EXACTLY
S(rho)=p kappa rho+Tr(rho) Bf,
Bf=3Kf Y Kf*, beta=Tr Bf.
Erase failure. Its acceptance z=p kappa+beta is input independent. Relative to the ORIGINAL-rate ideal(p id,q erasure), the complete diamond error is at most2max[p(1-kappa),beta]<=6e. For deficient positive rank use always-erasure, error2p=2e<=6e. Thus an explicitly selected instrument satisfies the improved universal bound

min{2p,30 sqrt[5(p+3q)Delta]}.                            (3)

Put epsilon=sqrt[5(p+3q)Delta]. If5epsilon<p, then e<=5epsilon<p guarantees rank three, and this actual fixed filter has
p kappa>=p-5epsilon,
beta<=15epsilon,
z>=p-5epsilon,
||S/z-id||_diamond<=30epsilon/(p-5epsilon).
The identity weight is at least(p-5epsilon)/(p+10epsilon), using beta<=15epsilon and p kappa>=p-5epsilon. In particular epsilon<p/10 guarantees the sufficient qutrit Choi witness gamma>1/4 for a non-entanglement-breaking accepted channel, with charged genuine identity throughput at least p-5epsilon. No unassisted-capacity claim follows.

These accepted maps are actual operations on the ORIGINAL source. The auxiliary scalar clock is used solely for the analytic epsilon bound. Neither the earlier same-main charged GLS counterexample nor the full-instrument entropy-monotonicity failure is contradicted: this proof bounds a different explicit instrument's error from the already acquired original entropy, rather than asserting entropy monotonicity under that instrument.

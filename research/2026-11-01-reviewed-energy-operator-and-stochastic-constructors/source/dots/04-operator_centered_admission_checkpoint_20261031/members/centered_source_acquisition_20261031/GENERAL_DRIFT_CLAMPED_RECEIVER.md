# Centered creation from an acquired product-weight drift certificate

31 October 2026. Separate candidate receiving theorem, not an amendment to the frozen guarded compiler. Independent review pending. Ordinary Schur inequalities, Metzler comparison and inclusive-amplitude Cauchy extraction are components; no new threshold or hardware claim is made.

## 1. Actual acquired interface

On finite source cells let P_i be acquired orthogonal projectors and Q_i=I-P_i. No rank-one or pure reference assumption is needed. Let V_u=product_i(I+u_iQ_i), 0<=u_i<=1. The ACTUAL source GKSL generator, with initialized Markov input fields, has a checked inequality

 G^dagger(V_u) <= sum_i(Mu)_i Q_i product_(j!=i)(I+u_jQ_j)
                  +sum_i a_i u_i V_u.                         (1)

M is an acquired real Metzler matrix. Every row and column sum is at most -kappa<0;0<=a_i<=a. Set D=max_i(-M_ii), so D>=kappa. The certificate includes D; no optimal diagonal-to-gap ratio is assumed. A source subset may propose a projector, but ALL actual generator terms must be included in checking(1).

A full fixed gate/idle schedule has location duration<=tau, at most g source cells per location, and at most one simultaneous location per source. Aggregate ALL unwanted terms on each(cell,location) into K_i, with an acquired uniform norm bound c on retained control-register blocks. Its local source blocks satisfy

 K_i=[[0,C_i^dagger],[C_i,F_i]],  ||C_i||,||F_i||<=c.

Thus P_i K_i P_i=0, but K_i P_i need not vanish. Intended system-only operations commute with V_u. A source-independent actual local Hamiltonian residual has integrated norm<=epsilon_ctl. All real unselected creating interactions remain ON. System patch support, controls, source fields and consumer gadget assumptions are real acquired premises; they are not supplied by this theorem.

## 2. Outside creation and the clamped weight

Put delta=kappa/4 and alpha=c^2/delta=4c^2/kappa. For a real K_i,

 i[K_i,I+u_iQ_i] <= alpha u_i(I+u_iQ_i)+delta u_iQ_i.

After factoring u_i, the diagonal majorant is alpha on P and alpha(1+u_i)+delta on Q, whose product is at least c^2. The operator Schur inequality proves this for arbitrary-dimensional P/Q blocks and system coefficients. Hence outside creation changes the linear drift to M'=M+delta I and activation to a_eff=a+alpha. M' has both row and column margins

 kappa'=kappa-delta=3kappa/4.

For selected locations with |z_l|<=R, hold every active selected u_i at1 in backward time. At entry into a selected interval, raise u_i to1. Free coordinates follow dot u=M'u; selected coordinates stay clamped. Row comparison gives0<=u<=1. A clamp requires nonnegative forcing

 f_i=-(M'u)_i,  kappa'<=f_i<=D-delta=:F.

There are at most g|S| impulses of size<=1, including the possible terminal clamp. Their forward-time weight jumps are downward, so they help the positive weighted comparison. Selected forcing-time volume is at most F g|S|tau. Column contraction of exp(M't) gives

 sum_i u_i(initial)<=g|S|(1+F/kappa'),
 integral sum_i u_i(t)dt<=g|S|(1/kappa'+F tau/kappa').        (2)

The first bound uses total impulse mass and instantaneous forcing<=Fg|S|; the second uses the impulse/forcing convolution and Fubini. All outside evolution and arbitrary gaps remain in place.

## 3. Selected complex creation is absorbed by the original row margin

At u_i=1, the exact upper-right block of i z_l* K_i V_i-i V_i z_l K_i is i(2z_l*−z_l)C_i^dagger, norm<=3Rc. The QQ diagonal is4 Im(z_l)F_i, bounded by4Rc Q_i.

The off-diagonal block is at most

 s_R V_i+(kappa/4)Q_i,  s_R=36R^2c^2/kappa.

Indeed s_R(2s_R+kappa/4)>=9R^2c^2. If R<=kappa/(16c), the QQ diagonal costs at most another kappa/4 Q_i. On a clamped coordinate the ORIGINAL source coefficient obeys (Mu)_i<=sum_j M_ij<=-kappa, since u_i=1 and0<=u_j<=1. Thus the selected complex term spends at most half the available original row margin. One does not charge the outside delta loss again there. Conservatively charging a_eff rather than a on selected cells is positive overestimation only.

Free coordinates' original drift plus real outside creation are canceled by the backward M' derivative. This termwise use of(1) remains valid even when some coordinates are clamped and others free. No source independence or classical trajectory factorization is assumed.

## 4. Complete initialized-dilation and fault amplitude

Define

 C0 = g(1+F/kappa')
       +a_eff g(1/kappa'+F tau/kappa').

The weighted non-TP evolution, including helpful forward downward jumps, yields the common jump-history dilation bound

 ||W(z)||^2 <= exp{|S|[C0+36R^2c^2g tau/kappa
                         +2R epsilon_ctl]}.

All finite source/system/reference correlations are admitted. Markov input fields are initialized as in the specified GKSL dilation; no arbitrary incoming-field extension is claimed. A single analytic family W(z) is used for all complex parameters. Finite bounded coefficients ensure the history-sector compact-set majorant; no independently selected Kraus gauges are substituted.

The standard multivariate Cauchy extraction therefore gives

 ||E(S)|| <= eta(R)^|S|,
 eta(R)=exp[C0/2+18R^2c^2g tau/kappa+R epsilon_ctl]/(R-1),
 1<R<=kappa/(16c).                                           (3)

This is the established inclusive fault-AMPLITUDE premise, not a probability inferred from one-point moments. A complete fault-tolerant consumer and all its physical operations remain external.

Choose a power-of-two R>=2 satisfying EXACT rational inequalities

 16cR<=kappa,
 72R^2c^2g tau<=kappa,
 2R epsilon_ctl<=1   (omitted if epsilon_ctl=0).

The first two allow at most1/4 quadratic exponent; the last at most1/2 residual exponent. No floating square root or logarithm is required. The largest such power of two loses at most a factor two relative to the minimum real cap, provided that real cap is at least2. An explicit arithmetic/search cap can instead return NOT_ADMITTED/UNKNOWN, never a fabricated radius.

For any nonnegative rational x, e^x <= (8/7)^ceil(8x): use e^(1/8)<=1/(1-1/8)=8/7 and monotonicity. Thus (3) has a finite rational upper. The integer exponent and resulting numerator/denominator sizes are actual costs; if they exceed an explicit budget the receiver refuses. This is not a constant-time exponential oracle.

The c=0 case uses the ordinary source-independent residual bound directly. The full schedule has positive finite durations; zero-exposure cases are not handled by division by tau or c.

## 5. What is actually different from the guarded mode

An X-coupled lossy qubit has PXP=0 for its lossy-ground projector but no nonzero annihilating coupling kernel. It can use this centered-creation receiver if its ACTUAL source generator earns(1). At fixed physical c the scale includes c sqrt(g tau/kappa); at fixed diffusion c proportional to sqrt(kappa), that contribution does not vanish. The leading logical dissipative disturbance is paid rather than erased.

The diagonal-to-gap conditioning F/kappa' and activation a_eff are retained. A huge negative M diagonal canceled by equally huge positive influences can make this certificate poor even when its gap is positive. The finder must not claim kappa alone determines the resource. Increasing activation to manufacture a formal drift is likewise visible in C0.

Where K_iP_i=0 actually holds, the frozen guarded receiver can be much cheaper and remains the appropriate option. No existing guarded record is silently reinterpreted as a centered-creation certificate. Neither mode proves experimental model correctness, constructs a physical source or supplies a new threshold number.

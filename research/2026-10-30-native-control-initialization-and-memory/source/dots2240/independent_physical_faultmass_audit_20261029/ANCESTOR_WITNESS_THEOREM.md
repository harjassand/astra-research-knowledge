# Local-stochastic marked-reset emissions in fixed physical-time cells

2026-10-29. Continuation of the transactional actual-reset tail. This is a physical-record faultmass statement, not a completed-data-update-index theorem and not a data-channel serialization or quantum-memory threshold theorem.

## 1. Model and conclusion

Take the transactional generator with the ACTUAL separately recorded terminal/abort reset instruments. The preceding certificate supplies finite-support positive witnesses

alpha I≤Z_h≤I,   (L−J_h)*Z_h≤−r Z_h,

where J_h is the designated reset gain, alpha>0, r>0 and witness support radius R are uniform. All clean local terms have fixed range. Fix a spatial coloring of owners with P colors so no clean term touches two Z supports in one color. Bounded geometry makes P finite. Same-color Z supports are disjoint and have the required buffer.

Add independent physical Poisson kick sources e, rate epsilon c_e, with CPTP quantum channels E_e of uniformly bounded support. Their actual generator contribution is epsilon c_e(E_e−id). The designated reset instruments remain actual physical channels. No arbitrary replacement of them by fictional nominal jumps is permitted.

A kick at e sets the classical mark of every h in a fixed local set H_e to 1, where |H_e|≤b. A designated reset at h emits its record, reports whether h was marked immediately beforehand, and clears its mark to 0. These are passive classical record annotations; they do not change the quantum dynamics. Initially ALL marks are 0. Initial quantum states may otherwise be arbitrary and entangled. Initially dirty/marked owners would require an additional initial-defect term and cannot obey a noise-vanishing estimate.

Assume

sum_(e:h in H_e)c_e≤nu_0,
sum_(e:supp(E_e) meets supp(Z_h))c_e≤J_R,

and any kick touches at most b_Z same-color Z supports. All constants are independent of volume and observation duration. Put D=alpha^(−b_Z), and assume

epsilon J_R(D−1)≤r/2.                 (A)

When D=1 there is no restriction from (A). Fix any physical-time cell width Delta>0 and cells (h,n) with interval [n Delta,(n+1)Delta). Let M_(h,n) be the event that at least one marked terminal/abort reset emits there.

Then, for every finite prescribed set S of DISTINCT owner/time cells,

P(all M_v, v in S)≤p_cell^|S|,
p_cell=(epsilon C_*)^(1/(bP)),        (B)

provided epsilon C_*≤1, with explicit finite C_* below. The same inequality holds in diamond norm for the corresponding CP record-event instrument, uniformly over arbitrary initial quantum states and references. One may write p_cell=[C (epsilon Delta)]^(1/(bP)) by C=C_*/Delta. No delay independence is assumed. The result is uniform in the number of cells and elapsed physical time.

## 2. Robust simultaneous survival with prescribed kick insertions

For a same-color set A of currently active owners put Z_A=product_(h in A)Z_h. Under the actual noisy killed generator suppressing designated resets at A, the clean product drift is ≤−r|A|Z_A. If e touches v≤b_Z factors,

E_e*(Z_A)≤alpha^(−v)Z_A≤D Z_A.

Untouched factors commute and factor out; on the touched factors use product Z≤I, CPTP adjoint unitality/positivity, and I≤alpha^(−v)product Z. Sources touching no factors contribute zero to (E_e*−id)Z_A. Summing incident rates gives

K_(A,epsilon)*Z_A≤−[r−epsilon J_R(D−1)]|A|Z_A≤−rho|A|Z_A,
rho=r/2.

This proves the required decay even with ALL unspecified kicks retained. Their delays and effects need not be independent of survival.

Consider a deterministic finite family of survival intervals, each labeled by an owner of this same color. For the same owner intervals must have disjoint interiors. Require no designated reset of that owner within its interval. Let their total duration be ell, and their number be m. Insert k additional specified physical CPTP kicks at deterministic source/time points. The CP instrument weight of all these survival constraints, conditional only on the prescribed insertions (not on rare reset records), is bounded by

alpha^(−m) D^k exp(−rho ell).         (C)

Proof: run the Heisenberg product-witness comparison backwards through consecutive interval endpoints and insertion times. On a segment with active set A, the preceding drift gives exp(−rho |A|dt). When an interval endpoint activates a new factor backwards in time, use I≤alpha^−1 Z_h. When its starting endpoint removes the factor, use Z_h≤I. A specified kick costs at most D. At no time is an owner counted twice, because its intervals are disjoint. Arbitrary intervening exterior dynamics is already part of the killed generator. No quantum-state conditioning on a future clock record is used. Formula (C) is a uniform operator/effect inequality and therefore includes reference entanglement.

## 3. Last-kick ancestors: genuinely bounded multiplicity

For each marked reset emission, choose the LAST kick incident to its owner before that emission. Since a designated reset clears the mark, that ancestor kick lies after the owner's preceding reset, and no designated reset occurs between the ancestor and the chosen emission.

One physical kick can be ancestor to at most one reset per owner and to at most b reset emissions overall. Multiple intervening kicks cause no difficulty: the LAST one is used. This bound is deterministic on every complete physical record, not an assumption about independent service times.

For each target cell select one marked emission in that cell, for example its first. Let s_v=n Delta denote the cell start. If its ancestor is (e,tau), then h_v in H_e and tau<s_v+Delta. For tau<s_v there is no designated reset in [tau,s_v]; for tau≥s_v no survival interval is needed. Its required interval length is (s_v−tau)_+.

For two selected emissions of the SAME owner in distinct cells, their ancestor-to-emission intervals have disjoint interiors: the earlier selected emission is itself a reset preceding the later ancestor. The shortened ancestor-to-cell-start intervals are therefore disjoint as well. This is why (C) applies, despite possibly overlapping intervals of different owners.

The selected emissions partition the target cells into ancestor groups G, each of size 1≤|G|≤b, whose cells have distinct owners. Each group shares one physical kick. Different groups use distinct kicks.

## 4. Poisson factorial expansion, without independent delays

First restrict to a target set S all of whose owners have one spatial color, and put m=|S|. Define the nonnegative kernel

w_v(e,tau)=1_(h_v in H_e) 1_(0≤tau<s_v+Delta) exp[−rho(s_v−tau)_+].

On any valid witness assignment, (C) bounds the survival instrument by alpha^−m D^k times the product of these exponential factors. Apply the Poisson factorial expansion to its k DISTINCT ancestor points: integrate their intensities epsilon c_e d tau, leaving every other Poisson kick in the evolution. This identity follows directly by distinguishing k factors in the Poisson/Dyson series; the remaining factors re-sum to the original noisy evolution. It does NOT condition on delay distributions or on a rare clock record.

We may drop further restrictions on allowed ancestor times, distinct-owner groups, and disjoint-interval ordering AFTER applying (C) on the valid domain, because the integrands are nonnegative. We do not apply (C) to invalid overlapping intervals. The resulting upper bound is the partition sum

P(all M_v, v in S)≤F(S),
F(S)=sum_(partitions pi of S, all |G|≤b) product_(G in pi) W(G),
W(G)=epsilon D alpha^(−|G|) sum_e c_e integral_0^infinity product_(v in G)w_v(e,tau) d tau.       (D)

Groups are canonically indexed by their least target label, so the factorial expansion has no missing or additional k! factor. Repeated use of the SAME kick is represented by one group, not by falsely independent copies. Distinct groups use the factorial measure; coincidence diagonals for continuous Poisson times have measure zero.

The original domain is a subset of the integration domain in (D); invalid assignments only enlarge this bound. This avoids any independence claim about kick-dependent completion delays.

## 5. Summable kernel removes the apparent Bell-number divergence

A crude count of partitions would be superexponential and would NOT prove local stochasticity. Spatial incidence and the exponentially summable physical-time kernel are essential.

For any source/time (e,tau), sum w_v over ALL owner/time cells v (not just the prescribed set). At most b owners lie in H_e. For each owner, at most one cell start lies below tau with its end above tau, followed by a geometric tail of later cell starts. Therefore

sum_v w_v(e,tau)≤B_Delta,
B_Delta=b[1+1/(1−exp(−rho Delta))].

This is a safe bound, including time-zero boundary cells. For a fixed target v,

sum_e c_e integral w_v(e,tau)d tau≤nu_0(Delta+1/rho).

Consequently, for 1≤j≤b,

sum_(G subset S: v in G, |G|=j) W(G)≤epsilon C_j,
C_j=D alpha^(−j) nu_0(Delta+1/rho) B_Delta^(j−1)/(j−1)!.

Use the expansion of the (j−1)-th power of sum w to dominate the sum over distinct other cells. Set C_*=sum_(j=1)^b C_j and q=(epsilon C_*)^(1/b)≤1.

Partition recursively by the group containing a fixed v. Inductively, F(empty)=1 and

F(S) = sum_(G contains v) W(G) F(S\G)
     ≤ sum_(j=1)^b epsilon C_j q^(m−j)
     ≤ q^m [epsilon C_* q^(−b)] = q^m.

For j>m the corresponding sum is empty. The inequality q^−j≤q^−b uses q≤1. Thus no factorial or volume-dependent combinatorial factor remains.

## 6. All spatial colors and the CP faultmass interpretation

For arbitrary S, choose a color subset S' with |S'|≥|S|/P. All-events-on-S implies all-events-on-S'. The preceding estimate gives

P(all M_v, v in S)≤q^|S'|≤q^(|S|/P)=p_cell^|S|.

The estimate holds uniformly for every initial joint quantum/reference state. For a CP trace-nonincreasing record-event instrument I_S this is equivalent to

I_S*(I)≤p_cell^|S| I,
||I_S||_diamond≤p_cell^|S|.

The mark register starts in its specified all-zero classical state; the diamond bound is on the resulting quantum-input instrument, not on arbitrary pre-existing mark-register inputs.

This is genuine local-stochastic CP faultmass for marked terminal/abort reset RECORDS in fixed physical-time cells. It retains the dependence between kicks, scheduling, locks, and reset delays. It is not a statement that the corresponding quantum DATA map admits replacement by ordinary faulty gate locations. That additional serialization/factorization remains separate.

## 7. Boundaries and useful failures

1. Without initially zero marks, a marked initial owner may emit with positive probability at epsilon=0; (B) is then false. An initial-source term is mandatory.
2. Without bounded ancestor multiplicity b, one kick could explain arbitrarily many target cells and no epsilon^(c|S|) law follows.
3. Without a summable delay kernel, the partition row sums can diverge with elapsed time.
4. A scalar single-owner lifetime mean or marginal exponential tail is insufficient for (C): correlated joint survivors require the actual local product witness.
5. Small noise is used to retain decay in the presence of UNSELECTED intervening kicks, not to assume that ancestors are isolated.
6. The physical kick channels must be additive genuine CPTP jump channels, while designated reset records remain actual. A merely CPTP total generator with a formal nominal-reset subtraction does not suffice.
7. Constants can be extremely poor: alpha and R come from finite-rate monitored paths, and P,J_R,b_Z inherit their witness radius. No useful numerical threshold is claimed.

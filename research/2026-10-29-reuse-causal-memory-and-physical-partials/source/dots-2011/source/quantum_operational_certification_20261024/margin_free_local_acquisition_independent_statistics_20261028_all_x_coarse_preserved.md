# Independent statistics: automatic local discovery without a supplied contrast number

28 October 2026. Separate mathematical support; not a change to any received source or receipt. No source samples, RNG, hardware calls, production solver or upload is involved.

## Source assumptions that remain essential

The source retains the fixed exact bounded-width logical Pauli algebra and complete current-coin nonanticipation of the received local source. The quantitative CP margin H_j-kappa G_total>=CP0 is replaced by the QUALITATIVE condition H_X>=CP0 and H_Z>=CP0 during acquisition. Thus the conditional signed blocks satisfy Delta_j=B_j R_j, 0<=R_j<=rho and [B_j,R_j]=0. Both true generators share an unknown interval I_i of length at most w. There is no supplied positive number kappa. These positivity and support assumptions are not learned by the algorithm; global identity dominance alone does not imply positive X/Z contrasts.

The positive blocks can be zero or rank deficient on all data collected. A caller-funded fixed cap and ABSTAIN are therefore necessary; no unconditional discovery or service promise follows from qualitative positivity.

## 1. Nonzero coarse signal certifies overlap

At each coarse call prepare all q logical inputs in independent signed X states and measure every physical output in a fresh independent Pauli basis. For every length-w candidate interval J retain s_i Z_J. Its conditional mean is the reduced X contrast. Put lambda_(i,t)=Tr R_(i,X,t) in [0,1].

For any J containing the entire true common interval I_i, the reduced mean is B_(i,X) R_J, with R_J positive and commuting with B, so its trace norm is EXACTLY lambda_(i,t). Averaging histories preserves the same fixed B and positive R, so the norm of that averaged contrast is lambda_bar_i.

For any J disjoint from I_i, conjugation by the complementary true B_(i,Z) changes the sign of Delta_(i,X), while acting wholly on the subsystem traced out. The reduced mean is therefore EXACTLY zero at every history. No contrast margin is needed for this cancellation. A nonzero coarse contrast can thus certify overlap, not necessarily containment. Expanding a certified length-w J by w-1 sites on each side and clipping/padding to W=min(n,3w-2) contains I_i. The received packing/color argument then applies.

## 2. Finite coarse schedule, threshold and probability

Let d0=2^w, M0=n-w+1, beta_c=beta/2, and fund a finite S0. Use

    eta_s=2^(-s)/4,
    Lc=ceil log2(2 d0 q M0(S0+1)/beta_c),
    Nc_s=4*12^w*Lc/eta_s^2
        =64*12^w*Lc*4^s, s=0,...,S0.                 (1)

The records s_i Z_J have centered norm <=2d0 and conditional variance <=3^w I. Matrix Freedman at operator radius a=eta_s/d0 gives

    P(||empirical-predictable average||1>eta_s)
      <=2d0 exp[-Nc_s (eta_s/d0)^2 /
                   {2(3^w+2eta_s/3)}].              (2)

Since eta_s<=1/4 and w>=1, the denominator is at most 3*3^w. Union over qM0 matrices and S0+1 reached stages costs at most beta_c. This holds conditional on every preceding complete history, with arbitrary source-memory drift.

Compute each known empirical trace-norm score to additive eta_s/4. A sufficient finite Frobenius residual is eta_s/(4d0), since trace norm is at most sqrt(d0) times Frobenius norm. Select a candidate only if its computed score is STRICTLY greater than 2eta_s. On the confidence event a disjoint candidate has score at most 5eta_s/4, so every selected candidate overlaps the true interval. Exact ties at the threshold do not qualify.

A true containing interval has computed score at least lambda_bar_i-5eta_s/4. Therefore lambda_bar_i>=4eta_s forces a qualifying score, with slack 11eta_s/4>2eta_s. Keep each logical's first certified interval if desired: the fixed support makes it valid forever, and later coarse stages need only resolve the remaining logicals. All intervals can still be estimated from the same full product records. The worst-case union and source cap do not depend on which were resolved earlier.

## 3. Automatic coarse completion and the declared occupation

On ONE simultaneous confidence event, each reached stage resolves every still-unresolved logical whose RANDOM predictable contrast mass lambda_bar_i,s is at least 4eta_s. Discovery completes once every logical has met this condition at some reached stage; the favorable stages need not coincide.

For a common persistent lower contrast mass lambda_*>0, used only for analysis, the first sufficient scale has eta_s<=lambda_*/4 and eta_s>lambda_*/8. For s=0 the same lower comparison holds because eta_0=1/4 and lambda_*<=1; for s>0 it follows from the previous failed geometric scale. Thus

    Nc_s<256*12^w*Lc/lambda_*^2,
    sum_(t=0)^s Nc_t <(4/3)Nc_s.                      (3)

The coarse fixed cap is exactly 64*12^w*Lc*(4^(S0+1)-1)/3. The funded cap must reach a sufficient scale. There is no supplied lambda_* and no inference that qualitative positivity provides one.

These completion assertions first concern the DECLARED calibration experiment with ideal trusted controls and the unknown noisy source. A high-probability completion result requires the excitation condition almost surely on reached histories, or a separate failure debit. Conditioning on a favorable random contrast mass does not preserve beta automatically. A resulting record event can be transferred to an imperfect implementation with its record-TV debit; a floor known only on a different imperfect-memory trajectory cannot be substituted into this declared experiment.

## 4. Fine direct-gap certification needs no numeric margin

After every logical has a certified envelope and coloring passes, use the received acquired-patch-excitation fine schedule, but only the DIRECT signed-gap guard. In each ordinary X/Z/sign bank estimate

    Y_(i,j)=2*1{j_i=j}*s_i*Z_(W_i), j=X,Z.

The conditional average is Delta_bar=B Rbar with Rbar>=0 commuting with fixed B. No inequality Rbar>=kappa rho_bar is used. The two signed matrices per logical have variance <=2*3^W I and centered norm <=4d, d=2^W.

Let beta_f=beta/2, fund S1, take the largest dyadic b with b^2<=epsilon/(18Aq), and set

    Lf=ceil log2(4dq(S1+1)/beta_f),
    a_t=2^(-t)/(16d),
    Nf_t=8*3^W*Lf/a_t^2.                             (4)

The 4dq numerator suffices for 2q matrices times two signs; retaining the previous 6dq log factor is harmless if the unsigned marginal is also retained. The same matrix martingale proof gives simultaneous signed operator errors <=a_t, with fine failure at most beta_f, conditional on ANY correct coarse stopping history.

Finite rational diagonalization supplies C=Q D Q† with additional Frobenius error <=a_t/4, so total error e=5a_t/4. The exact physical raw sign is S=Q sign(D)Q† with sign(0)=+1. Let h=min|D_kk|. The exact rational guard is

    h>5a_t/4,  10a_t<=b(8h-5a_t).                    (5)

If h>e, the true Delta_bar is invertible with gap at least h-e. Positivity of Rbar then proves sign(Delta_bar)=B. The two-sector Sylvester bound gives ||S-B||op<=2e/(2h-e), hence (5) certifies error <=b. This uses no unknown kappa, source eigenbasis or supplied floor. The sign is physical on every record, including records that fail the guard.

Retain EACH generator's first direct-gap-certified reflection permanently, and stop only once all 2q generators have been certified. The fixed true B makes an earlier operator certificate valid for every subsequent history. Keep the ordinary random X/Z/sign preparation schedule on ALL logical inputs unchanged; only classical accumulation for resolved items may stop. The 2q(S1+1) union already covers all reached-item tests. Different logicals and X/Z axes can be informative in different banks, and no common marginal or coincident excitation is required. The retained approximants may fail exact mutual Pauli relations; the uniform operator bounds and the received joint extractor, not such relations, justify their eventual composition.

If the actual predictable signed gaps of every unresolved item are at least gamma_*>0 and a_t<=b gamma_*/5, every remaining direct guard passes on the same confidence event. The received instance bound applies with gamma_*^2 in the denominator:

    Nf_t<=57600 A q 3^W Lf/(gamma_*^2 epsilon)+1,
    sum_(u=0)^t Nf_u <(4/3)Nf_t.                     (6)

More generally, on Good each unresolved item is certified whenever it has its own reached stage with a_t<=b times its actual gap divided by 5. A finite collection of such epochs suffices, even if no stage excites all items. The rate in (6) still needs persistent excitation or an explicit bound on when the last qualifying epoch occurs: mere eventual existence of positive-gap epochs cannot bound an arbitrary temporal delay. The same pathwise/random-gap and declared-versus-physical qualifications apply. Coarse nonzero contrast does NOT imply fine full-rank signed gaps. Both stages can legitimately abstain.

A physical example separates asynchronous from simultaneous acceptance. At one phase use logical Pauli branches I and X with weights 1/2 each, with a full mixed gauge; the X signed block equals the total gauge block while Z is zero. At another phase use I and Z with weights 1/2 each, reversing those roles. The unknown U and true B remain fixed. Retaining a certified X reflection from the first phase and Z from the second succeeds, while a rule requiring both nonzero gaps in one bank never qualifies. This source satisfies qualitative CP positivity without any positive common numeric contrast margin.

## 5. Combined cap, accepted service and comparison

The single good event has failure at most beta_c+beta_f=beta. The source cap is the sum of the two explicit finite geometric caps; no lambda_*, gamma_* or kappa is required as algorithm input. Conditional on valid acceptance, every acquired generator is within b in operator norm of its fixed true generator. The received colored full-reference extractor therefore has virtual loss at most (9/2)Aq b^2<=epsilon/4 for EVERY future gauge/retained-memory state. Only one later simultaneous q-input service is covered.

Future Pauli/gauge structure with the same fixed algebra remains required; CP identity dominance is separately required for comparison to the strongest same-current-memory full-CPTP oracle. Otherwise the comparator is specified exact logical extraction. One calibration-record TV discrepancy transfers false-accept and completion probabilities; one uniform future-service complete discrepancy transfers accepted risk. This is accepted unnormalized risk, not service after ABSTAIN or posterior correctness conditional on public acceptance.

All coarse/fine calls prepare q physical inputs and read n physical outputs. Coarse stages store at most qM0 known d0-by-d0 accumulators; fine direct-only stages need 2q known d-by-d accumulators. Finite trace scores, raw signs, controlled reflections, ancilla preparation, routing, random-sampler caps and timing padding remain paid. An equally informed conventional learner receives the same records and both finite certificate mechanisms. The relaxation removes a supplied numerical contrast number, not the qualitative oriented-Pauli source structure or real instance-dependent signal/gap scales.

## Independent zero-margin algebra checks

The deterministic script also verifies the candidate's genuinely zero-uniform-margin four-dimensional gauge example: alternating complementary rank-two projectors P, blocks G_I=(I+P)/8 and G_Z=(I-P)/8, total gauge I/4, H_X=P/4 and H_Z=I/4. Every call has an H_X kernel on which G_total is positive, so no kappa>0 exists; every even bank averages H_X to I/8, giving logical signed gaps 1/16 and 1/8. Oracle loss is exactly 1/4. All declared geometric stage lengths are even.

An exact scalar-Pauli counterexample confirms the separate source orientation assumption: probabilities (p_I,p_X,p_Y,p_Z)=(3/10,3/25,29/100,29/100) have identity as the largest Pauli weight but X contrast -4/25. Identity dominance alone therefore cannot replace qualitative CP-positive contrasts.

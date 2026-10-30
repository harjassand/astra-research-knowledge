# Exact local CP credit from a killed finite-controller resolvent
2026-10-30. Root construction, not independently reviewed.

## 1. Supplied model and scope
Consider ONE finite controller with Hamiltonian H_C, auxiliary-only internal jumps, and terminal reset jumps a_mu tensor K_s. All terminal outcomes implement the SAME idempotent DATA CPTP channel Phi with Kraus K_s, so sum_s K_s^dagger K_s=I and Phi^2=Phi. Internal operations act trivially on DATA. This can describe a gauged clean circuit-completion sector, but does not by itself describe overlapping native controllers or dirty aborts.

Let the full controller generator be L_C and terminal gain J_C. Put K_C=L_C-J_C (gain removed, losses retained). Write A=J_C^*(I)>=0, hence K_C^*(I)=-A. Assume actual terminal killing has a uniform finite tail, so the resolvent

    R=integral_0^infinity exp(t K_C^*) I dt

exists, is strictly positive, and K_C^*R=-I. More generally it is enough to have alpha I<=R<=Rmax I and K_C^*R<=-c I, with c>0. Such inequalities are the actual-reset Lyapunov form, not an assumption of a correction oracle.

## 2. Positive channel credit, not additive cost
Choose 0<beta<1/Rmax and set

    S=(1-beta Rmax)I+beta R.

Then 0<S<=I and

    K_C^*S <= -(1-beta Rmax) A-beta c I.

For any positive DATA observable V with d=V-Phi^*V>=0, idempotence gives Phi^*d=0. Define

    F=Phi^*V tensor I+d tensor S
     =V tensor S+Phi^*V tensor (I-S).

This is positive and is the image of V tensor I under the explicit local unital CP map

    T_S(O)=sqrt(S) O sqrt(S)
            +sum_s K_s^dagger sqrt(I-S) O sqrt(I-S) K_s.

Controller and DATA factors are ordered in the natural way. Completeness follows from S+(I-S)sum_s K_s^dagger K_s=I. In particular, this is a physical CP map for the proof observable, not a claim it must be executed as an extra recovery operation.

## 3. Exact service identity
The full DATA/controller generator annihilates Phi^*V tensor I: internal controller terms cancel by unitality, and terminal DATA action is Phi^*Phi^*V=Phi^*V. On d tensor S, terminal gains vanish exactly because Phi^*d=0; terminal losses and internal clock evolution remain. Therefore

    L_phys^*F=d tensor K_C^*S
       <=-beta c d tensor I
          -(1-beta Rmax)d tensor A.

No weak-drive limit, Taylor approximation, time average, or stationary clock assumption is used. The controller phase and coherent offdiagonal resolvent entries enter S. This is precisely what the fixed-horizon averaging counterexample lacked.

Also F>=s_min V, where s_min=1-beta Rmax+beta alpha>0; F<=V. For an individual extended animal and many independent controllers, local multipliers are required, not a single global lower bound. If these maps are composed in bounded depth, the previously reviewed local Stinespring noise-transfer and two-weight no-jump arguments are available subject to their actual hypotheses.

## 4. Why this is not the native many-hub theorem
For overlapping DATA channels, the maps T_S,h do not generally commute. A neighboring completion can activate a presently idle correction and produce terms proportional to d_h even when that neighbor's own decrement is zero. The raw occupation loss then cannot pay the cross term. The simple compiler's geometric blocker weights solve a special version of exactly this issue.

Moreover a native controller's killed resolvent may depend on neighboring ownership registers, and other terminals act nontrivially on DATA. One may not replace their actual generator by the isolated L_C used above. Dirty terminal/abort operations need their own earned token charge. Thus this lemma is a concrete local service-credit building block, not a closed compiler theorem.

Potential next use: engineer a local killed-resolvent credit that is suppressed on conflicting ownership sectors and increases when blockers clear, so neighbor activation is paid by actual blocker service. Preserve the native two-site/reset interface and exact uniform local inequalities throughout.

## 5. Local inverse and a mutually exclusive committed-sector interface
For S eigenvalues s_i in [s_min,1], the clock operator block |i><j| of T_S acts on DATA as

    a_ij Id+b_ij Phi^*,
    a_ij=sqrt(s_i s_j), b_ij=sqrt((1-s_i)(1-s_j)).

Idempotence decomposes DATA operator space into range(Phi^*) and ker(Phi^*). The respective eigenvalues are a_ij+b_ij and a_ij, both strictly positive. Hence the full local linear map is invertible. Its inverse need not be CP. Fixed dimensions and s_min>0 give a finite inverse norm; a bounded-depth product has local inverse cones. This does not justify a global extensive inverse norm bound.

A useful controlled variant has a controller projector P_h onto an actual good committed sector, S_h acting within it, and identity outside it. Its Kraus are A_h=I-P_h+sqrt(S_h)P_h and B_hs=sqrt(I-S_h)P_h K_hs. Suppose for two DATA-overlapping hubs h,g that P_h P_g=0, each S preserves both projectors, and all cross-controller factors commute. Since DATA Kraus commute with all these controller factors, A_h and A_g commute, A_h B_gs=B_gs A_h=B_gs, and B_hs B_gt=B_gt B_hs=0. Thus every pair of Kraus commutes and the CP channels commute exactly, even on offdiagonal coherences between h-committed and g-committed sectors. For DATA-disjoint hubs the usual disjoint-support argument applies.

This is an exact algebraic interface that may fit full-lock committed native transactions. It still needs verification for the actual monitor, workspace and ownership factors and for all exterior generator terms. It says nothing automatic about acquisition sectors.

For an extended raw animal, the no-jump comparison additionally requires [S_h,f_A]=0. Positivity S_h>=s_min I alone is insufficient when they do not commute. In the intended committed application, one must prove S_h preserves all actual syndrome and defect flags before using a two-weight barrier comparison.

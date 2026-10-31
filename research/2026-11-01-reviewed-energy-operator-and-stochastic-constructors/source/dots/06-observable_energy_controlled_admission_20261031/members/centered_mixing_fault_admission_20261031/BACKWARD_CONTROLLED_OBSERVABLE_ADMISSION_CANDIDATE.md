# Backward controlled-observable weights: removing the artificial control-variation bill

Status: new ROOT candidate, UNREVIEWED. Separate refinement of OBSERVABLE_DECAY_LOCAL_ADMISSION_CANDIDATE.md, which remains unchanged. This is a proposed exact finite-rate local-amplitude theorem, not an implementation of a new gate, a new threshold, or a historical-priority claim.

## 1. Scope and the missing control step

Receive the same actual finite circuit, initialized Markov fields, local source/data patches and common analytic dilation as the earlier observable-decay construction. At every time active source/data patches are disjoint. The actual source generator is block-local; no uncharged hopping/shared spectator term is permitted. Source blocks may be reused later and their initial state may be arbitrarily correlated with data, reference and other blocks.

Within each location the data/source PATCH is fixed, the source-only generator G is constant, and all time-dependent Hermitian unwanted couplings K(t) satisfy

  G^* K(t)=-r K(t),   r>0,   ||K(t)||<=c.

The identity must hold coefficientwise as an operator on source tensor the full local data/retained record space, with uniform bounds on allowed control branches. It is not a two-point-correlation estimate. All simultaneous real outside unwanted interactions remain ON and have disjoint patches. All imperfect implementation terms must be in the actual K or otherwise separately charged; declaring an ideal target does not eliminate its physical error.

The intended local data operation may contain arbitrary bounded time-dependent source-blind Hamiltonians and finitely many ideal data CPTP instruments with their records retained. Such an instrument acts on this location's fixed data/record patch; it is identity on every other currently active weight. Local adaptive records remain inside the fixed patch until its end. Global record-dependent scheduling/controls are admitted only at common weight-free boundaries with the same fixed support schedule and uniform bounds. No arbitrary mid-location cross-patch feedback or noisy apparatus outside K is silently admitted.

These ideal target/control operations are charged in the actual computational/physical task. The statement below removes a spurious extra ADMISSION penalty for their variation; it does not construct their hardware for free.

## 2. Finite-horizon backward observable

Let Phi_{s<-t} be the IDEAL joint evolution from t to s on this patch: source G, actual prescribed ideal data controls, and its local instruments, but without K. For t in [a,b], define

  B(t)=2 integral_t^b Phi_{s<-t}^*(K(s)) ds.              (1)

K is bounded measurable; ordinary piecewise continuous control suffices. The data controls commute as superoperators with source G. They act only on the coefficient operators of K, leaving its source eigenspace invariant. Unital CP adjoints are operator-norm contractions, also with references. Therefore

  ||Phi_{s<-t}^* K(s)||<=c exp[-r(s-t)],
  ||B(t)||<=2c(1-exp[-r(b-t)])/r<=2c/r.                (2)

No source mixing, stationary state, cold preparation or source reset is used. B is an ANALYSIS observable; the device need not compute or implement it. To apply the uniform bound, the verifier needs the actual coefficientwise decay identity and support/control premises, not a numerical solution of (1).

Between instruments it solves the exact backward equation

  partial_t B+G^*B+i[H0(t),B]=-2K(t),  B(b)=0.          (3)

At an ideal data instrument C with the output record retained,

  B(t-)=C^* B(t+).                                    (4)

There is no contribution from a bounded Hamiltonian at an instantaneous time. Instrument faults or finite-duration apparatus coupling belong in their actual assigned location and interaction model, not in a zero-duration fiction.

## 3. Positive complex weight and cancellation

For a selected location use a single complex coupling parameter z=x+i y with |z|<=R. Set

  V_z(t)=I+y B(t),   q=2Rc/r<=1/2.

It obeys (1-q)I<=V_z<=(1+q)I. The dependence on Im(z) is harmless: a norm majorant need not be analytic, while W(z) is analytic.

Using (3), the weighted generator for the complexified coupling is

  partial_t V_z+G^*V_z+i[H0,V_z]
      +i z* K V_z-i V_z z K
    =i y z* K B-i y z B K.                            (5)

The terms linear in y K cancel EXACTLY. K and B need not commute. The remaining Hermitian operator has norm at most

  2|y||z| c ||B|| <=4R^2 c^2/r.

Hence it is at most (8R^2 c^2/r)V_z. No derivative of K, gate Hamiltonian norm, commutator norm, pulse count or conditional ideal-control variation appears in this bound. That removal uses the source-only commutation/eigenspace premise and fixed local patch; it is not valid for arbitrary source controls.

At a local ideal instrument, unitality and (4) give C^* V_after=V_before. Its initialized Stinespring map therefore preserves the weighted quadratic form exactly. This is a receiving identity, not a product of marginal outcome probabilities or a bound on separately postselected rare outcomes.

## 4. All-selected-set receiving, endpoints and source reuse

At each time take the product of current selected-location weights. Its factors commute because their actual patches are disjoint. Block-local generators act on one factor at a time; real outside interactions commute with the product. Local instruments act as identity on the other factors, so the preceding receiving equation lifts to the product. This step would fail for general overlapping shared spectators or mid-location feedback into another active patch.

The squared norm grows by at most exp(8R^2 c^2 tau/r) during one selected location of duration <=tau. At its start, insert V_z(a)<=(1+q)I, costing a factor1+q. At its end V_z(b)=I EXACTLY, costing nothing. Reusing the source in a later selected or unselected location does not reset it: only the analytical weight is removed/reinserted. Initial arbitrary correlations are covered by the operator inequalities on the whole initialized-field domain.

For k selected locations, the common analytic initialized jump-history/Stinespring dilation satisfies

  ||W(z)||^2 <= (1+q)^k exp[8R^2 c^2 tau k/r].         (6)

The norm includes arbitrary finite source/data/reference inputs but initialized input fields. It does not refer to an arbitrary extension acting on excited incoming bath fields. All actual unselected interactions stay ON.

Inclusive faults use the same multivariate expansion of the physical common dilation: positive degree in every selected variable, all physical outside couplings unchanged. Cauchy on |z_l|=R gives, for 1<R<=r/(4c),

  ||E(S)|| <= eta(R)^|S|,
  eta(R)=sqrt(1+2Rc/r) exp(4R^2 c^2 tau/r)/(R-1).       (7)

For R=min(r/(4c),sqrt(r)/(sqrt(8)c sqrt(tau)))>=2,

  eta <=2 sqrt(3/2) exp(1/2)
           max(4c/r,sqrt(8)c sqrt(tau/r)).             (8)

These are conservative sufficient local amplitudes, not measured probabilities or threshold values. The c=0 case is exactly noiseless relative to these couplings and is handled without division.

## 5. Short-time and acquisition observations

Keeping the first bound in (2) gives a short-time variant: q can be replaced by 2Rc min(tau,1/r), and the integrated remainder can use

  integral_a^b ||B(t)||dt
    <=2c[tau/r-(1-exp(-r tau))/r^2].

In general, with q<1, the log squared-norm growth is bounded by

  [2R^2 c/(1-q)] integral_a^b ||B(t)||dt.

Thus the short-time scale can return to O(c tau); the c/r endpoint estimate is not a physical floor at zero duration. These variants require their own exact arithmetic treatment if used by a compiler; (7) is the main received formula here.

The conditional theorem itself does not acquire a real experimental generator. For known finite local matrices, coefficientwise G^*K=-rK is an exact linear identity, and the support/control conditions are explicit. An unknown physical apparatus needs a calibrated uniform residual and a separate robust receiver. A small empirical covariance is not enough. This document does NOT yet transfer the derivative-based approximate-J bound from the previous theorem: its backward integral propagates future K under the actual generator, and any approximate receiving must be derived explicitly.

## 6. Scope of the added consequence

The thermal X example remains an ordinary exact telegraph reduced process. Depolarizing sources with multiple noncommuting Pauli coefficients are genuinely within the same operator proof, without a classical commuting source dictionary. Standard finite-dimensional propagation is still a strong comparator for one patch.

The proposed general consequence is that arbitrary source-blind gate/instrument complexity within a fixed local patch need not increase the high-order fault-admission budget when the ACTUAL unwanted observable lies in an acquired decaying source eigenspace. The device still pays for the gate, the source dynamics, its initialized Markov ports and actual imperfections. This removes the previous proof's artificial integrated-control-variation burden; it does not erase an unsuppressed coupling bias or prove an efficient new quantum-computing architecture.

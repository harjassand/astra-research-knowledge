# Unknown-coset buffer from a shared noisy baseline: global-energy proof
2026-10-30. New candidate, using the frozen PERSISTENT_BASELINE_GPT_ANALYSIS.md identities. This is a native Poisson-CPTP *quantum-controller* extension conditional on a stable shared baseline, not a proof that the baseline hardware is reliable.

## 1. Interface and invariant
Fix one CSS sector and a true initial syndrome s0. Initial DATA occupy an arbitrary logical state in that syndrome coset. Choose any Pauli P_s0 mapping the ordinary code to that coset, solely as a mathematical reference; no computation or physical application of P_s0 is required. A recorded baseline m0=s0+eta is shared by all readers of each potential view. It is fixed during the buffered wait.

Let e be the actual Pauli error relative to that INITIAL coset. The controller sees H_v e+eta_v. With B={v:eta_v!=0}, b=|B|, and w the fixed view size, the frozen proof establishes

    U_eta(e)=sum_v t_v(H_v e+eta_v)>=0,
    |U_eta-U|<=wb,
    |U_eta(e+f)-U_eta(e)|<=2|f|.

Every accepted correction strictly decreases U_eta. The existing no-op convention on incompatible multi-view tuples is allowed: only hubs near B can differ from the true GPT decisions.

Before the relative error leaves the ordinary small-reduced-weight radius, the actual-good-service packing argument gives, for fixed physical windows j,

    u_(j+1) <= (1-a)u_j+A Q_j+B_M M_j+C_B b,          (1)

with fixed a>0 and constants A,B_M,C_B. Here u_j=U_eta at the window boundary, Q_j is the all-DATA support-multiplicity majorant, and M_j is the all-DATA actual-good-service miss majorant. The baseline is not treated as fresh noise each window.

The finite controller implements this modified local table by XORing the shared view baseline into each read value. Baseline resources must be included in read locks, footprints, and constant-incidence support budgets. Since their local alphabets and table lengths are fixed, take worst-case finite compiler/service constants over all program values. No ideal syndrome measurement or perfect quantum scheduler is substituted.

## 2. Fixed good event and a uniform energy cap
Choose constants b0,q0,m0>0. Consider the event

    b<=b0 N;   Q_j<=q0 N and M_j<=m0 N for every observed j.

Let

    v*=max{wb0, (Aq0+B_M m0+C_B b0)/a}.

The relative error starts at zero, so u_0<=wb0 N. Equation (1) inductively gives u_j<=v*N. Inside a window, clean steps lower U_eta and bad masks raise it by at most twice their support mass. Therefore

    U_eta(any intermediate event)<= (v*+2q0)N,
    U(any intermediate event)<= (v*+2q0+wb0)N.        (2)

A pre-existing relative residual of weight z0N is allowed by replacing wb0 in v* by 2z0+wb0.

## 3. First-exit argument closes the induction
Let r>0 be fixed, with rN strictly below the original confinement radius and 2rN+s<d, where s bounds any single good/bad Pauli edge support. Choose b0,q0,m0 sufficiently small that

    v*+2q0+wb0 < h r/2.                              (3)

Suppose a branch first reaches reduced weight >=rN. Immediately before that local edge its reduced weight is at least rN-s, because minimum syndrome weight changes by at most the edge support. It is still inside confinement, so its TRUE potential obeys U>=h(rN-s). For sufficiently large N this contradicts (2)-(3).

This proof is not circular: candidate packing for a window needs only its safe starting representative. Its energy estimate remains valid even if a later event were to leave the radius. The within-window bound then rules out that first exit. Thus all windows begin safely, all branchwise reduced weights stay below rN, and (1) remains applicable indefinitely on the good event.

For consecutive canonical representatives R,R' and local mask f, the same-syndrome difference R+f+R' has weight <d and is therefore a stabilizer. Every local edge has identity logical action in the fixed INITIAL-coset gauge. This proves relative logical preservation, not merely a small syndrome-energy estimate.

## 4. Positive-record quantum bound
The initial baseline defects have a fixed-set LS support bound at small p0, hence a large-total-weight tail Pr(b>b0N)<=exp(-c0N), after bounded view enlargement. This event is charged ONCE.

The native uniform positive-record moments, queried on the fixed all-DATA set, give

    ||instrument{Q_j>q0N}||_diamond <=exp(-c_Q N),
    ||instrument{M_j>m0N}||_diamond <=exp(-c_M N),

when the native noise and service-miss parameters are sufficiently small. Their bounds are unconditional from the original initialized state. No independence across windows, from eta, or from a retained bath is required. Union-bound the positive instruments over L windows:

    delta <= exp(-c0N)+L[exp(-c_QN)+exp(-c_MN)].       (4)

The actual baseline-acquisition record must supply a common support/defect majorant for every Pauli coefficient history. On the complement of (4), all compatible histories have the same relative logical identity. The common-correctable-span argument therefore gives a relative decoded diamond error <=2delta, with an additional initial preparation error if supplied by the source. Both CSS sectors are handled by a finite union and common worst-case constants.

This establishes exponential-duration relative protection for the linear-distance Tanner family, conditional on the baseline/read interface. Unlike the full animal argument, it pays global rare windows and uses the linear total-weight radius. It must not be transplanted to a sqrt(N)-radius family at fixed fault density.

## 5. What the decoder means
The mathematical final decoder is relative to the TRUE fixed initial coset s0, not to the noisy record m0. The theorem does not assert that applying an ordinary zero-syndrome decoder to the buffered physical DATA retrieves the logical state. Its operational purpose is to keep the pre-feedforward quantum boundary intact while its original factory Pauli correction is calculated.

Once that factory correction is actually applied, the original preparation theorem controls the resulting target-code residual. The buffer residual is then added to it, rather than pretending an arbitrary signed coset was already the ordinary code. See PENDING_FRAME_HANDOFF.md for the candidate controlled frame reconciliation.

## 6. Remaining physical resource
A fixed baseline is a real program memory. Unprotected baseline bits do not satisfy this premise for a long wait. Readers must share the same value for each view; the frozen file's two-owner counterexample shows why inconsistent private copies destroy finite work. Baseline protection, its noisy initial write, and access timing need their own quantified construction. The present result removes high-energy DATA decoding as a mathematical necessity; it does not make reliable classical records free.

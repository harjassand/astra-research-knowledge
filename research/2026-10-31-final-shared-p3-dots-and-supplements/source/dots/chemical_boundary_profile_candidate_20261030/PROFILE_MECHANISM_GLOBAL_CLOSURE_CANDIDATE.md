# Closing the actual profile mechanism on the low-A bottleneck test
Status: personal candidate, unreviewed. This is a demanding test of the composition-dependent return principle, not a general weak-reversibility theorem or a mission endpoint.

## Governing test contract
Use the multi-seed graph contract in FULL_CYCLE_INCOMING_PROFILE_CANDIDATE.md, 2<=a0<m, v=m-a0>0, q>m, with fixed positive coefficients. This includes the deficient-1, non-complex-balanced witness where the uniform scalar T/U gap is provably false. The new ingredient is a graph-earned bad-return operator, not another favorable scalar-gap hypothesis.

The candidate dependency closure is:
1. INCOMING_MOMENT_MEMORY_LEMMA_CANDIDATE.md: actual inverse-A profile transport and incoming-dependent killed-time bound.
2. BOUNDARY_RETURN_NEUMANN_PRINCIPLE_V1.md: exact positive-kernel section correction.
3. FULL_CYCLE_INCOMING_PROFILE_CANDIDATE.md: graph-derived whole-cycle profile/entry estimates and good-region occupation gap.
4. This file: actual N-directed cost and complementary infinite-strip closure.

None of these new files inherits the independent reviews of the earlier pure-source or A=1 siphon families.

## 1. The corrected section value pays actual cost
For each fixed theta>0 and integer j>=0 apply the operator construction with base weight Psi_j(r)=(1+r)^j exp(theta r), g(r)=r^-v, and bad set A<=r^gamma, where 0<gamma<min(v/m,v/(v+1)). Use the exact same shift-wise whole-cycle bounds for Psi_j; no differentiation of the previously constructed correction is needed.

The constructed correction H_j is supported on the bad section and satisfies 0<=H_j<=C g Psi_j. Its actual return drift is <=-c g Psi_j on bad inputs and <=-c U Psi_j on good inputs. Clearing-first probability tends uniformly to1, so the hazard comparison gives U>=c r^{-(m-1)} on every active section state. Since v<=m-2, g>=c r^{-(m-1)} as well. Choose j=m-1. Then

    P(Psi_j+H_j)-(Psi_j+H_j)<=-c exp(theta r).

The whole-cycle physical running exp(theta r)-cost is <=C exp(theta r), including actual seed waiting and all repair rounds. Telescoping the actual full-state section chain therefore earns the N-directed stopped value

    W_r=E int_0^{tau_{r<=r0}} exp(theta r_s)ds
        <=C(1+r)^(m-1)exp(theta r),
    LW_r=-exp(theta r) above threshold.

Arbitrary low or inactive initial inputs need only a fixed number of initial seed/race upward steps, so exponential weights pay a fixed multiplier rather than the factorial polynomial surcharge. Only constant-rate immigration can enter the positive domain from r<=r0; the target residual lies in a finite band. Thus (LW_r)^+<=C outside the domain, uniformly in the hidden populations.

## 2. The infinite inactive strip is not a finite head
Let I indicate an enabled composition source and Z=B-N-hI, h=q-m. The exact increment identities remain unchanged. For A>=a0, inactivity implies A<=m-1 and each reservoir count <=v-1. Such inactive states have N<=K0=(m-1)+(d-1)(v-1). But A<a0 permits arbitrarily large N. It would be false to put the entire inactive set into a finite phase alphabet.

A naive protocol requiring a0 consecutive immigrations at large hidden N would also be wrong for a uniform fixed-Z time bound: at positive A, activation competes at rate AB, and B=z+N can be arbitrarily larger than z. The correct protocol uses activation to seed the fast graph and the OUTPUT law to exit.

## 3. Large hidden-N blocks use output activity, not rapid mixing
The normalized active clearing time is uniformly bounded over N: use T<=CN^-v A^(1-a0) for large N and finite complex-path access on each small active class. The clearing compensator and A<=C[1+(A)_m] give a uniform normalized A-occupation bound. Therefore, uniformly over active composition and B>=q,

    P(activation before clearing)<=CB^(1-q),
    P(immigration before clearing)<=CB^-q,
    E(first connector time)<=CB^-q.

The actual clearing-output inverse-m-th moment is <=Cp0(N). Hence its probability of landing at A_after<a0 is <=C p0(N). For N larger than a fixed H>K0+m, every remaining inactive target must have A_after<a0, so a clearing stays active with probability at least1-Cp0(N), apart from the already bounded competing births.

- Large-N active start: prescribe clearing; with probability bounded below uniformly, its target remains active, giving a down Z exit.
- Large-N inactive start with A>=1: prescribe activation before immigration (probability1-O(1/B)); activation produces at least m A and enables the fast graph. Then prescribe clearing with an active target. This gives a down exit with uniform positive probability.
- Large-N inactive start with A=0: its next event is compulsory immigration with constant mean waiting time. Then apply the preceding case, unless activity has already turned on and exited down.

Every large-N block has bounded expected duration and down probability >=c>0. The only up possibility is an activation while already active, with probability <=Cz^{-(q-1)}. This is an actual output-kernel argument; it does not assume fast equilibrium or replace B by z in an immigration race.

For N<=H use the finite-head protocol from the reviewed trace: neutral inactive activation plus clearing decreases N by1; at most H such pairs reach A=0 or exit down. At A=0, at most m immigrations enable mA, and at most m-1 noncompulsory races each win with probability >=c/z because N remains bounded in this protocol. Thus, uniformly over all hidden states,

    P(block down)>=cz^{-(m-1)},
    P(block up)<=Cz^{-(q-1)},
    E(block time)<=C.

Conditional renewal earns first actual residual exit probability up<=Cz^-h and mean time<=Cz^{m-1}. The infinite inactive strip has been treated explicitly, not capped.

## 4. Exponential complementary cost and global comparison
For each theta>0, the Z-exit weight ratio obeys

    E exp(theta Z_exit)/exp(theta z)
       <=exp(-theta h)+Cz^-h exp(theta h)<1

for sufficiently large z. The same holds after a fixed polynomial enlargement. Thus the actual stopped value W_Z with running cost exp(theta Z) is finite and <=C(1+Z)^(m-1)exp(theta Z). Its generator is -exp(theta Z) above its threshold; its exterior positive leakage is <=CAB on an infinite threshold strip.

Both stopped values have first-holding lower bounds exp(theta residual)/poly(1+N+B). Their residual geometry is unchanged:

    max(r,Z)>=c(N+B)-C, c>0.

Their sum is normlike. On either threshold cylinder, the other exponential drift dominates the actual polynomial leakage. Choosing theta sufficiently large for any desired total-count exponential cost yields the stopped Foster bounds for every such cost. Nonexplosion follows independently from L(1+N+B)<=C(1+N+B), since fast reactions preserve N,B. Classwise recurrence and invariant exponential moments would then follow by the same stopped occupation/regeneration argument.

## Exact scientific scope
The new closure is conditional on the correctness of the full-cycle incoming-profile construction and its bad-entry estimate, which have not been independently audited. It is not a theorem for all weakly reversible graphs. Its importance, if validated, is that the boundary section potential is now SOLVED from a graph-earned small return operator and retains the A reserve through an entire physical cycle, even where the scalar occupation gap is rigorously impossible. Generalizing this structural profile to arbitrary boundary faces, not increasing catalyst orders, is the consequential remaining objective.

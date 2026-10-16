# Minimal staggered refresh: bounded investigation

Date: 2026-10-16. This directory is independent of the delivered synchronized proof packet. No acquired code was executed, no software was installed, and no external state or canonical packet was changed.

## Result and limits

**The actual minimal staggered product remains unresolved by this investigation.** No admissible violation of Q1 Q2 was found, and no proof of that target is claimed. In particular, the exact functional counterexamples below are not Hamiltonian counterexamples.

Two rigorous results were obtained:

1. For arbitrary staggered schedules, the endpoint joint effect is bounded by

       min(Q1 C2, C1 Q2) P_s,
       C_i = min(1, sum_k s(a_ik)),
       s(a) = sin^2(min(a, pi/2)).

   This improves the previous C1 C2 certificate and applies to both the broad parity contract and the original factorized virtual-seed subclass.

2. The apparent replacement proof using only entire type, uniform norm, gap-deletion nullities, and orthogonal mismatch branches is false, even with each branch's full odd/even gap parity. There is an exact strictly contractive vector counterexample with excess 5/1323 over the proposed two-gap Q bound. Even an entire lossless unitary completion does not supply the missing chronological record structure.

The bounded diagnostics consist of 36 local optimization runs, 13,471 objective evaluations total, in the explicitly described families below. Their nonviolations are not evidence of a theorem or a certified exhaustive search.

## Contract and actual schedule

There are exactly two internal pinches: Z1 at t1 and Z2 at t2, with 0<t1<t2<T, and both parities are measured at the endpoint. No missing pinch was inserted. H0 preserves both parities; V_i is odd only in its own parity and preserves the other. All interactions are fixed independently of private signs. Finite baths and a reference are allowed, with a specified initial joint parity sector P_s.

Let the own-gap actions be

    alpha = integral_0^t1 j1,   beta = integral_t1^T j1,
    gamma = integral_0^t2 j2,  delta = integral_t2^T j2.

Write p=s(alpha), q=s(beta), r=s(gamma), u=s(delta). Then

    Q1=p+q-pq,  Q2=r+u-ru,
    C1=min(1,p+q),  C2=min(1,r+u).

The original source scalar-to-operator sine lemma and singleton own-gap Q theorem are used below, with their stated hypotheses. The synchronized packet itself is not changed.

## Exact improved asynchronous certificate

Work with the actual record isometry W, retaining all prescribed records. For each own gap k of coordinate 1, let R_k project onto the output event that both terminal parities flipped and that coordinate 1's **first** recorded mismatch occurred in gap k. These projectors are fixed, mutually orthogonal output projectors. They partition the terminal double-flip event, since a terminal flip entails at least one recorded mismatch.

Scale V1 only within its k-th own gap by a parameter z and set

    F_k(z) = R_k W_k(z) P_s.

For every real z, coordinate 2's singleton theorem gives

    ||F_k(z)|| <= sqrt(Q2).

Indeed, z V1 remains Hermitian and preserves Z2, so it is part of a permissible coordinate-2 baseline; its size is unrestricted in that singleton theorem. The intervening coordinate-1 pinch also preserves Z2. Projection onto an additional coordinate-1 record event cannot increase the norm. This is an unconditional operator bound, not a statement conditioned on a future coordinate-2 error.

Deleting V1 throughout gap k makes a coordinate-1 mismatch across that gap impossible, even though coordinate-2 operations can lie inside the gap. Hence F_k(0)=0. The Dyson/record-isometry argument gives entire type at most a_1k. The scalar-to-operator sine lemma therefore yields

    F_k(1)^* F_k(1) <= Q2 s(a_1k) P_s.

Sum over the mutually orthogonal first-mismatch records:

    effect(terminal double flip) <= Q2 sum_k s(a_1k) P_s.

The coordinate-2 marginal gives the additional cap Q2 P_s, so the same effect is bounded by Q2 C1 P_s. Exchange the coordinate names to obtain Q1 C2 P_s and take the smaller scalar bound. This proof neither inserts pinches nor conditions on future errors.

For the minimal two-gap schedule, if p+q<=1 and r+u<=1, the remaining slack above the target is explicitly

    min(Q1 C2, C1 Q2) - Q1 Q2
      = min(Q1 r u, Q2 p q).

Thus one full own-coordinate survival discount is retained at a time; retaining both simultaneously is still the open step.

## Why the attempted whole-vector Q contraction fails

A natural attempted proof first obtains a uniform amplitude bound sqrt(Q1), then tries to apply a generalized two-gap sine lemma to coordinate 2's orthogonal first-mismatch output branches. The presumed lemma would upgrade that uniform bound to sqrt(Q1 Q2) solely using the two gap types and deletion-nullities.

That lemma is false, even with the full branchwise parity symmetry. Set a=b=arccos(2/3) and

    F(z,w) = (sqrt(20)/7) (
       sin(az) [1+cos(bw)/2],
       sin(bw) [1+cos(az)/2]).

The first component is odd/even and null at z=0; the second is even/odd and null at w=0. The respective exponential types are at most a,b. The exact real-plane norm maximum before the scalar prefactor is (9+6 sqrt(3))/8 <49/20, so ||F||<1 globally. Nevertheless

    ||F(1,1)||^2 = 3200/3969,
    1-cos^2(a)cos^2(b) = 3185/3969.

The gap is 5/1323>0. The full algebraic global-norm proof is in functional_obstruction_exact.md.

That file also supplies a lossless entire Householder completion with the same analytic nullity/parity features and a larger exact functional violation. Its full output-state overlap depends on the later-gap variable, whereas a complete chronological isometric continuation preserves overlaps between different earlier-gap inputs. This explicitly shows why that particular completion is not the required causal record dilation. It does not rule out every possible causal completion of a projected amplitude.

**Model classification:** these exact examples are failures of an abstract analytic lemma, not established members of either the broad admissible Hamiltonian/history model or the original factorized virtual-seed model. They must not be advertised as counterexamples to Q1 Q2.

## Bounded small-matrix diagnostics

All searches were declared before their corresponding runs. The original two-family search was followed by exactly one targeted sink extension because the initial families did not contain the multi-gap sharp sink witness. Numerical search stopped after that extension. L-BFGS-B's maxfun=400 is a nominal per-run budget: its final finite-difference/line-search iteration was allowed to complete, so several runs slightly exceed 400 evaluations. Actual totals are reported, not hidden.

### Six-pulse factorized and parity-edge families

Set t1=1,t2=2,T=3. In each elementary interval there is one pulse of each interaction, in one of two tested orders: 1 then 2 in all intervals, or 2 then 1 in all intervals. The six pulse actions in coordinate-labeled order are a0,...,a5, giving own-gap totals (a0,a2+a4) and (a1+a3,a5). Every pulse occupies half of an elementary interval; H0=0.

- Family F: two seed qubits and one shared bath qubit, dimension 8. Each pulse is exp(-i a_k H_k), with H_k=X_seed,i tensor A_k, where A_k is a Pauli-axis Hermitian involution on the shared bath. This **is** in the original factorized virtual-seed subclass. The objective is the largest eigenvalue of the endpoint effect over the initial bath, divided by Q1 Q2.
- Family P: two parity qubits without a bath, dimension 4. Each H_i consists of the two own-parity-flipping edges with independently adjustable complex phases and unit modulus; H_i^2=I. This is in the broad parity model. Generic conditional edges are **not** factorized virtual-seed interactions.

For each family: three action scale ceilings 0.15,0.45,0.72, two pulse orders, and two deterministic initial parameter vectors; 24 runs in total. Each of the six actions was parameterized by scale*(0.15+0.85 logistic(v)), v in [-4,4]. The two angular parameters for each pulse lay in [-2pi,2pi]. The complete script and output are search.py and search_results.json.

Actual objective evaluations: 9,804. Largest reported ratios:

- Factorized shared-qubit-bath family: 0.9988300847192422.
- Bath-free broad parity family: 0.9986994344734769.

Optimizers often reduced some actions toward their lower allowed boundary. Approaching one in this regime is not a structural proof.

### Nine-dimensional sink extension

Use two three-level spaces with basis 0,E,L and parity diag(1,-1,-1). Their tensor product has dimension 9. For coordinate 1, the first own-gap pulse couples 0 to E, and the second own-gap pulses couple 0 to L; for coordinate 2, the first own-gap pulses couple 0 to E and the last pulse couples 0 to L. Old sink states are isolated from later own-gap drives. Each coupling has an independent phase for each of the other three-level coordinate's states. Every Hamiltonian is an own-parity odd, other-parity preserving partial isometry with norm one.

This is a broad parity model on finite sector spaces. Generic conditional phases and the unequal sector dimensions do not supply a literal X_seed,i tensor A_i realization. No such classification is claimed.

All six pulses had the same fixed action theta, with theta=0.15,0.45,0.7. Test both global pulse orders and two deterministic starts (one close to all-zero phases and one spread over phases), for exactly 12 runs. Scripts and output are search_sink.py and sink_results.json.

Actual objective evaluations: 3,667. Optimized ratios never exceeded one beyond floating-point roundoff. The all-zero phase member has an **analytic** independent-coordinate equality witness:

    P_i(endpoint flipped)=sin^2(theta)+cos^2(theta)sin^2(2theta)
                         =1-cos^2(theta)cos^2(2theta)=Q_i.

The two coordinate channels factor, so the joint value is exactly Q1 Q2. This confirms that the family probes a sharp witness; it still does not certify that the optimized family, or the general model, cannot violate the bound.

## Verification boundary and next decisive step

No purported Hamiltonian violation exists here to be exact-certified. Numerical values are diagnostics only. The positive bound and functional obstructions have analytic proofs. The exact sink equality follows directly from disjoint sink transitions and factorization.

A decisive next step would need either a causal-record inequality that preserves the other coordinate's full Q contraction through an own-gap survival branch, or a concrete Hamiltonian/process realization violating Q1 Q2 with exact or rigorous error-enclosed verification. Uniform entire type, deletion-nullity, branchwise parity, and lossless completion alone cannot be substituted for that causal argument.

No endpoint label is interpreted as a physical fault or a hardware capability. No physical implementation claims are made.

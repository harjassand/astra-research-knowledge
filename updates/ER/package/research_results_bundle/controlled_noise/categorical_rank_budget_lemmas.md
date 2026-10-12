# Discrete categorical faults: pair representation and rank-budget Poissonization

Supporting lemmas, 2026-10-12. These support the extension with the compressed linear-control Poisson compiler. All vectors below are in F_2^D. Deterministic controls have already been pushed into the final output frame.

## 1. Exact pair representation of any categorical law

For any vector-valued distribution mu, draw X,Y independently from mu and an independent fair bit a. Then

    X+a(X+Y)

has law mu: it is X when a=0 and Y when a=1. Thus a state with conditional law C+Uniform(W), followed by one independent mu slot, has the exact positive hidden update

    C <- C+X,
    W <- W+span(X+Y).

The new uniform-subspace law follows from uniform convolution. No symmetry, laziness, or lower atom bound is required for this identity.

A supplied mode b may first be removed from mu. Its deterministic contribution is propagated and accumulated by the control grammar. For a law with at most s explicitly listed atoms, the centered law has mass at least 1/s at zero. If a centered atom v outside W has mass at least tau, then the pair update increases rank with probability at least

    2 mu(0) mu(v) >= 2 tau/s.

The two disjoint events are (X,Y)=(0,v) and (v,0).

## 2. Exact local Poissonization bound from an affine-uniform input

Let a slot add one random vector J of law mu to C+Uniform(W), and put

    q=Pr(J outside W).

Every mark in W is absorbed by Uniform(W). Consequently the slot's physical endpoint law is obtained by drawing a Bernoulli(q) count and, when it is one, adding a mark sampled from mu conditioned outside W.

The compound-Poisson law with unit intensity measure mu, applied to the same input, is also unchanged if all initially-inside-W marks are deleted. This is true because all translations commute, and translations in W preserve every translate of Uniform(W). Its physical endpoint is therefore obtained from a Poisson(q) count of the same conditioned marks.

Data processing and the exact Bernoulli-Poisson count distance give

    TV(discrete-slot output, Poissonized-slot output)
       <= TV(Bernoulli(q),Poisson(q))
       = q(1-exp(-q)) <= q^2.                         (1)

Here q<=1. This bound concerns the physical output law, not necessarily any arbitrarily chosen pair of hidden-state representations.

For a discrete heatbath slot I+p(K-I), where K adds a fair multiple of a random direction, its hidden span transition has actual innovation probability q_span=p a(W), with a(W) the probability that the direction is outside W. Discard initially-inside marks permanently. Applying the same count comparison directly to the hidden process gives

    TV(hidden one-slot kernels from W)
       <= [p a(W)](1-exp[-p a(W)])
       <= p^2 a(W)^2.                                (2)

In particular this implies the looser p^2 a(W) bound.

## 3. Global rank budget

For a sequence of discrete heatbath span kernels, use the telescoping identity with original prefixes and Poissonized suffixes. Total variation contracts under every suffix. Under the original prefix, the expected rank increase at slot i is exactly p_i a_i(W) for a one-direction update. Since rank starts nonnegative and increases at most D times,

    sum_i E[p_i a_i(W)] <= D.

Thus if p_i<=p_max throughout the sequence, (2) or its weaker version gives total endpoint error at most D p_max. No expanded slot count appears.

The original-prefix qualification matters: it is what makes the rank budget available despite exponentially many slots. The bound is not an assertion of small operator norm error on every point state.

## 4. All explicitly listed finite categorical slots

For each distinct slot type, center at a mode b and propagate all such deterministic drifts globally. Let s bound its support size. Classify each centered atom of probability at least tau as heavy.

Precompute the coefficient-image spans of only the heavy centered directions in every control-grammar node. A supplied suffix context M transforms these directions into the final frame. If the transformed heavy span lies in W, that entire subtree contains no heavy atom that can enlarge W. Otherwise descend to an occurrence with a heavy outside atom. Binary repetitions are already compiled into a polynomial-size concatenation DAG.

Process that one complete categorical slot using the exact pair update in Section 1. Track its representative shift C. Remove only that occurrence from the residual noise grammar by persistent path copying; retain its deterministic control and its already-accounted mode drift. A path has at most the compiled grammar depth, so each deletion adds only polynomially many nodes. Do not subtract it from a positive summary using negative weights.

Each visited slot increases rank with conditional probability at least 2 tau/s. There are at most D rank increases, so expected visited occurrences are at most D s/(2 tau). A negative-binomial tail cap gives bounded polynomial work. The selected occurrences may depend on previous revealed pairs: unrevealed slots remain independent with their original laws, because no unrevealed random value was inspected. Span unions and additive offsets commute in the final frame, so this adaptive reveal order is valid.

When no heavy outside atom remains, call the resulting span W*. For every residual slot, the total probability of a centered mark outside W* is at most s tau.

### Residual lazy re-representation

For analysis only, replace every residual mark already in W* by zero. This changes no final physical law from C+Uniform(W*), since all those inside translations are absorbed even in the presence of other additive marks. The resulting residual slot has nonzero probability p_i<=s tau. Provided s tau<=1/2, it has an exact discrete heatbath representation with activation probability 2p_i: conditional on activating, choose a nonzero mark according to its normalized probability and add either zero or that mark fairly.

Apply Section 3 starting at W*. Replacing all residual slots by their physical compound-Poisson laws has total error at most

    2 D s tau.                                      (3)

Choosing tau on the order of epsilon/(D s) makes this error small. The expected number of explicitly processed occurrences is then O(D^2 s^2/epsilon), polynomial even with exponentially many residual slots.

For the actual Poisson compiler, retain all original centered categorical atoms with their original probabilities as physical Poisson intensities. Atoms mapped into W* are null on the initialized Uniform(W*) distribution. Therefore no context-dependent filtered grammar needs to be explicitly built.

The residual leaves are finite explicit weighted mark lists, so they are a particularly simple valid input to the active-mass counting/conditional-acquisition compiler. Fresh categorical draws and exact linear algebra have polynomial bit cost. Its final output is shifted by the accumulated pair offsets C, the precomputed mode drifts, and the clean controlled initial state.

This yields approximate endpoint compilation for arbitrary supplied finite categorical fault laws, with no dominant-atom assumption. The support sizes and probability bit lengths are charged to the input. It does not depend on exact infinite divisibility of an individual discrete slot.

## 5. Structural boundary for nonlinear compressed controls

The linear-control restriction is substantive. If arbitrary supplied Boolean-circuit controls on polynomially many bits may be iterated a binary-encoded number of times, even the zero-noise problem includes deterministic polynomial-space Turing-machine simulation. A next-configuration circuit and an absorbing halt state, iterated for 2^(polynomial input size) steps, reveal the machine's answer. A polynomial-time endpoint sampler with constant TV error below 1/3 for that general interface would imply PSPACE is contained in BPP.

This is a complexity-theoretic boundary, not a barrier for all restricted nonlinear physical models. A further nonlinear extension needs additional structure; it cannot be inferred from the present linear compiler.

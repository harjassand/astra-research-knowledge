# Independent review: parity doubling and resolved-port completion

29 October 2026. Root supplied the two-copy conjecture; the
resolved-port version was independently reached here and by the
controlled_frontier agent. Both are correct at the scope below. These
are abstract CTMC constructions, not physical devices or a determination
of an unknown source's physical time reversal.

## 1. Full two-copy theorem

Let Q be a finite irreducible row generator, pi>0 its stationary law,
and Q*=diag(pi)^-1 Q^T diag(pi). Stationarity implies q*_xx=q_xx and
the same escape rate lambda_x in both generators. Define

    L_eps=[[Q-eps I, eps I],[eps I,Q*-eps I]],
    mu(x,+)=mu(x,-)=pi_x/2,
    Theta(x,+)=(x,-).

For eps>=0, mu is stationary and Theta invariant. For every directed edge,

    mu_z L_eps(z,z')=mu_(Theta z') L_eps(Theta z',Theta z).

Within one layer this is exactly the definition of Q*. A sign-flip edge
maps to itself under the combined reversal/parity operation. Escape rates
on paired states are both lambda_x+eps. These identities prove equality
of every stationary full-path density and its parity-reversed density:
initial weights, all holding factors, and telescoping jump factors match.
Generalized stationary entropy is therefore zero, with no missing holding
or endpoint term. Ordinary all-even entropy is a different quantity and
can remain positive.

For eps>0 the chain is irreducible. At eps=0 there are two closed components,
so only the positive-eps chain belongs to an irreducible model class.

If observation ignores sign, the eps=0 visible path law on [0,T] is

    P_sym=(P+P^rev)/2.

Here P is the original STATIONARY visible path law. The independent
state-independent sign-flip clock gives the exact decomposition

    P_eps=exp(-eps T)P_sym+(1-exp(-eps T))R_eps,
    TV(P_eps,P_sym)<=1-exp(-eps T).

In particular, if P is reversal invariant, the approximation is to P itself.
No stronger equivalence for arbitrary P was silently used. Indeed, any
reversal-invariant law R obeys TV(P,R)>=TV(P,P^rev)/2, and P_sym attains
this lower bound. Thus the distance to the fixed-horizon closure of finite
irreducible hidden-parity equilibrium explanations is exactly this half-
asymmetry distance for every visible law arising from such an original Q.

## 2. Preparation qualification and finite-data implication

Stationary preparation mu is substantive. Starting at one layer's (x,+)
reproduces Q until a sign flip but is a parity-asymmetric preparation.
An equal-sign mixture at fixed x gives the mixture of Q and Q* reset laws,
which need not equal the Q reset law. If the stationary visible law is
reversal invariant, conditioning on a visible initial label gives equal
future laws from pi(.|label) in the two layers; this does not establish
arbitrary microscopic preparation equivalence.

The full doubling also duplicates every observed native port. It therefore
does not by itself preserve a singleton-port warranty. Section 3 repairs
that issue exactly for the native excursion interface.

For n independent stationary paths with horizons T_i, independent couplings
give TV<=1-exp(-eps sum_i T_i) to the symmetrized data law. Consequently
any test of generalized equilibrium with false-positive probability <=alpha
uniformly over all finite irreducible parity-equilibrium models has power
<=alpha at a reversal-invariant original visible law, for every such finite
experiment: let eps decrease to zero.

This also holds for a one-path test stopping almost surely in finite time
under the target. First apply the bound to rejection by a deterministic T,
then let eps decrease to zero, and finally T increase to infinity. Uniform
size is essential. This does not say that a particular fixed eps model is
undistinguishable forever, or that supplied mixing/parity information is
irrelevant. Arbitrary interventions are outside this observation-only proof.

## 3. Exact construction retaining every singleton port

Let w>0 be stationary weights, f_xy=w_x q_xy, nonempty B the ports, and
I their complement. Keep each port b as ONE microscopic state of weight
w_b. Replace each hidden x by x+,x-, each of weight w_x/2. Theta fixes
ports and swaps hidden pairs. Set stationary edge flows

    f'_(x+,y+)=f_xy/2,       f'_(x-,y-)=f_yx/2,
    f'_(b,x+)=f_bx/2,       f'_(x+,b)=f_xb/2,
    f'_(b,x-)=f_xb/2,       f'_(x-,b)=f_bx/2,
    f'_(b,c)=(f_bc+f_cb)/2  for distinct ports b,c.

There are no cross-layer hidden edges. Divide each flow by its source's
new weight and set generator diagonals by row sums.

**Theorem.** This finite chain is irreducible, preserves total mass W,
preserves every original escape rate (at each port and both copies of each
hidden state), and satisfies generalized detailed balance under Theta.
Its hidden native excursion flux kernel and direct-jump flux are

    K_tilde(t)=[K(t)+K(t)^T]/2,
    f_tilde,BC=[f_BC+f_CB^T]/2  off diagonal.

The latter notation means the pairwise formula above for port edges.

### Stationarity, clocks and parity

Each hidden plus node receives and sends half its original balanced flux;
each minus node receives and sends the reversed half. At a port, total
outgoing flux is half its original outgoing plus half its original incoming
flux, equal to its original outgoing flux by stationarity. Incoming equals
the same quantity. The new weights therefore give exactly the original
escape rates, which are parity invariant. Total mass is unchanged because
only hidden weights were split. The generalized edge-flow identity follows
term by term from the displayed construction.

### Irreducibility without a slow bridge

Every original hidden state can be reached from a port without another
intervening port, and can reach some port. The plus-layer paths retain
these connections. The reversed original chain is also irreducible, so the
same holds for the minus layer. Original port-to-port connectivity survives
through the plus layer and symmetrized direct edges. Hence all new states
communicate. B nonempty is necessary for this argument; no eps bridge or
small mixing-rate limit is used.

### Complete native-law identity

The plus layer has killed generator Q_II, half the original port-entry
flux, and original hidden-to-port exit rates, contributing K(t)/2. The
minus layer has Q*_II and the reversed entry/exit flows, contributing
K(t)^T/2. Both layers preserve the original microscopic escape rates.
Every retained port hold is exactly its original exponential hold.

Thus whenever K(t) and the direct port flux are already symmetric, the
ENTIRE native event-time law is identical, including self returns, holds,
resolved reset ports and stationary departure intensities rho_i=w_i lambda_i.
Strong Markov regeneration at singleton ports extends this from one
excursion to every sequence of excursions and every adaptive choice of
which port to reset to. Stationary partial-cycle laws also agree: the
marked excursion kernel, Palm intensities and total mass W are preserved.

The observation here distinguishes ports and native excursion durations;
it does not reveal arbitrary additional labels inside I. If those are
observed, their complete marked excursion law needs the corresponding
reversal symmetry for the same argument to apply.

The state count is |B|+2|I|. All source rate ceilings and all known singleton
port preparations survive. Known hidden initial preparations or separately
specified interventions need not survive; a baseline construction supplies
neither their causal action nor a native physical parity implementation.

## 4. Exact rational nontrivial example

Take weights w=(1,2,3), clockwise cycle flows 2 on 0->1->2->0 and reverse
flows 1. Then

    Q=[[-3,2,1],[1/2,-3/2,1],[2/3,1/3,-1]],
    pi=(1/6,1/3,1/2),
    ordinary sigma=(1/2)log 2>0.

Retain singleton port 0 and hide states 1,2. Native port holds are Exp(3).
The hidden excursion Laplace transform from port departure to its return is

    Phi(s)=[(5/9)s+7/6]/[s^2+(5/2)s+7/6].

Direct two-by-two inversion gives exactly the same formula under Q*.
Thus the binary port/interior process is an alternating regenerative
process with a reversal-invariant stationary visible law despite positive
ordinary microscopic entropy. The full doubling gives six states. The
port-preserving construction gives five states, is irreducible, keeps the
port as one microscopic state fixed by parity, and exactly preserves the
native law without an epsilon limit. It has generalized entropy zero but
the same positive ordinary all-even entropy as the original chain.

## 5. Consequence and limitation

If the admissible explanation class leaves hidden parity unrestricted,
every reciprocal native excursion law of this form admits an exact finite
irreducible generalized-equilibrium explanation with the same singleton
resets and clocks. No amount of data from that identical baseline interface
can distinguish the explanations, including data beyond a finite horizon.

This does not invalidate the earlier all-even copositive certificate: its
physical reversal premise excludes the alternative model. The omitted
information is a physically warranted reversal or an additional intervention
interface. The construction establishes an abstract explanatory equivalence,
not that the physical source actually contains doubled odd states.

## 6. Independent executable checks

`check_parity_doubling.py` completed with PASS. It uses rational arithmetic
throughout the generator, stationary-weight, parity-flow, clock, direct-flow
and Laplace-transform checks. It generated no source observations and read
no native raw-record or private-source inputs.

The checks cover both full lifts of the nonuniform three-state chain at
eps=0 and eps=1/7; glued lifts with one, two and three retained ports; and
the accepted fifteen-state five-port source's algebraic generator. The
last source becomes an irreducible twenty-five-state parity-equilibrium
model preserving its five singleton ports and complete reciprocal native
law. Twenty exact Laplace-matrix checks at rational arguments validate
the displayed symmetrization against separately inverted killed generators.
Five additional exact checks verify the rational one-port formula above.

The nonreciprocal two-port test correctly produces a changed, symmetrized
law, rather than falsely preserving it. The all-ports test reduces to the
ordinary additive reversibilization, with zero ordinary entropy. The
one-port and fifteen-state tests retain positive ordinary all-even entropy
while their generalized entropy is exactly zero. These distinguish the two
reversal conventions rather than conflating their numerical values.

The executable checks are finite algebraic controls. Section 3's proof
establishes the all-time kernel identity, and Sections 1–2 establish the
full-path and statistical conclusions. Detailed results are recorded in
`PARITY_DOUBLING_CHECKS.json` together with the checker SHA-256.

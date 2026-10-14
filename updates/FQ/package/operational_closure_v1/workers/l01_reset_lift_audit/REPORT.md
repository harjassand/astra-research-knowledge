# Independent audit: reset-state double lift

## Finding

For every finite irreducible row-generator $Q$ on a state space $S$ with $|S|\ge2$, and every distinguished state $a\in S$, the proposed lift is an exact mathematical construction whose stationary binary observation law agrees with that of $Q$. The visible map sends $a$ to $A$ and every other state to $B$. This equality holds for every branch-flip rate $\varepsilon>0$. The lift is irreducible and reversible under the formal odd-parity involution $\theta(i,+)=(i,-)$.

The strongest qualification is interpretive. The construction has zero pathwise relative entropy with respect to the chosen $\theta$-reversal. Calling that quantity *physical* entropy production requires a physical model in which the branch is a genuine time-odd variable and the rates admit the appropriate local-detailed-balance interpretation. Under ordinary reversal that fixes the branch, a nonreversible $Q$ generally retains positive entropy production (or can have singular forward and reverse path laws when reverse edges are absent).

## Construction and notation

Use the row-generator convention, so $Q\mathbf 1=0$, and let $\pi$ be the strictly positive stationary column vector, $Q^T\pi=0$. Define
$$
Q^* = D_\pi^{-1}Q^T D_\pi,\qquad
\lambda=-q_{aa}=\sum_{j\ne a}q_{aj}>0,\qquad
B=S\setminus\{a\}.
$$

The lift has states $S\times\{+,-\}$. In branch $+$, use the off-diagonal rates of $Q$; in branch $-$, use those of $Q^*$. Add rate $\varepsilon$ between $(a,+)$ and $(a,-)$, with the same rate in each direction. There are no branch flips away from $a$. The visible map forgets the branch and maps the state coordinate to $A$ at $a$, and to $B$ otherwise.

The stationary law is $\widetilde\pi(i,s)=\pi_i/2$. Within each branch the stationary flows balance by $Q$ or $Q^*$; the two extra flip flows at $a$ cancel. Irreducibility follows because each branch is irreducible and the positive-rate flips connect the branches at $a$.

## Exact B-dwell identity

Let $T=Q_{BB}$, $u=Q_{aB}$ (a row vector), $r=Q_{Ba}$ (a column vector), and $D_B=\operatorname{diag}(\pi_i:i\in B)$. Irreducibility makes $T$ transient. Row sums give $r=-T\mathbf 1$, and stationarity restricted to $B$ gives
$$
\pi_B^T T=-\pi_a u.
$$

After leaving $a$ in the $Q$-branch, the entrance distribution into $B$ is $\alpha=u/\lambda$. Its B-dwell survival function is
$$
S_+(t)=\alpha e^{Tt}\mathbf 1.
$$

For the reversed branch, $T^*=D_B^{-1}T^TD_B$. Its own exit-flux distribution from $a$ is
$$
\alpha^*=Q^*_{aB}/\lambda
=\frac{r^T D_B}{\pi_a\lambda}.
$$
Stationarity at $a$ gives $\sum_{i\in B}\pi_iq_{ia}=\pi_a\lambda$, so $\alpha^*$ is normalized. Then for every $t\ge0$,
$$
\begin{aligned}
S_-(t)
&=\alpha^*e^{T^*t}\mathbf 1\\
&=\frac{r^T e^{T^Tt}\pi_B}{\pi_a\lambda}
 =\frac{\pi_B^T e^{Tt}r}{\pi_a\lambda}\\
&=-\frac{\pi_B^T e^{Tt}T\mathbf 1}{\pi_a\lambda}
 =-\frac{\pi_B^T T e^{Tt}\mathbf 1}{\pi_a\lambda}\\
&=\frac{u e^{Tt}\mathbf 1}{\lambda}=S_+(t).
\end{aligned}
$$
The penultimate equality uses $Te^{Tt}=e^{Tt}T$; the last uses $\pi_B^TT=-\pi_a u$. Thus the two phase-type B-dwell laws coincide at all times, not only in their means or moments. This identity pairs $Q^*$ with its own departure law $\alpha^*$; an arbitrary B-entry distribution would not satisfy it.

## A dwell and independence of visible cycles

At either copy of $a$, the total rate of a visible $A\to B$ departure is $\lambda$. The extra branch flip has rate $\varepsilon$ but leaves the visible label at $A$. The visible departure hazard therefore stays exactly $\lambda$ while the process remains at $a$. Equivalently, the killed hidden two-state generator on the A-fiber is a conservative flip generator minus $\lambda I$, so the survival probability is $e^{-\lambda t}$. Every visible A-sojourn is Exp$(\lambda)$, independent of its incoming branch.

Conditional on the branch at the start of a B-sojourn, its duration has the same law $S_+=S_-$. Conditional on the entire observed history before that sojourn and on the branch, the duration still has this same fixed law. It is therefore independent of the prior observed history and hidden branch. At the next visit to $a$, the branch may retain memory, and its orientation at departure can be correlated with the A-sojourn length. But the following B duration has a branch-independent law. Repeating this conditional-factorization argument shows that successive visible A and B durations are independent, with laws Exp$(\lambda)$ and $S_+$.

For the base chain $Q$, visits to singleton state $a$ are regeneration times by the strong Markov property, with exactly these same iid alternating durations. Both chains are stationary, and their A-entry Palm laws have the same iid cycle law with finite mean. The stationary equilibrium version of this alternating-renewal process is unique, so the full stationary binary path laws agree, including the age and residual-life behavior seen from an arbitrary stationary time.

## Reversal and entropy-production scope

Let $\theta(i,+)=(i,-)$ and $\theta(i,-)=(i,+)$. The stationary law is $\theta$-invariant. For same-branch transitions,
$$
\widetilde\pi(i,+)q((i,+),(j,+))
=\frac{\pi_i}{2}q_{ij}
=\frac{\pi_j}{2}q^*_{ji}
=\widetilde\pi(\theta(j,+))q(\theta(j,+),\theta(i,+)),
$$
and the analogous equality holds with the branch labels exchanged. The a-only flip edge obeys the same flux identity because both directions have the same rate and stationary weight. Diagonal holding rates also match under $\theta$: $q^*_{ii}=q_{ii}$, with the same extra $\varepsilon$ at $a$. Thus the stationary path measure is invariant under time reversal combined with $\theta$, and its log Radon–Nikodym ratio against that transformed path measure is identically zero.

This does not imply zero entropy production under reversal that leaves both branches even. If $Q$ has bidirectional support, the ordinary stationary entropy production of the lift equals that of $Q$: each branch contributes half, and the symmetric flip contributes zero. For example, on three states with uniform stationary law, clockwise rate $2$ and counterclockwise rate $1$ give ordinary entropy production $\log 2>0$ per unit time, while the parity-reversed path ratio is zero. If $Q$ has a one-way edge without its reverse, ordinary forward and reversed path laws can instead be singular.

## Scope and edge cases

- The nontrivial alternating-renewal claim assumes $|S|\ge2$, hence $\lambda>0$. For the one-state chain $Q=[0]$, the visible output is constantly A and the lift with $\varepsilon>0$ is still irreducible and $\theta$-reversible; the B-dwell formulas using $1/\lambda$ do not apply.
- The exact observation is only the binary label $A/B$. Resolving B into microstates, seeing branch flips, or observing hidden jump counts can distinguish the branches and is outside the theorem.
- Any $\varepsilon>0$ gives the same visible law. Setting $\varepsilon=0$ removes inter-branch communication, so the lift is no longer irreducible.
- The construction is an exact mathematical kernel. It does not establish that a physical device can implement $Q^*$, the required parity variable, or the flip mechanism at zero thermodynamic cost. Those claims require a specified physical realization and reversal convention.

No numerical test was needed: the claims follow from finite-dimensional generator identities. No external scientific source was used; this is a self-contained derivation and audit of the stated finite-state construction.

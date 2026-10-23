# Weak-prefix audit: occupation ratio versus completed information

This note challenges only the proposed all-control inequality relating raw
occupations. It does not prove or disprove a completed low-risk sensing
protocol. I used the Hamiltonian and noise conventions in the lead-owned
`PASSIVE_REFERENCE_DISSIPATION_OPENING.txt`.

## Short-pulse asymptotics

Take a nonzero nonnegative (C^1) bump (f:[0,1]\to\mathbb R) with
(f(0)=f(1)=f'(0)=f'(1)=0) and (\|f'\|_\infty\le1), for example a
rescaled (s^2(1-s)^2). Let
\[
H_c(t)=B^2h f(t/h)(|a\rangle\langle r|+|r\rangle\langle a|),
\quad 0\le t\le h,
\]
and turn it off after (h). Its norm is at most (B^2h\|f\|_\infty\),
so it respects the (B) amplitude bound for sufficiently small (h), while
\(\|\dot H_c\|\le B^2\). Start in (|r\rangle), with fixed finite (g,\kappa,\gamma\).

Write (F(s)=\int_0^s f(u)\,du) and
\(G(s)=\int_0^s F(u)\,du\). On the rescaled interval (t=hs), the
short-time Dyson/master-equation expansion gives
\[
\langle a|\psi(hs)\rangle=-iB^2h^2F(s)+O(h^3),\qquad
\langle e|\psi(hs)\rangle=-gB^2h^3G(s)+O(h^4).
\]
Here the amplitudes denote the leading coherent terms; fixed Markov dephasing
and loss perturb them only at higher relative order (O(h)). Equivalently,
for the unconditional populations under the stated Lindblad dynamics,
\[
p_a(hs)=B^4h^4F(s)^2+O(h^5),\qquad
p_e(hs)=g^2B^4h^6G(s)^2+O(h^7).
\]
Consequently, with positive constants
\(A_f=\int_0^1F(s)^2ds\) and
\(E_f=\int_0^1G(s)^2ds\),
\[
\int_0^h p_a(t)dt=B^4A_fh^5+O(h^6),\qquad
\int_0^h p_e(t)dt=g^2B^4E_fh^7+O(h^8).
\]
Thus \(\int p_e/\int p_a=(g^2E_f/A_f)h^2+O(h^3)\to0\). No positive
constant (c) can make \(\int p_e\ge c\int p_a\) hold uniformly over
all bounded, derivative-limited controls and arbitrarily short intervals.
The terminal-loss probability accumulated *during this prefix* is exactly
\(\rho_h=\gamma\int_0^h p_e(t)dt=\gamma g^2B^4E_fh^7+O(h^8)\).

At the end of the prefix the sensing modes have not been cleared:
\(p_a(h)=B^4F(1)^2h^4+O(h^5)\) and
\(p_e(h)=g^2B^4G(1)^2h^6+O(h^7)\). The leading (g)-dependent amplitude
is still in the lossy (e) mode. A coherent path that returns a (g)-dependent
amplitude to (r) must contain (r\to a\to e\to a\to r), so its first
possible contribution has two (g) interactions and two control interactions,
of order (g^2B^4h^6) in amplitude. That path-counting observation is not a
measurement or a uniform distinguishability bound. The prefix alone has no
specified safe readout, and its residual (a/e) components cannot be called
exported information merely because they depend on (g).

## What a completed-operation invariant would have to charge

The counterexample rules out a raw (a)-versus-(e) occupation comparison;
it does not evade the lead's fixed-reference coherence bound or supply a new
low-risk operation. To make an information-flow statement operational, the
protocol must be defined through a stopping time at which all parameter-bearing
amplitude is either (i) in a named, readable safe output register, with a
finite calibrated readout map, or (ii) counted as failure. The actual terminal
loss probability must integrate (\gamma p_e) through sensing, transfer,
cleanup, and readout, including every active-reference branch. The final
instrument law must include death, no-click, and abort outcomes; conditioning
on successful survivors alone is insufficient.

If the reference is moved or corrected during sensing, a prospective invariant
must include that branch's occupation/coherence and its coupling to the signal
operator, rather than assuming a fixed noiseless reference column. Any usable
cleanup guarantee must state the available bounded controls and their slew
rates, the time and loss to empty or export (a/e), the reset/preparation cost
for another attempt, memory lifetime of the safe register, and the permitted
measurement record. If these resources are unconstrained, a proof must handle
them explicitly; if they are constrained, their costs and failures belong in
the completed-channel distinguishability bound. None of these is supplied by
the short-prefix calculation.

**Scope:** asymptotic obstruction to one proposed occupation lemma only.
No all-control no-go, protected protocol, or advantage claim is established.

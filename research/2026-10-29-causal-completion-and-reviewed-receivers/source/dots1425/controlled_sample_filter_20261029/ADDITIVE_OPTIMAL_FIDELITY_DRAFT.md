# Additive-optimal fidelity on the large-ambient depolarized family
2026-10-29. Root-originated sharpening, author derivation; pending receiving review. The previous conservative composition draft is preserved.

For N_eta(rho)=(1-eta)E(rho)+eta Tr(rho)I_D/D with exactly reversible E, the optimal entanglement fidelity is
 F_opt(N_eta)=1-eta+eta/k^2.
Indeed every completed CPTP decoder, including its fresh training algorithm, gives entanglement fidelity exactly1/k^2 on the depolarizing payload branch. That branch has an independent maximally mixed logical reference; no subsequent decoder can correlate with it. The signal branch contributes at most1, and the known exact decoder of E attains1. This is an existence comparison, not supplied unknown-frame control.

Use the notation/parameters of ROBUST_COMPOSITION_DRAFT.md. The accepted code-supported channel is
 N_P=(t E_sig+b R_noise)/(t+b),
where R_noise is a replacement channel. For any fixed averaged CPTP learned decoder R, Fe(R R_noise)=1/k^2. The central learned-Petz bound gives
 Fe(R N_P)>=1-2b/(t+b)-xi,
with xi<=epsilon/32. Therefore
 t Fe(R E_sig)>=(t+b)(1-2b/(t+b)-xi)-b/k^2
 =t-(1+1/k^2)b-(t+b)xi.
The unconditional original depolarizing branch contributes eta/k^2 exactly, including all algorithmic failure completions. Discarding only nonnegative signal-failure contributions yields
 Fe(R_full N_eta)>=1-eta+eta/k^2
 -[d gamma+zeta+(1+1/k^2)b+(t+b)xi]
before exterior-pollution, numerical-instrument, acquisition-abort and synthesis budgets. All these are already strictly smaller than the conservative epsilon budget in the original draft, since (1+1/k^2)b <=2b/(t+b) and t+b<=1. Thus the LARGE-D branch sharpens to
 Fe>=F_opt(N_eta)-epsilon.
This is additive optimality for this particular isotropic-pollution family at the stated finite-memory/trusted-control/known-parameter-upper-bound interface, not general optimality of Petz.

The SMALL-D branch remains the squared-optimum bound of the frozen central Petz construction. Upgrading that branch to additive optimum would require an explicitly paid known-matrix recovery optimizer (e.g. conventional SDP) and synthesis. Such an optimizer is not supplied by this addendum and must not be silently assumed. The earlier large-D Fe>=1-eta-epsilon statement remains valid but weaker.

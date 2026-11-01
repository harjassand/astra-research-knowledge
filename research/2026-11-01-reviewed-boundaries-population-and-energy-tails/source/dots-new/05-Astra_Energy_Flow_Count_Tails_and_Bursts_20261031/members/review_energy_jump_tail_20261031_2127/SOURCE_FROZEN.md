# Energy-flow certificate lifted to actual jump-count tails

Status: new root construction, independent review pending. Ordinary positive
tilted-semigroup/Lyapunov machinery is credited; no priority or hardware claim.
This does not construct coherent simulation, acquire a dilation, or remove padding.

Assume an ACTUAL finite-dimensional Markov source and its specified counted jump
channels L_j, with source generator G (including any source Hamiltonian), and

  0<=H<=h I,  G*(H)<=-kappa H,  sum_j L_j*L_j=2H,

where kappa>0 and h<infinity. Couple it to arbitrary quantum data by Hamiltonian
sqrt(lambda) V, lambda>0, V Hermitian, and set C=||sqrt(H)V||. Operators H and
L_j act as identity on data when appropriate. Additional Hamiltonians commute
with H. Initially source and data may be correlated; E0=Tr(H rho0). Fix T.
No state-independent source reset or source stationarity is assumed.

Let N_T count all specified source jumps. For s>=0 put q=exp(s)-1 and require
4h q<kappa. Choose

  a=4q/(kappa-4h q),  W=I+aH,  r=2a C^2/kappa.

Then the actual jump-count moment generating function obeys

  E exp(s N_T) <= (1+a E0) exp(r T).                 (1)

Consequently P(N_T>=n) is bounded by the infimum, over the admitted s>0, of
exp(-sn)(1+a E0)exp(rT), also capped at1. This is a finite exponential-tail
certificate, not just an assumed bound on the number of faults. Its allowed
tilt and constants explicitly charge the source energy ceiling h.

Proof. The adjoint counted tilted generator differs from the actual generator
by lambda q sum_j L_j* (.) L_j. Positivity and H<=hI imply

  sum_j L_j* W L_j <=2(1+a h)H.

For every normalized positive joint state, Cauchy--Schwarz gives
|Tr(i[V,H]rho)|<=2C sqrt(Tr(Hrho)). Hence, as an operator inequality,

  i sqrt(lambda) a[V,H]
       <= (lambda a kappa/2)H +(2a C^2/kappa)I.

Combining this with G*H<=-kappa H yields

  L_s* W <= lambda[-a kappa/2+2q(1+a h)]H+rI = rI <=rW.

The tilted propagation is completely positive for real s. Comparison of the
positive evolution therefore gives E[e^(s N_T) W_T]<=e^(rT)Tr(Wrho0), while
W>=I gives (1). This argument is at the actual finite-rate model, with no
adiabatic elimination or discarded no-jump history.

For time-varying source-blind/data controls commuting with H the same inequality
holds pointwise. A bounded known C(t) replaces rT by int 2a C(t)^2/kappa dt.
Interspersed instruments/control maps require their aggregate adjoints to obey
sum_outcome Phi_outcome*(W)<=W, with outcome-adaptive future generators obeying
the same inequalities. This is an explicit no-uncharged-energy condition. Merely
having a small average energy for some preferred input is insufficient.

Differentiating the bound at s=0 recovers

  E N_T <=4E0/kappa+8C^2 T/kappa^2.

Thus the supplied expected resource-flow estimate is the zero-tilt member of
this stronger family under the EXTRA finite-ceiling hypothesis. No extension
to unbounded H is claimed without a different Lyapunov observable.

## Missed emissions, where an observation task changes the consequence

If each actual jump is independently missed with probability eta, the missed
count M_T has conditional generating factor (1+eta(e^s-1)) per jump. Replace
q by eta(e^s-1) throughout (1), now requiring4h eta(e^s-1)<kappa. This pays
inefficiency without claiming a perfect detector. A history-dependent miss
probability uniformly bounded by eta admits the same positive domination when
the stated physical measurement instrument genuinely supplies that thinning.
An unmodeled dead-time detector does NOT satisfy a small eta bound automatically;
inside a blind interval its conditional miss probability can be1.

This can bound missed-parity errors in an ordinary environment-assisted
commuting computation, provided the actual count/readout/initialization service
is constructed. It does NOT alone yield an all-selected-location fault theorem:
correlated source initial states, joint patch geometry, adaptive exposure, and
readout/control failures still require a multi-location receiving proof.

All operations, waiting, switching and readout during which the admitted
interaction acts must be included in T or the time-dependent integral. The
certificate does not make energy-injecting controls free, turn an abstract
Lindblad representation into observed photons, or transfer to a different G.

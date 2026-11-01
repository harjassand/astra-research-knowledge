# Proposed exact ancilla-current Lyapunov lift (independent derivation, pending receiving)

2026-11-01. This analyzes the parent's autonomous finite-ancilla dilation DIRECTLY. No adiabatic elimination or finite-time approximation is used. It appears to supply a dimension-independent exponential Lyapunov mechanism, conditional on the explicitly stated activity and locality bounds. It does NOT synthesize the still-high-body J operators from native few-body interactions. Independent audit is essential.

## 1. Assumptions and notation

On the system/witness sector under consideration, let W≥0 have commuting local terms. Exact-drop operators J_α obey [W,J_α]=−d_αJ_α, with 1≤d_min≤d_α≤d_max. Attach one two-level ancilla per channel, n_α=σ_α^+σ_α^−, and put

A_α=J_α σ_α^+, A=Σ_α A_α,
H=g(A+A†), N=Σ_α n_α,
Q=W+Σ_α d_α n_α,
C=i(A−A†).

The ideal full generator is L=-i[H,·]+γΣ_α D[σ_α^-]. The common g,γ are fixed positive rates; unequal rates require redoing the coefficients, not silently using these formulas. An additional Hamiltonian proportional to Q commutes with all observables used below.

Assume activity bounds

c W ≤ Σ_α J_α†J_α ≤ C_0 W,                         (A1)

throughout the chosen safe system sector. The lower bound is the controller's extensive move count. The upper bound needs explicit receipt: for fixed local downhill patterns of bounded incidence, every enabled move must touch a positive local W term, so charging it to such a term gives a fixed C_0. This argument must use the actual normalized channel list, including exact-drop splitting.

Assume ||J_α||≤j_*, each J overlaps at most z other J supports, and all supports, local dimensions, number of terms per site and term norms are bounded independent of n. Constants may be enormous functions of the fixed Tanner degree. There are O(n) ancillas.

## 2. Exact conservation, no high-W vacuum dark state

[Q,A_α]=0, hence [Q,H]=[Q,C]=0. Therefore

L*Q=−γΣ_α d_α n_α.

For all ancillas in vacuum, H maps a system vector ψ into orthogonal one-ancilla sectors and

||H(ψ⊗vac)||²=g²Σ_α ||J_αψ||²≥g²c<ψ,Wψ>.

Thus no all-vacuum high-W vector can be dark. This does not alone prove a spectral gap.

The correct exponential potential e^(aQ) has zero Hamiltonian drift, and its reset drift only sees occupied ancillas. The following current correction closes that observability gap.

## 3. Dimension-independent current bounds

For every vector ψ,

|<C>|≤2 sqrt(<Σ_α J_α†J_α><N>)
      ≤2 sqrt(C_0<W><N>)
      ≤sqrt(C_0)<Q>,

using d_min≥1 in the last inequality. The first line follows by writing <J_ασ_α^+>=<σ_α^-ψ,J_αψ> and applying Cauchy–Schwarz over α. Thus, as quadratic forms,

−sqrt(C_0)Q≤C≤sqrt(C_0)Q.                           (A2)

The reset dissipator acts as L_reset*C=−(γ/2)C. The coherent part is

i[H,C]=2g[A,A†].

Its diagonal terms are

Σ_α [A_α,A_α†]=−Σ_α J_α†J_α
 +Σ_α (J_α†J_α+J_αJ_α†)n_α.

For α≠β, the cross term is [J_α,J_β†]σ_α^+σ_β^−. Disjoint system supports give zero. For overlapping supports,

|<O σ_α^+σ_β^−>|≤||O|| sqrt(<n_α><n_β>)
 ≤(||O||/2)<n_α+n_β>.

Summing bounded-incidence overlaps therefore gives an O(N), NOT O(n²) or O(sqrt(nN)), error. A conservative choice is C_1=2(1+z)j_*², yielding

L*C≤−2gc W+2gC_1 N−(γ/2)C.                         (A3)

All inequalities are operator quadratic-form inequalities. No factorization of the quantum state or classical replacement of coherences is used.

## 4. A positive modified energy with extensive mean drift

Choose V=Q+εC with ε>0. Let η=εsqrt(C_0)≤1/2. By (A2),

(1−η)Q≤V≤(1+η)Q, and [V,Q]=0.                      (A4)

Using (A3), L*Q, and the sharper Cauchy–Schwarz bound,

L*V≤−2εgc W−γd_min N+2εgC_1 N+εγ sqrt(C_0<W><N>)

in quadratic forms. Young's inequality gives

L*V≤−εgc W+
 [−γd_min+2εgC_1+εγ²C_0/(4gc)]N.

Take

ε[2gC_1+γ²C_0/(4gc)]≤γd_min/2,
εsqrt(C_0)≤1/2.

Then

L*V≤−εgc W−(γd_min/2)N≤−c_V Q,
c_V=min(εgc,γd_min/(2d_max))>0.                     (A5)

This is an exact full-generator mean-energy statement, uniform in n. The sign matters: with C=i(A−A†), the correct choice is Q+εC.

## 5. Local exponential lift: an O(a²)n remainder is enough

Mean-energy decay alone is insufficient. Here locality yields the needed additional statement for sufficiently small fixed a>0:

F=e^(aV),
F^(−1/2)L*F F^(−1/2)=a L*V+R_a,
||R_a||≤C_2 a² n.                                  (A6)

Proof mechanism, to be independently checked with explicit constants: write V=Σ_X v_X, with finite maximum support s, incidence ζ and norm v_*. For any bounded-support O, nested commutators satisfy

||ad_V^k(O)||≤||O|| C_O^k k!,

with C_O independent of n. At step j only terms overlapping the current support contribute; its size is at most s_O+j(s−1). Bounding the product of these overlap counts by a constant^k k! proves a nonzero uniform convergence radius for e^(tV) O e^(−tV).

For each local Hamiltonian h, the exact weighted contribution is

i(e^(−aV/2)h e^(aV/2)−e^(aV/2)h e^(−aV/2))
 =ia[h,V]+O(a³),

with a local-norm remainder independent of n. For a local reset jump l, set A_l=e^(aV/2)l e^(−aV/2) and B_l=e^(−aV/2)l†l e^(aV/2). Its exact weighted dissipator is

A_l† A_l−(B_l+B_l†)/2=a D[l]*V+O(a²).

The same nested-commutator estimate bounds each remainder by a fixed constant times a²||l||². There are O(n) local terms, giving (A6). This is an identity/estimate for the actual finite-parameter generator, NOT a comparison of finite-time channels. No T appears.

Combining (A5) and (A6),

F^(−1/2)L*F F^(−1/2)≤−a c_V Q+C_2a²n I.            (A7)

For any fixed θ>0 choose a≤c_Vθ/(2C_2), also inside the commutator convergence radius. Then above Q≥θn the RHS is at most −a c_V Q/2. Below that region it is at most C_2a²n. Since Q COMMUTES WITH V and F, one obtains the global Foster–Lyapunov form

L*F≤−k n F+D n exp[a(1+η)θ n] I,
k=a c_Vθ/2,
D=k+C_2a².

Consequently the exact reflected/allowed dynamics has a uniform exponential moment bounded by its initial moment plus (D/k)exp[a(1+η)θn]. With a Q-boundary B=βn and (1−η)β>(1+η)θ, (A4) then gives exponentially small boundary occupation. This is the missing rare-event mechanism, not merely a mean-energy claim.

## 6. Reflection, noise and initialization obligations

The activity bounds are only promised in the safe Tanner basin, not on all syndromes. The intended application therefore uses the analysis-only reflected component, enlarged with ancillas and cut off by Q. Because each A_α conserves Q and every reset lowers it, the ideal dilation stays inside a below-Q-cutoff connected component. The component projector must be shown to commute with V; conservation and inclusion of all local adjoint edges provide a route, but this interface with the parent's precise component construction should be independently received.

Finite-temperature upward resets are NOT suppressed to zero. Treat their actual local jumps as additional perturbations. The same local exponential-conjugation estimates bound their weighted contribution by C a γ_up n for small a, with fixed locality constants. Likewise arbitrary bounded local Hamiltonian perturbations and local dissipators can be admitted directly in this weighted norm with fixed per-site budgets. They must be small compared with the earned coefficient k, not with exp(−const n). Constants and any Pauli expansion/support factors remain paid. This is a proposed new admission proof, not automatic inheritance of the original e^(aW) constants.

There is no need for perfectly pure initial ancillas if a preparation distribution has a sufficiently small extensive Q moment. For independent thermal ancillas with excited probabilities q_α and system W=0, (A4) gives

Tr[Fρ_initial]≤Π_α[1−q_α+q_α exp(a(1+η)d_α)].

A small fixed thermal excitation density can therefore fit the exponent margin; it must be specified, not assumed. Correlated preparations need their actual moment bound. Initial apparatus errors can also induce local data effects and must be included if present.

## 7. Scope and physical cost

If all derivations receive independent audit, this gives a genuine autonomous finite-ancilla, fixed-rate exponential Lyapunov mechanism for the parent's exact-drop dilation. It avoids a clock and avoids εT adiabatic-elimination transfer. Reset reservoirs remain real physical resources; finite-temperature errors are explicitly nonzero.

The crucial limitation is unchanged: H contains J_α, which still includes bounded-but-high-body syndrome projectors and witness flips. This note does NOT compile those couplings into native few-body interactions, prove a microscopic finite-reservoir Markov limit for exponentially long time, certify a finite Tanner instance, or establish competitive costs. The next hardware gate is the actual native J coupling or another potential-preserving few-body realization. Strong ordinary active qLDPC gets the same hardware.

Status: direct constructive derivation, not independently accepted. In particular receive (A1)'s upper bound for the exact channel list, the cross-term estimate, the local conjugation constants in (A6), and the reflected-component/noise consumer before using it as a theorem.

### Small algebra sanity check (not an independent proof or hardware experiment)

A direct 32-dimensional NumPy check used two system excitation bits with W=n1+n2, three channels J1=σ1^−, J2=σ2^−, J3=σ1^−σ2^−, drops (1,1,2), three reset ancillas, g=γ=1 and ε=.02. It gave ||[Q,V]||=0 and largest eigenvalue of L*V+.02Q equal to0. The exact weighted exponential remainder norm divided by a² was 2.99893, 2.99560, 2.98400 for a=.001,.003,.01. This checks signs and second-order scaling in an overlapping-channel instance; it does not certify general constants or the Tanner source conditions.

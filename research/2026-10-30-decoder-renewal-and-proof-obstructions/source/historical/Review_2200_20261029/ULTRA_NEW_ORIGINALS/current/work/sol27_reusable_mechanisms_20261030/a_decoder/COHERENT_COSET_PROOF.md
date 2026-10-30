# Robust dense Clifford recovery from a low mixed-nullity source

This constructs the missing robust acquisition step using actual copies of a fixed forward source, not a supplied stabilizer list, conditional state oracle, or controlled encoding inverse. Bell sampling and symplectic compilation are ordinary primitives. The distinctive link is a positive coset-projection inequality which handles GLOBAL coherent source errors without inferring a convex clean component.

The initial fixed-reference-label construction is A's. Root independently reconstructed that link and supplied the adaptive hyperplane refinement in Section 5, removing its exponential dependence on the number of logical qubits. C supplies the reusable public signed-Pauli compiler. Their source files and execution scope are kept separate from this derivation.

## 1. Source, promise and native operations

Let q logical qubits be encoded in n physical qubits. Write k=2^q and m=n+q. The ideal source has the form

`N0(w)=U0[w tensor |0><0|^(n-q-t) tensor sigma_t]U0^*`,       (1)

where U0 is an UNKNOWN physical Clifford and sigma_t is an arbitrary UNKNOWN mixed t-qubit state. The pure ancillas may themselves be in an unknown stabilizer frame, which can be absorbed into U0. The t-qubit state may have arbitrary rank, magic, degeneracy and conditioning. There is no local-support/weight promise on U0 or its logical Pauli images.

The actual source N is fixed memoryless CPTP, with normalized channel Choi states rho and rho0. The structural completeness hypothesis is

`Dtr(rho,rho0)=(1/2)||rho-rho0||_1<=eta`.                    (2)

It is a GLOBAL trace-distance hypothesis, not constant error per site, gate or output qubit. It is not inferred from an unverified device fidelity. In particular a nearby unitary channel need not have any nonzero convex identity component; that stronger and generally false inference is NOT used.

Native calibration consists of independently preparing q known Bell pairs, sending one half through N, and retaining its reference. Four such Choi programmes allow two transversal Bell measurements; XOR their phase-free Pauli labels to obtain a Bell DIFFERENCE label in F2^(2m). There are four forward calls per candidate. Verification of a specified candidate uses fresh Choi programmes and known product-Pauli measurements, one call per shot. Only finite known Clifford operations and computational-basis measurements are used. No unknown output frame is inverted during acquisition.

There are at most four Choi programmes live in the finder, and one in a verifier. All acquisition precedes the unknown payload. The output will be a CLASSICAL finite Clifford gate list which is reusable, with no online source call or quantum programme needed at decoding time.

## 2. Ordinary Bell algebra and a mixed-state Cauchy bound

Use phase-free labels a and Hermitian representatives P_a. Let p_rho(j) be the two-copy Bell distribution. Pauli action on either copy translates the Bell label by that Pauli label, up to an irrelevant phase. For two independent Bell outcomes, the difference law is

`b_rho(a)=sum_j p_rho(j)p_rho(j+a)`.

For ANY l-qubit mixed state rho and ANY Hermitian Pauli P_a,

`b_rho(a)>=|Tr rho P_a|^2/4^l`.                             (3)

Proof: set omega=rho tensor rho. In the Bell basis, P_a acting on one copy permutes j to j+a, with unit-modulus phases. Positivity gives `|omega_(j,j+a)|<=sqrt(p_rho(j)p_rho(j+a))`. Hence

`|Tr rho P_a|=|Tr omega(P_a tensor I)|<=sum_j sqrt(p_rho(j)p_rho(j+a))`.

Cauchy over the 4^l outcomes proves (3). No pure-state promise, tomography, measured purity, or spectral denominator is required.

Bell DIFFERENCE sampling is covariant under every Clifford, including for mixed states. A direct Pauli expansion gives

`b_rho(a)=4^-l sum_P (-1)^[a,P](Tr rho P)^4`.

Clifford conjugation permutes labels and changes coefficient signs, removed by the fourth power. This identity and the physical Bell circuit are established predecessors, explicitly Eq(27) of Tang--Steckmann2610.03307v2. They are not claimed as new.

## 3. The positive coset-projection operation

Let H be any COMMUTING subgroup of phase-free Pauli labels with specified consistent stabilizer signs, and let Pi_H be its chosen simultaneous-eigenspace projector. Suppose a commutes with H. Let E_(a+H) be the four-copy Bell-difference event whose output label belongs to the coset a+H.

For EVERY h in H, applying its Pauli on ANY ONE of the four copies shifts the difference label by h. The event a+H is unchanged. Consequently E_(a+H) commutes with Pi_H on each copy. It therefore obeys the positive operator inequality

`E_(a+H)>=Pi_H^tensor4 E_(a+H) Pi_H^tensor4`.              (4)

For p=Tr Pi_H rho>0 and rho_H=Pi_H rho Pi_H/p, (4) gives

`Pr_rho[BellDiff in a+H]>=p^4 Pr_(rho_H)[BellDiff in a+H]`. (5)

This is ANALYTICAL projection, not a physical operation the learner performs. H, its signs, Pi_H and the ideal frame can all be unknown. There is no convex-mixture hypothesis or free conditional query hidden in (5). Coherent off-diagonal state blocks disappear because the EVENT commutes with the projection, not because the state is asserted diagonal.

If H has rank m-l, use an analysis Clifford to map it to m-l pure ancilla Z generators. The conditional state has the form `|0><0|^(m-l) tensor tau_l`, with tau_l arbitrary mixed. Clifford covariance and factorization of Bell measurements show that the coset probability on the right of (5) is exactly the l-qubit difference probability at the active Pauli label of a.

If rho0 is stabilized by H and by the signed Pauli a, (2) implies p>=1-eta. Since a commutes with Pi_H, its wrong-sign probability after conditioning is at most eta/p. Its signed expectation is at least `1-2eta/p`. Combining (3)--(5) yields

`Pr_rho[BellDiff in a+H]>=p^2(p-2eta)^2/4^l`

`                         >=(1-eta)^2(1-3eta)^2/4^l`.     (6)

For eta<=1/16 the numerator is at least 38025/65536>1/2. This is the critical coherent-error acquisition inequality. It is dimension-sensitive only through the number l of active unprojected qubits.

## 4. First construction: fixed reference-labelled candidates

The ideal Choi state is `U0[Phi_(R,L)^q tensor |0><0|^(n-q-t) tensor sigma_t]U0^*`, with U0 on B only. Its strong stabilizer subgroup S contains rank m-t, consisting of the 2q Bell-graph generators and n-q-t pure ancilla generators. Its reference projection is surjective onto F2^(2q).

Let G be the subgroup of S with reference label zero. It has rank n-q-t and fixes rho0. For one desired reference X_i or Z_i, choose its true signed joint stabilizer a. The coset a+G contains only candidates with that desired reference label. Apply (6), now with l=2q+t, to get

`Pr[a useful candidate with that reference]>=1/(2k^4 4^t)`. (7)

Directly verifying this candidate avoids forming an O(n)-length product of approximate generators. It already gives a robust dense-weight decoder at polynomial cost for q=O(log n), t=O(log n), including arbitrary coherent perturbations allowed by (2).

## 5. Root's adaptive hyperplane refinement removes k^4

Maintain a space W of accepted reference labels. When dim W<2q, choose FOR ANALYSIS a nonzero binary functional phi which vanishes on W. Within the ideal S, set

`H={s in S: phi(ref(s))=0}`.

It has rank m-t-1. Choose a in S with phi(ref(a))=1. Every label in a+H has reference outside W. Equation(6) now leaves only l=t+1 active qubits, so

`Pr[BellDiff gives a true strong candidate extending W]>=1/(2*4^(t+1))=:p_*`.   (8)

No phi, H or a is constructed or queried. The ACTUAL algorithm simply checks reference linear independence, validates that individual signed Pauli against the actual source, and accepts it when validation passes. Equation(8) is valid conditional on ANY previous history and proper W, so no union over exponentially many possible spaces is needed.

Once 2q independent reference labels have been accepted, the full Bell projector is the intersection of their ORIGINAL commuting signed joint projectors, after exact classical conversion to a canonical reference basis. Their validation losses are summed only once. Changing generator basis need not cause a q^2 accumulation of physical errors.

## 6. Literal actual-source verification and finite work

Here is one complete conservative finite policy. Choose `0<tau<=1/8`, failure probability `0<delta<1/2`, and an upper budget t. Completeness will require eta<=tau/8; soundness of a returned decoder does not require the latent promise.

Let

`R=ceil[(2/p_*) log(8q/delta)]`, `Cmax=2qR`.

Each stage tries at most R fresh difference candidates. If its reference lies in W, skip it. Otherwise measure its Hermitian Pauli on

`V=ceil[(256/tau) log(16 Cmax/delta)]`                     (9)

fresh actual Choi programmes. Accept iff the empirical minority fraction is at most tau/2; the majority determines the sign. Directly check joint commutation and reference independence before adding the row; otherwise reject or abort. Finite upper ceilings/logarithms can be replaced by rational outward bounds, with no real oracle.

Suppose finder apparatus error in output TOTAL VARIATION is at most p_*/2 per candidate, and each specified Pauli verification has wrong-probability bias at most tau/16. These are explicit trusted-execution/calibration requirements, not learned for free from N.

For a true strong candidate, its actual wrong-sign rate is at most eta<=tau/8, so its observed rate is at most 3tau/16. For a sign whose true wrong rate is at least tau, its observed rate is at least15tau/16. Standard binomial upper/lower Chernoff bounds at threshold tau/2 make (9) sufficient for both completeness and rejection, with union probability below delta/2 over all Cmax adaptive tests. Each test uses fresh samples; conditioning on previous data therefore causes no generalization problem. This conservative V is O(tau^-1 log(Cmax/delta)); generic additive Hoeffding is a valid but unnecessarily larger upper bound here.

On the common good event, every accepted signed Pauli has true expectation at least1-2tau>=3/4. Two anticommuting Paulis have squared expectations summing at most one; hence ALL accepted joint Paulis commute exactly. True S candidates cannot be blocked by this commutation check. The noisy finder still hits a true extending coset with probability at least p_*/2, so the chosen R and a stage union bound make acquisition succeed with total failure at most delta.

The maximum number of original forward calls is

`Q<=4 Cmax+V Cmax`.                                      (10)

No payload waits during these calls. Finder storage is at most four m-qubit programmes plus known gate work; verification needs one. All retained scientific output is classical signed Pauli rows and a finite gate list. There is no quantum programme store at deployment.

Finite gate/measurement errors can be allocated over O(m) operations per Bell trial and per product measurement to meet the two explicit distribution/bias budgets. At t=O(log n), p_* is inverse polynomial, so this is a polynomial PRECISION requirement. It does not assert that a fixed physical per-qubit error rate meets it. In particular unmitigated independent readout errors on a dense parity can exponentially attenuate its contrast; that regime is not silently admitted.

Classical rank tests, Pauli phase arithmetic and symplectic elimination have polynomial bit complexity in n,q and the number of trials. Gates use exact H,S,CX,SWAP and Pauli signs. A gate-model compiler does not supply physical calibration or fault tolerance. Runtime is polynomial in 4^t and inverse accuracy, not polynomial merely in t or log inverse accuracy.

## 7. Actual reusable decoder and soundness

Write accepted rows as signed `R_j tensor B_j`, with the 2q reference labels independent. For each desired canonical reference X_i or Z_i, solve its GF2 expansion in those labels. Multiply selected rows in a fixed order, tracking raw mod4 Pauli phases on BOTH halves. The reference product's phase must be ADDED to the physical product phase when the target reference is canonical X_i/Z_i. This produces Hermitian physical canonical pairs, whose symplectic form agrees exactly with the reference pairs. Their full commuting joint projector is the SAME as that of the selected original rows.

C's public `pauli_compiler.py` maps these signed physical pairs to positive output X_i/Z_i. Apply that classical Clifford circuit to a payload and discard the other n-q qubits. This is CPTP on all payloads, with no postselection. A's acquisition implementation consumes the compiler read-only and credits its exact source bytes; it does not acquire U0 or reconstruct sigma_t.

The union bound for the original2q commuting projectors gives

`Fe(R N)>=1-2q tau`                                      (11)

on the common validation event. This is an actual-source statement for ANY fixed N whenever the procedure returns the verified frame. Without further structure it gives the ordinary normalized-Choi bound `halfdiamond<=k sqrt(2q tau)`, capped at one.

Root's separate rigidity theorem gives a stronger all-input transfer under the ADDITIONAL warranted global hypothesis `halfdiamond(N,N0)<=Delta`. Ideal correlation cannot be zero when `1-2tau-2eta>0`, so conjugation by U0 forces each selected physical generator's logical label to match its reference transpose. The resulting ideal composite is Pauli diagonal and hence a Pauli CHANNEL. Therefore

`halfdiamond(R N,id)<=Delta+eta+(1-Fe(R N))`

`                         <=Delta+eta+2q tau`,             (12)

plus any implementation error of the known decoder. Choi-only closeness does not grant Delta; it retains only (11) and its k-dependent conversion. The stored classical decoder can be reused on every later independent payload. A one-time learning failure is common to these uses; an averaged T-use bound has at most T times the per-use channel error plus delta, rather than treating acquisition failure as a newly sampled event per use.

## 8. Genuine boundaries and ordinary methods

The method permits dense logical strings and arbitrary mixed active junk, but REQUIRES low mixed nullity t for polynomial acquisition. It does not solve the arbitrary-maximally-mixed-junk noisy case: root's full-source LPN family has t proportional to n. The computational LPN boundary is conditional, not an unconditional lower bound or an inference from failed spans.

Tang--Steckmann2610.03307v2 learns approximate WEAK invariance of noisy images of PURE low-nullity states; its projected-purity output is not automatically the strong signed Bell frame needed here. Hinsche--Eisert--Carrasco2505.15770v3 explicitly distinguishes mixed weak invariance from unit-expectation strong symmetry in SectionII.4. Those methods and their full costs remain ordinary comparators. A low-t pure-junk special case is already covered by stronger prior stabilizer-learning machinery. We make no generic Bell-learning or stabilizer-compression novelty claim.

The constructed operation is a robust, directly verified, reusable CLASSICAL decoder under the native source promise above. The positive coset projection and adaptive reference acquisition pay the coherent/mixed interface explicitly. Whether older mixed-state agnostic methods already imply the same operation at equal/better resources is part of the ongoing primary comparison; historical priority and physical/practical advantage remain UNKNOWN.

# Independent review: noncommuting proof circuits and a valid spectral exit basin
2026-10-30. Reviewer: `producer-workspace/review_simple_compiler`.

## Result and precise scope

**SCOPED PASS for the abstract compressed-circuit / inner-spectral-basin mechanism under the structural premises stated below.** The higher-moment identity and the boundary telescoping close the two previously missing transfers: use of raw-basin coverage after the noncommuting congruence, and a legitimate CP/TNI killed moment inequality. This does not certify the actual native-LOCC service, locality, canonical-module or initialization premises.

Reviewed root sources:

| Source in `noncommuting_basin_root_20261030` | SHA-256 |
|---|---|
| `COMPRESSED_CIRCUIT_SPECTRAL_BASIN_CANDIDATE.md` | `1e84145e634e955c757b4ed286780bd9356ac1fed4ce87dce34bd05d35208daf` |
| `BOUNDARY_TELESCOPING_AND_EXIT_PROOF.md` | `86e4933271b67eb782900b60b0e24ee27b6f0498904129299704b93f0c979698` |

The proof below independently verifies the exact algebra and completes the operator/reference-uniform estimates, not just scalar heuristics. Exact snapshots and diagnostics are saved alongside this receipt. Earlier accepted commuting-witness and recipient reviews are not changed or broadened.

## 1. The original obstruction is real; the easy alternatives do not fix it

Take one qubit, `P=|0><0|`, `H=X`, `S=diag(1,sqrt(M))`, and the positive proof gate `Y=exp[delta(I+PauliY)/2]`, with M>1 and delta>0. Let `W=S Y†Y S`. Then

    P i[H,W] P = -2 sqrt(M) exp(delta) sinh(delta) P < 0,

whereas the complete Hamiltonian compression has `PHP=0` and hence `L_P*(PWP)=0`. Thus the tempting order `L_P*(PWP)<=P L*W P` is false even for one bounded local positive proof gate arbitrarily close to identity. Positivity, raw-potential comparability and a polar/log entropy estimate do not supply that order.

A Schur-complement or W-orthogonal projection is not automatically a physical repair: the corresponding oblique projection generally has norm greater than one, so its Kraus map need not be trace nonincreasing. Nor does an absorber designed solely to have a chosen negative W-drift automatically have a positive physical loss effect.

Killing directly in a full-space low-W spectral subspace would resolve commutation but can include remote low-energy sectors outside the Tanner canonical-radius regime. The successful mechanism therefore keeps an outer canonical basin and compresses the proof generators before defining the inner spectral cutoff.

## 2. Receiving hypotheses that are actually needed

Let P=P0 be the outer canonical-radius projector and Q=I-P. The following are substantive hypotheses, not conclusions of the repair:

1. E is a commuting local energy, `0<=E<=e_max N`; V=exp(sE). P commutes E and the credited potential `A=V prod_i D_i`, with positive commuting local discounts satisfying `exp(-c_t tN)V<=A<=V` and uniform local inverse bounds.
2. Every physical system leg and every proof Xi has fixed support and uniformly bounded energy bandwidth. Every P/Q crossing has **both endpoints** in a common high-energy strip. One may take R to be the energy spectral projector `{E>=bN-C0}` containing these endpoints, so R commutes V. For a radius cutoff this requires its O(1)-width boundary on both sides to remain inside the admitted confinement radius. The O(1) width must cover the largest complete structural support, not just one-qubit flips.
3. The original uncompressed finite-depth circuit Y has O(N) positive local gates with strengths at most delta. Its local weighted conjugation bounds are uniform. All gate/witness norm, support, depth and local-discount constants remain fixed as t and delta are chosen small.
4. The actual generator has an **unconditional coverage-observable drift**

       L*W <= S†[-kappa D+rho_coeff N I]S,
       S=Y A^(1/2), W=S†S,

   where `PDP>=c PEP`, and D,E have O(N) norm. This is not replaceable by an unexplained raw-P-compressed drift of the original W. The constant c is absorbed into kappa below. The new first-order assembly is designed to retain exactly this unconditional D form; whether it has earned it is a separate audit.
5. The generator's bounded system-supported terms have total incident norm O(N), with the stipulated common-bath/reference regularity. There is an actual CP/TNI complete-loss compression. Bath-only terms commute system projectors and are not assigned an unbounded extensive norm.
6. For the desired logical conclusion, all P-compressed proof and physical system legs preserve the admitted canonical correctable module. Arbitrary-logical identity on the whole bilateral space is not inferred from a Bell-target theorem. For a Bell resource, the common Bell-target/shared-gauge module is the appropriate premise.

These conditions prevent the proof from silently applying Tanner density beyond its radius, treating globally compressed gates as local, or importing an unearned logical statement.

## 3. Exact higher moments on the compressed spectral subspace

On P H set `Xi,0=P Xi P`, `Y0=prod exp(epsilon_i Xi,0/2)`, `A0=PAP`, `S0=Y0 A0^(1/2)` and `W0=S0†S0`. Define

    P1=1_(W0<=exp(aN)) on P H,       F=W0+Q.

Thus P1<=P and `[F,P1]=0` exactly. All inverses below are restricted to P H. The compressed gates are generally nonlocal; no finite-depth local Taylor estimate is applied to them.

Since P commutes A and V, compression preserves the weighted norm bound of each local generator. For fixed theta,

    ||A0^theta Xi,0 A0^-theta|| <= C_theta,
    ||V0^theta Xi,0 V0^-theta|| <= C'_theta.

The A bound follows by cancellation of the original commuting local discount factors disjoint from Xi and by bounded raw-energy bandwidth. Multiplying O(N) exponential norm bounds, without any compressed locality assertion, gives corresponding `exp(C_theta delta N)` bounds for Y0, its inverse, adjoint and inverse adjoint.

Write G0=Y0†Y0. For each fixed integer k>=1, the ordered identity

    A0^k W0^-k
       = prod_(j=k down to 1)
           A0^(j-1/2) G0^-1 A0^(-j+1/2)

is exact. It follows either by adjacent power cancellation or by induction from `W0^-1=A0^-1/2 G0^-1 A0^-1/2`. Its norm is at most `exp(C_k delta N)`. Squaring its norm as an operator inequality and congruencing by W0^k yields

    A0^(2k) <= exp(C_k delta N) W0^(2k).

Because A0 and V0 commute, their lower comparison may legitimately be raised to powers. Hence

    V0^(2k) <= exp([2k c_t t+C_k delta]N) W0^(2k).

This is not the false rule of raising an arbitrary noncommuting Loewner inequality to a power. On P1 it gives the operator/vector estimate

    ||V^k P1|| <= exp([ka+k c_t t+C_k delta]N),             (A)

with harmless constants absorbed into C_k. It remains true after reference amplification.

## 4. The needed tail is an operator tail for every partial word

Let B be any word containing O(N) original or block-diagonalized proof gates, a fixed number of bounded local system legs, and a fixed number of A powers. Exponents of these A powers are bounded independently of k and N. For the gate/local-leg portion,

    ||V^k B V^-k|| <= C_k exp(C_k delta N).

A powers commute V and cost at most `exp(C_A N)`, where C_A is fixed independently of k. Equivalently, one can use an additional fixed higher moment for a rightmost A^(1/2). Projections P,Q and the energy strip R do not worsen the weighted bound.

Using `||R V^-k||<=exp(-ksbN+O(k))` and (A),

    ||R B P1||
       <= C_k exp{[-k(sb-a)+k c_t t+C_k delta+C_A]N}.     (B)

This is the load-bearing estimate. It holds for arbitrary intermediate words, not just the original input or a final state. It also applies to the reverse/adjoint words needed below. The constants attached to finitely many local insertions may depend on k, but do not multiply N except through the explicitly displayed controlled exponents.

Choose a<sb. First fix k large enough to beat every coarse extensive norm cost appearing in the finite calculation. Then choose t and delta small enough that `k c_t t+C_k delta` preserves the desired negative exponent. C_k may grow very rapidly; no uniform k limit is needed. All choices are fixed before N and before running the apparatus. Polynomially many terms can then be absorbed by a slight decrease of the exponent.

## 5. Exact boundary telescoping, without a hidden outside block

Use the full-space block-diagonal generator

    Xi,bd=P Xi P+Q Xi Q,

not the zero-extended P Xi P. Pinching commutes with energy conjugation and is norm contractive, so the same weighted generator bounds apply. Crucially,

    Xi-Xi,bd=P Xi Q+Q Xi P=R(Xi-Xi,bd)R.

The exact Duhamel difference of `exp(epsilon Xi/2)` and `exp(epsilon Xi,bd/2)` contains one such R-supported crossing. The factors on its right form a partial word of the type in (B); the factors on its left may be bounded coarsely. This proves an exponentially small difference on P1-supported vectors, including after A^(1/2) and any fixed number of local insertions. Telescoping all O(N) gates gives the same statement for Y versus Y_bd.

Keeping the Q Xi Q block is important: the difference between Xi and zero-extended P Xi P also contains Q Xi Q, which is not itself a boundary operator. One can organize a first-crossing proof instead, but it is not licensed to call that whole difference boundary-supported. The block-diagonal route avoids this problem entirely.

Set `W_bd=A^(1/2)Y_bd†Y_bd A^(1/2)`. Its P block is exactly W0. For uniformly bounded fixed-support system operators U,Vloc, write each matrix element of

    P1 U†(W-W_bd)Vloc P1

as a difference of inner products of `Y A^(1/2)U psi` and `Y A^(1/2)Vloc phi`, and their block-diagonal counterparts. One vector difference is exponentially small by telescoping; the other has at worst a fixed `exp(CN)` norm, already paid in (B). Uniformity in both unit vectors proves an **operator-norm** bound, not merely a bound for a selected state.

Next, `F-W_bd` is Q-supported. A local U or Vloc can map a P1 input to Q only through the same high-energy strip. The coarse norm of its Q block is again `exp(CN)`. Therefore, after the fixed hierarchy above,

    ||P1 U†(F-W)Vloc P1|| <= exp(-cN).                  (C)

Every local Hamiltonian, gain and complete-loss contribution to L*(F-W) is a bilinear expression of this form. Summing O(N) terms gives

    ||P1[L*F-L*W]P1|| <= exp(-cN).                     (D)

For the Q-supported difference alone, Hamiltonian and anticommutator-loss terms vanish exactly on a P1 input; gains require local Q crossings. For the circuit difference, (C) controls all terms without dropping losses.

For bounded joint HP perturbations, expand only the finite system legs. The accompanying bath maps/operators are controlled by the given joint cb norm, up to a fixed system dimension factor. Apply (C) after reference amplification. No finite bath dimension, bath Kraus coefficient sum, or preferred fault unraveling is assumed. Pure bath terms cancel.

The vector comparison also gives, for every positive trace<=1 P1-supported state, including an arbitrary reference,

    ||S rho S†-S0 rho S0†||_1 <= exp(-cN).              (E)

Here S0 is extended as a map into P H. The trace estimate follows from the two Hilbert-Schmidt factors; their coarse exponential norms were already paid. Equations (D),(E) prove the candidate's equation (9), with exact operator orders and uniformity. Since S0 rho S0† is exactly P-supported, **now** the raw coverage inequality D>=E may be used. O(N) norms of D,E only add a polynomial factor to the error.

## 6. Legitimate killed drift and scalar moment

The comparison yields, on P1-supported states,

    Tr(L*F rho)
      <= -kappa Tr(S0† E S0 rho)
          +rho_coeff N Tr(F rho)+exp(-cN).

Weighted gate norms and A0<=V0 give

    S0 S0†=Y0 A0 Y0† <=exp(gN)V0,       g=O(delta).

Operator monotonicity of log, followed by the polar functional-calculus identity, gives on P H

    S0† E S0 >=[W0 log W0-gN W0]/s.

Now compress the **actual full generator** at P1 with complete losses retained. This is the stipulated CP/TNI comparison, not the HP effective similarity treated as a physical process. Since F commutes P1, its killed adjoint differs from the compressed full adjoint only by subtraction of positive outgoing gains. Hamiltonian/complete-loss cross-block errors do not remain. Thus, for `x=Tr(F rho_killed)`, scalar spectral Jensen at subnormalized mass gives

    x' <= -(kappa/s)x log x
            +(rho_coeff+kappa g/s)N x+exp(-cN).

Choose a fixed `nu>g+s rho_coeff/kappa` with nu<a and an initial moment below exp(nu N). At x=exp(nu N) the negative term dominates the additive exponentially small error for sufficiently large N. This proves the invariant moment bound without dividing by the killed mass. Neither the state nor W0 must commute with E.

## 7. Local-leg transfer and actual full-versus-killed exit

For the original finite-depth/local-discount circuit, the separate local-conjugation hypothesis gives `||S J S^-1||<=C_J` for each bounded local system leg J. Therefore `J†WJ<=C_J^2 W`. Applying (C) with U=Vloc=J and with both identity yields

    P1 J†FJ P1 <= C_J^2 P1 F P1+exp(-cN)P1.           (F)

This proves the candidate's equation (13); no locality is falsely assigned to Y0.

On P H, `P-P1<=exp(-aN)W0`. The Q component of a local J on P1 is separately bounded by (B). For a positive P1-supported state,

    Tr[(I-P1)J rho J†]
       <= C_J^2 exp(-aN)x+exp(-cN).                  (G)

Hamiltonian and loss legs obey the same estimate as bounded operators. Trace-norm Cauchy-Schwarz bounds the complete boundary source by `C N exp(-aN/2)sqrt(x)+exp(-cN)`, with fixed support/cb constants. Finite-system-leg expansion gives the corresponding common-bath statement. The actual full propagator is CPTP and contracts the forward Duhamel integral. With x<=exp(nu N), the full-minus-killed channel error is at most polynomial(N) times physical time times `exp[-(a-nu)N/2]`, plus the separately paid initial projection discrepancy and the smaller telescoping errors.

This comparison does not require P1 to be local or physically measured. A sufficiently small exponentially long time interval is allowed by the resulting exponent; no unspecified uniform-in-time zero error is implied.

## 8. Initialization and logical conclusion are separate, explicit inputs

If the supplied positive initial channel is P-supported and has `Tr(W0 rho_initial)<=exp(nu_init N)` with nu_init<a, Markov and gentle compression bound its initial P1 projection cost exponentially. Positivity and source-bad bookkeeping remain necessary; a generic dirty initial apparatus or merely small reduced fidelity is not covered.

Under the canonical-edge premise, every P Xi P is identity on the admitted logical coordinate, or preserves the relevant Bell-target/gauge module. Since Xi is self-adjoint, the latter invariant module is reducing. Exponentials, A0, W0 and its spectral P1 then preserve it by functional calculus. The P1-compressed physical legs also preserve the same module. Thus the killed process has exactly the required common correctable span; it does not acquire an artificial logical gate from its analytical spectral projection.

For the native LOCC application the target scope is the accepted **known Bell-target/shared-gauge module**, not arbitrary logical identity on the full bilateral logical space. The ordinary fixed recovery is still a mathematical decoding benchmark unless a separate physical decoder implementation is supplied.

## 9. Independent diagnostics and what remains open

The finite regression tests the ordered inverse-power identity at k=1,2,3 on noncommuting compressed circuits for N=3,4,5, with relative residual below 1.1e-15. It verifies the exact block-diagonal P-block witness and the full crossing strip, including the two-site bandwidth. It also exhibits the one-site failure of naive killed compression: compressed full drift -0.182161 while killed drift is zero. These small matrices verify algebra, not asymptotic exit probabilities; those follow from the fixed-k weighted-word estimates above.

The abstract repair is therefore sufficient under its receiving contract. Still unearned by this receipt: the actual unconditional useful/debt/activity inequality, its classical-contention terms, a common actual high-energy radius boundary for every proof/operator support, all raw discount commutants, uniform witness constants, and the exact native Bell-module preservation. Those need an actual-model audit. The older noncommuting entropy statement by itself was insufficient; the compressed-circuit construction and boundary estimates are essential additional work. No whole continuous-noise LOCC lifetime theorem is accepted here, and no publication or external mutation occurred.

# A fixed faithful qubit channel with unbounded complete entropy-comparator ratio
2026-10-29. New exact obstruction; independent receiving review pending.

Let Φ=Ad_X∘AD_(1/2), σ=diag(1/3,2/3), as in the stronger addendum. It is self-compatible and σ-preserving. Let R be a qubit and
ρ_e=(1/3)|01><01|+(2/3)|ψ_e><ψ_e|,
|ψ_e>=√e|00>+√(1−e)|11>, 0<e<1.
All channels act on A; R is unchanged. Define
L_j(e)=D(ρ_e||σ⊗ρ_R)−D((Φ^j⊗id)ρ_e||σ⊗ρ_R).
Since the R marginal is unchanged,
L_j=S(Φ^jρ_e)−S(ρ_e)+Tr[(Φ^jρ_e−ρ_e)(logσ⊗I)].

The input spectrum is {1/3,2/3,0,0}. The first output consists of a rank-one block on span{|10>,|01>} and a scalar on |11>. Its nonzero eigenvalues are (1+e)/3 and (2−e)/3. Its A=0 population decreases by e. Consequently, writing h for binary entropy in nats,
L_1(e)=h((1+e)/3)−h(1/3)+e log2
       =(4/3)e log2+O(e²).

Spectral pinching of σ is computational dephasing. Directly,
D(ρ_e||Δσρ_e)=(2/3)h(e)=(2/3)e log(1/e)+O(e).
Therefore D(ρ_e||Δσρ_e)/L_1(e) diverges as log(1/e)/(2log2).
NO finite reference-uniform constant bounds this fixed-spectral-dephasing entropy loss by one-step relative-σ entropy loss, even for this one fixed faithful-stationary self-compatible qubit channel.

For completeness Φ² is generalized amplitude damping with effective damping3/4 and equilibrium q=1/3. Its output matrix is
[[e/3, 0, 0, √(e(1−e))/3],
 [0, 1/3−e/6, 0, 0],
 [0, 0, e/3, 0],
 [√(e(1−e))/3, 0, 0, 2/3−e/2]].
The 00/11 block has trace 2/3−e/6 and determinant e/9−e²/18. Its smaller eigenvalue is e/6+O(e²). Together with the explicit eigenvalue e/3, these generate entropy (e/2)log(1/e)+O(e). The remaining eigenvalues approach1/3,2/3. The logσ term is O(e), so
L_2(e)=(e/2)log(1/e)+O(e),
L_2/L_1 ~ [3/(8log2)]log(1/e) → infinity.
Thus NO finite complete one-step-to-two-step loss comparison holds here.

## Exact scope
This is not an N371 counterexample: no prior-adapted EB recovery impossibility is proved. It concerns a fixed spectral comparator and an entropy-loss transfer. The positive Petz-square subclass remains an important distinction: Φ is KMS/Petz-selfadjoint but has negative eigenvalues; Φ² is a positive KMS operator and has the thermal coverage already established. The counterexample does NOT rule out an EB minorization theorem restricted to positive Petz squares, nor a recovery-fidelity bridge using a different functional. It does rule out silently converting that square's entropy bound to original one-step entropy loss by a constant factor.

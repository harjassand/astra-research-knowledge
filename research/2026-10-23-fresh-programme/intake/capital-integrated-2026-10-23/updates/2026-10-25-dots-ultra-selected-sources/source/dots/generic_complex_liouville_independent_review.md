# Independent review and extensions of the literal complex-POVM lift obstruction

24 October 2026. Exact symbolic source `generic_complex_liouville_obstruction.py` rerun successfully. This note checks the construction and adds fixed-interface robustness and a positive PPT-baseline class. None of these statements proves a separation of the optimized information coefficients.

## Exact uniqueness and transpose convention

The six effects E_(j,+/-)=(I +/- sigma_j/2)/6 span M_2 over the complex numbers: their sums span I and their differences span X,Y,Z. Consequently specifying Tr_A(E_i G) for every outcome fixes every physical operator block of G. The forced solution for target outputs

    B_i*=[sigma_i tensor I + I tensor sigma_i^T]/(2r)

is exactly the displayed formula using sigma^(T_R). Partial transpose on R commutes with the physical effect contraction, so Tr_A[E_i sigma^(T_R)]=sigma_i^T. Full transpose instead replaces E_i by E_i^T and fails for the Y effects.

For sigma=.9 Phi_2+.1 I_4/4, Pauli expansion and a local Y conjugation put the forced G in the form

    I_8/8 + (.9/16) sum_j sigma_j^A (sigma_j^(R')-sigma_j^R).

The coupling has spectrum 0 with multiplicity4 and +/-2sqrt(3) each with multiplicity2. This reproduces the exact negative eigenvalues 1/8-9sqrt(3)/80. The input and every POVM effect remain strictly positive.

## Larger references with a common CP extraction do not repair this target

Suppose a larger-reference positive state is followed by any common trace-preserving completely positive reference map to HS(R). Such a reference map commutes with every physical measurement effect. The extracted state would therefore be a positive trace-one G on the original specified target space satisfying the same output constraints, contradicting uniqueness and negativity.

The statement also excludes exact common positive compression/extraction when its nonzero common normalization is fixed. It does not address arbitrary outcome-dependent processing or a different realization that preserves only the desired metric ratios.

## Quantitative summed trace-error floor

For any attainable trace-one positive G on A tensor HS(R), let B_i be its cq output blocks and define

    epsilon=sum_i ||B_i-B_i*||_1.

Reconstruct

    S0=sum_i B_i,
    Sj=6(B_(j,+)-B_(j,-)),
    G=[I tensor S0 + sum_j sigma_j tensor Sj]/2.

Because ||I_2||_1=||sigma_j||_1=2, this gives

    ||G-G*||_1 <= epsilon+6epsilon=7epsilon.

Write a=9sqrt(3)/80-1/8>0. The forced G* has negative-part trace2a. Since both G and G* have trace1, their difference has trace zero; testing its positive part against the negative eigenspace of G* yields

    ||G-G*||_1 >=4a.

Therefore every such approximation has

    epsilon >=4a/7=(9sqrt(3)-10)/140 > .0399.

The same floor holds after any common trace-preserving CP extraction from an arbitrarily large reference. This is summed block trace norm, without a factor1/2. It is not a universal approximation lower bound for all conceivable information-coefficient constructions.

## Positive realization for arbitrary POVM pairs at PPT baselines

If the faithful input baseline sigma is PPT across A:R, then sigma^(T_R)>=0. The literal generic-complex lift

    G=[sigma tensor I + Swap(sigma^(T_R) tensor I)Swap]/(2r)

is then positive definite, because its first summand is positive definite and its second is positive semidefinite. It meets the arithmetic-mean output targets for EVERY complex effect, not merely real or common-antiunitary effects. The rectangular tangent construction X_ab=vec(H_ab) still has zero reference marginal whenever H_R=0.

Thus arbitrary complex POVM pairs admit the same faithful boundary BKM realization of every equal-reference SLD ratio whose baseline is PPT. This is a genuine restricted positive theorem, not a repair of a sufficiently NPT baseline. Positivity of the lift can also hold for some NPT inputs; in the isotropic family above its threshold is visibility1/sqrt(3), while PPT already fails above1/3.

## Consequence for possible prior-driven separations

Suppose a uniform complete equal-reference Umegaki comparison holds between two arbitrary POVM channels. The PPT lift implies the corresponding SLD comparison at every PPT baseline. The reference-score gauge changes the tangent but not its PPT baseline. Tensoring the auxiliary reference qubit used in the SLD-to-BKM integral preserves PPT, and affine interpolation between PPT state pairs stays PPT. Therefore the complete comparison extends to the conditional Umegaki comparison on PPT input pairs.

Consequently a separation between the global conditional and complete relative orders for measurement-channel pairs, if one exists, cannot be witnessed by PPT input pairs. It requires NPT input priors somewhere. This conclusion is limited to measurement-channel comparisons; it is not a theorem for arbitrary quantum-output channel pairs.

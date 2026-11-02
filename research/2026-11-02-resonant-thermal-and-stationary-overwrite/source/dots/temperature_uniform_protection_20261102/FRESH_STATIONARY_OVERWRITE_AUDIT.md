# Fresh stationary-overwrite audit and independent regression

2026-11-02. **PASS:** the theorem and its stronger commutator-variance version are valid for finite-dimensional L tensor G, one logical qubit, any stationary density matrix rho, and nonnegative storage time. Neither a logical twirl nor a Gibbs assumption is needed.

## Proof checks

- The auxiliary SWAP identity has the correct factor 1/2 and Y sign. Starting from the independent product xi_AR tensor rho_LG, tracing A after SWAP gives exactly xi_LR tensor Tr_L rho, even with logical/gauge correlations in rho and entanglement of input/reference. This is an ideal overwrite, not the original stationary state.
- In Duhamel's integral, stationarity permits commuting exp(-iHt) past rho^(1/2). Left/right unitary invariance then gives `||[U_T,Q_j]rho^(1/2)||_2 <= T sqrt(Tr rho C_j^dagger C_j)`, C_j=[H,Q_j]. No assumption on the overwritten state's stationarity is made.
- In the larger tensor product, each input Pauli tensor I_R is unitary, so `||sigma_A xi_AR^(1/2)||_2=1`, including mixed and entangled inputs. The SWAP triangle bound is therefore T/2 times the sum of the three commutator standard deviations.
- The two-unitary output inequality contributes exactly factor2. Stationarity gives `(I_AR tensor U_T)Omega(I_AR tensor U_T^dagger)=Omega`, so comparing U_T S with S U_T indeed compares storage against the overwritten input after tracing A.
- Partial traces over A and then G contract the trace norm of the Hermitian state difference. The bound holds for every reference/input with a fixed channel defined by tau_G; thus it bounds the diamond norm of the decoded storage channel minus identity (trace norm convention, not half trace distance).
- Under C_j=C_j P, `C_j^dagger C_j <= c_j² P`. Hence its rho expectation is at most c_j² Tr(P rho), regardless of whether P commutes with rho. This proves the projector version. The variance version is strictly more general and needs no projector.

The resulting bound is exactly `min(2,T sum_j sqrt(Tr rho C_j^dagger C_j))`, and at most `min(2,T sqrt(p) sum_j c_j)`. The coefficient6 for c_j<=2vn is correct, though individual vanishing commutators can improve it.

## Independent numerical regression (corroboration, not proof)

Code: `independent_stationary_overwrite_regression.py`; full reproducible results: matching `.json`.

Model: Delta=2, epsilon=.15, g=.4, with `H=Delta I_L⊗P1+epsilon I_L⊗X_G+g Z_L⊗P1`. The Gibbs exponential is evaluated by subtracting its minimum eigenvalue before exponentiation, including beta=10^6. Checked actual Gibbs states and separately exactly stationary fully polarized logical states `|±Z><±Z|⊗Gibbs(Delta P1+epsilon X±gP1)`. Inputs include Bell_LR, +X logical, and +Z logical, each with an explicit reference register.

Across 324 combinations (six temperatures, three stationary states, three inputs, six times), exact full-state and decoded trace errors satisfy both bounds and partial-trace contraction. Maximum numerical violation is 5.4e-16. All projector-support residuals vanish. The variance and sharp projector bounds agree to 1.2e-16, as expected here: for X,Y, `C_j^dagger C_j=4g²P`, while C_Z=0. Thus this model checks equality of the two certificates; it does not illustrate a strict variance improvement.

Selected actual-Gibbs Bell-input results at T=1:

| beta | logical <Z> | p | exact joint error | decoded error | both bounds |
|---:|---:|---:|---:|---:|---:|
| 1 | -.04925 | .129522 | .107685 | .100745 | .575826 |
| 100 | -.22614 | .006744 | .055277 | .004818 | .131397 |
| 10^6 | -1 | .008564 | .080818 | .005462 | .148066 |

The strongly polarized very-cold Gibbs example confirms that logical polarization does not invalidate the consumer. It also illustrates its honest limitation: virtual excited-clock admixture leaves a nonzero p floor as beta grows. The theorem has removed an unnecessary temperature factor in the dynamical consumer, not established a vanishing full-Gibbs bad-sector weight or indefinite storage.

## Boundary

The proof presupposes an exact decoded tensor factor and ideal overwrite/readout. It neither supplies physical WRITE controls nor constructs the stationary resource, nor establishes the required small commutator variance or projector probability for the actual many-body native Hamiltonian. Those remain separate static/implementation obligations.

# Exact weighted acquisition loss and general quantum-retention duration

The [general ledger proof](package/joint_root/general_acquisition_ledger.md) applies to **every permitted causal receiver** of the [fixed stream](README.md), including nontracial initialized workspace, arbitrary instruments, classical histories and inaccessible logical references. It evaluates an actual receiver's information loss; it does not optimize the attainable memory/processing tradeoff.

At tracial logical input, the actual source/receiver reference factors as `I_S/2 tensor sigma_j`, including each classical history. This is not independence for arbitrary or entangled inputs. In the changing-reference Hilbert norm, let a_j be average logical-Pauli squared norm in the source-identity sector and q_j the source-traceless part. q_j is an information quantity, not a qubit count. With `a_0=0,q_0=1` and nonnegative processing losses,

```text
a_j=a_(j-1)+s^4 q_(j-1)-ell_j^P,
q_j=r q_(j-1)-ell_j^Q,
a_N=1-r^N-L_N,
L_N=sum_j[ell_j^P+(1-r^(N-j))ell_j^Q]>=0.
```

The weighted terms separate already acquired information from information that could still be exported in later collisions. CPTP contraction of the appropriate monotone norm supplies positivity; it is not an independent scalar-tracial approximation.

## Recovery meaning and physical scope

Every final decoder has `epsilon_opt>=3(1-sqrt(a_N))/4`. The source constructs a physical global Clifford-twirled receiver with a Petz finish attaining `epsilon=3(1-a_N)/4=3(r^N+L_N)/4`, at separately paid synthesis/control costs. These bounds differ by at most two. They do not assert a cheap efficient Petz implementation for every arbitrary instrument/history.

Thus target epsilon requires `L_N<=1-r^N-(1-4epsilon/3)^2`, while `r^N+L_N<=4epsilon/3` suffices with the stated finish. Existing monotone quantum chi-square and pretty-good/optimal recovery comparisons are explicitly credited; the source-specific ledger and physical normalizations are the supplied deductions.

## Audit correction and width-sensitive witnesses

The supplied [channel audit](package/joint_channel/ledger_audit_and_rank_bound.md) corrects a refinement detail: revealing hidden Kraus labels can improve recovery. The refined positive-effect witness's energy is **at most**, rather than always equal to, three quarters of the actual unrefined cumulative losses. Equality holds for a fully Kraus-refined receiver. The core exact ledger is unchanged, and the stated lower bound retains its valid inequality direction. This correction is preserved rather than silently importing an equality for a more informative receiver.

The same audit proves a positive-rank isotypic witness using collective SU(2) sectors. It gives an exact finite-angle width-dependent loss bound involving the nonscalar spectral gap beta_n and an explicit rank penalty D_n(m). Beta_n's fixed-prefix quadratic weak-angle expansion is **not uniform for growing n**. No cumulative entropy bound or optimal joint scaling is supplied from it. Positivity/rank adds information beyond a generic Choi density cap without magically evaluating the needed growing-prefix spectrum.

## A duration converse, distinct from peak width

For `C_epsilon=4epsilon-8epsilon²/3`, let pi_j be the Bell-input probability of retaining at least one coherent qubit at cut j. The [quantum-retention theorem](package/joint_root/quantum_retention_window.md) gives

```text
pi_j >= [1-C_epsilon r^(-(N-j))]_+.
```

At equal collision spacing Delta, summing yields the necessary expected qubit-time `Delta sum_j[1-C_epsilon r^(-(N-j))]_+`. Its small-error sufficiently-long-horizon order is `Omega(Delta theta^-4 log(1/epsilon))`. This says quantum information must remain protected for a duration; it does not determine peak qubit count. The source audit states the nonvacuous error range explicitly.

[48-case ledger checks](package/joint_root/general_ledger_checks.json) exercise pure/mixed initial memory and recorded/unrecorded outcomes. These are finite implementation checks, not a universal optimization or laboratory experiment. All files are preserved unchanged; Capital performed no scientific replay or new proof audit. [Costs, restricted mechanisms and other evidence](processing-and-evidence.md), [original package/provenance](SOURCES.json).

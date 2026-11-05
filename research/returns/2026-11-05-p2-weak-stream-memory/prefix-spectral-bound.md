# General prefix memory converse and the unresolved spectral estimate

The supplied [complete proof](package/boundary/source_granted_converse.txt) and [report](package/weak_stream_memory.tex) derive a necessary memory condition for arbitrary causal receivers of the [fixed weak stream](README.md). This includes general quantum instruments, initialized workspace, arbitrary classical records/feedback and prior block processing. The physical source is granted to a hypothetical decoder **only as a lower-bound relaxation**: it can simulate the remaining known source collisions. The proposed receiver does not gain source access.

For a prefix of ell emitted qubits, set `D=2^ell` and let U_ell be the actual ordered source-collision unitary. On bath operators define

```text
T_ell(K)=Tr_S[U_ell(I_S tensor K)U_ell*]/2,
H_ell=I-T_ell T_ell*,
0=lambda_0<=...<=lambda_(D^2-1)<=1.
```

The identity is a zero mode; uniqueness is not presumed. All coherent systems retained across this cut count toward each branch's quantum dimension m_y. If every branch has dimension at most m and `0<=epsilon<=1/2`, successful eventual half-diamond recovery requires, for integer `L=D/m`,

```text
(lambda_0+...+lambda_(L-1))/L <= e_epsilon,
e_epsilon=3epsilon(1-epsilon).
```

For noninteger D/m, put `a=m/D`, `k=floor(1/a)`; the left side becomes `a sum_(j<k)lambda_j+(1-ka)lambda_k`. This is a **dimension** bound; qubit storage is `ceil(log2 m)`.

## Witness, profile and memory tails

A common transpose/Petz witness for the prefix instrument produces a normalized Choi state Z with both marginals `I/D`, `Tr(H_ell Z)<=e_epsilon`, Schmidt number at most m and density cap `0<=Z<=(m/D)I`. The receiver need not implement this witness or reconstruct the entire output. Filling low eigenspaces under the cap gives the profile bound. Dropping further Choi/marginal constraints makes it necessary, not sufficient for compression.

For `n_ell(a)=rank 1_[0,a)(H_ell)` and `Z_ell(t)=Tr exp(-tH_ell)`, any `a,t>0` give

```text
m >= [D/n_ell(a)] [1-e_epsilon/a]_+,
m >= D exp(-t e_epsilon)/Z_ell(t).
```

Under the actual physical Bell-input branch law, variable capacities obey

```text
Pr(m_y>m) >= [1-e_epsilon/a-m n_ell(a)/D]_+,
Pr(m_y>m) >= [exp(-t e_epsilon)-(m/D)Z_ell(t)]_+.
```

Summing at thresholds `m=2^j` bounds expected coherent occupancy; summing across actual physical time intervals bounds memory-time. Maximum capacities of mutually exclusive branches cannot be added as expected occupancy. Unlimited classical history does not evade the theorem, but the useful spectral estimate remains to be supplied.

## Exact moments carry an explicit cost

The source derives a `16^k`-dimensional finite transfer matrix M_k for `mu_k=Tr[(T_ell T_ell*)^k]`, with `mu_k=<0| M_k^ell |0>` in the specified replicated boundary convention. Direct dense powering costs `O(16^(3k) log ell)` arithmetic and `O(16^(2k))` storage, before precision/conditioning. Direct prefix operator space is `4^ell` dimensional. These are finite constructions, not efficient large-stream certification algorithms.

Exactly, `mu_1=4^(ell-1)[1+3cos(theta)^(4ell)]` and `Z_ell(t)=exp(-t)sum_(k>=0)t^k mu_k/k!`; truncating at K has absolute error at most `D^2 Pr(Poisson(t)>K)`. The rank-four dilation gives `mu_k>=D^2/4^k`. Elementary moment bounds therefore need replica number of order ell to certify the exponentially small slow-mode fraction relevant to a linear-qubit conclusion. Fixed low moments or a bulk limiting law do not settle it.

The exact two-site swap trial extends with factor `r^(ell-2)` and gives an **upper bound** on the minimum gap. At `.1` it already makes the gap-only one-percent converse vacuous. A lower bound on the restricted single-Pauli Gram is likewise not a full-space gap lower bound. Nonnormal homogeneous transfer eigenvalues, ordinary integrable fusion, a small MPO bond or closure of an operator algebra supplies neither the needed singular profile nor a physical compression.

[Moment barriers](package/boundary/moment_profile_barriers.txt), [finite moment receipt](package/boundary/moment_transfer_receipt.json), [trial witness](package/boundary/transfer_witness.json) and [short-prefix spectra](package/boundary/singular_gap_profile_0p1.json) retain the actual evidence. The ell=4–8 eigensolver diagnostics are not interval-certified asymptotic bounds; a small residual alone cannot exclude a missed slower mode. Existing transpose recovery, Schmidt-number and transfer-matrix machinery is credited. No Capital computation or fresh audit occurred. [Original package/provenance](SOURCES.json).

# Passive realization of the full deterministic Gaussian memory–noise frontier

Root extension, 29 October 2026 Australia/Brisbane. Status: authored theorem; independent review pending. This extends the receiver class in the accepted-if-reviewed noise-path theorem, rather than changing its proof file or silently broadening its review.

## 1. The stronger comparison

The fixed passive/vacuum synthesis theorem already gives an exact criterion for a final reported Gaussian POVM. An equally informed comparison should also permit active Gaussian processing and fresh Gaussian preparations. The following result shows that those additional ideal operations do not lower the retained canonical-mode requirement for this **destructive final-measurement task** at fixed added covariance.

The assertion concerns quantum modes across specified input-arrival cuts. It does not preserve an internal lossy hardware topology, a fresh-mode minimum, squeezing/energy budget, classical gain budget, or deadlines for releasing individual output values. It does not implement a full quantum input-output channel or return the measured field.

## 2. Receiver classes and theorem

The field arrives in fixed batches with specified features f_(i,t). The target final classical n-vector has Gaussian POVM characteristic function

    Mhat(u)=W(Fu) exp(-u^T N u/2),
    F=direct_sum_t f_t, Omega_t=Im Gram(f_t).

The enlarged deterministic Gaussian class permits, at each arrival:

- arbitrary finite Gaussian unitaries, including squeezing;
- fresh independent normal Gaussian ancillary states with finite covariance;
- Gaussian channels realized by fresh local Gaussian environments and discarding;
- ideal homodyne/general-dyne measurements, with their standard Gaussian dilation;
- fixed affine processing and linear displacement feedforward from previous records;
- arbitrary classical storage, but no hidden quantum system or correlated future ancillary supply crossing an arrival cut without being counted.

The symplectic transformations, measurement axes and linear gains are fixed from the supplied model. Nonlinear outcome processing and record-dependent choices of a new squeezing matrix, interferometer or measurement axis are not included. Every accessible quantum register that can influence later outcomes counts toward q_t. Any initial Gaussian register is introduced at the first batch and counted if it survives. Internal measurement records may be kept; the prescribed output statistics are final, with no separate early-release deadlines.

**Theorem.** This enlarged Gaussian class realizes the target with at most q_t retained modes if and only if the same path conditions hold:

    S_0=S_T=0, rank S_t<=2q_t,
    Gamma_t=S_t-S_(t-1)-Omega_t,
    N_t=N_t^T real, N_t+i Gamma_t>=0,
    sum_t N_t=N.                                               (1)

Whenever it is feasible in the enlarged class, a passive receiver with fresh independent vacuum, ideal homodyne and fixed classical linear processing realizes the same final reported POVM with no greater retained count at any arrival cut. It may use different fresh modes, live width, records and reporting delays.

## 3. Necessity beyond passivity

Each finite-covariance Gaussian ancillary state admits a local Gaussian purification from vacuum. Introduce that purification at the same arrival as the corresponding ancillary state. Its purifying output is never an accessible bypass into the future. This is mathematical dilation, not a free physical store. A Gaussian channel is treated similarly with its discarded environmental output. Mixedness does not create a new path for earlier information to influence later measurements.

Represent each fixed Gaussian measurement by a local Gaussian unitary and commuting homodyne quadratures. Linear displacement feedforward can be removed by carrying a known classical frame, or retained explicitly as an affine shift of the memory quadratures by earlier commuting records. It changes neither their canonical commutator nor the required quantum register size.

In this dilation, every final reported coordinate is a real linear function of the original input quadratures and the independent vacuum coordinates introduced batch by batch. All reported coordinates commute. Write their original-field coefficient as F' and their ancillary coefficients as g_t. Equality of the characteristic function for every original normal input fixes F'=F, with the given noise factor. Therefore

    Gram(g_t)=N_t+i Gamma_t>=0,
    sum_t N_t=N.

At a physical cut, a later outcome's past-supported component has access only to past classical records and the retained canonical quadratures. Pulled back to the introduced input/vacuum coordinates, it has the form

    Y_(past,t)=B_t y_(past)+L_t R_(memory,t).

The actual records commute with each other and with the surviving register, including in a linear displacement frame. Discarded outputs and virtual purifications cannot independently contribute to later outcomes. Thus

    S_t=sum_(s<=t)(Omega_s+Gamma_s)=L_t J_(q_t)L_t^T,

which proves the rank condition. Final commutativity gives S_T=0, and S_0=0 before any introduced input. No step requires the Gaussian unitaries to be passive. It requires only the specified linear dilation and physical causal accounting.

## 4. Passive sufficiency and reach

Given (1), factor each N_t+i Gamma_t as the Gram matrix of independent vacuum feature columns g_t. The augmented features (f_t,g_t) have prefix commutator S_t and globally commute. The accepted passive compression lemma constructs a single compatible causal receiver with retained count rank(S_t)/2. Tracing the detector vacuum gives exactly the required Gaussian characteristic function. This is the previous sufficient construction, now matching a stronger necessary class.

Consequently the weighted trace-noise path optimization and its exact two-batch spectral tail apply equally to this enlarged deterministic Gaussian class. Allowing active Gaussian processing does not defeat those ideal lower bounds. Passive implementation can use more fresh detector modes than a squeezed or mixed-ancilla implementation; only the retained-mode/noise frontier is equated.

The result can be applied to the entire final raw Gaussian record of another fixed Gaussian receiver by treating every such record coordinate as part of the target. Equality then preserves its destructive reference assemblage. It still does not guarantee that each record is emitted at its original time. If an external adaptive device consumes an early record before later inputs, those causal output deadlines impose a stronger instrument contract and need their own synthesis theorem.

The source-erasure conversion remains separate. Its complete raw-record bound is proved for the receiver actually delivered; matching a smaller reported POVM alone does not match source feedback on a larger unreported refinement.

## 5. Limits that matter physically

Finite loss or detector inefficiency can change which active operations are useful. The theorem permits ideal readout and constrains only the input order and retained canonical-mode count. It does not promise to reproduce an active design using the same compulsory lossy links or detector efficiencies. For example, squeezing before an inefficient detector can change its effective noise cost; it is excluded from the separate passive inefficient-detector benchmark, not ruled out by the present ideal theorem.

The passive realization has bounded interferometer amplitudes but can require large classical gains and precise mode capture. Input energy can concentrate into a small retained register. Preparation fidelity, record precision, local-oscillator resources, collection, latency, source coherence and reuse remain operational costs. Infinite-squeezing nonnormal ancillary states are not available states in either class; sharp ideal homodyne is a measurement idealization treated by spectral measures.

The conclusion is a general measurement-synthesis principle at an explicit ideal interface. It makes the strongest deterministic Gaussian alternative part of the characterization. It does not imply optimality against arbitrary nonlinear/adaptive or non-Gaussian receivers, nor establish a device advantage or historical priority.

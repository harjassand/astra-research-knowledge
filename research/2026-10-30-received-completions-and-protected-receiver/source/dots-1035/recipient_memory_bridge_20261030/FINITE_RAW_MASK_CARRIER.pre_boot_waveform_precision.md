# Actual finite raw Bell-mask carrier: uniform outcome-register moment
2026-10-30. Component derivation for RATE_SEPARATED_RECIPIENT_CANDIDATE.md; not an independent receipt.

## 1. Fixed local hardware and dynamics
At each physical Bell column i there are two actual readout pointers with labels WAIT,0,1. After the finite CNOT pulse, their jumps measure X_Q and Z_A:

    J_b^Q=sqrt(kappa)|b><WAIT| tensor Pi_b^X,
    J_b^A=sqrt(kappa)|b><WAIT| tensor Pi_b^Z.

The measured outcomes are retained physical registers. No conditioning on a normalized rare outcome occurs. Define W_Q,W_A as their WAIT projectors.

A private, directed classical path of fixed length L connects this column to the recipient. Each carrier register has the exact five-symbol alphabet {WAIT,00,01,10,11}. At rate nu, link 1 measures the two pointer labels in their declared classical basis and overwrites carrier 1 with WAIT if either pointer is WAIT, and otherwise with their two-bit pair p. At rate nu, link j>=2 measures carrier j-1 in that basis and overwrites carrier j with that symbol. These are explicit bounded-body CPTP measured-classical copy maps. They transmit no coherent quantum state; copying is of basis values, not arbitrary qubits. Every link has finite local dimension, finite rate and finite spatial length. The per-column path length is fixed independently of N, and N columns have O(N) parallel bandwidth. Replacing this by a long-distance or N-dependent network changes the latency bound.

Before this one transfer, all pointers/carriers are finitely reset to WAIT. Actual failures form a sparse boot set under the accepted finite-reset moment, not a promise of perfect reset. On a column outside that set and every subsequent inserted-fault support, all non-WAIT values are the correct physical Bell bits, by induction along the directed path. Stale initial values on a boot-failed column are charged to that column. An ordered sequence of copies can also flush them, but no such unproved freshness assumption is needed for the theorem.

Copies may continue during the final recipient pulse. On a clean completed column all values are the same fixed p and remain so; partial/corrupt columns are charged. The source pointers are held only for this fixed finite endpoint, not exponentially long.

## 2. Explicit full-Hilbert waiting witness
Let W_j be carrier j's WAIT projector. The diagonal waiting algebra is autonomous under the nominal pointer/copy generator, even when DATA, pointer values and a common bath are correlated:

    L*W_Q=-kappa W_Q,       L*W_A=-kappa W_A,
    L*W_1=nu(W_Q OR W_A-W_1),
    L*W_j=nu(W_(j-1)-W_j),  j>=2.

The first identities use sum_b Pi_b=I, not an assumed measurement outcome. Pointer/old-memory DATA dynamics not acting on pointer/carrier registers annihilate these observables. Set

    b_j=2^(L-j),
    a=2 nu b_1/kappa,
    R=a(W_Q+W_A)+sum_(j=1)^L b_j W_j,
    Rmax=2a+sum_j b_j,
    r=min(kappa,nu)/2.

Since W_Q OR W_A<=W_Q+W_A, the EXACT full-Hilbert order inequality is

    L*R <= -(kappa a/2)(W_Q+W_A)
             -sum_(j<L)(nu b_j/2) W_j -nu b_L W_L
           <= -r R.

Let B be the OR of all L+2 waiting projectors, and A=R/Rmax. With a0=min(a,b_L)/Rmax>0,

    a0 B <= A <= B <= I,       L*A <= -r A.          (2.1)

This is a concrete witness, not a numerical Lyapunov assumption. It treats all label coherences because it is a full operator inequality; the nominal maps preserve its diagonal algebra. It bounds unfinished columns, not the truth of arbitrary already-non-WAIT initial values. The latter are paid by the actual boot/error support as stated above.

## 3. Shared-bath and outcome-uniform hierarchy
For any column set S, M_S=product_(i in S) A_i is positive. Every other nominal generator, including old DATA read/correct maps and new-controller-only boot, annihilates each A_i. Thus

    L_nom* M_S <= -r |S| M_S.

Let the SAME local bounded normal HP perturbation annihilate identity termwise, have per-column incident cb norm sum <=eta_ep, and touch at most q carrier columns. Centering a TP total perturbation into identity-annihilating local terms is allowed with its explicit factor-two norm cost. For K=S intersect supp(Z),

    N_Z* M_S <= ||N_Z*||cb M_(S\K).

This follows by locality and 0<=A<=I, retaining arbitrary bath/reference coefficients. The standard induction gives

    Tr M_S rho_T <= p(T)^|S|,
    p(T)^q=e^(-qrT)+(eta_ep/r)(1-e^(-qrT)),

provided eta_ep<r; p(0)=1 covers arbitrary initial correlations. Hence

    Pr(all columns in S unfinished) <= [p(T)/a0]^|S|.  (3.1)

Choose a fixed T_carrier and then eta_ep so p(T)/a0 is below the prescribed inclusion target. A subset union gives exponentially small probability of more than beta_carrier N unfinished columns. This single unconditional CP-instrument estimate includes every physical outcome block with its true weight. It does NOT normalize by individual Bell-outcome probabilities or assume outcome/noise independence.

The old DATA maps themselves commute every A_i and need not contribute eta_ep here, even though they are separately charged for the quantum transfer. A generic fault/control term touching carrier or pointer registers does contribute. All these registers remain physical sites in the same incident norm model, never an unconstrained bath.

## 4. Actual raw mask and sparse exceptions
At the fixed deadline, the recipient's Hamiltonian is controlled by the final carrier value. For p in {00,01,10,11}, choose Hermitian P_p in {I,X,Z,Y} with the usual Bell correction up to an outcome-dependent scalar phase; set H_WAIT=0 and

    H_p(t)=f(t)(I-P_p),    integral f(t) dt=pi/2.

The waveform is bounded and has fixed finite duration, including finite ramps. On an intact completed column it implements P_p exactly. The full control is block-diagonal in the actual carrier value, so it preserves all waiting projectors. Continuing clean copy/measurement dynamics leave p fixed there.

Define the exceptional support as the union of: finitely boot-failed columns; analytically selected unfinished columns; actual Poisson fault/old-DATA attempt supports; and the local supports of retained forward-Duhamel control-error insertions. Its size is bounded by the corresponding sum of budgets. Outside this set, the mask is precisely the actual full Bell outcome. Inside it, no hidden completed Bell measurement is assumed. The companion joint-span lemma expands the remaining Q,A functional in a local Bell basis and retains virtual labels coherently as auxiliary coefficients. The difference between the applied mask and that virtual full outcome is a Pauli supported only on the exceptional set.

Therefore this carrier supplies finite noisy physical feedforward with explicit latency/bandwidth and sparse missing arrivals. It supplies neither indefinitely reliable classical memory nor an autonomous command schedule.

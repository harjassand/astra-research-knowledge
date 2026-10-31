# Excitation-preserving lossy qubit registers: explicit candidate interface
31 October 2026. Root corollary candidate; depends on the not-yet-reviewed whole graded compiler.

## Physical model
Take r private qubits initially |0...0>, n_i=|1><1|_i, N=sum n_i, and sigma_i^-=|0><1|_i. The system-register free Hamiltonian H_f commutes with N. Examples include system drift, known diagonal excitation interactions n_i n_j, and number-conserving XY exchange. The couplings are

    R_plus=sum_i F_i sigma_i^+,
    J_i=2sqrt(lambda) sigma_i^-.

Every F_i is system-only with supplied controlled block encoding, accessible normalization f_i, and paid adjoint/selection cost. Set g^2=sum f_i^2, Gamma=g^2/lambda. Neither a Gaussian bath nor harmonic-oscillator CCR is assumed. Unknown H_f remains expensive if its actual controlled evolution is expensive.

## Earned removal and raising maps
On a bitstring x with Hamming weight n>0, coherently prepare a color i uniformly over its n occupied bits, then erase that bit:

    V_minus |x> =sum_{i:x_i=1} |i>|x-e_i>/sqrt(n).

Distinct input strings have orthogonal output supports because (i,post-string) uniquely reconstructs the original string. This is an isometry on N>0 and can be implemented with polynomial-in-r reversible population-count and controlled state-preparation arithmetic. Vacuum is flagged separately. Its inverse unitary supplies the adjoint block. The color is retained for physical emissions.

Prepare the system stack W/g=sum_i |i>F_i/g by amplitudes f_i/g and the supplied controlled F_i/f_i blocks, retaining i. Since sum F_i^dagger F_i<=g^2I, this is an acquired contraction. Applying V_minus^dagger after that stack on an n-excitation string gives

    O_plus|H_n=R_plus/[g sqrt(n+1)].

If i was already occupied, the corresponding proposed insertion lies outside the image of V_minus and contributes zero. This implements hard-core exclusion rather than pretending sigma_i^+ is bosonic. Hence R_plus R_plus^dagger<=g^2N follows, and the stacked physical jump is 2sqrt(lambda) V_minus sqrt(N), with no gratuitous sqrt(r) normalization.

## Interface with the abstract scalar bridge
The no-jump decay is -2lambda N. Since H_f preserves N, its propagation is the scalar decay on each total-excitation sector times the paid H_f unitary. Every interaction insertion changes total excitation by one and is bounded/encoded by g sqrt(n+1) or g sqrt(n). The same one-dimensional oscillator positive kernel therefore majorizes the operator-valued words, including their exact (-i)^V phase. It is a majorant, not a claim that the private qubits are oscillators. Events attempting an unavailable hard-core insertion naturally have zero physical block.

Physical sectors have dimension binomial(r,n) times the system dimension, but coherent preparation reads only n and scalar endpoint labels. It must never enumerate those sectors. The actual within-sector state is propagated by the selected H_f and O_plus/O_minus circuits.

One may use total cutoff min(r,L). For L>=r there is no physical truncation at all. For L<r the already local-reviewed uniform moment/cutoff calculation applies, because it used only the grading relations, R_plus R_plus^dagger<=g^2N, total loss intensity4lambda N and downward jumps. Prescribed system instruments and retained reference records are allowed; physical bath colors stay private.

The remaining conclusion is conditional on the whole graded receiver: poly(r,1+Gamma T+p,log microscopic rate,log1/error) administrative overhead with the actual H_f and operator-encoding costs paid. It is not a free fast-forwarding theorem for arbitrary interacting Hamiltonians. It does not cover unequal losses mixed by H_f, excitation-creating H_f, arbitrary thermal preparations, public reservoir measurements or unpriced source acquisition.

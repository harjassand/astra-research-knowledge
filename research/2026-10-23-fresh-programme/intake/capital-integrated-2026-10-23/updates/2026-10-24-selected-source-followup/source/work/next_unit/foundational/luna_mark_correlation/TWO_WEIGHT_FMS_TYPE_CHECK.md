# Check: grouping the four equal Schmidt weights

For the FMS state \(\psi=(|00\rangle+\sqrt2\sum_{j=1}^4|jj\rangle)/3\), every length-\(n\) Schmidt string with exactly \(a\) nonzero symbols has the same amplitude \(2^{a/2}/3^n\). There are
\[
D_a=\binom na4^a
\]
such strings. Therefore the normalized sector vector
\[
|\Phi_a\rangle=D_a^{-1/2}\sum_{z:\,\#\{i:z_i\ne0\}=a}|z,z\rangle
\]
is maximally entangled on a local support of dimension \(D_a\), and its squared Schmidt-sector weight is
\[
p_a=D_a\frac{2^a}{9^n}=\binom na\frac{8^a}{9^n}.
\]
These \(n+1\) orthogonal sectors exhaust the tensor-power state: \(\sum_{a=0}^n p_a=(1+8)^n/9^n=1\) and \(\psi^{\otimes n}=\sum_a\sqrt{p_a}\,\Phi_a\). Hence one sector has weight at least \(1/(n+1)\). This is exact grouping by equal nonzero Schmidt coefficients, not an approximation or an unrecorded projection.

For every full input tuple \(q\), the original product of fine five-outcome FMS PVMs defines a joint all-win projection \(W_q\) with \(W_q\psi^{\otimes n}=\psi^{\otimes n}\). Thus \(W_q\ge|\psi^{\otimes n}\rangle\langle\psi^{\otimes n}|\) and the fixed largest-weight \(\Phi_a\) wins all coordinates with probability at least \(p_a\ge1/(n+1)\), pointwise for every \(q\). Use \(\Phi_a\) embedded in the original local \(5^n\)-dimensional spaces and keep the original fine PVMs and their outcome records unchanged. Alternatively, restrict to the sector support and compress each PVM to a complete POVM with the same fine labels. No success-conditioned resource or nonmaximally entangled resource is used.

This confirms the draft's two-weight coarsening. The \(n+1\) sectors replace the finer \(\binom{n+4}{4}\) count and strengthen the pointwise lower bound to \(1/(n+1)\); the later greedy argument needs only a polynomial lower bound.

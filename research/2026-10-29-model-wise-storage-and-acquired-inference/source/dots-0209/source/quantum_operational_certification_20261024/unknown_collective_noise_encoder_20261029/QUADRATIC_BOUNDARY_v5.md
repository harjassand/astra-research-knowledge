# Quadratic frame-mismatch cost for a singlet memory
2026-10-29. New theorem proposed for review; improves v1's linear boundary bound. No change to the structural promises.

Let P denote the ENTIRE exact total-spin-zero sector. Let E embed the chosen logical L into P. In exact aligned coordinates, the learned encoder is S=WE, where W is a system-only unitary basis mismatch. Define Loff=QWE, Q=I−P, and ℓ=||Loff||op. Let U be the complete unitary dilation of an arbitrarily long storage process. The fixed full joint collective algebra implies
U=(P tensor U0) direct-sum UQ,
where U0 is a bath unitary, UQ acts on Q and bath, and the bath starts independently of the fresh logical input. Any added discarded bath registers can be included in the dilation. This theorem is stated directly for such unitary dilations; do not infer one from reduced-channel marginals alone.

The learned decoder projects onto S's code and applies S†; orthogonal outcomes are erased or reset without retaining coherence with the code outcome. Its code-return amplitude on system+bath is
A=(S† tensor I)U(S tensor I).
Write B=PWE and Loff=QWE. Since B†B+Loff†Loff=I_L,
A−I_L tensor U0
 = (Loff† tensor I)[UQ−I_Q tensor U0](Loff tensor I),
so ||A−I tensor U0||≤2ℓ². This is an exact identity, not a Taylor expansion and not an assumption that error directions are Pauli.

The orthogonal-code leakage amplitude Kbad=(I−SS†)U(S tensor I) has norm at most 2ℓ: subtract (S tensor U0), which the output projection kills, and note
[U−I_system tensor U0](S tensor I)=[UQ−I_Q tensor U0](Loff tensor I).

Purify the fixed initial bath state. The good branch amplitude and ideal amplitude are contractions, so their induced CP-map difference has diamond norm at most
(||A||+1)||A−I tensor U0||≤4ℓ².
The completed bad CP map has diamond norm equal to its maximal trace, at most ||Kbad||²≤4ℓ². Triangle inequality gives
||LearnedService−Ideal||diamond ≤8ℓ².
Partial tracing bath, arbitrary external reference, and either decoder completion preserve this bound. No observation/conditioning on leakage is required. The ideal is embedded in the non-erasure output for an erasure decoder. The statement also holds for the general finite-dimensional subsystem when the full exact algebra is identity on the same logical factor, but ONLY the singlet version is claimed here.

Since ℓ≤||W−I||≤α from v1,
||LearnedService−Ideal||diamond ≤8α²
 ≤192(n−1)² e²/g²
 ≤15552(n−1)² η²/g².
For ε≤1 choose η=sqrt(ε)g0/[128(n−1)]. This implies the sign-rounding condition and error ≤ε. Pooled v2 acquisition therefore costs
O(n² g0^(−2) ε^(−1) log(n/δ)) full-array calls,
and O(n³...) physical-qubit preparation/readout, plus actual compiler/control errors. This improves the ε dependence, not the structural generality or known novelty status.

Gap-adaptive v3 may replace its linear stopping criterion by
192(n−1)² e_j²/gL_j² ≤ ε.
It still supplies the sign condition for ε≤1, and retains all model/failure caveats. No per-time symmetry-breaking perturbation is covered; those errors can accumulate even when basis-mismatch error does not.

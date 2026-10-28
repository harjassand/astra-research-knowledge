# Low-trace decoder localization under square-root operator noise

27 October 2026. Local post-cutoff deterministic lemma; independent receipt requested.

Use the exact orthogonal-reset source and feasible SDP of
`low_trace_decoder_sdp_relative_learning_root.md`. Thus P=Pi is a projector
of rank<=r, A commutes with P, A<=2|H|, and any feasible F satisfies
0<=F<=I and TrF<=r. Put L=Tr H(P-F)>=0 and D=F-P.

Then

                    ||D A^(1/2)||_1 <=4 sqrt(r L).       (1)

Indeed, relative to P and Q=I-P write A=A1 directsum A2 and F in blocks.
Set l1=Tr A1(I-F11), l2=Tr A2 F22. Then l1+l2<=2L.
The diagonal blocks satisfy, by Hilbert-Schmidt Cauchy and factorization,

 ||(I-F11) A1^(1/2)||_1<=sqrt(r l1),
 ||F22 A2^(1/2)||_1<=sqrt(r l2).

Here Tr(I-F11)<=r and TrF22<=r. Offdiagonal blocks have rank<=r.
From F^2<=F, F12F21<=F11-F11^2<=I-F11 and
F21F12<=F22-F22^2<=F22. Hence their nuclear norms are bounded by
sqrt(r l1), sqrt(r l2), respectively. Summing the four embedded blocks
proves (1). This does NOT assume rank F<=r.

Suppose an acquired estimate obeys the mathematical decomposition

 Hhat-H=A^(1/2)Z+Z* A^(1/2)+R,
 ||Z||<=z, ||R||<=b.

No knowledge of A or Z is required by the optimizer. Let F maximize
Tr Hhat F over the actual feasible SDP. Variational optimality gives

 L<=|Tr(Hhat-H)(F-P)|<=8z sqrt(rL)+2rb.

Young's inequality yields

                        L<=64 r z^2+4r b.              (2)

An additive optimization tolerance delta adds 2delta on the right.

A sufficient acquired interface uses a KNOWN G with G<=c(A+tI). Let
S=sqrt(G) and acquire a Hermitian filtered error E0 with ||E0||<=epsilon,
so Hhat-H=S E0+E0 S. Douglas factorization gives
S=(A+tI)^(1/2)K, ||K||<=sqrt(c). Since
||(A+tI)^(1/2)-A^(1/2)||<=sqrt(t), take Z=K E0 and obtain
z<=sqrt(c)epsilon, b<=2sqrt(ct)epsilon. Equation (2) becomes

             L<=64 c r epsilon^2+8r sqrt(ct)epsilon.

In particular epsilon=O(sqrt(t)) gives L=O(rt), without any spectral gap
or minimum success eigenvalue. This is a deterministic receiving lemma;
it does not, by itself, establish acquisition of the filtered estimate.

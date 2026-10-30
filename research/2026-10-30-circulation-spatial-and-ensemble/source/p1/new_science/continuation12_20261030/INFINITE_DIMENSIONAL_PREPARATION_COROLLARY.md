# Qualification when no finite predictive space closes

30 October 2026. Root analytic corollary. This uses the standard circle
heat semigroup to exhibit the scope of the new preparation receiver; it
does not claim the heat equation, infinite rank or smoothing obstruction
as new. Earlier Astra infinite-rank and sharp-readout results remain intact.

Let the hidden coordinate x lie on a circle of circumference 2 pi, with
uniform law mu and visible label Y=1{0<x<pi}. An actual fixed call is the
reversible thermal diffusion kernel

    P = exp(tau kappa partial_x^2),    tau>0, kappa>0.

Its unknown fixed diffusivity need not be estimated. The actual port must
supply that reciprocal kernel, the clock, noninvasive label, fresh warranted
uniform preparations and the stated conditional deployment preparation.
The supplied input is f=2Y. It can be prepared by rejection of the other
label from independent uniform specimens, with the full record/clock
qualifications in the accompanying proofs. This is a fixed-kernel example;
it does not impose a hidden jump-rate cap on a diffusion.

The actual output after n calls has density rho_n=P^n f. In L2(mu),

    f(x)=1+(4/pi) sum_{k positive odd} sin(kx)/k,

    rho_n(x)=1+(4/pi) sum_{k positive odd}
                     exp(-kappa tau k^2 n) sin(kx)/k.       (1)

## 1. The reachable family is genuinely infinite dimensional

Suppose sum_{n=0}^L c_n rho_n=0. Comparing each odd sine coefficient in
(1) gives the polynomial identity

    sum_{n=0}^L c_n z_k^n=0,
    z_k=exp(-kappa tau k^2),    k=1,3,5,... .

The infinitely many z_k are distinct. A finite polynomial with these
roots is identically zero, so every c_n is zero. Thus every finite initial
segment of the reachable family is linearly independent. In particular,
no finite-dimensional P-invariant space contains the nonconstant sharp
readout f. This is consistent with the earlier smoothing obstruction.

## 2. A finite physical experiment still measures the full density error

The actual chronological echo for words of lengths m and n is simply
m+n calls on one fresh baseline specimen with report f(Y_0)f(Y_end).
This report is either zero or four. Its expectation is

    K(m,n)=1+(8/pi^2) sum_{k positive odd}
                          exp(-kappa tau k^2(m+n))/k^2.

Three such experiments acquire

    D(m,n)=(8/pi^2) sum_{k positive odd}
       [exp(-kappa tau k^2 m)-exp(-kappa tau k^2 n)]^2/k^2.  (2)

The experimenter does not evaluate this series or learn kappa: the
display is the analytic explanation of the measured quantity. For every
common later causal receiver on the included physical state,

    TV_later <= min(1, sqrt(D(m,n))/2).

The literal reverse-word witness has probability gap D(m,n)/4. Finite
data supply the same bounded-report confidence calculation as in the main
proof, and the actual trial duration is (m+n) tau plus initialization,
sensing, switching and restoration. No hidden Fourier mode is sensed,
copied or fitted. There is no observation-depth factor after the single
qualified substitution, even though exact finite closure is impossible.

## 3. What this establishes

The positive receiver is not relying on a secretly finite predictive
model in the numerical demonstration. Infinite hidden complexity and
infinite reachable rank can coexist with a finitely acquired full-state
comparison of specified reachable preparations. This does not provide a
uniformly efficient search over all words, a cheap initializer, arbitrary
hidden-input tomography, exact finite-data equality, or a claim that the
unknown diffusivity cannot be estimated by an ordinary method. It explains
which stronger representation is unnecessary for the selected task.

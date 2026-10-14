# Nonlinear point-query sampler: matched 8D benchmark

## Finding

The incoming tangent-resummed sampler passes its stated certificate and gives a finite expected-work point-query algorithm on this coupled nonlinear example. It does **not** unlock the requested 1% answer: an equally informed deterministic constant-tangent correction already has a rigorous error bound below 1%, using a finite sparse Fourier calculation. In one compiled implementation the sampler is much faster per query, while the deterministic method gives a stronger deterministic certificate. This is a bounded counterexample to a practical-advantage claim, not a general lower bound against the sampler.

The benchmark is synthetic. It is an 8D nonlinear elliptic reaction field with no closed-form nonlinear solution used or known in this experiment; it is not a calibrated physical system. Its Fourier input is supplied to every method, and exploiting that structure is part of the matched comparison.

## Supplied problem and cost contract

On the flat torus \(\mathbb T^8=[0,2\pi)^8\), solve

\[
-\Delta u+u+25u^4=26+10g(x),\qquad
g(x)=\frac1{16}\sum_{j=0}^{15}\cos(k_j\cdot x+\phi_j).
\]

For \(j=0,\ldots,7\), \(k_j=e_j\); for \(j=8,\ldots,15\), \(k_j=e_{j-8}+e_{(j-7)\bmod 8}\). The phases are \(\phi_j=0.17(j+1)+0.013(j+1)^2\). The cyclic pair modes connect all coordinates, and the quartic reaction multiplies modes and creates many mixed frequencies. The query is \(x_q=(0.21,0.40,\ldots,1.54)\). The displayed model and its 16 Fourier terms, predictor, and coefficients are supplied. No unknown physical parameters, reference solution, or mesh are acquired.

The predictor is the screened linear solution

\[
v=1+e_0,\qquad e_0=\frac{10}{16}\sum_{j=0}^{15}\frac{\cos(k_j\cdot x+\phi_j)}{101+\lVert k_j\rVert^2}.
\]

It uses the linearization at \(u=1\), not the nonlinear answer. The exact coefficient \(\ell^1\) bound gives \(\lVert e_0\rVert_\infty\le A=5/102+5/103=1025/10506\). Thus \(v>0\), the tangent is \(V=1+100v^3\), and the residual is exactly

\[
r=-25(6e_0^2+4e_0^3+e_0^4).
\]

With \(h=1/40\), exact rational arithmetic verifies \(R=\lVert r\rVert_\infty\le1.52292120552642\), \(74.49372336665321\le V\le133.21743480539783\), \(P(h)=0.11466019495936204\), \(\Gamma(h)=9.242194552821683\), and enclosure slack \(\lambda h-R-P(h)=0.22476168368054844>0\). All listed values and their exact fractions are in `analysis_results.json`; `analyze.py` asserts the rational inequalities directly. The certificate build uses the supplied 16 modes and rational coefficient arithmetic, about \(O(16\cdot8)\) elementary coefficient operations. It performs no grid solve or residual sampling.

For each FJ tree endpoint the compiled model evaluator draws eight Gaussian coordinates and an exponential time, wraps the endpoint to the torus, evaluates the 16 displayed cosine phases to obtain \(v\), then evaluates the algebraic residual, tangent, branch probabilities, and one branch draw. A residual terminal event evaluates the residual formula; it does not call a separately acquired source oracle. With \(\epsilon=0.01\), \(\delta=0.05\), Hoeffding requires 47 independent trees. The theorem's expected endpoint bound is \(\Lambda/(\lambda-\Gamma)=2.0415986756\) per tree, hence at most 95.9552 expected endpoints for the reported query.

The measured alternatives below use the same supplied coefficients. They are costed at three levels: analytic arithmetic counts, executable wall time, and (where stated) finite-precision certification. Wall times are single-host diagnostics, not complexity claims.

## Executable sampler result

`benchmark.cpp` implements the incoming quartic sampler. The 47-tree run generated 68 endpoints (35 residual-terminal events; largest single tree 4 endpoints) and returned \(0.9926195636097664\). The 100,000-tree diagnostic generated 145,797 endpoints and returned \(0.9926341239612660\). The constant-tangent deterministic estimate below is \(0.9926389995241438\); the difference in the larger stochastic run is about \(4.88\times10^{-6}\). This is only an internal consistency diagnostic, not an exact reference value.

Across 1,000 repetitions of the 47-tree query, the C++ run took 15.83 microseconds per query on the recorded host. The mathematical Hoeffding statement assumes exact independent draws and arithmetic. This executable uses `std::mt19937_64`, standard floating-point exponential/normal transforms, and ordinary double arithmetic; it has no interval error or pseudorandom-distribution bias analysis. Its observed runtime and estimates therefore do not themselves certify the advertised probability statement.

## Strong deterministic comparator

Let \(e=u-v\), \(V_{\rm mid}=(\lambda+\Lambda)/2\), and \(P_x(e)=150v(x)^2e^2+100v(x)e^3+25e^4\). The exact correction satisfies

\[
e=T(e)=(-\Delta+V_{\rm mid})^{-1}
\big[r+(V_{\rm mid}-V)e-P_x(e)\big].
\]

The incoming tube theorem gives \(\lVert e\rVert_\infty\le h\). On that tube,

\[
\lVert T(e)-T(0)\rVert_\infty\le q_D\lVert e\rVert_\infty,
\quad q_D=\frac{(\Lambda-\lambda)/2+\Gamma(h)}{V_{\rm mid}}
=0.3717089694.
\]

Therefore the first deterministic correction

\[
e_1=T(0)=(-\Delta+V_{\rm mid})^{-1}r
\]
obeys the all-point bound \(\lVert e-e_1\rVert_\infty\le q_Dh=0.00929272423588759<0.01\). This already meets the same absolute point-error target with probability one in exact arithmetic. It does not require knowing \(u\). Since \(r\) is a polynomial in the supplied finite Fourier predictor, \(e_1\) has finite Fourier support and each mode is divided by \(V_{\rm mid}+\lVert k\rVert^2\).

Sparse convolution uses 232,129 complex coefficient products/updates to form \(e_0^2,e_0^3,e_0^4\); the residual has at most 21,487 candidate modes. A query then evaluates those modes plus the 16 predictor modes. The double-precision C++ implementation took 4.33 ms for one build plus query and 0.239 ms per query after coefficients were cached. It is about 274 times slower than the measured FJ query for one query, or 15 times slower per query when cached. This speed comparison is only a diagnostic: neither wall-time path has a matched interval validation for every transcendental/random operation.

To close that gap for the deterministic side, `deterministic_interval.py` evaluates the finite Fourier expression with `mpmath.iv` 1.3.0 at 40 decimal digits. It encloses

\[
e_1(x_q)\in[0.992638999524143754352980818652567523202772059,
0.992638999524143754352980818652567523203346031].
\]

Combining that interval with the exact rational contraction radius yields the solution enclosure

\[
u(x_q)\in[0.983346275288256165291455485935588180159443184,
1.00193172376003134341450615136954686624668639].
\]

The run took 7.78 seconds including interval convolution and query on this host. This validates the finite deterministic expression and its pointwise PDE enclosure within the interval-arithmetic implementation; it is not a field-wide enclosure or a validation of FJ's pseudorandom implementation. The measured cost, interval output, and exact error-radius fraction are in `deterministic_interval_results.json`.

## MLP and branching comparators

For a matched multilevel Picard comparator, clip the correction argument to \([-h,h]\) in the fixed-point nonlinearity. This preserves the certified solution and makes the periodic extension globally Lipschitz on \(\mathbb R^8\). In the standard-Brownian normalization of Beck, Gonon, and Jentzen, the mapped constants are \(\lambda_M=V_{\rm mid}/2=51.9277895430\), \(L_M=(\Lambda-\lambda)/4+\Gamma/2=19.3020251361\), and \(\lVert f(x,0)\rVert_\infty\le R/2\). Corollary 3.11's pointwise RMS bound, with the source integral bounded by \((R/2)^2/(\lambda_M-L_M)\), requires RMS at most \(\sqrt{0.05}\,0.01\) to obtain a 95% error statement by Markov's inequality on the squared error. The theorem's strict branching parameter condition gives \(M\ge18\). Searching integer \(M\in[18,100000]\) and the corresponding level using the published error bound selects \(M=487,n=8\), RMS bound 0.00223451, and about \(4.07\times10^{23}\) endpoint-evaluation tasks. This count uses the full-history recurrence normalized to one endpoint task per unit; the paper's operation recurrence charges \(d+1\) per sample term. In this 8D instance each endpoint also requires Brownian coordinate generation, the shared 16-mode feature evaluation, and the scalar MLP arithmetic. No MLP wall-time run was performed.

That MLP number is the cost of this conservative published certificate after the stated mapping. It is not an observed run and not a lower bound on a tuned MLP implementation. In particular, MLP remains a serious high-dimensional comparator, not something ruled out by this calculation. The source paper establishes polynomial complexity under its hypotheses, while its authors note that theorem constants can be poor. See [Beck, Gonon, and Jentzen (2024), Corollary 3.11 and Theorem 3.16](https://link.springer.com/article/10.1007/s42985-024-00272-4).

The uncentered independent-product branching representation of \(u=(-\Delta+1)^{-1}(s-25u^4)\) has no uniformly finite absolute first moment here. If \(m\) were its absolute expectation, positivity of the resolvent and \(s\ge16\) imply \(m\ge(-\Delta+1)^{-1}(16+25m^4)\). Taking \(w=\inf m\) gives \(w\ge16+25w^4\), which is impossible. This is a failure of that representation only; it does not lower-bound MLP or deterministic methods.

## Certificate acquisition boundary

The cheap certificate above depends on the supplied Fourier representation. In contrast, an evaluator-only verifier cannot generally infer a global residual bound from a few point queries. On \(\mathbb T^8\), radius-\(1/8\) balls centered on a 25-per-axis grid are disjoint because spacing \(2\pi/25>1/4\). A smooth height-10 bump can be placed in any of the \(25^8=152{,}587{,}890{,}625\) supports while returning zero outside it. A deterministic verifier making fewer queries misses at least one support; for a uniformly selected hidden center, an adaptive randomized verifier with \(q\) queries hits with probability at most \(q/25^8\). This argument assumes value-only access and no supplied derivative or analytic majorant. It is not a barrier for the represented Fourier instance.

For this benchmark's fixed tangent and coefficient bounds, the enclosure inequality cannot pass for a residual sup bound as large as 10 for any tube radius: \(\lambda h-P(h)\le\lambda^2/(4B_2)=7.6776615239<10\). The exact threshold and bump-count statement are recorded in `analysis_results.json`.

## Scope and prior art

This benchmark establishes a finite-work FJ construction under supplied global certificates and shows that, on a coupled 8D example, a deterministic correction already reaches the same 1% target. It does not demonstrate practical superiority over the strongest deterministic algorithm on other model classes, nor a dimension scaling law, physical validity, a global field solution, or historical novelty. The MLP calculation is a theorem-certificate comparison, not an experimental performance result.

The broader pattern “use a surrogate, derive a defect equation, and stochastically correct it” is already present in the 2026 ICLR SCaSML paper, whose official abstract describes a Law-of-Defect PDE and stochastic correction up to 160 dimensions ([Fan et al., ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/cf8353a0efc3644454a5591a7cb55c17-Abstract-Conference.html)). The incoming note also records established branching and defect-correction precedents. This work makes no novelty claim for the general strategy.

All floating-point timings are one run on Apple clang 17, macOS 25.4, arm64. No calibration, repeated timing distribution, exact nonlinear reference, or physical measurements were acquired. The exact rational certificate and interval-evaluated deterministic correction are separate evidence from those timings.

## Reproduction

From the repository root:

```sh
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic work/FJ-nonlinear-benchmark/benchmark.cpp -o work/FJ-nonlinear-benchmark/build/fj_benchmark
work/FJ-nonlinear-benchmark/build/fj_benchmark 100000
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic work/FJ-nonlinear-benchmark/sparse_deterministic.cpp -o work/FJ-nonlinear-benchmark/build/sparse_deterministic
work/FJ-nonlinear-benchmark/build/sparse_deterministic
python3 work/FJ-nonlinear-benchmark/analyze.py
work/FE-hidden-gate/venv/bin/python work/FJ-nonlinear-benchmark/deterministic_interval.py
```

The C++ executables emit JSON to stdout. `analyze.py` writes `analysis_results.json`; the interval script writes `deterministic_interval_results.json`. Timing values vary by run.

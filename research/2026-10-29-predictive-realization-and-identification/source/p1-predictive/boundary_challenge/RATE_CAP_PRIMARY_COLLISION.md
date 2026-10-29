# Rate-capped record completion: primary-source collision check

This is a targeted literature extension of `DIRECTED_TRANSPORT_LITERATURE_COLLISION.md`. Root and the other proof agents own the network theorem and its validation; this note does not re-audit those proofs or claim historical priority.

## Finding

**The scalar clock-cap envelope is inherited from classical uniformization and the published discrete phase-type minimum-variance result.** The adjacent-Erlang equality construction is inherited too. The potentially substantive addition is the stationary network completion: simultaneously satisfying calibrated left/right residence margins, prescribed Schur flows, hidden clock ceilings and finite port-exit budgets, with feasibility reduced to a transport linear program. None of the primary sections checked here or in the preceding collision note supplied that joint network criterion. A selective negative search does not establish novelty.

## Closest exact scalar precedent

A. Bobbio, A. Horváth, M. Scarpa and M. Telek, *Acyclic discrete phase type distributions: properties and a parameter estimation algorithm*, Performance Evaluation **54** (2003), 1–32, [DOI 10.1016/S0166-5316(03)00044-0](https://doi.org/10.1016/S0166-5316(03)00044-0); [author PDF](https://people.unipmn.it/bobbio/Ph-paper/8-discrete-PH.pdf).

Section 4, Theorem 2, equation (23), journal pages 12–13, gives the minimum squared coefficient of variation of an order-`r` discrete phase-type absorption count with mean `mu`. Writing `theta=mu-floor(mu)`, it is `theta(1-theta)/mu^2` when `mu<=r`, and `1/r-1/mu` otherwise. Page 13 explicitly gives the first-branch equality law: the two adjacent deterministic counts, mixed to give mean `mu`. The paper attributes the theorem to M. Telek's MAM3 (July 2000) proceedings paper. I read the complete 2003 statement and attaining construction; I did not retrieve the original 2000 proof. Section 2 takes positive integer counts, with zero-atom extension identified but not developed.

## Direct bridge to the proposed envelope

Here is the short mathematical deduction, to make the degree of overlap testable. Let a hidden CTMC's total exit rates be at most `L`, and uniformize it at `L`. Its absorption duration can be represented by an absorption count `N` and independent exponential ticks of rate `L`, so

\[
 E\tau=EN/L,\qquad E\tau^2=E[N(N+1)]/L^2.
\]

For `mu=EN` and `n=floor(mu)`, integer support alone gives

\[
 (N-n)(N-n-1)\ge0,
 \quad E[N(N+1)]\ge(n+1)(2\mu-n).
\]

Equality requires `N` supported on `{n,n+1}`. For event flux `f>0` and residence `x=f E tau`, this is exactly

\[
 fE\tau^2\ge
 \psi_L(x,f)=\frac f{L^2}(n+1)(2Lx/f-n),
 \qquad n=\lfloor Lx/f\rfloor.
\]

Adjacent counts produce a mixture of Erlang(`n`,`L`) and Erlang(`n+1`,`L`). When `n=0`, the first component is a direct zero-duration transition, not a zero-length hidden state. Without such a direct component, an actual excursion has `N>=1` and hence mean at least `1/L`. The elementary inequality above covers the zero-atom extension independently of the cited paper's positive-count convention. At integer `mu`, one Erlang law suffices.

The published theorem's order constraint creates no gap here: when hidden-state count is unrestricted, choose `r>=ceil(mu)` and use its first branch. A clock ceiling is distinct from a fixed number of phases or a fixed dominant eigenvalue. The newly attained equality at the clock-capped threshold should therefore not be presented as a new scalar minimum-variance phenomenon.

## Uniformization and adjacent-Erlang sources

P. G. Harrison and W. J. Knottenbelt, *Quantiles of Sojourn Times*, in *Computer System Performance Modelling in Perspective*, Imperial College Press (2006), 156–194, [author manuscript](https://www.doc.ic.ac.uk/~wjk/publications/harrison-knottenbelt-sevcik-2006.pdf). Section 5.2, manuscript pages 21–22, explicitly represents first-passage densities as Erlang mixtures using the uniformized transition matrix `P=I+Q/q`. Its strict choice `q>max exit` is for numerical aperiodicity; the representation at `q=L>=max exit` used above follows directly from the Poisson construction. This author chapter is a checked explanatory source, not a claim about original discovery.

B. Melamed and M. Yadin, *Randomization Procedures in the Computation of Cumulative-Time Distributions over Discrete State Markov Processes*, Operations Research **32** (1984), 926–944, [DOI 10.1287/opre.32.4.926](https://doi.org/10.1287/opre.32.4.926), is original primary work on this cumulative-time randomization route. Only its publisher abstract was checked here; its detailed proof is not being represented as read.

R. Bierbooms, I. J. B. F. Adan and M. van Vuuren, *Approximate analysis of single-server tandem queues with finite buffers*, Annals of Operations Research **209** (2013), 67–84, [DOI 10.1007/s10479-011-1021-1](https://doi.org/10.1007/s10479-011-1021-1). Section 6.1, equation (4), gives common-rate adjacent-Erlang moment fitting and an explicit Coxian implementation. This establishes the attaining family as a conventional practical construction; it is not a global rate-cap network-completion theorem or the earliest source of that family.

## What remains specific to the proposed network result

The target fixes the boundary record `(S,b_R,b_L,w_B,c)`, hidden ceiling `L`, and port ceilings `ell_i`. Its transport variable `M` has the prescribed residence margins. Off-diagonal event budgets are the trace flows `F_ij=-S_ij`; diagonal returns consume the port spare `a_i=w_i ell_i-sum_{j!=i}F_ij`. Root's construction couples these budgets to the scalar envelopes, including the distinction between actual diagonal excursion flux and a direct off-diagonal zero-duration component. Its asserted conclusion is exact positive stationary completion if and only if the resulting transport cost is at most `2c`, with the appropriate support and port conditions.

That coupling and stationary realization are the candidate addition. The scalar extremal law, its piecewise-linear lower envelope, and adjacent-Erlang implementation should be explicitly credited as established ingredients. The preceding note already distinguishes this task from PH/MAP full-law realization, positive partial linear-system realization, fitted-generator quadratic programming and forward Markov-flow aggregation. The additional searches here did not identify a closer source with the same calibrated network inputs and conclusion. No claim is made that every rate-constrained realization paper has been excluded.

No new stochastic experiment was performed. No claim about acquisition precision, sample complexity or the cost of learning the record follows from this literature check.

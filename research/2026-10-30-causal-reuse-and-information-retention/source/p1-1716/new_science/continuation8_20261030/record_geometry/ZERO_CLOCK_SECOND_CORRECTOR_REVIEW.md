# Receiving review: the native-event second corrector

30 October 2026. Actual reviewed input: `ZERO_CLOCK_SECOND_CORRECTOR.md`, SHA-256

`3193c0a5c9501b8b48c1e42b96f8a71a4ebab2e3bc7ee2c5da655e6c087eb3b8`.

The exact input is preserved as `ZERO_CLOCK_SECOND_CORRECTOR_REVIEWED_3193c0a5c950.md`. Previously reviewed root action and hidden-supplier files were not changed.

**Disposition: accepted.** The second corrector closes the zero-external-clock actual weighted-current gap at the stated fixed-ellipticity ring interface. Its hidden-phase extension is valid. The optional extension to every nonnegative `gamma_N=o(N)` also follows. No substantive correction is required. It removes an actual external shared-bit clock from the receiving theorem; atomic native-event/bit coupling remains necessary.

This review reconstructs the new finite-difference bound and all normalizations. It uses the accepted inverse-activity theorem without reopening its validation. No new optional numerical fixture or formal verification claim is attached.

## 1. Local mixed differences really have the required order

Write `B=||H||_infinity`, `F=A_H/A`, `g=L_ex F`. The accepted bounds give `|g|<=8B`, `|Delta_i F|<=8B/A`, `|Delta_i A|<=2`, and `A(eta^i)>=A/2` on active exchanges.

In `Delta_i g=sum_j[Delta_j F(eta^i)-Delta_j F(eta)]`, only the at most five indices `{i-2,i-1,i,i+1,i+2}` share the local data controlling activity increments. Each such difference costs at most `16B/A+8B/A`, giving a safe total `120B/A`.

For the other indices, exchanges commute and their increments of `A,A_H` are additive. Inactive distant bonds remain inactive, so at most `A` distant terms contribute. Their four configurations have `(A,A_H)`, `(A+a,A_H+p)`, `(A+b,A_H+q)`, and `(A+a+b,A_H+p+q)`, with `|a|,|b|<=2` and `|p|,|q|<=2B`.

If `A>=8`, the interpolation rectangle has denominator at least `A/2`. Every point also satisfies `|y|<=Bx`, since it is a convex combination of four actual corners with that property. For `f(x,y)=y/x`,

\[
|f_{xx}|\le8B/A^2,\qquad |f_{xy}|\le4/A^2,\qquad f_{yy}=0.
\]

The directional mixed derivative is at most `64B/A^2`. For `2<=A<8`, the four-corner difference is at most `4B`, hence at most the root's safe `196B/A^2`. All corners are actual configurations in a nontrivial particle sector, so none has zero activity. Summation gives the explicit safe bound

\[
|\Delta_i g|\le316B/A.
\tag{1}
\]

This establishes the absolute-constant claim. It uses locality of the *activity increments*, without requiring typical extensive activity. Smoothness of `H` is still used by the earlier `D F` estimate through its bounded discrete variation.

For `h=g/A`, the quotient difference yields

\[
|h|\le8B/A,\qquad |\Delta_i h|\le664B/A^2.
\tag{2}
\]

The clean total rate is `cA`, so `|L_native h|<=664cB/A`. Under bounded hidden amplitudes the same result holds with the corresponding actual upper-rate constant. No derivative or locality assumption on those amplitudes is needed.

## 2. Exact generator identity and rare-event normalization

Every native event flips `u`, so

\[
L_{\rm native}(uh)=-uL_{\rm native}h-2uh\sum_i r_i
=-uL_{\rm native}h-2cug.
\tag{3}
\]

The root's signs and factor `1/(2c)` are correct. Each jump of `uh` has size at most `24B/A`, giving clean physical bracket rate at most `576cB^2/A`. Thus the bound is uniform even at `A=2`.

Let `M^h` be its actual Dynkin martingale. On macroscopic time,

\[
\int_0^tug\,dv
=-\frac{(uh)_{N^2t}-(uh)_0-M^h_{N^2t}}{2cN^2}
-\frac1{2c}\int_0^t uL_{\rm native}h\,dv,
\tag{4}
\]

with integrands evaluated at the physical state `N^2v`. The endpoint is `O(N^-2)`. A speed-`N` Chernoff estimate tests the martingale as `bM^h/N`: physical time `N^2T` times squared multiplier `b^2/N^2` times bounded bracket rate gives log cost `O_b(1)`, which vanishes after division by `N`. The maximal exponential martingale inequality gives the uniform-time result. The remaining integral is dominated by `C_H int 1/A`, already proved superexponentially negligible.

For smooth time-dependent fields, `F,g,h` are linear in `H` at fixed configuration. Their time derivatives obey the same bounds. The physical derivative has an extra `N^-2`; its contribution after current normalization is indeed `O(N^-2)`.

## 3. The first correction and arbitrary initial conserved sectors

At zero external clock, the first actual-current identity contains the endpoint of `uF`, its native correction martingale, and `int uL_native F`. The martingale already has bracket rate `O(1/A)`. The remaining drift splits into `c uL_ex F+c alpha D F`. The new estimate controls the first term, and the accepted quotient bound controls the second by `C_H/A`. There is no omitted clock compensation. Hence the complete actual weighted-current bridge holds, not merely a covariance identity for a substitute current.

Although `sigma=u p(eta)` is conserved at zero clock, reducibility creates no gap. In `(eta,sigma)` coordinates the native rates are reciprocal and elliptic within each visible canonical sector. The fair mixture is a reversible reference, and an arbitrary initial occupancy and recorded bit have density ceiling at most `2 binom(N,M_N)` against it. The inverse-activity, occupation and energy arguments allow this ceiling and do not require the sector weights to mix. Dynkin and bounded-jump martingale bounds apply to each initial state.

The four-site trace-clock example remains a valid warning against inferring elapsed time from its stationary mean. It does not contradict this new theorem, which uses the actual generator and physical time throughout.

## 4. Corrected weak tilts

Establish the base-law superexponential event first. Every predictable native tilt `|q_i|<=K/N` has the already stated exact second-moment likelihood bound `E Z_q^2<=exp(C_KNT)`, because the total native rate is `O(N)` on physical horizon `N^2T`. Cauchy–Schwarz transfers the entire bad event, including uniform-time corrections.

It is unnecessary, and would generally be incorrect, to reuse the clean total-rate cancellation as an exact identity of the tilted generator. The root does not do that: it uses likelihood transfer. Therefore the reviewed corrected spatial-tilt LLN, action identification, topology, goodness and smooth lower approximation retain their required inputs. The comparison process remains in its initial conserved sector, but the estimates and PDE uniqueness argument are uniform in that sector.

## 5. Compatible unknown phase amplitudes

For the stipulated actual combined rates, total intensity is `cA+R_tot`. Since `h` and `uh` are independent of the phases, the phase generator annihilates them. The exact identity becomes

\[
ug=-\frac1{2c}L_{\rm actual}(uh)
-\frac1{2c}uL_{\rm actual}h
-\frac1c uR_{\rm tot}h.
\tag{5}
\]

The root's signs and coefficients are correct. Equation (2) and bounded actual rates give `|L_actual h|<=C_H/A` and bracket rate `O(1/A)`. The last source is phase-linear with coefficients independent of all actuated phases and uniformly bounded. The valid sum of squared coefficient suprema is `O(N)`, so the independent-phase Feynman–Kac estimate removes it for `kappa_N -> infinity`. No factorization of the evolving density or invalid supremum/sum interchange is used.

The previous first-corrector phase-linear terms remain covered. The active heat warmup supplies the same complete `exp(O(N))` density ceiling and negligible initial visible changes at zero shared-clock rate. Frozen sectors, actual initial association and complete conditional future laws keep their earlier restrictions.

## 6. Every nonnegative sublinear external-clock sequence

For `0<=gamma_N<=1`, the full generator adds `-2 gamma_N uh` to (3). Its resulting remainder is bounded by `C_H/A`. Clock jumps of `uh` contribute bracket rate `O(gamma_N/A^2)`, also harmless.

The first correction's `gamma_N int uF` needs the separate step that the root includes. Put `k=F/A`; direct quotient subtraction gives

\[
|k|\le B/A,\qquad |\Delta_i k|\le20B/A^2,
\qquad |L_{\rm native}k|\le C_H/A.
\tag{6}
\]

The identity for `uk` has leading term `-2c uF`; its clock correction is `O(1/A)`. Hidden rates add the same removable phase-linear source `uR_tot k`. This proves uniform superexponential negligibility of `int uF` for bounded nonnegative clocks. Multiplication by `gamma_N<=1` preserves it. The first clock martingale has bounded bracket rate and is negligible at the current normalization.

On the subsequence `gamma_N>1`, the accepted positive-clock proof applies when `gamma_N/N -> 0`; its other condition `N gamma_N -> infinity` is automatic. Splitting into these subsequences proves the claimed range `0<=gamma_N=o(N)`. No inverse-gamma estimate is invoked at zero or very small rates.

## 7. Accepted consequence and limits

The clean nonlocal action and the compatible unknown-amplitude extension now have a proved zero-external-shared-clock receiver, at fixed `alpha<1` and `b<1` and their reviewed initializer and complete-future-law interfaces. Only native-event updates are required for the shared bit. Independent phase actuators remain required for the displayed unknown-kinetics family. Global coupling, atomic updates and their real costs remain.

This conclusion concerns the stated even ring and its supplied transitions. It does not automatically cover extra occupancy-changing transitions that fail to update the bit, arbitrary graphs without the needed exchange-form supplier, singular closed gates, or unmeasured kinetic composition. The full spatial action at `alpha=1` or `b=1` remains outside this proof. A zero-clock functional CLT is not inferred from the LDP extension. Finite-data acquisition, arbitrary apparatus-record conditioning, practical feasibility or advantage, and priority remain separate.

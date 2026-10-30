# Actual force work of the finite-response interacting-carrier supplier

30 October 2026. Constructive work comparison for the sibling's actual finite-period supplier. Input read: `record_geometry/FINITE_DURATION_INTERACTING_CARRIER_PORT.md`, SHA256 `73d6f367bd012fca68d92358d6a902a5a3741e8d8337905b4869d81f83a29fd9`. An exact input snapshot is preserved beside this note. No amendment to the supplier is made.

The format-corrected source SHA256 `362497578e0a88cd0b85948804ee2526de06fc0198fc60ccc1aeb58db19d6ed6` was subsequently compared line by line with that snapshot; the changes repair inline math delimiters only. Its exact snapshot is also preserved. The missing explicit plus sign in this note's displayed Eq. (6), reported independently by root and the source author, is corrected; Eqs. (7)–(9) and the derivation did not change.

## 1. The endpoint correction need not be mistaken for physical work

The supplied cell has period `p=pi/(2g)+b`, `beta=2/g+b`, and actual carrier momentum and displacement satisfying

\[
P_{k+1}=-Y_k+R d F_k,\qquad
\Delta J_k=P_k/g-dY_k+R eF_k,
\tag{1}
\]

where

\[
d=1/g+b,\quad e=1/g^2+b/g+b^2/2,\quad
A=\beta^2/2=e+d/g.
\tag{2}
\]

The incoming `Y_k` is a freshly supplied `N(0,R)` variable, independent of the force-selection history. These identities retain arbitrary unknown translation-invariant relative interactions. They count motion during both the transport and finite bath stages.

The corrected-current identity is `Delta J+Delta P/g=-beta Y+RA F`. Its force times corrected displacement is not the actual force work. The latter is

\[
W=\sum_kF_k\Delta J_k.
\tag{3}
\]

The construction below bounds (3) exactly, including the switching/momentum term highlighted by the supplier.

## 2. Actual delayed block commands eliminate the dangerous fresh-seed correlation

Hold a common force `F_m` for `L` complete cells, with communication blocks aligned to cell boundaries. There are `M` blocks and total physical time `T_*=MLp`. Require the command for block `m` to use only records from the start of block `m-1` or earlier. This is precisely a full-block delayed controller, not a command selected from the just-completed terminal momentum or bath readout.

In particular, `F_m` is independent of the last fresh input `Y_(mL-1)` of the preceding block. It can be correlated with all earlier forces and with the unknown native state. Assume `F_0=0`, as in the initially unarmed governor; equivalently, a centered initial momentum independent of `F_0` suffices. Set `F_(-1)=0`.

For the first cell of block `m`,

\[
\mathbb E[F_mP_{mL}]=Rd\,\mathbb E[F_mF_{m-1}].
\tag{4}
\]

For every later cell in that block,

\[
\mathbb E[F_mP_k]=Rd\,\mathbb E[F_m^2].
\tag{5}
\]

Both statements follow from (1) and independence of the relevant fresh Gaussian input. No conditioning on a future controller event is used. The native state after an arming trigger need not be equilibrium.

Substituting (4)–(5) into the **actual** work (3) gives

\[
\boxed{\mathbb E W
=RLA\sum_{m=0}^{M-1}\mathbb E F_m^2
+\frac{Rd}{g}\sum_{m=0}^{M-1}
\mathbb E[F_mF_{m-1}-F_m^2].}
\tag{6}
\]

Equivalently,

\[
\mathbb E W
=RLA\sum_m\mathbb EF_m^2
-\frac{Rd}{2g}\sum_m\mathbb E(F_m-F_{m-1})^2
-\frac{Rd}{2g}\mathbb EF_{M-1}^2.
\tag{7}
\]

Thus the real momentum/switching term has been retained and evaluated. It is not silently set to zero. Equations (6)–(7) imply

\[
R(LA-2d/g)\sum_m\mathbb EF_m^2
\le\mathbb EW\le RLA\sum_m\mathbb EF_m^2.
\tag{8}
\]

The lower coefficient is nonnegative for all `L>=1`, since

\[
A-2d/g=b^2/2\ge0.
\tag{9}
\]

For `L` of order `N` or `N log N`, actual mean force work agrees, within a relative `O(1/L)` error in this quadratic comparison, with the corrected-cell quadratic work. Exposing fresh bath inputs to force selection would invalidate (4) and can change this conclusion.

## 3. The rare-arming work improvement survives this actual supplier

Before arming, `F=0`. The corrected auxiliary current is an independent Gaussian random walk with per-cell variance `2RA`; the true current differs by the momentum endpoint in (1). The supplied Gaussian initial momentum and the exact cell formulas bound the entire within-cell excursion as well. Hence the unforced auxiliary current obeys the same `O(RT_*)`-variance maximal estimate needed in `RARE_EVENT_ARMING_AND_VANISHING_MEAN_HEAT.md`.

Together with a stationary reversible native current of total activity `O(N)`, or a native aggregate martingale under arbitrary initial law, the threshold

\[
b_N=N^{3/2}\log(2+N)
\tag{10}
\]

has arming probability at most `C exp[-c log^2(2+N)]` over the physical horizon `N^2T`. Unknown relative carrier interactions require no positional equilibration for this statement; force conservation and the charged momentum/fresh-input preparations are the suppliers.

For any full-block delayed command which is identically zero before arming and then obeys `|F_m|<=a_N`, (8) gives

\[
0\le\mathbb E W
\le\mu R_N T_* a_N^2\Pr\{\hbox{arming before }T_*\},
\quad \mu=A/p.
\tag{11}
\]

Choose `a_N=K_N/R_N`, `1<<K_N<<R_N<<N`. The result is

\[
\mathbb E W\le C\frac{N^2K_N^2}{R_N}
e^{-c\log^2(2+N)}\longrightarrow0
\tag{12}
\]

faster than any inverse polynomial. This establishes the actual **force-work** part of the stronger ordinary comparator for this finite-response supplier. It does not independently reprove the sibling's delayed-queue tracking theorem. Any use of that theorem must retain its actual force range, delay, endpoint, initial-state and noise premises.

The finite-duration thermal operations continue during the unarmed period. Their `O(R_NN^2)` fresh neutral preparations and retirements, switching, timing and associated work are not priced by (12). The distinction is therefore even more consequential here: vanishing carrier force work alone can coexist with a large continuously operating thermal apparatus.

## 4. Sustained mean correction still costs order `N^2/R_N`

Summing the actual corrected-current identity gives

\[
\mathbb E J(T_*)
=RLA\sum_m\mathbb E F_m
-\frac{\mathbb E P_{ML}-\mathbb E P_0}{g}.
\tag{13}
\]

For bounded commands the last term is `O(R_N a_N)=O(K_N)`, negligible beside an `O(N^2)` delivered mean displacement. Cauchy–Schwarz in (8) then gives, when `L->infinity`,

\[
\mathbb E W
\ge(1-o(1))\frac{[\mathbb EJ(T_*)]^2}{\mu R_N T_*}
\tag{14}
\]

for a sustained nonzero mean transport target. At `T_*=N^2T` and mean current of order one, (14) is `Omega(N^2/R_N)`. A constant force realizes the corresponding leading mobility/work relation. This is a comparison at the supplied finite-response port and delayed-block schedule, not a universal bound covering arbitrary extra baths or feedback informed by fresh bath noise.

## 5. Scope of the receipt

The supplied cell algebra (1) was reconstructed from the actual transport and bath stages. This note resolves its displayed force-switching correlation for a specific, physically delayed command filtration; it does not certify apparatus realization, a hidden reservoir reset, total heat, or the entire joint path-law theorem. Its evidence is analytic and no additional numerical fixture was needed.

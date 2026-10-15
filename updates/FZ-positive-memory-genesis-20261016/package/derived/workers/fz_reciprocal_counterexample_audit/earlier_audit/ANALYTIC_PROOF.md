# Independent exact audit: reciprocal lower cut at order two

**Verdict: the supplied candidate is a legal counterexample to universal
unaugmented full real order-two containment under the algebraic hypotheses
explicitly displayed in `reciprocal_report.txt`.** The whole truncated
functional passes, including its singular full moment matrix, all eight
original voltage-bound localizers, and every required equality multiplier.
The exact violated value is `-59330890897/661500000000`.

This conclusion concerns those algebraic hypotheses. No passive-network embedding was checked for this earlier transcribed version. No selected PGLib model, complete passive admittance matrix, branch/generator limits, prescribed interior power balances, or stronger incumbent formulation was checked.
External correctness review and literature priority are UNKNOWN.

## 1. Inputs, independence, and scope

This historical audit uses the exact rational table and model metadata transcribed from the earlier initial read, saved as earlier_read_snapshot.json. The earlier producer file was overwritten before its raw bytes were pinned; its original raw-file hash is NOT_CAPTURED_BEFORE_OVERWRITE. This snapshot is not claimed to reproduce those original file bytes. The initial `rationalize_order2.py` was also read before the
producer finalized the candidate, but is never imported or executed. For moment
positivity the verifier uses only the rational table as witness data, not the producer's
status, positivity pivots, search output, numerical solution, or rounding recipe.
`verify_exact.py` regenerates all substantive artifacts in this audit directory.
`HASH_RECEIPT.json` pins the inputs and generated outputs.

The independently checked arithmetic is integer/Fraction arithmetic. Positivity
uses fraction-free Bareiss determinants and Sylvester's criterion. This is a
saved, replayable mathematical certificate with software trust, not a
proof-assistant proof or external review.

## 2. The exact problem instance

Use four complex voltage coordinates `V=(x,y,u,v)`, with all imaginary
coordinates zero in the embedded functional. Select the fixed-injection buses
`i=1,j=2` and linear rows `B_i=(0,0,1,0)`, `B_j=(0,0,0,1)`. Thus the currents
`J_i=B_i V=u` and `J_j=B_j V=v` are linear functions of the original voltage
coordinates; they are not additional independent current variables.

The fixed-power equations are `conj(x)u-1=0` and `conj(y)v-1=0`. On the real
subspace they are `xu=1` and `yv=1`. All four original voltage-coordinate bounds
are included:

* `1 <= |x|^2 <= 4` and `1 <= |y|^2 <= 4`;
* `1/64 <= |u|^2 <= 64` and `1/64 <= |v|^2 <= 64`.

The source's displayed containment hypotheses constrain `B_i,B_j` only by their
linearity in the voltages. The selector rows satisfy that requirement. This
selector construction itself does not rely on any physical admittance
realization. For the final version, Section 11 separately verifies a connected
passive realization after changing original voltage coordinates and boxes.
Neither construction certifies the selected PGLib case.

For `alpha=1`, `beta=-1`, the source definitions give `z=u-v`, `q=y-x`, and
`a_i a_j=1`. Therefore the lower reciprocal cut is
`f=(y-x)^2-(u-v)^2 >= 0` on this real subspace.

## 3. Complete normalized truncated functional

For every `a,b,c,d >= 0` with `a+b+c+d <= 4`, define

`L(x^a y^b u^c v^d)=m[a-c,b-d]`, with `m[k,l]=m[l,k]`.

The complete defining table for sorted labels `k<=l` is:

| k | l | m[k,l] |
|---:|---:|---:|
| -4 | 0 | `98806889279569/58344300000000` |
| -3 | -1 | `235072827/200000000` |
| -3 | 0 | `0` |
| -3 | 1 | `246664539/1000000000` |
| -2 | -2 | `475524076154453/350065800000000` |
| -2 | -1 | `0` |
| -2 | 0 | `821303142091/1323000000000` |
| -2 | 1 | `0` |
| -2 | 2 | `4654149238937/3969000000000` |
| -1 | -1 | `486563319/1000000000` |
| -1 | 0 | `0` |
| -1 | 1 | `28038087/31250000` |
| -1 | 2 | `0` |
| -1 | 3 | `1844882523/1000000000` |
| 0 | 0 | `1` |
| 0 | 1 | `0` |
| 0 | 2 | `1234416733/600000000` |
| 0 | 3 | `0` |
| 0 | 4 | `16283328197/3000000000` |
| 1 | 1 | `491995449/250000000` |
| 1 | 2 | `0` |
| 1 | 3 | `5235709149/1000000000` |
| 2 | 2 | `4802252851/900000000` |

Every label arising from a degree-at-most-four monomial is covered. In
particular, `L(1)=1`. All odd-total-degree monomials vanish, and swapping
`x<->y,u<->v` preserves the functional. The audit explicitly enumerates and
saves all 70 original real moments in `REBUILT_MOMENT_FUNCTIONAL.json`.

## 4. Every equality multiplier through total degree four

Multiplication by `xu` leaves `(a-c,b-d)` unchanged, as does multiplication by
`yv`. Thus for each monomial `t` of degree at most two,

`L(t(xu-1))=0` and `L(t(yv-1))=0`.

The 15 such monomials span all permissible multipliers for quadratic equalities
at order two. The verifier separately evaluates all 30 identities from the
full degree-four table and saves their exact zero residuals. Linearity then
establishes the identities for every polynomial multiplier of degree at most
two, including every equality combination of total degree at most four.

## 5. Full 15-by-15 moment positivity

The full degree-at-most-two basis, in the audit's independently generated
graded lexicographic order, is

`(1, v, u, y, x, v^2, u v, u^2, y v, y u, y^2, x v, x u, x y, x^2)`.

Reducing these monomials by `xu=yv=1` leaves the 13 distinct representatives

`(1, v^2, u v, u^2, y u, y^2, x v, x y, x^2, v, u, y, x)`.

Let `C` be the 13-by-15 one-hot matrix assigning each original monomial to its
representative, and let `Q` be the corresponding 13-by-13 Gram matrix. Every
entry is reconstructed from the full original moment table, and the audit
checks the exact identity `M_2=C^T Q C` entry by entry. The matrix `C` has row
rank 13 since every representative occurs in the original basis.

The first nine quotient representatives have even degree; the final four have
odd degree. Since every odd moment vanishes, `Q` is the direct sum of a 9-by-9
even block and a 4-by-4 odd block. Every leading principal determinant of each
block is strictly positive, with exact values reproduced below. Sylvester's
criterion proves both blocks positive definite, so `Q` is positive definite and
`M_2` is positive semidefinite of rank 13. Its two-dimensional kernel is exactly
the coefficient span of `xu-1` and `yv-1`.

This argument proves positivity for every square of a polynomial of degree at
most two, not just selected submatrices or the cut value.

## 6. Every original voltage-bound localizer

Use the complete degree-at-most-one basis `(1,v,u,y,x)`. For each of the eight
quadratic bound polynomials

`x^2-1, 4-x^2, y^2-1, 4-y^2, u^2-1/64, 64-u^2, v^2-1/64, 64-v^2`,

the verifier reconstructs the entire 5-by-5 localizing matrix with entries
`L(g*b_r*b_s)`. All five leading principal determinants of each matrix are
strictly positive. Thus all eight localizers are positive definite of rank five
and `L(g*p^2)>=0` for every linear polynomial `p`. The exact matrices and all
determinant certificates are saved and displayed below.

The verifier also explicitly expands and evaluates all 36 unordered scalar
pair-products, including self-products, of these eight quadratic bound
polynomials. Every degree-four value is nonnegative, and the full complex
modulus-bound products have the same exact values. These additional scalar
voltage-bound preordering constraints therefore do not remove the witness.
All 36 exact evaluations are saved in `REBUILT_MOMENT_FUNCTIONAL.json`.

## 7. Full complex embedding

Write the eight real coordinates as
`(xr,xi,yr,yi,ur,ui,vr,vi)`. Define a degree-at-most-four moment to be zero
whenever an imaginary coordinate occurs; otherwise use the corresponding real
moment above. This defines all 495 moments explicitly and has `L_C(1)=1`.

The complete complex-as-real order-two matrix has size 45. Its rows containing
an imaginary coordinate are zero; its remaining principal matrix is exactly
the full real 15-by-15 matrix. An explicit coordinate projection therefore gives
`M_2^C=P^T M_2 P`, proving PSD and rank 13.

Each modulus-square voltage localizer has size nine. Its imaginary-coordinate
rows are zero and its remaining principal matrix is the corresponding real
5-by-5 localizer, so all eight are PSD of rank five.

The real part of `conj(x)u-1` is `xr*ur+xi*ui-1`, and its imaginary part is
`xr*ui-xi*ur`; the analogous formulas hold for `y,v`. The real parts reduce to
the previously verified identities, and every imaginary term vanishes. The
verifier explicitly evaluates all four real equality components against all 45
degree-at-most-two monomial multipliers: 180 exact zero checks. Hence the
embedding meets the full complex-voltage order-two constraints.

## 8. Exact cut violation and consistency with other source claims

Expanding the cut directly in the original variables gives

`L(f)=L(x^2)+L(y^2)-2L(xy)-L(u^2)-L(v^2)+2L(uv)`

`=2*(1234416733/600000000 - 491995449/250000000`
`     - 821303142091/1323000000000 + 486563319/1000000000)`

`=-59330890897/661500000000 < 0`.

Thus a normalized feasible order-two truncated functional violates the claimed
universal lower containment. This is a rigorous algebraic separation witness,
not a physically feasible voltage vector. It has no representing positive
measure supported on the stated feasible voltage set. Unrestricted truncated
representability on all of `R^4` is not decided here.
Indeed, at every actual real point satisfying `xu=yv=1` and `x^2,y^2>=1`,

`f=(x-y)^2*(1-1/(x^2*y^2))>=0`.

The witness does not satisfy the source's *augmented* order-two relaxation. The
valid current upper bound `u^2<=1` has, for the linear test polynomial `p=u`,

`L((1-u^2)u^2)=-625874207133559/583443000000000 < 0`.

The valid scalar current bounds `L(u^2),L(v^2)<=1` do hold, emphasizing the
distinction between scalar bounds and all their localizing constraints. There
is no contradiction with the source's upper-cut, order-three, or augmented
order-two containment statements. No independence from complete QC/RLT/OBBT or
any specified sparse implementation is established.

## 9. Exact positivity certificates

Each list below consists of the leading principal determinants in order, using
the bases and blocks already specified. For the eight localizers the basis is
`(1,v,u,y,x)`. The verifier clears a common positive denominator and computes
integer determinants by exact fraction-free elimination; the displayed reduced
fractions are the resulting exact determinants. All comparisons to zero use
integers, not floating-point approximations.

### quotient_moment_even_block

1. `1` > 0
2. `2289667827178520664147719/1750329000000000000000000` > 0
3. `431721250270066275812140237600727495863/612730321648200000000000000000000000000` > 0
4. `14855191889680286211293501686955053426606902141850187/42899186046406890312000000000000000000000000000000000` > 0
5. `14112907116256204192926256402680880589217317519140879258169984107/4256671735454723691208200000000000000000000000000000000000000000000` > 0
6. `26209864174780288180482740363866415580423081715773380149657671251914859803/7094452892424539485347000000000000000000000000000000000000000000000000000000` > 0
7. `88833599204843152683803636311543758140711399621579180358453852828285917985196518211/14078941765016498608671121500000000000000000000000000000000000000000000000000000000000000` > 0
8. `1315871321029560740108330777875822984819349761874945369414354735649579955256505924914575541/63355237942574243739020046750000000000000000000000000000000000000000000000000000000000000000000000` > 0
9. `1409435190919232318746964231075970115300356968244481541957260014080629479738291278507486598690013/21118412647524747913006682250000000000000000000000000000000000000000000000000000000000000000000000000000000` > 0
### quotient_moment_odd_block

1. `821303142091/1323000000000` > 0
2. `16259950095873398299807/109395562500000000000000` > 0
3. `19158923417307764665480240626191/328186687500000000000000000000000` > 0
4. `242113033540204175420481868755366476291/196912012500000000000000000000000000000000` > 0
### x_lower

1. `634416733/600000000` > 0
2. `173690598304603363339/297675000000000000000` > 0
3. `135334382753418698533675433768233/3150592200000000000000000000000000` > 0
4. `95938578498196928532311681934479129586437/14177664900000000000000000000000000000000000` > 0
5. `505272000017658803367806037808444197620045185649/28355329800000000000000000000000000000000000000000000` > 0
### x_upper

1. `1165583267/600000000` > 0
2. `1212553583928752765677/476280000000000000000` > 0
3. `1290258338766919787083239588540071/787648050000000000000000000000000` > 0
4. `16787057322947016969527082950775964064249/1417766490000000000000000000000000000000000` > 0
5. `293201725182984757641049496095632740275183214753/1890355320000000000000000000000000000000000000000000` > 0
### y_lower

1. `634416733/600000000` > 0
2. `318284881550992991297/793800000000000000000` > 0
3. `135334382753418698533675433768233/3150592200000000000000000000000000` > 0
4. `7920364710078411846089117485599967174649/3150592200000000000000000000000000000000000` > 0
5. `505272000017658803367806037808444197620045185649/28355329800000000000000000000000000000000000000000000` > 0
### y_upper

1. `1165583267/600000000` > 0
2. `571780533995542991297/198450000000000000000` > 0
3. `1290258338766919787083239588540071/787648050000000000000000000000000` > 0
4. `4043391220231770508890238817675894057561/150028200000000000000000000000000000000000` > 0
5. `293201725182984757641049496095632740275183214753/1890355320000000000000000000000000000000000000000000` > 0
### u_lower

1. `800631267091/1323000000000` > 0
2. `120960268789275507705306298597/148203857088000000000000000000` > 0
3. `189900522343105297166239034435933513623261891/345874011963975936000000000000000000000000000` > 0
4. `35829362261115298285034046037507054770882258743857812267887/87857533023041311358976000000000000000000000000000000000000` > 0
5. `21270418644172965299035252621364381342251719992026549146485691486683/5622882113474643926974464000000000000000000000000000000000000000000000` > 0
### u_upper

1. `83850696857909/1323000000000` > 0
2. `5631728018080867907784322569283/2315685267000000000000000000` > 0
3. `48096030737954465038059464766721634968638882299/1351070359234281000000000000000000000000000` > 0
4. `519770834762848210689463859831623302503500316833210782252091/670299781975107661125000000000000000000000000000000000` > 0
5. `5543903614048021934398696996980526843238556715010262313975081604557837/5362398255800861289000000000000000000000000000000000000000000000` > 0
### v_lower

1. `800631267091/1323000000000` > 0
2. `50339061985066444076507587639/49401285696000000000000000000` > 0
3. `189900522343105297166239034435933513623261891/345874011963975936000000000000000000000000000` > 0
4. `9056570201276254472470692445136440623678301536612598831/22135936765694459904000000000000000000000000000000000000` > 0
5. `21270418644172965299035252621364381342251719992026549146485691486683/5622882113474643926974464000000000000000000000000000000000000000000000` > 0
### v_upper

1. `83850696857909/1323000000000` > 0
2. `930423724709760950771603804423/385947544500000000000000000` > 0
3. `48096030737954465038059464766721634968638882299/1351070359234281000000000000000000000000000` > 0
4. `1045638049849192024042798386038604484849903499413509924379/1351070359234281000000000000000000000000000000000000` > 0
5. `5543903614048021934398696996980526843238556715010262313975081604557837/5362398255800861289000000000000000000000000000000000000000000000` > 0

## 10. Replay and limits

Run `python3 verify_exact.py` from this directory, or use its absolute path. It
reconstructs all moments, every matrix, the congruence identities, determinant
certificates, equality checks, exact cut value, this proof, and the hash receipt.
No optimization solver or third-party Python package is required.

The certificate resolves the algebraic universal-containment question under the
reported hypotheses. It establishes no runtime advantage, external novelty,
selected-case strengthening against an unexecuted incumbent, experimental
physical validation, or new optimization capability. Those claims remain
outside this audit; external correctness and priority remain UNKNOWN.
No passive embedding claim is made for this historical snapshot.

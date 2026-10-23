# Pro1 Cycle6 continuation

## Current owned result

The temporal benefit per call is provably unbounded in the **full operator**
variational problem. Its exact dual is A_k=(ln2)v_k/8, and for k>=4,
k^(3/2)/32 <= v_k <= k(k-1). The complete nonlinear construction achieves
Q >= 3/2+(ln2/4096) beta^(64/17) for every fixed 0<beta<=2^-11,
using k=floor(beta^(-8/17)/8), fixed before the transmission horizon.

The same deterministic unassisted encoder/decoder sequence works pointwise
for every fixed normal initializer, with vanishing full-diamond error.
The actual tau_pi is included. There is one evolving bath and no return
promise, reset, bath access, free entanglement, postselection or timing wire.

## Read actual source before continuing

1. `TEMPORAL_GROWTH.tex`, or the merged `COMPLETE_PROOF.tex.txt`.
2. `contributions/temporal_operator_dual.md`: closest-point optimizer,
   exact endpoint decomposition and norms uniform in k.
3. `contributions/temporal_constructive_structure.md`: all-length guard
   and meander proof; whole-bath raw words versus bulk coefficient.
4. `contributions/uniform_transfer_challenge.md` and the two focused
   guard challenge notes. The final sections accept the actual 64/17
   exponent; the initial 7/2 route is explicitly conditional.
5. `INHERITED_OPERATOR_CODING.tex` and `INHERITED_COMPRESSION.tex`:
   actual same-bath overflow-to-code operation, including r^2,
   auxiliary CPTP normalization and polar repair.
6. `FAILED_ROUTES.md`, `REVIEW_STATUS.md`, `RESOURCE_RECORD.json`.

The unchanged exact Cycle5 ZIP is in `preserved/` and contains the entire
earlier chain. Its 3,763,692 bytes have SHA256
`7cc0ba564d5e9d483527b9c4f55928d17bcba0b27db9604875286faa27128654`.
The source was actually extracted and read from the verified attached
complete collection; no summary or manifest substituted for its proofs.

## Exact model and dual objects

E=C2_seed tensor F(C2); S_j prepend colors and R exchanges vacuum seeds.
U=[[R,S1,S2],[S1*,0,0],[S2*,0,0]], V_s=cos(s)U+i sin(s)I.
All calls preserve total port color charge plus bath depth. The actual
initializer has depth mass (2/3)3^-h, uniform on 2^(h+1) vertices.
Reference eta remains diag(3/4,1/8,1/8).

For k calls let sigma=diag(1/2,1/4,1/4)^tensor k and Q count colored
ports. G(b)=G0+bG1+... is the exact charge-pinched bulk displacement
Q-W*QW on the first k bath colors, valid at initial depth>=k.
G0=(2Q-kI) tensor I. A sufficiently deep toggling computation gives
G1=[C_-,C_+], C_i=U0...U_(i-1)UiU_(i-1)...U0. This identifies the
physical finite-prefix coefficient and does not extend its formula to root.

For an arbitrary prefix density zeta, H_zeta=Tr_prefix[(I tensor zeta)G1]
+2Q-kI is charge-preserving and input-offdiagonal. Let v_k=min Tr sigma H^2.
Its minimizing H obeys T(sigma H)>=v_k I by the closest-point condition.
The minimizer zeta is an ANALYTIC dual state, not a replacement initializer.

## Actual constructive transfer

With l=ln2, b=beta², v=v_k and minimizing H, choose
X=-(l/2)sigma H, m=3lv/16, Y=(4m/k)sigma(Q-k/2),
rho=sigma+bX+b²Y. For k>=4 and b k^(17/4)<=2^-12,
rho is positive, its exact bulk drift is at most -lvb²I/16, and
S(rho)-3k/2>=lvb²/32. The uniform remainder ||R_b||<=4k^5b²
is contracted only against rho-sigma because sigma has exact zero
bulk drift at every b. Retain that cancellation.

The guarded-word identity is reusable: guard bit1 at i-1, endpoints01,
and a nonnegative middle meander yield P(I-SWAP) tensor I_E for raw
word difference C_j C_i-C_i C_j on that selected sector. It identifies
the corresponding raising/lowering coefficient ONLY IN THE BULK. The
raw identity itself is whole-bath and works through vacuum. Both distinctions
matter. Endpoint pairs occupy orthogonal binary-pattern matrix blocks.

## What is settled and what remains open

Preserve both Cycle5 achievements: the sharp restricted quartic fixed-block
law and the genuinely usable non-scalar operator-drift construction. The
new k(beta) leaves the controlled logarithmic window and does not refute
the fixed-k law. No full-capacity/feedback converse is supplied.

Quadratic v_k growth is still unproved. Exact small blocks suggested it;
that finite pattern is not a theorem. The completed k^(3/2) lower suffices
for the actual 64/17 power. The 7/2 conditional transfer is not a claim
about this device until a stronger all-prefix lower is proved.

## Selected next scientific operation

Resolve the sharp growth of v_k between k^(3/2) and k². Start from the
token decomposition and its exact input-only subblocks, not an averaged
prefix susceptibility. Either identify additional non-meander patterns
whose total contribution remains independent of every coherent prefix,
or construct a full prefix dual density with an O(k^(3/2)) upper.
The finite symmetric-prefix certificates are candidate starting evidence,
not justification for assuming that density optimal for all k.

If a stronger growth law is proved, use the uniform transfer already
available; its conservative k^5 remainder may then be the next genuine
barrier. Do not optimize a tiny fixed-four-call constant to keep the
programme occupied. Exact small-angle capacity order and nonzero-angle
feedback equality remain broader open questions, with no imposed claim
that the current exponent is sharp.

## Replay, review and delivery

`VERIFY.md` gives two short exact replays and source identity checks.
The guard replay is symbolic wiring, not an all-length proof. The k4
rational certificate is explicitly a finite diagnostic. No paid resources
or outreach were used. Recorded runtime/memory are process observations;
total discovery, inference and review costs are unknown.

The archive and private Page source are for Max and the evaluator.
Delivery receipts are external to the archive. Receipt is not reading,
scientific acceptance or integration. This checkpoint does not close
Pro1's research mission or transfer protected programmes.

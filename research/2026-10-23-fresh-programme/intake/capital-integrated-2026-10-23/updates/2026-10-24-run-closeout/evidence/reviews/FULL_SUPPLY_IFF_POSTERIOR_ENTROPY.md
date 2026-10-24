# Hash-specific independent review of the full-supply criterion

23 October 2026, W38. **PASS, no fatal gap found** in W44
`FULL_SUPPLY_IFF_POSTERIOR_ENTROPY.md`, SHA256
7ba6eacc4217bfe6a0b9718cd64a428ee0d0b7b836753f8660a5aae06e4f1c84,
retained as `w44_full_supply_iff_snapshot.md`.

The theorem says that at FIXED finite D,L,p, for arbitrary actual finite
source-preserving duplicated record families Z_r, ideal supply B is achievable
by zero-aid ordinary LOCC iff H(K^r|Z_r)=o(r), equivalently
I(K^r:Y^r|Z_r)=o(r). Y is a mathematical Bell eigenlabel and is not supplied
operational data. Source clocks remain inaccessible. Output rank is fixed on
all branches and the error target uses the OWN complete actual residual.
Record alphabets may grow arbitrarily; the source alphabet is fixed first.

W44 proposed the product-channel/Pinsker/Fano necessity; root independently
supplied the source-extension and direct finite-output entropy step. I
reconstructed these before reading the final frozen proof. I checked the
following exact potential failure points:

- Pairwise Bell-label TV is 1-D^(-2|k-l|), not the physical sample-channel
  distance. Pinsker's NATURAL-log factor and the l1/TV factors give precisely
  c_D=(1-D^-2)^2/2>=9/32.
- The mutual-information chain conditions on Y_past,Z throughout. The
  entropy chain uses exact K_past,Z and is bounded ABOVE by conditioning
  on the noisier Y_past,Z; the required direction is correct even when
  Z correlates all inventories. Product conditional label noise is essential.
- The Fano/Jensen function g_L is monotone on [0,1-1/L], so the cap and
  inverse are valid. L=1 is handled separately. Using the fixed prior's
  actual support size instead of L is an optional valid sharpening.
- An extension copying the actual classical record removes its duplicated
  classical correlation, giving E_sq(input)<=rB-I_r/2 with no additional
  H(Z) term. This witness does not provide any new record to the receivers.
- For every output extension, weak monotonicity and SSA imply E_sq>=Ic
  directly. Applying this after a composed bilateral Weyl twirl gives the
  exact finite (1-2epsilon)lnN-h2(epsilon)<=rB-I_r/2. Neither an output-iid
  limit nor entropy continuity of an infinite actual residual is used.
- The governing normal finite-tree approximation is taken at fixed r,Z,N;
  the finite inequality passes through the output Bell overlap. Apparatus
  is independent local product and supplies no entanglement.
- This necessity matches the EXACT frozen W38 sufficiency proof
  `SUBLINEAR_POSTERIOR_FULL_RATE.md` SHA256
  393db7888adbe0cf666dfd87f19acbdb762168f3f1e0c7a02551769542c07d76.
  W44 independently reconstructed and checked its physical list sampling,
  ML/Hamming guarantee, fixed retained rank, composite-D Bell twirl,
  arbitrary correlated Bell-error ball, one-shot smoothing and actual-residual
  lift. All sampling loss and failures remain paid. It is zero-aid two-way
  LOCC; only its final finite hash code is one-way.

The primary E_sq source was read directly: Christandl–Winter,
quant-ph/0308088v3 Definition1, Proposition3 and Proposition10,
https://arxiv.org/html/quant-ph/0308088v3 . General monotonicity and hashing
machinery are established prior art. Independent own sufficiency diagnostics
are in `sublinear_sampling_checks.json`; W44's checker imports no peer code
and retains its own 59540 exact ML events and other finite controls. Neither
set of finite calculations is an executed quantum distillation code.

Strict forward LOCC cannot replace ordinary LOCC in this iff statement.
The independently reviewed complement-record example has H_r=ln2 but
forward rate lnD, versus ideal two-way rate 1.5lnD with one backward bit.
Conversely the Hamming-center record example permits a Z-only one-coordinate
approximation and wholly forward full-rate hashing despite Z-alone block
error tending to one. The distinction is the geometry of the possible
inventory vectors, not a free entropy-average receiver.

This theorem does not give a partial-rate Shannon formula for arbitrary
collective records and does not resolve the ORIGINAL unflagged H+O(1)
second-order problem. Record formation/delivery remain supplied physical
premises. No efficient compiler, hardware validation, historical novelty,
external correctness or practical advantage is established.

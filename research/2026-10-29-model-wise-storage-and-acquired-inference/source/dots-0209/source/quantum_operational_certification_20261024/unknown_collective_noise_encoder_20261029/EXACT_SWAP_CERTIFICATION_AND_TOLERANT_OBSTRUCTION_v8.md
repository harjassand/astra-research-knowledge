# Exact swap lifting versus a rare-subspace finite-precision obstruction
2026-10-29. New follow-on argument, not part of reviewed v1-v5. Proposed for review.

## Exact global-channel certificate from a faithful spectator mixture
Let N be any CPTP channel on A tensor B, dim(A)=4, dim(B)=D. Let S be a known twisted two-qubit SWAP on A (a Hermitian unitary). Define X=N†(S tensor I_B), a Hermitian contraction because N† is unital positive. Suppose complete pair tomography with spectators maximally mixed establishes
E_B(X):=Tr_B(X)/D = S.
Then X=S tensor I_B EXACTLY.

Proof: with Π±=(I±S)/2, positivity I∓X≥0 and the conditional expectation imply
Tr[(Π+ tensor I)(I−X)]=0,
Tr[(Π− tensor I)(I+X)]=0.
For positive Y and projection Π, Tr ΠY=0 implies YΠ=ΠY=0. Thus X equals +I on Π+ and −I on Π−, with no cross-block entries.

Moreover, in a Kraus representation N(ρ)=ΣK_aρK_a†,
Σ_a (SK_a−K_aS)†(SK_a−K_aS)=2I−N†(S)S−S N†(S)=0.
Hence every Kraus commutes with S. If the exact globally lifted fixed operators are a compatible collection of all star twisted swaps, their generated permutation algebra has commutant equal to the corresponding collective-unitary algebra by Schur–Weyl duality. Therefore the current reduced channel is noiseless on its multiplicities without assuming random-unitary structure.

This requires complete pair tomography including identity and one-body sectors, not only the 9×9 correlation block. The v1-v2 physical schedule is not itself this stronger certificate. Exact equalities cannot be established by finite noisy sampling. Also, a certificate for a channel produced from one initial bath state does not imply that arbitrary future bath states share the algebra. The memory promise is NOT discharged.

## Why a dimension-free tolerant lift is impossible
Take even n≥6. Split four target qubits T from remaining n−4 spectator qubits B, D=2^(n−4). Let |s_B> be a fixed singlet spectator state, Π=|s_B><s_B|. Let Z be Pauli Z on target qubit1. The unitary
U=I_T tensor(I_B−Π)+Z tensor Π
acts nontrivially only on the rare spectator subspace. For maximally mixed spectators its target channel is
(1−1/D)id+(1/D)Ad_Z,
so its entire four-target reduced channel differs from identity in diamond distance ≤2/D, and any target-pair swap test is exponentially close to a fixed-swap result. Yet on |s_B> and a target singlet logical code, Z moves target total spin zero to spin1 (since P_singlet Z_1 P_singlet=0). The nominal global singlet encoder can therefore suffer complete leakage on an allowed logical state: the data-bath model promise is violated, and local finite-precision evidence at the mixed-spectator interface can hide it.

This explicit target/spectator example proves an exponential-dimensional obstruction to lifting approximate local channel identities uniformly over arbitrary spectator inputs. It does NOT by itself prove a lower bound for every possible all-pair adaptive experiment or for actively prepared entangled probes. Stronger calibration access may directly target the dark spectator sector. The model must account for that access instead of assuming it.

The exact-vs-tolerant distinction is useful: local symmetry can be an exact global certificate at a faithful interface, but robust certification needs a separate observability/excitation assumption controlling rare sectors. It does not resolve the main construction's future joint-bath algebra obligation.

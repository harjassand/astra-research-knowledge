# A causal pair factory with bounded active storage and a workload error contract

Author root, 29 October 2026. Author construction; review is separately recorded.

## 1. The bridge

The fixed-pair reduction supplies an optimal large entanglement bank in
principle, but an N-pair bank can require N coherent storage slots and long
startup. This construction prepares, compresses, transports and releases
repair resources in finite blocks, with a complete causal-workload guarantee
and an explicit binary control program. No unknown logical input enters it.

The strongest conventional route is the construction used here: locally
prepare a known state, compress one half coherently, send it and decompress.
Schumacher compression, pure-state dilution and reversible conditional state
preparation are established machinery. The added bridge is to an arbitrary
declared causal repair processor, including its old purifications, actual
records and returning apparatus, without a physically stored global bank or
a sum of N separate one-pair approximation allowances. This is a resource
compiler, not a computing advantage over direct coupling or reset.

## 2. Exact finite resource certificate

The required pair is

    |phi> = sqrt(p)|00> + sqrt(q)|11>,  p=1-q, 0<q<1/2.

For block length b and integer cutoff k define

    W_(b,k) = {x in {0,1}^b : weight(x)<=k},
    M_(b,k) = sum_(w=0)^k binom(b,w),
    Z_(b,k) = sum_(w=0)^k binom(b,w) p^(b-w) q^w.             (1)

Prepare the pure Schmidt truncation

    |Phi_(b,k)> = 1/sqrt(Z) sum_(x in W) p^((b-|x|)/2)
                                       q^(|x|/2) |x>_Z |x>_A. (2)

Its squared overlap with |phi>^tensor b is exactly Z. It requires
Q_(b,k)=ceil(log2 M_(b,k)) noiseless communicated qubits and no initial shared
entanglement. If k>b/2, (1) still applies but the simple entropy bound below
is not used. For k=b the construction is exact with b communicated qubits.

All equally likely strings at the cutoff are included. At fixed Q this can
be worse than the unrestricted top-2^Q Schmidt mass: type-complete truncation
buys a simple control program, not one-shot optimality. That stronger bank
optimum remains the comparator in the information branch.

For N calls prepare B=ceil(N/b) independent equal-sized blocks. At most b-1
last-block pairs are unused. They remain declared inventory or are explicitly
retired. They cannot be reset for free. Actual and ideal whole-source squared
fidelity is Z^B. Every fixed causal processor using those sources obeys

    epsilon_strategy <= sqrt(1-Z^B) <= sqrt(B(1-Z)).          (3)

All actual records and returning memory can be included, with the same total
physical extensions and allowed tester slots on both sides. The dilation may
also retain inaccessible noise and retirement outputs. This is a workload
comparison error, not a conditional per-call error or device fault rate.

### Causal proof without physically storing future banks

Each block preparation is a fixed isometry on independent pure registers,
invoked at its scheduled time. Mathematically these independent sources are
equivalent to a product source feeding the same causal slots. The comparison
injects an exact b-pair block at each same slot; its overlap is Z^(B/2).
All intervening controls and any adaptive tester form one CPTP map, so trace
distance cannot increase. The supplied total physical extension specifies
that map outside the ideal code support too. No future block needs to be
physically stored for this proof.

An input-correlated source or uncontrolled returning preparation register
cannot be replaced by this product source. It needs the joint source contract
proved in the information branch. Here every work register is explicitly
uncomputed to zero before reuse.

## 3. Reversible binary preparation and transport

The spectrum and its computational Schmidt basis are supplied. Put
A(r,t)=Pr[Bin(r,q)<=t], with A(r,t)=0 for t<0 and A(0,t)=1 for t>=0.
Keep a coherent prefix-ones count w. With r bits still to write, use

    P(0|prefix)=p A(r-1,k-w)/A(r,k-w),
    P(1|prefix)=q A(r-1,k-w-1)/A(r,k-w).                    (4)

A controlled Y rotation with positive amplitudes writes the next bit, then
a controlled increment updates w. Zero-probability prefixes receive any fixed
total extension. After b steps uncompute w from the completed string. This
prepares amplitudes sqrt(p^(b-|x|)q^|x|/Z) on precisely W_(b,k).

Compute the lexicographic rank j(x) in W reversibly into Q zero qubits. At
each 1 at position t add the allowed-completion count for a 0 at that position:

    count_0 = sum_(v=0)^(k-w) binom(b-t-1,v).                (5)

Increment w and continue. The resulting state is

    sum_x sqrt(Pr(x)/Z) |x>_Z |j(x)>_J.

Send only J. At the replacement laboratory, coherently unrank J into b zero
A registers, then clear J by XORing the recomputed rank of A. This produces
(2), with message and arithmetic workspace clean. Define unrank(j>=M) to
return a fixed string and rank(x outside W) to return a fixed integer. The
compute-XOR routines are total reversible circuits; clearing is guaranteed
on their qualified input support.

The cleaned message qubits J are now **at the replacement laboratory**.
They can be reused there or leave as declared pure outputs. Reusing the same
carriers at the helper requires an additional counted return transfer. The
forward communication count Q does not include that optional return service.

No measurement is used in this preparation route. Teleporting J instead adds
supplied ebits, two classical bits per transmitted qubit, actual records and
measurement purifications. With ideal corrected teleportation the common junk
factors from the bank; it is still part of the apparatus/resource bill.

### Arithmetic, synthesis and calibration

The tables have O(b^2) entries, with O(b)-bit numerators and denominators for
fixed-bit-length rational p,q. A straightforward unrolled implementation uses
b writing rounds, O(b^2) selected rotations and reversible arithmetic on O(b)
bits. Polynomial(b) gates and O(b) scratch suffice: compute the scalar counts,
add/compare, then uncompute scratch at each stage instead of keeping all
intermediates. This is not an optimized native gate count.

The executable checks exact conditional probabilities and rank/unrank logic,
not device rotations. With acquired complete-channel allowances eta_l for
implemented primitives, a conservative synthesis/control addition is
sum_l eta_l. Calibration, message loss, helper decoding, holding noise and
cleanup errors remain distinct from the representation error (3).

## 4. Storage, startup and service

An active block has at most b pair halves at each laboratory. A separate next
block can be prepared concurrently. Double buffering uses O(b) quantum
storage per side, O(b) arithmetic work and a Q-qubit message. The constants
depend on actual overlap of preparation, transport and release. Controller
tables occupy polynomial(b) classical space and need physical control access.

Each new block consumes qualified pure input ports: b helper string qubits,
Q helper message qubits and b receiver expansion qubits. Arithmetic scratch
starts pure and is uncomputed locally. Consumed helper pair halves become
the old-purification output during repair; they are not automatically clean
inputs for the next block. Receiver halves leave the factory as replacement
systems. Their replenishment and the ongoing old-partner retirement or reset
are physical services. The clean J output is on the receiver side as stated
above. Thus O(b) active storage describes a factory with continuous supplied
and outgoing systems, not an autonomous finite closed apparatus. It can use
fresh pure ports, qualified resets, or explicitly counted routing to supply
those inputs; the theorem does not select a free implementation.

For acquired times T_prep(b), T_send(Q), T_expand(b), and call spacing tau,
a sufficient stable double-buffer condition with separate parallel resources is

    T_prep(b)+T_send(Q)+T_expand(b) <= b tau.                 (6)

The first block must be acquired before the first call. Without parallel
resources, the valid schedule pauses between blocks and has different
throughput. A prepared half may wait for the acquisition delay plus one block
service time. That holding loss and dephasing must enter the physical error
budget. A Schmidt spectrum does not supply these speeds, controls or storage.

## 5. Entropy rate with polylogarithmic active storage

Choose t>0 with q+t<1/2, and k=ceil(b(q+t)). For sufficiently large b,

    1-Z <= exp(-2 b t^2),
    Q/b <= h_2(q+t+1/b)+1/b.                               (7)

The first is the elementary Bernoulli tail estimate. The second uses k/b<=1/2
and the binomial type count. Choosing b>=ln(N/epsilon^2)/(2t^2) yields
B(1-Z)<=epsilon^2 and hence (3). If b exceeds N, uncompressed exact blocks
remain valid; the asymptotic guarantee is not a small-horizon saving.

For fixed supply-rate slack Delta>0, take t small enough and then b large
enough that Q/b<=h_2(q)+Delta. Active storage is O(log(N/epsilon)), with
real startup and execution costs. For vanishing slack one can set
t_N=1/log N and epsilon_N=N^(-s), s>0: then b=O(log^3 N), supply rate tends
to h_2(q), and complete-workload error tends to zero. A finite fixed alphabet
has an analogous typical-set construction; only the binary program is
explicitly executed here.

This matches the established entropy rate for the bank while furnishing
causal release and bounded active storage. It is not a new compression
theorem or a converse on every processor that might consume the bank. The
sharp converse applies to the specified bank target, or to full restorations
which expose the corresponding target, as proved in the information branch.

## 6. Simultaneous connection supply and purification drain

Compose the factory with exact helper restoration and direct retirement of
each old Schmidt partner. The ideal retirement output has entropy N h_2(q),
and clean work is returned. The root flow law shows that polylogarithmically
many retained quantum **qubits** can save only a polylogarithmic additive
amount of this joint entropy under fresh losses. Thus the fixed spectrum
sets both leading supply and drain rates, at different physical ports.
Exact zero-error connection costs still follow rank, not entropy.

Do not simply impose that ideal law on the approximate output. In the finite
qubit dilation here, F has N qubits; (3) and entropy continuity give

    |S(F_actual)-N h_2(q)| <= epsilon N+h_2(epsilon),          (8)

for epsilon<=1/2. The drain rate therefore tends to h_2(q) when epsilon_N->0.
Extra retired factory outputs must be included separately. Here work is
uncomputed and unused pair inventory remains retained. Infinite-dimensional
baths need energy-sensitive continuity premises instead of (8).

The repair branch constructs a five-qubit nonflat erasure code with spectrum
(4/5,1/5) at one node and correction of every single-site erasure. It does
not retain its base code's distance-three guarantee. Thus nonflat spectra
need not arise only from appending a dispensable pair. Even this does not
demonstrate advantage for a general protected computation: another encoding,
logical-only recovery or direct gate can remove the full-restoration target.

## 7. Executable scope and finite costs

`pair_factory.py` exhaustively verifies small-block amplitudes, rank/unrank
and clean message uncomputation. Large-block resource certificates use exact
integer arithmetic and an exact rational acceptance inequality; decimals
are descriptive. Directly transmitting b halves is the strong simple baseline.

At a stringent finite workload error, a smaller supply rate can require
thousands of protected bank qubits. That startup, memory, control and reuse
cost can outweigh the communication saving. The delivered result is the
theoretical compiler with those costs visible, not a physical advantage.

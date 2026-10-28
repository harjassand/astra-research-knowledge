# Actual independent audit: controlled retirement and vacuum absorption

29 October 2026 (Australia/Brisbane). Reviewer: adaptive_modes. Author of
the reviewed composition: root.

**Status: ACCEPTED with the mandatory saved transmission-phase/witness
clarification.** No numerical bound, program or frozen parent proof changes
were required. The correction concerns the exact naming of the attenuator
and the chronology of the nonempty witness; its scope is stated below.

## Actual reading, execution and review boundary

I fully read PASSIVE_ABSORPTION_COMPARATOR.md,
CONTROLLED_RETIREMENT_COMPARISON.md, controlled_retirement_certificate.py,
its final JSON, and PASSIVE_DUMP_PHASE_CLARIFICATION.md. I also read the
relevant sequential theorem, full two-cut schedule, witness clarification,
and the interface/formula of the already reviewed general occupied-retirement
theorem. This audit checks the NEW passive-dump and control-composition bridge.
It does not revalidate accepted foundations or claim an independent review
of my own total-moment acquisition theorem.

The second-moment theorem has a separate actual independent acceptance by
conventional_solver. The base sequential theorem/example has a separate
actual independent acceptance by challenger. Both review receipts are
hash-pinned in this audit. Their contracts are inputs here.

I executed the root program in an isolated temporary mirror with identical
pinned dependencies. Its output JSON was byte-for-byte identical to the
final saved receipt, and the root originals were unchanged. The independent
review_controlled_retirement.py imports no author helpers. It reconstructs
25 exact fraction/outward-decimal pairs with binary-search integer root
enclosures, rebuilds the aligned parity constant from its displayed theorem,
checks all four preserved failed sufficient certificates, and checks 120
passive-loss moment cases using probability-generating-polynomial convolution
rather than the author's direct binomial formulas. Its execution passed.

Reviewed root SHA256 values:

- PASSIVE_ABSORPTION_COMPARATOR.md:
  ffda8fe43892b6ecf1e3dbe0c53758f41ad2c9ff8221d30dc438d6d9c0cc1cbc
- CONTROLLED_RETIREMENT_COMPARISON.md:
  9e2cb47134fd047027695ad77523edb66f2544c7668859f02dc660f9b7740b2e
- controlled_retirement_certificate.py:
  42918a33ff5f3e5946368ba599646d901fd8929451807c07ceafe1479c4d0350
- controlled_retirement_certificate.json:
  a744300f0fce1ca578823eef91b72805f3e01c07acdc7961c4776f5420b8f66b
- Mandatory PASSIVE_DUMP_PHASE_CLARIFICATION.md:
  18197e32bab5ddba825075ae4a85cf9b5d402cb4a7cc4a698eb0849f98b9e1fc

## 1. Exact finite near-swap channel

The stated i g(t)[b-dagger a(r)-a-dagger(r)b] is a passive self-adjoint
two-mode generator. Its fixed one-particle generator exponentiates to the
beam-splitter rotation; all scalar-time generators commute. On every number
sector the retained amplitude is cos(phi), phi=integral g, so at
phi=pi/2+epsilon its intensity is

    eta=cos^2(phi)=sin^2(epsilon)<=epsilon^2.

There is no small-angle dynamics approximation. The last inequality follows
from |sin epsilon|<=|epsilon|. A fresh independent vacuum dump gives the
vacuum attenuator, with the possible residual retained-mode phase determined
by the sign of cos(phi). The root clarification correctly supplies that
phase qualification. At exact swapping the output retired factor is vacuum,
and the phase is immaterial.

This local trace-preserving channel preserves the full reduced state of
every other subsystem, including correlated sources, active fields,
references and existing records. It multiplies the selected-mode mean by
eta. Neither identity assumes an incoming product state between that mode
and the retained systems. No count record is generated or independently
sampled. The unknown residual phase is harmless to the invoked arbitrary-
state mean-based retirement estimate; no parity symmetry is assumed for
the post-loss state.

For the duration-one-quarter sin-squared pulse, integration gives the exact
declared area and differentiation gives peak 2|phi|/h and maximum slew
2pi|phi|/h^2. The zero extension is C1. The saved rational upper bounds use
pi<22/7 and the allowed angle tolerance. This proves a finite scalar
waveform under the stipulated isolated passive generator. It does not turn
that unbounded Fock generator into a bounded operator or acquire an actuator.

## 2. Total-moment contraction through passive vacuum loss

On system bath B and fresh dump E, the commuting integer-valued number
operators obey, as positive quadratic forms,

    N_B <= N_B+N_E,
    N_B^2 <= (N_B+N_E)^2,
    (N_B+N_E)(N_B+N_E-1)-N_B(N_B-1)
          =2N_B N_E+N_E(N_E-1) >= 0.

The factorial inequality uses the integer spectrum: N_E(N_E-1)>=0. No
incorrect general operator-monotonicity claim for squaring is needed.
The passive Stinespring unitary conserves N_B+N_E. Pulling these inequalities
back through it and then through the fresh-vacuum embedding proves

    L-dagger(N_B)<=N_B,
    L-dagger(N_B(N_B-1))<=N_B(N_B-1),
    L-dagger(N_B^2)<=N_B^2.

Finite incoming total second moment makes the relevant forms finite; the
identities also follow sectorwise with positive limiting forms. Arbitrary
reference/source correlations cause no change. Nor does a wrong selected
mode, since it is still a passive coupling within the same total bath plus
fresh dump. This is stronger than a test on uncorrelated number states;
the 120 executable cases are consistency checks of the operator result.

The first and second annihilation-row norms therefore cannot increase at a
dump insertion. The separately reviewed moment recurrence can be continued
through every correct or incorrect dump channel using the same conservative
action envelopes. In particular the supplied M2_1=987/50 and M2_2=22449/64
remain valid on the required control-replacement hybrids. This audit uses
those independently reviewed inputs; it does not re-prove their acquisition.

Fresh vacuum and permanent dump inaccessibility are essential premises.
Thermal or correlated incoming dumps, excitation injection or apparatus
return are different channels, with no allowance assigned here.

## 3. Wrong-mode charge and comparison order

For a misaligned mode obtained by W=exp(-iG) on the system bath, extend W
by identity on the dump. The wrong beam splitter is conjugate to the correct
one by this passive unitary. During its middle near-swap term the number in
the SYSTEM alone need not be preserved; the proof correctly uses total
number INCLUDING the dump. That total is preserved by all three unitaries,
and initially equals the supplied system-bath moment because the new dump
is vacuum. The two product-difference terms therefore cost at most

    2theta sqrt(M2).

Tracing the dump is contractive. There is NO random-coin factor on this
charge: the swap is applied on every run. The parity charge, by contrast,
has the independently proved identity-branch cancellation and factor 1-p.
The certificate uses these different factors correctly.

Every wrong-mode control is replaced while all system bath factors are
still present in the common full-channel comparison. Subsequent common
complete channels are contractive even when a later wrong selector touches
an earlier targeted mode. Only after all these replacements are made does
the E_i-based retirement argument run. Then later correctly aligned phase
or dump operations act on orthogonal factors and are K-only for each earlier
retirement. This order avoids an uncharged access/reactivation channel.

The fixed selector and fixed operator generating the scalar pulse are in
the declared interaction picture; the scalar coefficient itself varies with
the saved waveform. Both windows have an ALL-bath coupling blackout. This
includes bath 1 in [1/2,3/4], even though the intended second selector lies
in bath 2. Intended-selector commutation would not suffice for a wrong
selector. Source-only complete operations may continue because they commute
with the bath/dump generator. No background coupling or time-varying selector
has been silently factorized.

## 4. Occupied retirement after absorption and causal composition

For a correctly aligned operation, the post-loss uniform mean satisfies
E_loss<=eta E. In the executed regime eta E<=1, the nonvacuum amplitude
obeys p_occ<=sqrt(E_loss). Inserting P=p_occ=sqrt(E_loss) as upper bounds
into the accepted general occupied allowance yields

    F^2+2PF+(1+sqrt(2))P^2 F+D P^2.

Every substituted term is nonnegative and monotone in the supplied bounds.
With F^2<=W and D<=W/2 this is exactly the loss expression used in the
program. It retains the initial cross-term charge 2PF and does not import
the stronger full-number-dephasing or parity estimate into an arbitrary
attenuated state. At eta=0 it reduces to W per cut, not zero: future
re-excitation of the reset factor remains budgeted.

The aligned operations preserve the exact reduced state at their logical
cuts. Moving their delivery from the isolated earlier window to that cut
commutes only through operations on the complementary factor. This is an
operator/channel identity even for correlated states. Preparation 2 may
straddle the first logical cut because it is R1-trivial. Later local dump
operations are likewise K-only for the first retirement. Exact conditional
retained states and actual feedback records are carried through the common
hybrid prefixes; no independent record sampling, reset source or normalized
rare-branch contract is used.

The future integral is over the whole remaining horizon. For each retired
mode, its nonzero q support has duration at most one and amplitude at most
one. The high-amplitude preparation of the OTHER continuum has q_i=0.
Therefore F_i^2<=W is consistent with the larger total action used for the
global moment contract. The added blackout only removes exposure from that
support. It changes neither bath kernel nor the definition of the selected
mode, and does not license future reintroduction beyond the declared horizon.

The nonempty preparation witness is an existence statement before absorption
for the specified uninterrupted preparation. It is preserved by the parity
operation, not by dump loss. The mandatory root clarification explicitly
states this and distinguishes the equivalent logical-cut input from the
already-absorbed physical state. No after-dump nonempty lower bound is used
in the budget.

## 5. Independently reconstructed exact allowances

Both rows use the same actual smooth preparations, the same declared final
source/active/reference/actual-record interface, the same conservative
continuum exposure, the strengthened blackout schedule and geometric
tolerance theta<=5e-9. Preparation approximation contributes zero because
the processes compared in each construction share their actual preparation.

| Mechanism | Aligned deletion upper bound | Mode-control upper bound | Total upper bound |
|---|---:|---:|---:|
| Hidden parity | 8.445412160082037e-7 | 1.158608667858491e-7 | 9.604020827940528e-7 |
| Vacuum near-swap | 6.748177041626738e-7 | 2.317170992297136e-7 | 9.065348033923874e-7 |

All displayed values in this table are rounded upward. The exact certificate
and independent arithmetic match. They also preserve the four useful failed
sufficient certificates: doubling theta, for either mechanism; doubling the
swap-area tolerance in the aligned dump model; and using only the first
TOTAL moment in the conventional mode-continuity bound. These are failures
of the stated sufficient bounds, not actual process-error lower bounds.

The root receipt labels its decimal margin fields as upward-rounded. For
any later allocation use their exact rational values or round downward;
the upward-rendered last decimal is not extra certified headroom. No new
physical channel was allocated that margin in this construction.

## 6. Fair comparison and scientific limits

The conventional dump is a strong equally informed competitor for the same
unrecorded retirement interface. It uses the selected mode and full process
history; it is not a product of fitted memoryless source channels. On the
stated sufficient bounds it is smaller and tolerates a larger area error.
It spends a fresh independent vacuum oscillator per cut and removes stored
excitation. Parity spends independent hidden random bits and need not empty
the factor. The coefficient units refer to different physical generators,
so the smaller dump peak/slew is not a hardware cost comparison.

This is a complete finite-horizon model-substitution result under explicit
preparation, control, isolation and output assumptions. It does not certify
those hardware resources, retained-solver cost, active loss, thermal noise,
source leakage, measurement delivery, fault tolerance or total workload
error. The 1e-6 budget is a chosen test specification. No count record, device
error rate, hardware winner or computing advantage is fabricated. Within
that scope the new composition is mathematically sound, executable, and
ready to be included with its actual upstream reviews and this clarification.

# Certified same-apparatus operating window: ordinary private Z twirling

Status: executed finite scientific numerical certificate using exact rational/Gaussian-integer arithmetic and analytic norm remainders. This is not a quantum gate backend, an experimental calibration, or a novelty/advantage claim over ordinary twirling. All figures below concern one time interval, with no bath reset during it.

## Result

For the exact cold-input qutrit apparatus below, time T=1, rate lambda=1,000,000, and target complete logical error 1/10,000:

* The unpaired positive-sign apparatus FAILS the target. The explicit rational system input |1><1|=(I−Z)/2 and Pauli observable Y certify an absolute expectation discrepancy greater than 0.0002266611872732366.
* The positive CPTP average of the positive- and negative-interaction apparatus PASSES. Its complete qubit-channel diamond error is less than 0.000000988465317203069.

These are strict rationally verified inequalities, not conclusions from floating exponentials. The displayed decimals are only readable summaries; the JSON stores exact rational lower/upper bounds. The paired upper applies to all system/reference inputs with the explicitly fixed cold source, not arbitrary initial bath states or retained bath outputs.

The winning ordinary operation is precisely system-Z twirling. There is no claim of an advantage over that operation. For a freely chosen logical implementation, the separately exhibited direct generalized-amplitude-damping ancilla circuit remains a strong and usually cheaper ordinary comparator.

## Exact apparatus and target

Use source-first tensor ordering, source basis 0,1,2, and qubit basis 0,1. Let sigma_minus=|0><1| and sigma_plus=sigma_minus^T. The source jumps are

    L1=(|0>+|2>)<1|,
    L2=sqrt(2)|0><2|.

The second jump is represented arithmetically as 2 D[|0><2|], so no irrational jump entry is rounded. The first jump has coherent dark/excited output; this is the mixed-output generator, not its split-output replacement. H=.5 sum L†L=diag(0,1,1), and the dark source is |0>.

The coupling and system Hamiltonian are

    K=|1><0| tensor sigma_minus
       +(1/2)|2><0| tensor sigma_plus + adjoint,
    H0=I3 tensor Z/3.

There is no QQ coupling term. The physical generator is lambda sum D[L_j tensor I2]−i[H0+1000K,.]. Initial source is exactly |0><0| and final source is traced. K^2=diag(1/4,1,1,0,0,1/4), hence ||K||=1. The actual negative branch is obtained by conjugating the entire positive branch by I3 tensor Z at its two ends: this preserves H0 and the source dissipator and reverses K exactly. A fair independent private bit selects whether these two Z operations are used. No sign record is exposed.

The target generator is

    −i[Z/3,.]+2 D[sigma_minus]+(1/2)D[sigma_plus].

This is the previously derived genuine effective GKSL generator. Its coefficient acquisition and the dark-source proof are separate from this finite exponential calculation. For this target, the exact generalized-amplitude-damping formula is another possible evaluation route, but the certificate computes its exponential by the same rational procedure to avoid unpriced transcendental evaluation.

## Certified exponential algorithm

The physical generator is a 36 by 36 superoperator. All real and imaginary entries are rational with denominator dividing 12. The target generator is 4 by 4 with the same denominator convention. Vectorization is column-major. A separate direct-action test checks all 36 physical columns against L rho L†−{L†L,rho}/2 and −i[H,rho], not only the Kronecker construction.

A safe physical generator diamond norm is C=8,002,002: each dissipator costs at most twice the squared jump norm, giving 8,000,000, and the Hamiltonian commutator costs at most 2(1000+1/3). The target has C=6, since its dissipative contribution is at most 5 and its Hamiltonian contribution at most 2/3.

Choose N=2^s>=4C. The physical calculation uses N=33,554,432 (s=25), the target N=32 (s=5). Compute the degree-48 Taylor polynomial for the scaled generator exactly by integer Horner arithmetic. Both real and imaginary numerator matrices and their common denominator are exact. Since the scaled diamond norm is at most 1/4, the Taylor remainder is bounded by

    t0=2/4^49.

Round the polynomial entries to nearest multiples of 2^-128, and perform s exact Gaussian-integer matrix squarings, rounding each result to the same dyadic grid. Real/imaginary rounding is signed and deterministic. No floating matrix exponential or interval inferred from floating output is used.

For a d-level channel, a conservative complete norm bound for one such entrywise rounding is r0=2d^3 2^-128: reshuffling preserves the Frobenius norm, the unnormalized Choi matrix has dimension d^2, and diamond norm is bounded by its trace norm. This bound is deliberately loose. If e is the current diamond error relative to the exact CPTP exponential, one square plus rounding obeys e_next<=2e+e^2+r0. Set x=e+r0. Then x_next<=(1+x)^2−1 and x_base<=t0+2r0. With N(t0+2r0)<=1/2, the final error is bounded by 2N(t0+2r0). The code verifies this rational premise.

The resulting physical exponential error is at most

    67108891 / 158456325028528675187087900672,

less than 4.24e-22. The target exponential error is at most

    67108865 / 166153499473114484112975882535043072.

Prepending the cold source and tracing it out are exact channels and cannot increase these bounds. The approximate dyadic exponential itself need not be CP; this is a certified numerical enclosure of a known exact CPTP exponential, not a synthesized channel.

## Exact lower and complete upper

The script extracts the cold reduced 4 by 4 superoperator by summing the three source-diagonal output blocks. System Z conjugation has Liouville diagonal (1,−1,−1,1), so averaging the two physical signs keeps precisely the even-parity entries. This exact identity avoids a second physical exponential. The target commutes with this Z conjugation.

For input |1><1| and observable Y, the dyadic unpaired-minus-target expectation is exactly

    −38564402647223524088246402358727473
      /170141183460469231731687303715884105728.

Subtracting the two certified exponential errors from its absolute value gives the exact lower bound

    38564402647223524016188710610292529
      /170141183460469231731687303715884105728 > 1/10000.

Since ||Y||=1, this is a trace-norm and hence channel diamond lower bound. No rare event, postselection, statistical sampling or reference preparation is needed for this witness.

For the paired channel, form the unnormalized 4 by 4 Choi difference by reshuffling the dyadic superoperator. Its Frobenius norm squared is computed exactly as the sum of the squared real and imaginary numerators. The certificate uses

    ||Delta||diamond <= ||J(Delta)||1 <= 2 ||J(Delta)||F.

An integer square-root ceiling supplies a rational upper bound on the last quantity. Adding both certified exponential errors gives

    164236971561091887388162260993
      /166153499473114484112975882535043072 < 1/10000.

This is a complete qubit-channel upper bound, not merely one input-state check. Exact fractions and the Frobenius square are in the report, and the full dyadic reduced/target matrices are retained for independent replay.

## Executed checks and immutable artifacts

* certify_same_apparatus_window.py — SHA-256 c1d37c0d6e47abad3f6eeffd0011639f08b02ddefe059e4b1e5e140c9e3c05df.
* test_same_apparatus_certificate.py — SHA-256 03c7670b4a369103ec8af2d57f9b69497a71cae60f01a93f007a72fc0221d318.
* same_apparatus_exact_matrices.json — SHA-256 2055bf9f224a169d0e3822cab9d556b8da8c4ac11dd3b76315921b730e1ef8a4.
* same_apparatus_certified_window.json — SHA-256 55af8b690b94b5d3387963657971842b65082e4048915cb8710a17ae5b0a08ae.

Both scripts ran successfully. Tests check the 36 direct generator columns, exact K norm and Z sign conjugacy, and replay the physical exponential at 160 bits/degree 52. The latter result lies within the sum of the two analytically certified errors in a Choi trace upper bound. The acceptance decisions themselves compare exact fractions with 1/10000; elapsed-time and decimal fields are descriptive only. The initial denominator-6 attempt rejected the target's quarter-valued entries before computing a certificate; the final implementation correctly uses denominator 12 throughout.

## Scientific interpretation and limitations

This is a rigorous small same-apparatus operating-window separation: at the specified finite rate, time, cold input and target operation, the unpaired logical channel is demonstrably outside tolerance while its ordinary private-Z-twirled counterpart is inside. It is stronger than comparing two sufficient analytic admission rates, but it is only this fixture. It does not prove a uniform rate threshold, an optimized resource crossover, or a generic lower bound for unpaired implementations.

The physical source runs continuously for time one in both branches. There is no intermediate bath reset or source modification. Cold preparation, actual apparatus calibration, the two optional Z gates and their errors must be supplied and paid. The paired numerical margin leaves room for those errors, but no laboratory or gate-synthesis error has been measured here. The direct effective GAD circuit may avoid the apparatus altogether; the result claims no advantage over it or over system-Z twirling, which is exactly the improvement used.

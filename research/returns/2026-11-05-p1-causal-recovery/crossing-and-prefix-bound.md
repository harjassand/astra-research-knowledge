# Crossing, interpolation and an all-instrument prefix memory bound

The [complete crossing proof](package/operational_constructor/crossing_gap_proof.md) and [independent sharp-profile audit](package/channel_constructor/sharp_profile_and_gap_audit.txt) concern the [actual fixed weak stream](README.md). Partial transpose, complex spectral shifts and inverse monodromy appear solely in a mathematical converse, not as proposed physical receiver operations.

For n emitted carriers put `D=2^n`, let U_n be the chronological collision unitary and define the bistochastic bath map `T_n(X)=Tr_S[U_n(I tensor X)U_n*]/2`. Its singular defect is `H_n=I-T_n T_n*`. The source is granted to a hypothetical decoder at the prefix only to make recovery easier: it can simulate the remaining known collisions. This does not grant source access to a physical construction.

Refine a general prefix instrument into Kraus outcomes K_x and reveal the refinement. With `A_x=sqrt(K_x* K_x)`, `rank(A_x)<=m` and `sum_x A_x^2=I`, the witness

```text
Z=(1/D)sum_x |A_x>><<A_x|
```

has unit trace, both marginals I/D and `0<=Z<=(m/D)I`, despite unlimited classical branching. The logical-qubit Petz recovery has the exact identity `Tr(H_n Z)=1-F_P`. Renes's established sharp inequality `F_P>=F^2+(1-F)^2/3` gives, for the small-error regime,

```text
Tr(H_n Z)<=eta(epsilon)=2epsilon-(4/3)epsilon^2.
```

It sharpens the earlier `3epsilon(1-epsilon)` budget throughout `0<=epsilon<=1/2`. The density-cap spectral filling, heat-trace and branch-tail consequences retain the earlier theorem's quantifiers. They are necessary conditions, not an implementable compression criterion. [Independent recovery/cap audit](package/algebra_constructor/renes_profile_audit.txt).

## Quantitative singular gap

Let `u=cot(theta)` be real, finite and nonzero and `M_n(z)=(zI+iP_Sn)...(zI+iP_S1)`. Source partial transpose and Pauli-y conjugation give the crossing identity `C[M_n(z-i)]=(z^2+1)^n M_n(z)^-1`. For an almost-preserved traceless bath operator X, set Y=T_n(X). Their intertwining defect is small. **X and Y need not agree**: crossing alternates them, and even shifts restore the original pair.

Interpolation at n+1 even shifts controls both the leading coefficient X-Y and the value at zero. At zero the monodromy is the cyclic permutation of all n+1 sites. Commuting single-site trace projections, or the sharper Dirichlet-path cycle estimate, then force X toward scalar identity. Thus identity is the only singular-value-one direction for this angle range.

With

```text
B_n=(u^2+4n^2)/|u|,
K_n=B_n^n[(|u|+2n)^n+1]/n!,
alpha_n=4sin^2(pi/[2(n+1)]),
```

the supplied proof gives `gamma_n>=6/[n(n+1)(2n+1)K_n^2]` and the sharper `gamma_n>=alpha_n/K_n^2`, hence `gamma_n>=exp[-4n log n-O_theta(n)]`. This is an actual singular-gap lower bound, in contrast to variational upper bounds from trial modes.

Since the kernel is one dimensional, the witness energy is at least `gamma_n(1-m/D)`. Choose n=q+1 at a cut with peak capacity q, provided n<=N; then `m/D<=1/2`. The sharpened recovery budget yields the [fixed-angle memory consequence](README.md). If q>=N, storage is already linear. The bound remains too weak to rule out all o(N) receivers.

## Exact small-prefix floors and a retained failed route

At two carriers, when `tan(theta)^4<=1/3`, `gamma_2=2sin(theta)^4-sin(theta)^8`. Every receiver retaining at most one qubit after that cut has an error floor beginning `theta^4/2+O(theta^6)`. At three carriers the exact leading coefficient is `(7-sqrt(33))/2`, giving a two-qubit error floor beginning `(7-sqrt(33))theta^4/8`. These include arbitrary instruments/classical histories, but vanish with the angle.

The [exponential-gap attempt](package/algebra_constructor/exponential_gap_status.txt) proves an exponential resolvent/fixed-point-defect bound and an ordinary eigenvalue bound. A contraction can have singular value one despite a nonzero fixed-point defect; the retained nilpotent/block counterexamples explain why that route does not establish the desired exponential singular gap. Integrable eigenvalues/Jordan structure do not repair this implication. Finite symbolic and matrix checks corroborate formulas, rather than establish asymptotics by extrapolation. [Source package and proof status](SOURCES.json).

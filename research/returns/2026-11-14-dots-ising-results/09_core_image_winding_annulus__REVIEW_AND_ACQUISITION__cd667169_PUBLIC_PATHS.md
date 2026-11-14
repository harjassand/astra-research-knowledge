# Independent winding-annulus review and source-acquisition construction

Reviewed n1722_winding_annulus_20261113/RESULT.md, its scalar/geometry checks, the actual source core interface and optimized-cut capacity JSON.

## Proof and topology
The source is explicitly G={x XOR D:x in A, S minus, Nplus_D(x)<|D|/2}, not every state with a positive-magnetization annulus. D consists of2R whole columns, S its two inner boundary columns and two outer collar columns. Complete pinned columns separate core components across both physical and fixed nearest-diagonal edges. A core component cannot bypass a full column by a diagonal step; its filled contractible domain cannot enclose a pin on that separating column without crossing the column. Thus the conditional exterior is the actual r-core gas with minus boundary, including its thermal entropy, independently of fixed interior bits.

The reweighting w(x XOR D)/w(x)=exp[-4phi Nplus_D(x)] acts only on interior bits. It changes the marginal interior source law but not the needed conditional exterior law. Therefore the exterior MGF remains the stated field-tilted core MGF. It is not an unjustified Gibbs replacement for an incoming current.

Each retained inner boundary is a full plus noncontractible loop. Keeping D fixed preserves this actual winding witness while exterior sites are flipped. All native path edges remain outsideM5. The partial-column boundary excess<=2 is valid before, between and after completed columns; touching the second collar only reduces it. First-B stopping and positive M_D guarantee termination at the actual target. Source states already inB take zero paths.

For fixedD, source reconstruction from an oriented edge and its flipped-site prefix is unique. Interior labels add no multiplicity. Pairing the resulting divergence against the GLOBAL original soft-source voltage is legitimate even though the paths leave any capped-area region.

The reported capacity constants exp(-1548),exp(-4136),exp(-21502),exp(-217281) match the independently acquired optimized-cut JSON for exactly the listed R,r,n. Its bound drops kappa<=1 only in an upper-bound term, so this does not change the original soft clock. This review does not independently reprove that capacity proof's joint-contour geometry.

## Packaged baseline, including the R10000 instance
This packaged acquisition contract uses the conservative rho<=1/8000000 bound proved by the LOCAL check.py and used in RESULT.md. It does not depend on the reviewer's optional stronger external density calculation. The same injection/target-exclusion argument gives

    Z_(G minus B)/ZA >=1-36L rho-6rho.

At L=8R this is .99711925,.99279925,.96399925,.63999925 for R80,200,1000,10000, respectively. These are substantial Gibbs masses on exactly the non-target sector, so the exponentially small actual-voltage occupation is genuinely stronger than v<=1 there. No generic winding coverage follows.

## Constructive acquisition: no unavailable conditional sampler
The core's acquired TV sampler suffices to sample the annular Gibbs source. Draw x from mu_A, compute y=x XOR D, and accept with

    a(x)=1_{S minus, Nplus_D(x)<|D|/2, y notin B}
         *exp[-4phi Nplus_D(x)].

The acceptance probability is exactly p=Z_(G minus B)/ZA and the accepted y has exactly the Gibbs law onG minusB if the core draw and Bernoulli coin are exact. No probability evaluation for mu_A, new normalizer, conditional Gibbs oracle or native rare-exit simulation is needed. The lower p0 above gives expected at most1/p0 core calls. Membership/pins, plus counts and XOR require polynomial work in n. This is a Gibbs-source sampler for the flow, NOT an actual incoming-current sampler.

For the real acquired approximate core sampler, suppose TV error<=delta and implemented acceptance differs pointwise by at most zeta. The accepted laws differ by at most4(delta+zeta)/p0 when delta+zeta<=p0/2 (a conservative normalized-subprobability bound). Taking delta=zeta=p0*epsilon/32 leaves at most epsilon/4 conditional error. Cap the number of attempts at ceil[(2/p0)log(2/epsilon)]; acceptance is at leastp0/2, so failure probability<=epsilon/2. Arbitrary fallback on that event adds at most that probability to TV. Total error is less thanepsilon. Evaluation of exp(-4phi N) to absolute errorzeta uses ordinary certified arithmetic; terms belowzeta can be truncated rather than represented with enormous denominators. All costs, including core sampling and cap, are polynomial in the source interface's stated parameters.

Acceptance-probability estimation also acquires Z_(G minusB)/ZA to relative accuracy with polynomial samples because p>=p0. Multiplying by the existing relative core normalizer acquires this restricted source normalizer, with confidence/bias budgets charged separately. A sampled source can be replayed along at most n flips; an edge has at most two reconstructed candidate sources. Thus the restricted path representation is algorithmically accessible, rather than a2^area Poisson solve.

The exact core interface supplies approximate sampling, not a hidden exact oracle; the finite-error construction above is the advertised algorithm. It gives no sampler for arbitrary winding states or the unknown full residence measure.

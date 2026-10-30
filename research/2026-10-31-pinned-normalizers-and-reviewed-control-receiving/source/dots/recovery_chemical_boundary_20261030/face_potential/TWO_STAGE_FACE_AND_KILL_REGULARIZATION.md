# A genuinely multi-step face certificate and a reusable killing transform

New local construction, not a full-network theorem or independently reviewed extension. This supplies a non-one-hold witness for the face-potential method without postulating a uniform initial population reset.

## 1. Multi-step hidden dynamics

On D=0 consider the A-neutral conservative face moves

    C+E -> C+F   at alpha C E,
    C+F -> C+E   at delta C F,
    C+F -> C+D   at beta C F,

with positive alpha,beta and nonnegative delta. The first two are internal; the third exits to positive D. Let z=E+F. The active face is C>=1,z>=1. Its internal moves preserve this face and the pool E+F+D. There can be arbitrarily many internal reversals before restoration; a one-hold description is false.

Set v=1/alpha and u=(1+delta v)/beta, and define

    psi0(E,F,C) = [u + v E/z]/C.

Then 0<psi0<=(u+v), uniformly in population. Let Q0 be the hidden subgenerator killed at restoration. Direct calculation gives

    -Q0 psi0 = alpha v E/z - delta v F/z
                  + beta F(u+v E/z).

If F=0, this equals alpha v=1. If F>=1, the last term minus delta v F/z is at least F(beta u-delta v)>=F>=1, while the first term is nonnegative. Therefore -Q0 psi0>=1 at every active face state. This is an actual all-population bounded face potential, not a finite truncation or an assumed spectral gap.

For alpha=beta=delta=1, psi0=(3E+2F)/[C(E+F)]. In this case

    -Q0 psi0 -1 = F(3E+2F-2)/(E+F)>=0,

with the F=0 case interpreted as zero. The inequality is exact already at the one-label face states, where the mean restoration times are 3/C and 2/C.

## 2. Adding the seed/clear hazard without losing ingress compensation

Let c>=0 be a killing rate constant DURING this face excursion; for the chemical module c=(k_seed+k0)(a)_2 because a stays fixed until the exit. If a bounded nonnegative psi0 satisfies -Q0 psi0>=1, define

    psi_c = (4/3) psi0/(1+c psi0).

Then for Q_c=Q0-cI,

    -Q_c psi_c >=1,
    psi_c <=(4/3) min(psi0,1/c)       (the second term omitted at c=0).

Proof: f(t)=t/(1+ct) is concave, increasing and f(0)=0. Including the restoring cemetery value0, Q0 f(psi0)<=f'(psi0)Q0 psi0. Hence

    -(Q0-cI) f(psi0) >= 1/(1+c psi0)^2 + c psi0/(1+c psi0)
                       = 1 - [c psi0/(1+c psi0)^2] >=3/4.

Scaling by4/3 proves the claim. This is a reusable certificate transformation. It correctly includes the actual seed/clearing kill; simply using psi0 can fail the a-born ingress test.

For the unit-rate face the resulting rational potential is

    psi_c = (4/3)(3E+2F) /
                  [C(E+F)+c(3E+2F)].

It is uniformly bounded by4 and is a concrete member of a finite rational denominator dictionary.

## 3. Actual ingress bounds

A positive-D ingress C+D->C+E at D=1 has rate kappa C. At its actual output,

    kappa C psi_c <= (4/3) kappa (u+v),

so it satisfies the summed entrance-cost certificate independently of population.

An a+D->2a ingress at D=1 has rate kappa_a a and actual output a_out=a+1. If that output lies in the active face, its seed/clear kill is c_out=k(a+1)a, k=k_seed+k0>0. Thus, for a>=1,

    kappa_a a psi_(c_out) <= 4 kappa_a/[3k(a+1)],

and the a=0 ingress has zero rate. This pays precisely the growing a-born ingress that a hidden-only mean-time bound would miss. Contributions of different ingress reactions must be SUMMED.

These calculations exhibit an acquired multi-step face potential, uniform face moments, and exact entrance compensation. They do not by themselves certify a full raw network: connector, positive-D pool/baseline, true-F terminal, activity and weak-reversibility checks are still required. Their purpose is to show that replacing one-hold tracing by (P),(I) is a substantive extension with a realizable symbolic witness, not a formal relabeling of the old denominator.

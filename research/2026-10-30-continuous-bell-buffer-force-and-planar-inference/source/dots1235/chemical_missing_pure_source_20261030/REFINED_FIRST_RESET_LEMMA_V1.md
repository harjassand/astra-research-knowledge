# First-reset occupation-sensitive escape bound
Status: personal derivation, not independently reviewed. This is a local positive-kernel lemma; no global recurrence conclusion.

Fix integers q>m>=2 and a large residual r. Stop low/fast excursions at the first nonzero r exit, a return to the pointwise active section B=q, or a designated bad event. Fast processing at a launch phase b>=2 is assumed to have the following EARNED properties, uniformly in its full incoming composition:

1. Bad-event probability <=Cp; otherwise it returns to a low phase <=b-1 or makes a safe downward exit.
2. Its joint reset output law satisfies the inverse-moment bound <=Cp relative to the low-return mass. Phase correlations are retained in the kernel.
3. The phase-dependent reset-walk bound from a fresh low reset at phase b is <=C p^{min(q-b,m)/m} for upward/bad escape before the return target, with constants depending only on fixed m,q and rates.

For the A-catalytic family, a high-B clearing output with A=0 is a designated bad event. Its mass is <=Cp by the same inverse-moment bound. It is not treated as an active fast episode. Its physical continuation must be separately paid in a global repair construction.

Let nu be the FIRST law at B=0 after clearing, with total mass <=1 and

    int (1+A)^-m dnu <=t.

There is no pointwise bound on the output A and no independence assumption. Take the compulsory physical immigration from B=0 to B=1. It increases A, so the moment bound remains <=t. A zero-length immigration run from B=1 activates immediately into B=q and terminates safely at the section, before any new fast process.

For 1<=ell<m, let E_ell mean that exactly ell additional immigrations occur before activation, without an earlier upward exit. Since every positive low phase has immigration-versus-activation probability <=C/(1+A), its conditional probability given initial A is <=C_ell(1+A)^-ell. Integration and Holder give

    nu(E_ell)<=C_ell t^(ell/m).

If ell>=m, the mass of ever reaching the m-th additional immigration before activation is <=C_m t. Any earlier upward exit lies in this term because q-1>=m. This term can safely be charged in full.

For 1<=ell<m, activation launches at b=ell+1. This is a new fast ENTRANCE, before observing its reset. Conditional on its full incoming state, either a bad event occurs with probability Cp, or a fresh reset lands at phase <=ell, or a safe downward exit occurs. The later escape probability is therefore <=

    C[p+p^{min(q-ell,m)/m}]
       <=C p^{(m+1-ell)/m},

using q>=m+1. This bound is uniform at the entrance: it does not condition the inverse-moment estimate on an observed rare reset composition. Integrate it against the E_ell entrance kernel and sum the finitely many ell. Thus

    P(upward/bad escape before return to section)
       <=Ct+C sum_{ell=1}^{m-1}t^(ell/m)p^{(m+1-ell)/m}. (R)

The first and later laws are deliberately different. Replacing t by its worst-case upper bound p can lose the decisive comparison with the ACTUAL incoming activation opportunity.

## Application to the local occupation lemma
At B=q, let T and U denote actual time and A-occupation up to the first connector event. The first clearing-output subprobability law satisfies t<=CT by the clearing compensator and

    (A)_m/(1+A-m)^m<=C_m.

Its total mass need not be normalized: the proof of (R) used total mass <=1, and Holder continues to give int f^ell<= (int f^m)^(ell/m). The first immigration probability is k_I T, while the first activation probability is k_T q U.

Suppose the local estimates supply T<=e_N U, U>=u_N, and every later fast processor has p_N. Dividing (R) by U yields

    escape/U <=C e_N
       +C sum_{ell=1}^{m-1} e_N^(ell/m)
            (p_N/u_N)^(1-ell/m) p_N^(1/m).             (G)

For the A-catalytic source contract,

    e_N=C N^-gamma log(N+1),
    u_N=cN^{-(m-1)}, p_N=C N^{-(m-1)}log(N+1),
    gamma=(m-1)/(2m).

The ell-th cross term divided by e_N is at most a power of log(N+1) times

    N^{gamma(1-ell/m)-(m-1)/m},

which tends to zero for every 1<=ell<m. Hence the whole ratio is O(e_N). In particular it remains small after multiplying by a factorial upward-jump ratio O(r^{alpha h}) when alpha h<gamma and N is comparable to r at the section.

This is the relative event gap needed by the section drift. Global conclusions still require the actual weighted repair of the designated bad events, including physical seeding at A=0, as well as a complementary unbounded-direction value. Those are not hypotheses hidden in this local lemma.

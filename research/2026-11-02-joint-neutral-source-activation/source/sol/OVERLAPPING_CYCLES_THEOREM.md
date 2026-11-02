# A globally paid source-switch construction for two overlapping ordered cycles

Same-principal author proof, not independently reviewed or historically cleared. The raw coupled network is a diagnostic for a reusable operation; arbitrary weak reversibility remains the destination. No inventories, physical clocks, source choices or receiving laws are frozen.

## 1. Whole theorem, raw list and strongest ordinary baseline

On (A,B,C,D), consider eight genuine channels, with arbitrary fixed positive constants alpha_0,...,alpha_3,beta_0,...,beta_3:

    I:  0 -> A+B -> 2A+B+C -> 3A+2B+2C ->0,
    II: 0 -> B+C -> 2B+C+D -> 3B+2C+2D ->0.

**Theorem.** The actual CTMC on N^4 is nonexplosive and irreducible positive recurrent. For some beta>0 its stationary law has

    E_pi[(1+q) product_(i=1)^4(X_i!)^beta]<infinity.            (O1)

In particular E_pi[(1+q)exp(rN)]<infinity for EVERY r>0. A positive physical return to zero has a finite exponential moment at some positive argument. No numerical head, moment normalizer, useful mixing bound or spectral gap is claimed acquired. The exact statewise source-word selector IS acquired by the accompanying program.

Each cycle alone is the admitted deficiency-zero k=3 family; its ordinary product-Poisson solution is already known. The union has seven complexes, one linkage and rank four, hence deficiency two. It is complex balanced exactly when the two one-cycle balance points are compatible on B,C:

    (a,b,c)=(alpha_0 alpha_3/alpha_2^2,
             alpha_2^2/(alpha_1 alpha_3),
             alpha_1 alpha_2/(alpha_0 alpha_3)),
    (b,c,d)=(beta_0 beta_3/beta_2^2,
             beta_2^2/(beta_1 beta_3),
             beta_1 beta_2/(beta_0 beta_3)).

The all-unit locus has the ordinary independent unit product-Poisson law. It supplies no new recurrence evidence. At alpha=(1,1,1,2), beta=(1,1,1,3), the required shared B,C values are respectively (1/2,1/2) and (3,1/3), so that ordinary Poisson premise is impossible. The theorem covers all positive rates, rather than a tuned fixture.

Irreducibility follows using the already banked literal deletion words: cycle I decrements each of A,B,C with all other coordinates unchanged; cycle II decrements D. Their sources are enabled whenever the coordinate to be deleted is positive. Weak reversibility supplies reverse paths. Thus every state communicates with zero. This reachability fact is not substituted for the clock/reward proof.

## 2. The common value and what the accepted predecessor actually supplies

Use the ACTUAL carried product mark t, residual z=x-t, V=sum log(z_i!), and W_alpha=exp(alpha V), exactly as in BOUNDED_SOURCE_SWITCH_EPISODES.md. All receiving values and physical rewards use this SAME marked quantity.

The unchanged accepted N1567 exact cone constructor was run on these raw endpoints. Its receipt is results/overlap_accepted_terminal_gap.json. It acquires exact nonnegative cone witnesses for fourteen of the fifteen nonempty divergence subsets I. Its only refusal is I={B}, with dual weight w_B=1. The new verifier checks the inherited fourteen witnesses by raw membership, outside-coordinate availability, nonnegative rational weights and gains >=1; it does not relabel the rejected whole certificate accepted.

The B refusal is also transparent directly. If two complexes s,c satisfy s_A<=c_A, s_C<=c_C, s_D<=c_D, then s_B<=c_B: within each chain, the outside coordinates bound its index, while a cross-chain source cannot have larger B without exceeding C or D (or A). Thus every accepted-cone pair has B gap <=0. This is failure of that architecture, not instability.

For each of the other fourteen I, the accepted cone argument already proves: along every residual sequence divergent exactly on I, one raw terminal c in the sole linkage has actual p_(z+c)(c)->0. Paths from every actual initial mark t to c exist in the raw graph and use at most six edges. Those ordinary carried-target candidate episodes remain available unchanged. Their previous acceptance is neither re-audited nor inherited by the new conclusion.

## 3. Complete repair of the entire remaining B face

Let z=(a,b,c,d), with b->infinity and a,c,d fixed nonnegative integers. There are four exhaustive raw rows:

1. If a>=1, use raw terminal 0. At x=z, source A+B is enabled and

       p_0(z)<=(alpha_0+beta_0)/(alpha_1 a b)->0.

2. If c>=1, use raw terminal 0, now with source B+C, giving

       p_0(z)<=(alpha_0+beta_0)/(beta_1 b c)->0.

3. If a=c=0 and d>=1, use raw terminal t=2A+B+C. At z+t,

       (z+t)_t=2(b+1),
       (z+t)_(2B+C+D)=b(b+1)d,

   so p_t<=[2alpha_2/(beta_2 b d)]->0. A raw path to that terminal exists from every mark.

4. The only remaining row is a=c=d=0. From any carried mark follow a raw path to zero, retaining the same residual z. Then designate I0, I1, and I1 AGAIN. The physical states and actual marks after those three edges are

       (1,b+1,0,0),   mark A+B;
       (2,b+1,1,0),   mark 2A+B+C;
       (3,b+1,2,0),   mark 2A+B+C.

   At the repeated-source state the exact equality is

       (2,b+1,1,0)_(A+B)=2(b+1)
                         =(2,b+1,1,0)_(2A+B+C).              (O2)

   Hence this actual SOURCE switch has Delta V=0, although its source differs from the carried mark. The residual changes from (0,b,0,0) to (1,b,1,0), whose factorial product is still b!: no invisible receiving-law change has occurred.

   At the final physical state the carried factor is 12(b+1), whereas source 3A+2B+2C has factor 12b(b+1). Therefore

       p_(2A+B+C)(3,b+1,2,0)<=alpha_2/(alpha_3 b)->0.         (O3)

   Take one final ordinary genuine jump and stop. All unexpected channels at any earlier phase also stop immediately at their actual endpoints. The whole new candidate uses at most seven genuine jumps, including the ordinary terminal jump. The guard z_A=z_C=z_D=0 is exact raw count data, not a supplied face oracle.

These four rows cover EVERY fixed outside residual profile; outside profiles diverging in any additional coordinate are already among the other fourteen I. The repair therefore closes the global availability argument, rather than one favorable launch.

## 4. Full competing paths and the physical receiver

Every designated edge in the inherited path library has zero marked increment. The new repeat has zero increment by (O2). At each phase its designated-channel probability is at least q_0 p_t, with q_0=min kappa/max outgoing constant, including when the selected source differs from t. Thus the full-jump multiplicative recursion and the already banked scalar envelope apply with h=6, m=7 and c=1.

The finite candidate library contains every ordinary raw path to every terminal, plus the new B candidate when its exact guard holds. Choose the candidate with LEAST actual final mark probability, computed exactly from the raw rates and deterministic designated prefixes. The preceding coverage proves that for every fixed positive terminal threshold its failure set in the actual marked class is finite. The selector requires neither that threshold nor head membership to operate.

Choose alpha,eta>0 by the finite real recursion in (S6). Outside the proved finite head,

    E W_alpha(actual output)<=(1-eta)W_alpha(input).           (O4)

This includes every mismatch and all actual landings. At all prejump points of a continuing designated word W_alpha is exactly unchanged. Consequently

    E integral (1+q)W_alpha dt
       <=7(1+1/kappa_min)W_alpha(input).                     (O5)

Take C>=[7(1+1/kappa_min)+1]/eta and U=C W_alpha off the head, zero inside it. Equations (O4)-(O5) give one global physical contract

    E[ integral (1+q)W_alpha dt+U(actual output)]<=U(input)-1. (O6)

No phase resampling, stationary conditional distribution, uniform mixing gap, infinite-rate limit, neighboring-profile transport or off-face return law has been assumed. The actual occupation and activity contract closes before the recurrence conclusion.

Repeat these actual episodes, then close the original finite-head trace as in the banked multiplicative theorem. This pays an entire regenerative cycle, proves nonexplosion and positive recurrence, and gives an exponential genuine-jump return moment. Since q>=min kappa>0, actual holding-time MGFs transfer a sufficiently small positive argument to physical return. The bounded mark size absorbs full factorial moments at any beta<alpha into W_alpha. Regeneration of (O5) gives (O1), including its genuine activity weight.

## 5. What is new and the genuine remaining obstruction

The earned operation is a FACTORIALLY NEUTRAL SOURCE SWITCH followed by the same raw rarity/receiver calculus. It resolves a face that the complete accepted terminal-gap cone refuses, in a coupled four-species nonconservative network with no one ordered source chain or shared +1/-k anchor. The broader bounded-source-switch calculus shows how to receive and pay such operations at one common quantity. The finite exact selector is implemented; the enormous existential exponent/head and stationary normalizer are not presented as numerical outputs.

The previously identified competing surfaces A~sqrt(D) and A~D^(2/3) do not force following a long mesoscopic excursion: the new marked representation receives competing branches earlier. They remain correct rate identities, not impossibility evidence. The diagnostic is now solved rather than promoted as a substitute for the general programme.

The full weak-reversibility target remains open. A universal uniformly multiplicative word grammar is already excluded by the banked ordered-cycle example with no exponential physical return moment. General rare source switches and interacting unbounded debts require a weaker shared return/reward rule, or a different global representation. The support/persistence and reciprocal-bath theorems in this packet are separate complete assets; none is automatically composed into that unrestricted principle.

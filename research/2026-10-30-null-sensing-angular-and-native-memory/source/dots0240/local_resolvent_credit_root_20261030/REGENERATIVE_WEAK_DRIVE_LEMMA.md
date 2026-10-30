# Regenerative weak-drive resolvent: sufficient finite-matrix conditions
2026-10-30. Root derivation candidate; actual native instance verification belongs to the weak-initiation construction.

Let K_epsilon be an analytic finite-dimensional CP substochastic killed generator, with K_epsilon=K0+epsilon K1. It describes the actual isolated controller with only useful terminal gains deleted; identity abort/cleanup returns remain. Assume:

1. K0 has a simple semisimple eigenvalue zero. All other eigenvalues have strictly negative real part. The zero mode is a regenerative idle class with a unique stationary monitor state; it need not be pure.
2. There is an exact sign covariance K_(-epsilon)=Ad_Z K_epsilon Ad_Z for a fixed controller involution Z. The simple slow eigenvalue is consequently even.
3. A real monitored path yields, for fixed T,c>0 and sufficiently small epsilon>0,

       exp(T K_epsilon^*) I <=(1-c epsilon^2)I.

   This is an actual instrument lower bound, not an effective rate assumption.
4. The zero-mode harmonic effect Q0 is normalized to identity on the idle class, obeys 0<=Q0<=I, and has a spectral gap below I on a subspace E. Its first perturbative coefficient Q1 has support only between E and the maximal-eigenvalue subspace of Q0 (or inside E), with P_max Q1 P_max=0. In the intended acquisition model, Q0 is the probability of returning to idle before a useful completion; every legal acquisition state has a fixed positive success probability, while cleanup states have Q0=I and no coherent first-order coupling to idle.

## Strict second-order decay
Analytic finite-matrix perturbation theory supplies a unique analytic eigenvalue lambda(epsilon) near zero. Semisimplicity follows also from boundedness of the unperturbed CP semigroup. Sign covariance gives lambda'(0)=0. Assumption 3 bounds the spectral radius of exp(TK_epsilon) by 1-c epsilon^2, hence Re lambda(epsilon)<=T^(-1)log(1-c epsilon^2). The slow positive mode is real, so

    lambda(epsilon)=-a epsilon^2+O(epsilon^4), a>=c/T>0.

Thus the second-order useful rate cannot vanish. No explicit susceptibility formula is necessary once the actual path bound is proved.

## Laurent expansion and the spectral excess
The remaining spectrum stays separated from zero. Normalize the analytic right Heisenberg eigen-effect Q(epsilon)=Q0+epsilon Q1+O(epsilon^2) and its left eigenfunctional so the resolvent on identity has form

    R_epsilon=integral_0^infinity exp(t K_epsilon^*)I dt
             =r_epsilon Q(epsilon)+O(1),
    r_epsilon=Theta(epsilon^(-2)).

The bounded remainder is in operator norm. Positivity follows from the survival integral. On the maximal-eigenvalue block of Q0, the first-order compression vanishes. Completing the square across the fixed gap on E gives

    Q0+epsilon Q1+O(epsilon^2) <=(1+C epsilon^2)I.

Therefore ||R_epsilon||<=r_epsilon+C' with C' independent of epsilon. On the idle block, R_epsilon=r_epsilon I+O(1); idle/excursion coherences are O(epsilon^(-1)). Choose Rmax=r_epsilon+C'' strictly above the norm and beta=b epsilon^2. The exact CP service credit then has

    S_idle=I+O(b epsilon^2),
    S_idle,excursion=O(b epsilon),
    S_excursion=I-b c0(I-Q0)+O(b epsilon),

with S bounded uniformly away from zero for small fixed b. Its generator service is exactly -beta d minus the retained terminal intensity loss, as in SINGLE_CONTROLLER_CP_CREDIT.md.

## Actual-path verification strategy
From an idle clock label, select one weak initiation hop, then a finite monitored path through the fast acquisition/commit/C chain to useful terminal. The weak hop has probability at least c1 epsilon^2 over a fixed short interval, because its first nonzero amplitude is linear in epsilon and the local remainder is uniformly bounded. All subsequent selected transitions have fixed positive rates. From any other isolated state, a fast path either yields useful completion or returns to idle; an initial clock-monitor instrument handles arbitrary coherent input. This can establish assumption 3 if the actual alphabet and monitors have the stated paths.

For assumption 4, distinguish irreversible jump connections from coherent ones. The first-order forcing ad_(H_init)Q0 connects idle only to acquisition. If fast controller evolution preserves that coherence sector, Q1 never reaches the gapless cleanup-return sector. An irreversible ready reset does not create an idle/cleanup coherence. These facts must be verified for the real monitor/workspace/register model, not inferred from a classical transition graph alone.

This lemma is a finite-dimensional normal-form ingredient. It does not establish a uniform many-hub expansion, activity-collision bounds, dirty-sector surgery, or the native memory theorem.

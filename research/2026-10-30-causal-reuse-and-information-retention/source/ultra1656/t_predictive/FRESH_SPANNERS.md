# Fresh-only robust distributional spanners, without child coverage

Proof reconstruction and specialization of Liu--Moitra Sections5--6. The new use
is that only these fresh rows enter the projection's FIRST argument/measure.
The children never enter this acquisition lemma. P samples and Q conditionals
remain distinct resources throughout.

Fix a cut. Let p_h=P(future|h), q_h=Q(future|h), and let the p_h lie in a linear
space of dimension<=r. Choose N independent full-trajectory P samples and retain
their cut prefixes h_i. Suppose (on an event paid below) ALL their rows satisfy

    ||p_(h_i)-q_(h_i)||1<=eta.                         (1)

## 1. Population coverage by some sampled true rows

An exact barycentric spanner of N vectors in an r-space can be selected among
them with at most r elements and coefficient bound1. With high probability it
can also cover1-gamma0 population mass. A direct sample-compression proof avoids
an independence mistake with data-dependent bases: fix an index subset I of at
most r, condition on its row values, and let K_I be its symmetric parallelotope.
If P(p_h in K_I)<1-gamma0, the chance that all OTHER N-|I| independent samples
are in it is at most exp[-gamma0(N-r)]. Union over at most(r+1)N^r subsets.
Thus whenever

    (r+1)N^r exp[-gamma0(N-r)]<=p_fail,                (2)

every sample-containing parallelotope covers the required mass. The hidden
max-volume true-row basis is used ONLY as an existence witness. It is not queried
or computed by the learner. Lemma5.4 of the predecessor supplies the same ordinary
distribution-spanner operation; the conditioning above makes its union bound literal.

## 2. Computable finite row sketch

Set mu_geo=(U+sum_i q_(h_i))/(N+1). Draw M independent futures from mu_geo and
evaluate every q_i on them. The uniform row is part of the MEASURE, not an extra
column in the rank test. Consequently mu_geo>=1/((N+1)O^L), which pays finite
absolute probability precision. Columns

    u_i(j)=q_i(f_j)/(M mu_geo(f_j))

have coordinates<= (N+1)/M and bounded norm. The unknown true columns
v_i(j)=p_i(f_j)/(M mu_geo(f_j)) have rank<=r. Under(1), Markov and a union bound
give, with probability>=1-N M eta/theta,

    |p_i(f_j)-q_i(f_j)|/mu_geo(f_j)<=theta   for all i,j.

Then ||u_i-v_i||2<=theta/sqrt(M) and the singular values beyond r are at most
sqrt(N)theta/sqrt(M). Truncate at a threshold between2 and4 times this quantity,
and compute a2-barycentric spanner of the retained coordinates. Each original
column is approximated by the selected <=r columns with coefficients<=2 and
L1 sketch residual at most4(1+2r)sqrt(N)theta. Choose

    theta=zeta/[100(r+1)N].                          (3)

The residual is then below zeta/10. A threshold gap can be chosen among r+1
candidate levels in that interval; no supplied spectral gap or inverse singular
value is used. The retained singular values are bounded below by the chosen
threshold, so the ordinary volume-doubling algorithm has polynomial logarithmic
conditioning cost. This is precisely the robust truncation purpose of LM5.6.

Separately, uniform Hoeffding/net concentration for coefficients in[-4,4]^N gives
L1 norm preservation within zeta/10. The envelope is4N(N+1) and a coefficient
net has logarithmic size O(N log(N/zeta)). Thus a sufficiently large fixed
polynomial M in N,1/zeta,log(1/p_fail) suffices. The explicit resource schedule
below takes a much larger M, rather than suppressing this cost.

Hence every sampled q_i is within zeta/2 in FULL L1 of a bounded combination of
the selected teacher rows. Every sampled p_i is within eta+zeta/2. Combining with
the hidden population spanner in Section1 shows that, except on gamma0 P-mass,
p_h is within r(eta+zeta/2)<=r zeta of a combination of selected q_i, with each
coefficient bounded by2r. No query to p_h was used in construction.

## 3. Normalize and acquire feature-positive proxies

The approximate combination has mass s within r zeta of1. If r zeta<=1/4,
divide its coefficients by s: each is bounded by3r, its mass is exactly1, and
its L1 error is at most4r zeta. Append the uniform row and define
mu=(sum selected q_i+U)/S as in ASYMMETRIC_OPERATION. Pad the normalized proxy
towards mu with weight4tau. Its coefficient bound is below C=8(r+1), its mass
is1, and its target error is at most4r zeta+8tau.

If the unpadded proxy is>=-tau mu at a feature, the padded one is>=tau mu there.
The probability under mu of violating the former inequality is <=4r zeta/tau.
For D fresh projection features, the expected P-mass of histories without a
feature-positive proxy is at most

    gamma0+4 D r zeta/tau.                           (4)

Markov over the INDEPENDENT fresh feature set pays a high-probability population
bad-mass bound. The coefficient state encountered during generation may depend on
all the features: uniform gradient/negative-part bounds handle that dependence.
The proxy condition is evaluated under P's prefix law in the KL telescope, so it
does not incur selected-child sampling bias. There is no N_previous recursion.

## 4. Paying(1) from the stated global teacher promise

Chain rule and Pinsker give at every cut

    P_(h~P[:t]) {||p_h-q_h||1>eta} <=2Delta/eta².

For T independent fresh batches of N prefixes, all their raw rows satisfy(1)
except with probability at most2 T N Delta/eta². This is the ONLY target/teacher
conditional localization used. Queried propagated children need not be close at
all; their effect is paid by the asymmetric logarithm and exact restriction rule.

## 5. Explicit conservative polynomial resource schedule

Let confidence delta in(0,1/4), r>=1,O>=2,T>=1 and choose0<tau<=1/(100A), where
A=ceil[1000(r+O+T+1/delta)]. Put x=A/tau and d'=delta/(100T). At every cut use

    C=8(r+1), b=tau/O, a=b/2, theta_floor=tau/[4(r+1)],
    D=ceil(x^40), v=a tau, xi=tau,
    gamma0=d' tau/100,
    zeta=d' tau²/[100 D(r+1)],
    N=ceil(x^60), M=ceil[(A N/zeta)^10],
    theta_geo=zeta/[100(r+1)N],
    eta=min{zeta/[100(r+1)], theta_geo d'/[100 N M]}.

The displayed conservative exponents are not practical complexity claims. They
are finite constants, independent of T,r, and remove unspecified polynomial gates.
Standard nets above have strictly smaller polynomial bounds: D pays both fresh
sketch events, N pays(2), M pays full-L1 representation, and eta pays the
pointwise row-sketch perturbation. All good-row/sketch/population failure bounds
sum to less than delta after union over cuts, provided

    Delta <= d' eta²/[100 T N].                       (5)

One coarse simplification is eta>=x^(-1400), d'>=x^(-2), N<=x^61 and M<=x^1200.
Thus Delta<=x^(-4096) suffices for(5). Detailed exponent/constant checks and the
finite precision implementation still need a separate receiver before treating
this simplification as a final central theorem. No finite diagnostic substitutes
for those general bounds.

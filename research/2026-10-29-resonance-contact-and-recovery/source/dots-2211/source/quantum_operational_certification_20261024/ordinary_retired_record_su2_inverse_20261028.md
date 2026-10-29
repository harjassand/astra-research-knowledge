# Ordinary acquisition of a noncommuting qubit inverse with retired-record complete error

28 October 2026. New candidate construction; independent review pending. The finite implementation below closes the continuous-Haar design obligation rather than assuming analog random controls for free. This is not a general unknown-channel decoder or unknown-code theorem.

## 1. Source and operational contract

Calibration uses independent starts of the physical qubit channel Ad_U composed with the isotropic depolarizing map rho->a rho+(1-a)I/2, where U is an arbitrary unknown fixed qubit unitary and 0<a<=1. Equivalently Bloch vectors transform by a R, R in SO(3). A supplied or separately acquired lower bound a0>0 is needed to choose a certified requested-accuracy horizon; the estimator itself does not use a. This draft does not construct unknown-a automatic stopping.

After calibration, the same U may follow ANY joint service map A:P M->P M', including coherent retained error amplitudes. The service memory/input is independent of the training records conditional on U,a. The private decoder controller may use its acquired program, but all calibration records, random design labels and program registers are inaccessible to the service source and external controller. The claim is about the record-AVERAGED decoder channel, so it does not contradict the retained-record lower bound. Calibration-correlated continuing memory is excluded.

The capability is learning an inverse for all three noncommuting qubit directions without reconstructing the environment, with O(a^-2/epsilon) ordinary source calls for one-use complete error, at explicit structural and information-interface cost. Conventional rotation estimation is the algorithmic baseline, not a claimed new estimation primitive.

## 2. Ideal rotationally covariant experiment and actual estimator

For analysis first draw independent uniform unit Bloch vectors u,v on the two-sphere. Prepare rho_u=(I+u.sigma)/2, measure v.sigma, and retain Y in {-1,+1}. Its mean is a v^T R u. For N>=3 independent records set

 C=(1/N)sum_t Y_t v_t u_t^T, M=9C/a.

Only C is used by the learner. Choose Rhat in SO(3) minimizing ||C-S||_F. Positive scalar rescaling leaves the minimizer unchanged, so M is only an analysis normalization. The decoder implements a qubit unitary with Bloch rotation Rhat^T.

Independent sphere second moments E uu^T=E vv^T=I/3 give

 E M=R,
 E||M-R||_F^2=(81/a^2-3)/N=:v_a/N.                         (1)

Nearest-rotation optimality gives ||Rhat-R||_F<=2||M-R||_F, hence

 E b_U <= v_a/(2N),
 b_U=(3-Tr(Rhat^T R))/4=||Rhat-R||_F^2/8.                  (2)

This fits a proper rotation, not an unconstrained reflection. On exceptional nonunique fits use any measurable selection; for the continuous design N>=3 the exceptions have measure zero. Alternatively one may randomize over minimizing rotations with an invariant rule. For the finite implemented estimator below arbitrary deterministic algebraic tie handling is allowed; its comparison uses a unique well-conditioned polar region and explicitly pays the complement.

Under u->B u, v->A v, the design law is invariant, R->A R B^T, and C->A C B^T. Away from the null exceptional set the fitted rotation has the same equivariance. Therefore the distribution of Rhat^T R is invariant under conjugation by SO(3). Its average is lambda I. The record-retired averaged inverse error channel is exactly

 E[Ad_Uhatdagger composed Ad_U]
   =(1-b) id+(b/3)(Ad_X+Ad_Y+Ad_Z),
 b=E b_U<=min(1,v_a/(2N)).                                 (3)

The half-diamond distance from identity is b (the Bell outputs of the four Paulis are orthogonal). Composition after any independent complete joint service map A preserves this bound, irrespective of its coherent memory. It is important that averaging the private decoder is legitimate BEFORE its action on the independent service; (3) is not inferred from a reduced Pauli model of A.

## 3. A finite algebraic approximation to the random design

Here is a fully finite design with an explicit bias budget. Let 0<h<=min(1,a0/(100N^2)). Uniform sphere coordinates are z uniform[-1,1] and phi uniform[0,2pi). Couple them to finite midpoint grids:

 - Choose z' uniformly among M_z equal interval midpoints, with M_z a power of two >=128/h^2.
 - Choose phi'=2pi(l+1/2)/K uniformly, with K a power of two >=(88/7)/h.
 - Set u'=(sqrt(1-z'^2)cos phi',sqrt(1-z'^2)sin phi',z'); similarly v' independently.

The midpoint coupling has |z-z'|<=1/M_z<=h^2/128 and |phi-phi'|<=pi/K<=h/4. Since |sqrt(1-z^2)-sqrt(1-z'^2)|<=sqrt(2|z-z'|), it gives ||u-u'||_2<=h, and likewise for v. Every prepared vector and measurement direction is algebraic. Exact finite uniform integers require O(log(1/h)) bits per sphere vector, with no unbounded rejection loop.

Use the ACTUAL finite-grid records to form C'=(1/N)sum Y'_t v'_t u'_t^T and choose a nearest proper rotation Rhat'. The physical estimator requires neither the ideal real vectors nor a. It has finite data and algebraic entries. Exact real-algebraic singular/eigenvalue isolation and sign decisions provide a terminating proper-rotation minimizer, including degeneracies. The algebraic degree/bit cost can be large and is not claimed polynomial in log N here.

## 4. Complete error transfer from the ideal experiment

Couple the ideal/finite labels as above. Their conditional binary outcome laws differ in TV by at most a h<=h per probe; maximally couple outcomes. The chance any Y differs is <=N h. If every outcome matches, then

 ||M'-M||_F <=18h/a=:e,

where M'=9C'/a is again only for analysis. Our choice h<=a0/(100N^2)<=a/(100N^2) gives e<=.18/N^2<1/4.

Let G be the event ||M-R||_F<=1/4 in the ideal experiment. Markov gives P(G^c)<=min(1,16v_a/N). On G, M has smallest singular value >=3/4 and positive determinant. M' has smallest singular value >=1/2 and positive determinant. Both nearest proper rotations are their unique polar factors. The polar perturbation estimate

 ||polar(M')-polar(M)||_F
 <= [2/(sigma_min(M')+sigma_min(M))] ||M'-M||_F <=2e

has a direct proof. Write M=QH and M'=Q'H' with H,H' positive. The two optimality gaps satisfy Tr(Q^T M)-Tr(Q'^T M)>=sigma_min(M)||Q-Q'||_F^2/2 and the exchanged inequality for M'. Indeed I-(Q^T Q'+Q'^T Q)/2 is positive semidefinite and has trace ||Q-Q'||_F^2/2. Adding the gaps gives Tr((Q'-Q)^T(M'-M)), bounded by ||Q-Q'||_F ||M'-M||_F, which proves the displayed estimate after division. Thus no unproved stability oracle is needed. For qubit unitary channels, half diamond distance is ||Rhat'-Rhat||_F/(2sqrt(2)), at most e.

Thus coupling the actual decoder channel and the ideal channel, paying bad records by their full mass, yields

 half ||E[Ad_Uhatprime_dagger Ad_U]-id||diamond
 <= min(1, (33/2)v_a/N + N h +18h/a).                       (4)

In particular h=a0/(100N^2) gives an explicit O(a^-2/N) bound, although the constants are loose. This proof avoids falsely assuming finite grids are exactly Haar covariant. It pays their actual effect on the measurement records and on the fitted inverse. It also does not make record-wise posterior claims or guarantee every fitted inverse is close; poor fits remain physical and their probability is paid.

## 5. Preparation, implementation and scope

The finite vectors specify actual qubit preparations and binary measurements. A proper algebraic rotation lifts to an algebraic SU(2) matrix up to physically irrelevant global sign. The received finite endpoint compiler supplies a route from a known finite algebraic channel/isometry to approximate physical gates; its assumptions, expanded gate-output cost and independent review remain separate dependencies. Alternatively any certified one-qubit synthesis may implement these known matrices. No unknown U gate or environment access is requested.

A complete preparation/readout/synthesis budget nu adds to (4) by a whole-protocol hybrid: a sufficient per-probe discrepancy is O(nu/N), plus O(nu) for the deployed inverse. Finite arithmetic precision and sign isolation are charged, not replaced by floating SVD as proof. Exact Haar draws and infinitely precise analog controls are NOT part of the implemented protocol.

This extends the record-retirement principle from an Abelian phase to an arbitrary noncommuting SU(2) mixer within an isotropic calibration family. It does not learn arbitrary anisotropic noise, guarantee independence from an unreset environment, or establish efficient many-qubit scaling. Reuse of the same random program requires a new analysis; a single-use depolarizing average does not make different service slots independent. Historical novelty and practical advantage over equally informed conventional methods remain unestablished.

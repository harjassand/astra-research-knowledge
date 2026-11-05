# A finite robust planner from the acquired step table

## Contract

The input is the acquired rational, piecewise-linear step table S_hat on [0,T], anchored by S_hat(0)=0 and extended by zero to negative lags. The calibration event supplies ||S-S_hat||infinity<=eta_S. A separately paid readiness operation supplies a measured baseline b and a uniform free-response/baseline error eta_0 for the entire allocated deployment window. A drive-delivery and meter-backaction allowance eta_d is also supplied. On that one event, every admitted input of total variation at most V obeys

\[
\|x-\widehat x\|_{\infty,[0,T]}
\le\epsilon_*:=\eta_0+V\eta_S+\eta_d.
\tag{1}
\]

The same event holds for every coefficient vector below. Coefficients may therefore be selected after calibration. Equation (1) is an input contract earned by the preceding physical construction, not a fresh inference from the proposed optimizer or its sampled output.

## 1. A physically finite control family

Let

\[
\phi(s)=\begin{cases}
0,&s\le0,\\10s^3-15s^4+6s^5,&0<s<1,\\1,&s\ge1.
\end{cases}
\]

Choose rational starts 0<=t1<...<tJ and a rational ramp h>0 with tj+h<=t(j+1) and tJ+h<=T. Use

\[
f_c(t)=\sum_{j=1}^J c_j\phi((t-t_j)/h).
\tag{2}
\]

This input starts at zero and is C2. The ramps do not overlap. If F_j=sum_{i<=j}c_i, then the following finite constraints are sufficient, and the first two are exact characterizations of the associated amplitude/variation restrictions:

\[
-F\le F_j\le F,\qquad \sum_j|c_j|\le V,
\tag{3}
\]

\[
\|f_c'\|_\infty={15\over8h}\max_j|c_j|,
\qquad
\|f_c''\|_\infty={10\sqrt3\over3h^2}\max_j|c_j|
\le{6\over h^2}\max_j|c_j|.
\tag{4}
\]

The prefix bounds hold throughout each ramp because phi is monotone from zero to one. Variation adds exactly because each individual ramp is monotone and only one changes at a time. The derivatives vanish through order two at the endpoints, so splicing introduces no instantaneous velocity or acceleration change.

For the permanent trap k>0, center q=f_c/k. Thus center travel is TV(f_c)/k, center speed is bounded by 15 max|c_j|/(8kh), and center acceleration by 6 max|c_j|/(kh^2). These become linear bounds on each signed coefficient c_j. Known jerk bounds can also be imposed using 60 max|c_j|/(kh^3). Requiring sum c_j=0 gives a finite return to zero input within the program. Otherwise a separately charged return must precede a later unforced readiness operation.

A finite coefficient encoding and finite polynomial command clock implement (2). Force-gain, position-tracking and clock errors must fit the supplied eta_d; exact rational coefficients do not remove those physical errors. The actual trap force is k(q-x), so its cap additionally uses the acquired energy bound on x. With H_start<=E and |f|<=F, H<=E+F^2T/(4gamma), and hence |x|<=sqrt(2[E+F^2T/(4gamma)]/k). A conservative trap-force cap is F+k|x|_max; moving-center absolute work is at most this cap times V/k. These are explicit hardware costs of the planned program.

More explicitly, encode each coefficient to p binary fractional bits, with coefficient error at most 2^(-p). If each ramp start and duration has error at most delta_t and h_min=h-delta_t>0, its normalized argument changes by at most 2 delta_t/h_min where the ramps can differ. The force discrepancy from coefficient and timing encoding is therefore at most J 2^(-p)+(15/4) V delta_t/h_min, before gain and tracking errors. A fixed finite accuracy chooses p and delta_t so that this plus those calibrated errors is at most the permitted force discrepancy; its trajectory contribution is bounded by the established L2 force-error inequality. A finite polynomial-command controller requires only the stored starts, durations and coefficients and a fixed number of arithmetic operations per command evaluation. The hardware must enforce slew and acceleration caps with margin for encoding, clock, gain and servo errors; a position-error bound alone does not imply derivative-error bounds. The bounds (4) are the nominal command demands, which determine those finite hardware margins. Reliable classical memory, clock and arithmetic require their own supplied fault budget and protection cost, exactly as in the acquisition contract.

## 2. Exact linear prediction coefficients

Let rho_h(s)=phi'(s/h)/h on [0,h]. The acquired prediction is

\[
\widehat x_c(t)=b+\sum_j A_j(t)c_j,
\qquad
A_j(t)=\int_0^h\rho_h(s)\widehat S(t-t_j-s)\,ds.
\tag{5}
\]

All grid coefficients A_j(t_l) are rational when the table, starts, h and planning times are rational. On each table segment S_hat(u)=m_i u+a_i, the integral is an integral of a polynomial of degree at most five over rational limits. Thus it is computed with additions, multiplications and divisions of integers; no ODE solver or unknown-plant evaluation is invoked.

For efficient coefficient construction, precompute the five prefix moments

\[
M_r(z)=\int_0^z u^r\widehat S(u)du,\quad 0\le r\le4.
\]

Since rho_h(s)=30s^2/h^3-60s^3/h^4+30s^4/h^5, binomial expansion evaluates each coefficient from M_r at two clipped endpoints. This costs O(M) preprocessing for M table intervals, then O(log M) table search and a fixed number of rational operations per coefficient. A direct segmentwise integration supplies an independent exact check. The complete response path is piecewise polynomial of degree at most six, with breakpoints among t_j+tau_i and t_j+h+tau_i, where tau_i are table knots.

Let

\[
L_S=\max_i\left|{S_{i+1}-S_i\over\tau_{i+1}-\tau_i}\right|.
\tag{6}
\]

The anchored extension is globally Lipschitz with constant L_S on all required lags. Positivity and normalization of rho_h imply Lip(A_j)<=L_S, so

\[
\operatorname{Lip}(\widehat x_c)\le V L_S.
\tag{7}
\]

This is the actually acquired table's Lipschitz constant; the planner does not substitute an unobserved smoothness constant.

## 3. Whole-trajectory safety from a finite LP

Let 0=t0<...<tP=T be a rational planning grid, with fill distance Delta=max_l(t(l+1)-t_l)/2. For constant desired safety bounds L<=x(t)<=U, impose

\[
L+\epsilon_*+VL_S\Delta
\le b+\sum_j A_j(t_l)c_j
\le U-\epsilon_*-VL_S\Delta
\quad\text{for every }l.
\tag{8}
\]

For any time t choose a nearest planning node. Equation (7) bounds the surrogate motion to that node and (1) bounds the true-to-surrogate error. Therefore (8) proves the full continuous-time physical safety band, including between nodes. Time-dependent safety bounds with Lipschitz constants L_lower,L_upper require the corresponding additional L_bound Delta margins.

Introduce v_j>=0, -v_j<=c_j<=v_j, sum v_j<=V. Add (3), individual coefficient derivative/acceleration caps, and (8). These are finitely many rational linear inequalities. The target maximize x(T) is the linear objective maximize sum A_j(T)c_j; b is an irrelevant objective constant. Weighted absolute tracking objectives can be expressed with further epigraph variables. Quadratic tracking gives a convex quadratic programme, but the delivered implementation below uses a linear objective.

If the tightened polytope is empty, it means that this basis and these sufficient margins contain no certified plan. It does not establish that the unknown plant lacks every possible safe input.

## 4. Finite optimization, bit cost and certificates

Let n be the number of LP variables, m the number of inequalities, and L_bit bound the numerator/denominator bit lengths of its rational coefficients. These are finite functions of the table encoding, planning grid, physical budgets and basis. Exact prefix integration makes their construction explicit. With arbitrary independent denominators in the input table, a conservative coefficient bit bound grows linearly in M times the input bit length; a common dyadic grid usually yields much smaller actual encodings.

There are standard exact LP algorithms polynomial in (m,n,L_bit). A simple fully explicit fallback is vertex enumeration: for every n-row subset of the bounded polytope, solve its rational equality system, retain solutions satisfying all inequalities, and choose the smallest objective. A nonempty bounded rational polytope has a vertex. Thus this is a finite algorithm with at most binomial(m,n) systems, each requiring polynomial rational linear-algebra and verification work. Clearing denominators and determinant bounds give a conservative vertex encoding of O(n^2 L_bit+n log n) bits per coordinate. This fallback is expensive and is not advertised as polynomial.

The executed planner may use a floating LP as a proposal. It reconstructs an active vertex in exact rational arithmetic and checks every original inequality. It then constructs an exact feasible dual, so acceptance and the final optimization gap do not depend on trusting floating feasibility or optimality reports.

For minimization d^Tz subject to Az<=b, include explicit finite box bounds l_i<=z_i<=u_i among the rows. Round proposed multipliers to nonnegative rationals lambda. Let r=d+A^Tlambda. If r_i>0, add multiplier r_i to the lower-bound row -z_i<=-l_i. If r_i<0, add -r_i to the upper-bound row z_i<=u_i. This gives lambda'>=0 and

\[
d+A^T\lambda'=0.
\tag{9}
\]

The exact primal and dual certificates are therefore

\[
Az_*\le b,\qquad\lambda'\ge0,\qquad
d+A^T\lambda'=0,
\]

\[
0\le d^Tz_*+b^T\lambda'\le\epsilon_{\rm opt}.
\tag{10}
\]

All comparisons can be checked with integers. A verifier can reconstruct the coefficients directly from the acquired table, independently of the prefix-moment implementation, then verify (10). If a proposed vertex fails exact checking, it is rejected or the finite fallback is used.

Classical memory, coefficient construction, LP search and verification are paid operations. The low dimension of a physical port does not make a general optimization problem free. The delivered small programme reports its actual matrix dimensions, coefficient bit sizes, arithmetic checks, run time and exact primal-dual gap.

## 5. Quantifiers, objective guarantee and timing

For the fixed admissible polytope, the one calibration/readiness event supplies (1) for every coefficient vector. The optimizer's dependence on acquired data therefore creates no additional union bound. For a path objective J with sup-norm Lipschitz constant L_J, an epsilon_opt-optimal surrogate plan is within

\[
2L_J\epsilon_*+\epsilon_{\rm opt}
\tag{11}
\]

of the best true objective over that same polytope. This does not compare with every physically feasible control outside the basis or outside the robust tightening. Endpoint maximization has L_J=1.

If optimization depends on the fresh readiness baseline, reserve a finite planning latency inside the randomized readiness window. During that latency the input remains zero, and its duration enters the window length and waiting bound. A measured computer run time is evidence of one execution, not a worst-case latency proof. A guaranteed implementation budgets the finite work bound against its certified hardware clock and memory reliability. Alternatively precompute a plan, or a finite parametric family of plans, before the fresh readiness draw. A counterfactual planner run on a saved readiness record does not constitute a second actual physical deployment.

The delivered planner also constructs a concrete parametric region. For its selected independent active rows B, write the LP right side as b0+b1 times the unknown baseline beta. Solve B z0=b0_B and B z1=b1_B exactly. Then z(beta)=z0+beta z1 is affine. Each inequality becomes one linear bound on beta; their intersection is an exact rational interval. The same dual certificate remains feasible because A and the objective do not depend on beta. Its gap is affine and can be checked at both interval endpoints. On a zero-gap region this is an optimal plan for every baseline in that interval. After a fresh readiness readout, only an interval check and finitely many rational multiply-adds are needed. Outside the stored interval this one-region implementation abstains; a finite collection of all feasible basis regions can be precomputed at the charged vertex-enumeration cost. The confidence remains the original unconditional physical event, not a stronger conditional-on-acceptance probability.

## 6. Exactly what approximation to a larger force class is proved

The main guarantee is optimality within the declared quintic basis. There is a conditional approximation result. Let a target f satisfy f(0)=0, |f|<=F, TV(f)<=V, and a time-Lipschitz bound L_f. On a uniform grid of width Delta choose increments c_j=f(t(j+1))-f(t_j) and use a full-width quintic ramp in each interval. Convexity of each interpolation gives

\[
\|f-f_c\|_\infty\le L_f\Delta,
\quad\|f_c\|_\infty\le F,
\quad\operatorname{TV}(f_c)\le V.
\tag{12}
\]

Its slope is at most (15/8)L_f and acceleration at most 6L_f/Delta. By the physical force-error energy bound, its output differs by at most

\[
L_f\Delta\sqrt{T/(2\gamma\kappa)}.
\tag{13}
\]

Thus approximation to this larger class is earned only when those actual slew/acceleration caps are available, and when any safety margins survive (13). At fixed acceleration cap, these particular zero-slope-at-every-knot quintic programmes need not be dense as Delta shrinks. No fixed-hardware universal approximation or global optimality claim is inferred.

## 7. Executed acquired-table planner

The delivered constructor reads `../bridge/acquired_step_response.json` (SHA256 `c1527bb91029dd3141a1b3583d4e8cd82c7f50b4b30473ed05ff37f16ad421ce`) and no microscopic source. It uses 100 acquired table intervals, five possible ramps starting at 0, 1/5, 2/5, 3/5 and 4/5, ramp duration 1/20, per-increment cap 2/5, force and variation caps 1, and 64 uniform planning intervals. The safety band [-3/10,3/10] was chosen after inspecting the acquired table to exercise a binding safety constraint; it was not used to generate or select the table.

The physical error radius uniformly valid over every candidate of variation at most 1 is 0.09692661. The acquired table Lipschitz constant is 0.5390167236328125, giving intergrid radius 0.004211068153381347 and total grid tightening 0.10113767815338134. The LP has 10 variables and 171 inequalities. Its exact primal-dual gap is zero. The attained predicted endpoint is 0.19886232184661864, saturating the upper tightened endpoint constraint. These numbers imply physical safety throughout [0,1] on the same acquisition/readiness/delivery event; no event is selected anew after optimization.

The exact nonzero force increments are

\[
c_0={393985013027\over1045129658000},\qquad c_1={2\over5}.
\]

The remaining three increments vanish. Their total variation is 812036876227/1045129658000. The selected programme's sharper physical error, using that actual variation, is 0.08438833166123201, yielding endpoint interval [0.11447399018538665,0.28325065350785067]. This sharpening is legal because the original bound holds simultaneously for all coefficients through the deterministic TV inequality.

At trap stiffness 1, center speed is at most 15 and center acceleration is at most the rational bound 960. Center travel is the displayed variation. After the prediction horizon, two extra quintic ramps of duration 1/20 each return the force to zero. Those return ramps add the same amount of center travel and 1/10 time; the [0,1] safety claim does not extend to this unforecast return. Its energy injection and tracking errors must be paid before another readiness experiment.

The constructor's one measured execution required about 0.054 seconds for coefficient construction, proposal, exact reconstruction and certification; this is not a hard realtime guarantee. The independent verifier used direct segmentwise polynomial integration for all 325 response coefficients, checked all 171 inequalities, all 10 dual equations, all 171 nonnegative dual multipliers, and exact zero gap. Maximum constraint coefficient payload was 106 bits; reported primal and dual maximum integer payloads were 174 and 172 bits. One active-basis system sufficed. The explicit fallback worst-case enumeration bound is 4,505,395,859,893,071 basis systems, which is finite but intentionally not represented as practical. A standard polynomial rational LP implementation can replace this fallback without changing the physical theorem.

The complete selected prediction has 100 rational polynomial segments of degree at most six. A separate verifier checked 700 exact identity points using 7,350 exact degree-five quadrature boxes, checked every partition point and continuity, and checked the physical-error composition. The optimization certificate hash is `58a584ef631bf7e079f28084646747d9c533ded2425be271d87fd373ccdd4b56`; the path hash is `1a273bd6ba9341b4615696d2bf146a2bd339924b15e4374417b9c95b6dcb4dba`.

### Finite online plan without a fresh LP

The exact active-basis certificate also supplies a precomputed baseline interval

\[
\beta\in\left[
-{53841850173\over3276800000000},
{364210013027\over3276800000000}
\right]
=[-0.016431228690490723,\;0.1111480752645874].
\]

Throughout this interval an optimal certified programme is

\[
c_0(\beta)={364210013027\over1045129658000}
-{1638400000\over522564829}\beta,
\qquad c_1(\beta)=2/5,
\qquad c_2=c_3=c_4=0.
\]

All 171 primal inequalities were checked at both interval endpoints, hence throughout the interval; the same dual is feasible and the affine duality gap is identically zero. A new readiness baseline inside this interval therefore needs no online optimization: two interval comparisons and one nontrivial rational multiply-add suffice for the two nonzero coefficients. The generic saved ten-variable representation uses at most ten rational multiplications and ten additions. The exact arithmetic's bit length depends polynomially on the fresh baseline encoding and the displayed constants. The controller must reserve its certified execution/communication latency; a fast-looking formula does not make delay zero. Outside the interval this single-region controller abstains, with no assertion of physical infeasibility and no conditional-on-acceptance improvement of confidence.

There is an especially explicit integer implementation. Write the fresh finite report as beta=a/q, q>0. Compute R=3276800000000*a, P=364210013027*q, L=-53841850173*q, and D=1045129658000*q. Accept only if L<=R<=P, and set c0=(P-R)/D. No rational reduction is required. Thus the exact online core is four products of a report integer with a fixed integer of at most 42 bits, one subtraction and two comparisons; c1=2/5 is already stored. If a and q have at most B bits, the intermediates require at most B+43 bits. Rounding the coefficient to p fractional bits adds one shift and one integer division on at most B+43+p bits. Schoolbook arithmetic gives O((B+p+43)^2) bit work and O(B+p+43) working bits, or the measured certified bound of a chosen processor. Its worst-case arithmetic time plus sensor-transfer and actuator-load time must fit the explicitly reserved postread latency; otherwise increase that latency and recompute readiness. None of the measured offline LP timings is substituted for this finite bound.

This execution is counterfactual optimization using the already recorded readiness baseline. It is not a second physical deployment. The region construction can be completed before a future private readiness draw, after which the online arithmetic and command delivery fit a declared latency budget. Source-simulation accuracy, the physical premises and metrology confidence remain the acquired-table contract. No microscopic realization, initial mode state, actual repeated specimen or hidden-model simulator enters the planner.

## 8. Comparison with established control constructions

Step-response-based prediction and finite control optimization are established machinery: Cutler and Ramaker's Dynamic Matrix Control uses numerical response coefficients and linear superposition to form predictions and optimize control moves. Explicit parametric optimization is likewise established; Bemporad, Morari, Dua and Pistikopoulos derive piecewise affine explicit constrained controllers, replacing online optimization with evaluation. The active-basis interval above is a particularly small exact instance of that method. Quintic smooth ramps, LP dual certificates and robust constraint tightening are also ordinary tools.

The present consequence is therefore not a new general MPC algorithm or new parametric-LP principle. It is the complete finite implementation from this programme's acquired response contract: the same finite measurement event supports data-dependent optimization over a whole physical input class, finite continuous-time path safety, known actuator slew and acceleration, exact independently verifiable numerical optimization, and a precomputed online interface. The unusual premise is the supplied acquisition/readiness theorem for unknown passive environments with retained initial state, not hidden state access supplied to the planner. Closed-loop recursive feasibility, infinite-horizon safety and optimality over all possible physical controls are not claimed.

Primary comparisons:

- C. R. Cutler and B. L. Ramaker, *Dynamic Matrix Control—A Computer Control Algorithm*, Joint Automatic Control Conference (1980), paper WP5-B. [Original paper](https://skoge.folk.ntnu.no/puublications_others/1980_Cutler-Ramaker_Dynamic-matrix-control_JACC1980.pdf).
- A. Bemporad, M. Morari, V. Dua and E. N. Pistikopoulos, *The explicit linear quadratic regulator for constrained systems*, Automatica 38 (2002), 3–20. [Authors' institutional record](https://old.control.ee.ethz.ch/publications/2002/12.html), [DOI](https://doi.org/10.1016/S0005-1098(01)00174-1).

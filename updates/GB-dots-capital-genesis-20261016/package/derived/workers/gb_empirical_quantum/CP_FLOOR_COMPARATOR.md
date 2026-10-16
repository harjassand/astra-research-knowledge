# A paid exact ideal-branch compiler and its targeted comparator

Status: internally derived isolated-channel calculation with floating-point Choi checks. No historical novelty, shared-bath qualification or physical implementation is claimed.

## 1. Restricted input/output contract

Let `D(rho)=P0 rho P0+P1 rho P1` be exact unread qubit Z pinching. Consider the specified bath-independent implementation

`E_theta = Ad_(exp(-i theta X)) composed with D`.

The source CP-coin obstruction shows that, for nontrivial small theta, no positive w makes `E_theta-wD` completely positive. Small channel error therefore does not establish a nonzero exact ideal branch. This is an exact Choi-support obstruction, distinct from average readout error or fidelity.

Test a deliberate operation: after E_theta, apply an independent replacement by the completely depolarizing channel `T(rho)=Tr(rho)I/2` with probability eta. Its resulting channel is

`E_theta,eta=(1-eta)E_theta+eta T`.

Replacement is a real paid modification, not an inferred native floor. This memo asks for the largest w such that

`E_theta,eta = w D + (1-w) F`

for some CPTP F. It does not assume that the physical laboratory uses this unraveling. Within this isolated memory-only channel contract, equality of CP maps supplies an equivalent fresh-coin representation on arbitrary reference-entangled inputs. That conclusion does not transfer to a channel's unspecified persistent environment, recorded measurement instrument or feedback controller.

## 2. Exact maximum ideal weight

Use the unnormalized Choi convention. In each of the two orthogonal input blocks, `J(E_theta,eta)` has the form

`A=(1-eta)|u><u|+(eta/2) I`,

where u is the rotated computational-basis output and the corresponding ideal block is `|e><e|`. For `0<eta<=1`, A is positive definite. A rank-one subtraction is positive semidefinite exactly when

`w <= 1/<e|A^-1|e>`.

Both blocks give the same condition. Set `s=|sin theta|`, `c=|cos theta|`. The eigenvalues of A along u and its orthogonal direction are `1-eta/2` and `eta/2`. Therefore

`w_max(theta,eta)=eta(2-eta)/(2[eta+2(1-eta)s^2])`.

Complete positivity of the difference is sufficient: both original maps preserve trace, so its trace is `(1-w)Tr(rho)`, and dividing by `1-w` gives a CPTP F. At theta zero and eta zero, w=1. At eta zero with `s!=0`, the original support obstruction gives w=0. At eta one, w=1/2.

`cp_floor_tests.py` directly assembles the 4x4 Choi matrices at 35 nondegenerate (theta,eta) points. At the formula's boundary their least eigenvalues vanish to numerical tolerance; increasing w by `10^-6` makes them negative. These numerical checks corroborate the analytic rank-one argument; they are not its proof.

## 3. Optimizing the paid replacement probability

For `0<|theta|<=pi/4`, differentiation gives

`eta_star=2s/(c+s)`, `w_star=1/(c+s)^2`.

For `pi/4<=|theta|<=pi/2`, the maximum over `0<=eta<=1` is achieved at eta=1 with w=1/2. One way to check the stationary point is to write `a=s^2`; the derivative numerator is proportional to

`4a(1-eta)-(1-2a)eta^2`.

Its root in the small-angle regime is eta_star. The endpoints and derivative sign give the global optimum on the interval. As theta tends to zero, `eta_star=2|theta|+O(theta^2)` and `1-w_star=2|theta|+O(theta^2)`. The price of forcing an exact ideal branch this way is linear in the small coherent angle, despite the ordinary basis-state error being quadratic.

For illustration only, theta=0.01 gives eta_star about 0.019803 and ideal weight about 0.980393. These numbers are model parameters, not device calibrations.

## 4. Established targeted randomization defeats this candidate in its own scope

Assume an additional ideal, physically effective, independently sampled output I/Z operation. Averaging its two branches gives output pinching:

`(Id+Ad_Z)E_theta/2 = D E_theta`

`= c^2 D + s^2 Ad_X D`.

The two components have orthogonal Choi supports, so the largest exact ideal-pinching weight is c^2. Its fault weight is `sin^2 theta`, quadratic at small angle. For `0<=|theta|<=pi/4`, `c^2 >= 1/(c+s)^2`, since `c(c+s)>=1` is equivalent to `c>=s`. At theta=0.01 the targeted ideal weight is about 0.999900, substantially above the uniform replacement optimum at the same angle.

This is an exact channel comparator, not a same-resource hardware verdict: output randomization and replacement have different physical implementations and no measured costs here. It blocks an operation-family novelty claim or a claim that uniform depolarization is an inherently efficient solution. The targeted family is established measurement noise tailoring. Primary prior: [Beale and Wallman, Randomized compiling for subsystem measurements](https://arxiv.org/abs/2304.06599); [Hashim et al., PRX Quantum 6, 010307](https://doi.org/10.1103/PRXQuantum.6.010307). The former's rendered HTML is incomplete, so only its abstract/introduction-level operation-family claim was used, not an imported general theorem.

The random operation must actually change the physical channel under the task's retained/erased register contract. A software Pauli-frame update alone does not implement output pinching. Giving a bath or subsequent controller the seed can change the relevant joint channel; an averaged marginal channel is not automatically the required joint-input interface. Ideal randomizing gates may themselves need qualification and support/cost accounting. Ware's compiled equal-pulse-budget experiment cannot certify those assumptions on another device or on a new measurement slot.

## 5. What this does and does not close

Obtained: an exact paid compiler formula, its optimal replacement parameter, and a stronger established targeted comparator for a specified isolated unread qubit channel.

Open: actual positive native floors, physical randomizer quality and independence, full-reservation support, duration/error/energy costs, complete outcome instruments, persistent shared baths, and a same-device memory comparison. Memory-only mixing is not a cure for arbitrary continuous bath coupling. This calculation does not supply N881's required arbitrary-joint-input bath factor or close its acquisition gate.

The correct next action is to acquire a declared actual control/instrument interface and match its physical comparator. No unqualified hardware test or universal CP-coin inference follows from aggregate counts, chi fidelity or randomized-compiling fit quality.

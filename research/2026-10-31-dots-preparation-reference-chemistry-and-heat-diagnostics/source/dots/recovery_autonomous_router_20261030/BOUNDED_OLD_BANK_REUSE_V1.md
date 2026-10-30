# Bounded-rate reuse of the old bank while protected transfer continues
30 October 2026. Root new candidate extending the preset-bank theorem. Independent review pending. This is not detached output or a fresh logical input encoder.

## Task and added resource
Keep the accepted preset-bank initialization/hardware. In addition to weak admitted physical noise, allow an arbitrary actual time-dependent bounded-body generator acting ONLY on physical old Q and auxiliary consumer systems, never on B, routing labels or native apparatus. It may reset Q, couple different old-Q columns, or interact with a retained external source. Its local system support is at most q_hot; total incident joint adjoint-cb norm per old-Q site is at most J, fixed independently of N. It is trace annihilating, and the entire actual dynamics has the required CPTP/compression regularity. Consumer-only terms are separated. Initial consumer/bath state is fixed independently of the protected unknown input; references retained as usual.

J need not be small relative to the native-memory noise threshold. Router strength Lambda is instead chosen sufficiently LARGE but fixed, after J and the code/proof margins. Scale Omega,kappa,mu together by Lambda. The normalized clock A, its ratio a and the local product-witness condition number stay fixed; r scales by Lambda. This pays stronger quantum couplers/resets and is not a free parameter change after observing noise.

This statement permits old-bank use while protecting the ORIGINAL logical input only. It does not promise preservation/encoding of a new input written on old Q, nor standalone receiver storage after deleting paired native hardware.

## 1. Exact auxiliary corner
In the fixed G frame, let P_D be the all-DONE projector on the router labels belonging to the old-Q support of one hot term, and P_A=I-P_D. A physical operation on old Q preserves every router label. On P_D it acts only on canonical spare, hence annihilates every memory witness F times the router witness V_r. Since V_r has no DONE/active off-diagonal block, the full adjoint action is supported in P_A:

 L_hot,e^*(F V_r)=P_A L_hot,e^*(F V_r) P_A.             (1)

For a completely general local HP map use finite system legs (rather than a fictitious jump expansion); the same corner statement follows because all old-Q legs preserve the labels and are auxiliary on P_D. Center each local term to annihilate identity, as in the original receiving contract. A consumer-only term annihilates the whole observable and is omitted.

The accepted local relative-norm bound for the positive native witness F, together with the bounded condition number of the touched router factors, gives

 -C_hot J_e P_A F V_r <= L_hot,e^*(F V_r)
                       <= C_hot J_e P_A F V_r.         (2)

F commutes P_A and V_r. The same proof applies to the actual positive BUSY witness G_busy. The constants are uniform for 0<u<=u0 because the router factor condition number is bounded there, and depend only on the fixed native proof circuit, finite grouped dimensions and q_hot, not Lambda or bath dimension. A factorized local error bound for F is a premise imported from the governing native theorem; it is not a bound for arbitrary positive observables.

Since P_A<=sum_(i in supp e) B_i^r, summing the actual incident strength gives

 sum_e L_hot,e^*(F V_r)<= C_hot J M_r F V_r.           (3)

This is an OPERATOR estimate for the actual correlated state, not mean error rate times independent active probability. Coherences between0 and e are retained. Strong old-bank operations can slow/entangle the clock but are charged in (3), not omitted from its dynamics.

## 2. Joint memory/route moment using the actual positive pullback
Import the exact native statement from GLOBAL_EXPONENTIAL_COMPILER.md:

 F=T(V_G), V_G=exp(sE) G, [G,E]=0, I<=G<=exp(gN),
 L_mem^*F <= -lambda T(E V_G)+rho N F.

T is the actual fixed positive unital proof pullback on native-memory variables; it is identity on canonical spare/router. All inequalities are used on the SAME canonical basin/killed process as in the original theorem. Do not replace this by an unproved operator F logF inequality.

Put W=F V_r=T(V_G V_r). Exact router product drift gives

 L_route^*W <= -c_r M_r W,
 c_r= r u/(1+u).

Combine weak physical noise, (3), and the unchanged native terms:

 L_total^*W <= -lambda T(E V_G) V_r
              -(c_r-C_hot J) M_r W +(rho+C_noise eta)N W.   (4)

The constant C_noise can include all fixed enlargement factors. Choose Lambda so

 c_r-C_hot J >= (lambda/s) log(1+u).                   (5)

For positive subnormalized killed rho, sigma=T_*(rho) is positive with trace<=1. Since log(V_G V_r)=sE+log G+log V_r, and log V_r<=log(1+u) M_r, scalar spectral Jensen yields

 lambda Tr[E V_G V_r sigma]
 +(c_r-C_hot J) Tr[M_r V_G V_r sigma]
 >= (lambda/s) [x log x-gN x],  x=Tr W rho.

Thus the SAME nonlinear moment law and limiting coefficient as the old memory proof hold, apart from a new fixed weak-noise constant. Initial routing0 costs at most log(1+u)N in log x(0). Choose u>0 sufficiently SMALL so g+log(1+u) lies below the existing barrier with a fixed margin; only then choose Lambda sufficiently large for (5). This order avoids hiding an extensive unqualified initialization.

## 3. Basin exit and fixed logical module
W>=F because V_r>=I and acts on disjoint canonical factors. Therefore the original sector-sensitive lower bound for F still controls the SAME canonical-energy boundary. The extra hot term has bounded system support, fixed bandwidth and total norm O(JN), so boundary telescoping changes only a fixed polynomial prefactor, not the exponential rate. Compress the actual total CPTP evolution with complete losses. Positivity allows removal of outgoing gains; no individual HP hot/noise piece is assumed CP. The source-local canonical logical identity for bounded support inside the basin remains the original code-distance argument.

A positive common-logical-module comparison therefore survives, IF (1)--(4) and their exact native local relative contract are verified. The high-strength operation is not declared weak noise; its extensive effect is paid by the router negative term.

## 4. Physical BUSY density and output
The same construction is needed separately for G_busy, whose original full-Hilbert log-moment law and positive representation are in DIRECT_SINGLETON_DERIVATION_V1.md. If its operator form is -lambda_b G_busy log G_busy+rho_b N G_busy, its product with V_r is direct. If it uses a positive pullback, repeat section2 with that exact representation. Do NOT infer a new BUSY tail from the memory energy alone.

Choose u below BOTH native-energy and BUSY initial-moment margins; increase the same Lambda to absorb both C_hot constants. The original routing-only tail also holds with hot operations charged as O(J) unless its Lyapunov drift absorbs those operations: apply the same corner estimate with F=I, giving L_total^*V_r<=-(c_r-C_clock J)M_r V_r+C_noise eta N V_r. Choose Lambda so c_r>C_clock J with a fixed margin. Convert M_r V_r >= V_r log V_r/log(1+u), then use scalar Jensen as before. This yields a fixed startup dwell and exponentially small routing density at every later fixed time.

Transfer the two physical tail bounds to the positive canonical comparison and use the SAME common bare-B Pauli span/ordinary decoder as in the reviewed preset theorem. The original logical input remains protected while bounded-rate old-Q processing continues. This final paragraph remains conditional until the exact BUSY receiving form and joint complete-loss compression are checked.

## Scope and meaningful consequence
Unlike a clean DONE flag argument, this prices receiver/routing faults that temporarily expose the canonical protected factor to strong old-bank operations. It permits a meaningful source-reuse interface at a paid router-rate hierarchy. It still requires the paired correction hardware and ordinary ideal decoder benchmark. It does not protect arbitrary strong operations on the receiving B bank, prevent adversarially unbounded source drive, or make a sequence of gates causally correct. Historical novelty and practical advantage are not established.

# Whole review of expected stopping and bounded-force extension

**ACCEPTED at the declared common-policy, zero-start, well-posed
controlled-diffusion scopes.** I independently checked the complete
STOPPED_SHIFT_BOUND.txt, including its final bounded-force corollary.
No model, recurrence, numerical coefficient or observation was rerun.
This closes the stopping qualification left open in my separate
fixed-duration review; it does not silently substitute E tau into a
fixed-time pointwise moment estimate.

For a common local stop sigma, Ito applied to R^m=||X||^(2m) gives

    E R_sigma^m
       <=-2m kappa O_m
                    +2m theta(n+2m-2)O_(m-1),
    O_j=E int_0^sigma R^j dt.

R_0=0 and the terminal term is nonnegative. Dropping it BEFORE any
limit gives O_m<=theta(n+2m-2)O_(m-1)/kappa. The SAME local stop
must be used at all three moment orders, as the proof specifies.
Thus O_3<=(theta/kappa)^3 n(n+2)(n+4)E sigma. Increasing local/time
cutoffs and monotone convergence prove the occupation inequality at
tau. No uniform integrability of the terminal sixth moment and no
independence of tau from hidden fluctuations is needed.

The kernel inequality is pathwise at each realized tau: integrate
the positive convolution over the random triangle 0<=s<=t<=tau and
bound each inner kernel integral by r0=g0/b0. This proves

    int_0^tau F_t^2 dt<=a^2 r0^2 int_0^tau X_v(t)^6 dt.

Local adapted Girsanov applies on the augmented record, with the
same port-history policy and common independent controller seed under
both laws. Turning the drift change off after a stop only changes an
auxiliary continuation, not the stopped experiment. Localization may
use the alternative's error reconstruction as a COMMON functional of
the augmented record. Under the alternative it is the actual state;
under the reference it remains just a well-defined comparison
functional. No hidden state is measured or controlled by the observer.

For deterministic T, the resulting entropy upper at tau intersect T
is the expected stopped control energy divided by 4theta. The
sigma fields of these records increase and determine the complete
finite stopped transcript. Entropy's variational characterization
therefore passes the bound to tau. The assumptions that tau is
observable, finite almost surely under both laws and E_a tau finite
are load-bearing. If that expectation is infinite, the finite upper
becomes vacuous rather than a finite resource statement.

The accepted result is exactly D(P_a||P_0)<=C_a E_a tau with the
source's coefficient. Pinsker then gives the lower on E_Delta tau,
and hence on worst-case expected duration. It does not give a
separate lower on E_0 tau or a pointwise deadline. Randomized tests,
controller logs and finite noisy exposure processing are covered by
the common-policy/data-processing argument. Fresh stationary samples
and altered physical access are still excluded.

For the optional common force |u_t|<=U, the force cancels from the
augmented drift difference even when selected by observable feedback.
Young's inequality 2u X_p<=kappa R+U^2/kappa changes the generator
estimate to

    L_t R^m<=-m kappa R^m
        +m[2theta(n+2m-2)+U^2/kappa]R^(m-1).

The same stopped occupation argument gives B_m as stated and the
entropy constant a^2(g0/b0)^2 B_1 B_2 B_3/(4theta). This bound is
eight times the sharper zero-force moment constant at U=0, so keeping
the old zero-force result separately is correct. At fixed U it still
has only polynomial n growth multiplying the exponentially small
endpoint gain squared. It need not remain useful when U grows with
inverse gain; no sharp peak-resource crossover is proved.

The n32 zero-force numerical duration is inherited unchanged from A's
qualified packet and was not recomputed. The result does not lower-
bound the n4 star's sufficient 1e37 point-read plan, all chain designs,
negative/nonuniform shifts, modified baths or unknown metrics.
Mechanical force, native observation time and irreversible work are
different quantities. This is not a work/power/dissipation floor.

The method uses ordinary stopped Lyapunov estimates, entropy/control
comparison and two-point testing. Historical novelty, practical
advantage and a physical device have not been acquired.

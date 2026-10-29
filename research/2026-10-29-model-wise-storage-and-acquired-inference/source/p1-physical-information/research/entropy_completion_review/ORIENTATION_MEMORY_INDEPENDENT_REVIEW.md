# Independent review: orientation memory and a vanishing sustained rate

29 October 2026. Reviewed the new construction in
`../ORIENTATION_MEMORY_AND_SUSTAINED_ENTROPY.md`. Both the two-orientation
lift and its equal-clock fourfold lift are correct at the stated passive
coarse-path scope. No numerical fixture is needed for the identities.

## 1. Two orientations

Let alpha=1-epsilon, d=1-2epsilon, a=kappa epsilon and b=kappa alpha,
with 0<epsilon<1/2 and kappa>0. The product law

    rho(x,+)=alpha pi_x,   rho(x,-)=epsilon pi_x

is stationary: each internal generator Q or Q* preserves pi, and
alpha a=epsilon b balances orientation switches. Irreducibility follows
from irreducibility of Q and positive switching rates.

Under Theta(x,+)=(x,-), an internal edge's rate ratio is pi_y/pi_x.
Its stationary mean log ratio vanishes separately in each orientation.
Each orientation-switch edge is its own reversed-parity edge, so that
log ratio is zero. The two total escape rates are lambda_x+a and
lambda_x+b. Their contribution is

    alpha(b-a)+epsilon(a-b)=kappa d^2.

Thus sigma_2n=kappa d^2 exactly, even if the source's ordinary all-even
entropy is infinite. Every positive internal edge has its reversed-parity
counterpart in the other orientation.

The stationary boundary term is

    B=D(rho||rho Theta)=d log(alpha/epsilon).

Consequently the full stationary microscopic path KL over a duration T
is B+T sigma_2n. Omitting B would incorrectly force small sustained rate
to imply small finite-window irreversibility.

## 2. Complete path coupling

Start the source from pi, and sample the lifted orientation independently
with probabilities alpha,epsilon. If it starts in +, use the same source
x and internal Q jumps. Until its first + to - switch the entire x paths
agree. That switch has state-independent hazard a. Hence

    TV(P_lift[0,T],P_Q[0,T])
       <=epsilon+alpha(1-exp(-kappa epsilon T))
       <=epsilon+kappa epsilon T.

This is a full path-law coupling bound, not just a sampled-word or moment
comparison. It passes to every deterministic even readout g(x). The
one-time readout distribution already agrees exactly for all parameters.

## 3. Equal-clock padding

Take c_0>0, Lambda=max_x lambda_x+c_0, c_x=Lambda-lambda_x, and
0<kappa<c_0. Duplicate every lifted state with a bit h. Keep all actual
lifted transitions bit preserving; toggle the bit at rates

    u_x=c_x-kappa epsilon in +,
    v_x=c_x-kappa alpha in -.

Both are positive, and every microscopic escape rate is exactly Lambda.
The stationary law is rho(x,s)/2. Projection forgetting h is strongly
lumpable onto the preceding lift: its aggregate rates between different
(x,s) states do not depend on h. Thus the entire x path law and coupling
bound remain unchanged. Positive toggles make the fourfold model
irreducible.

Set Theta(x,s,h)=(x,-s,h). Holding-rate differences now vanish. Internal
and orientation-switch jump terms vanish as before. Summing the two bit
directions gives

    sigma_4n=sum_x pi_x [alpha u_x-epsilon v_x]log(u_x/v_x)
             =sum_x pi_x d c_x log[(c_x-kappa epsilon)
                                      /(c_x-kappa alpha)].

The identity alpha u_x-epsilon v_x=d c_x is exact. Since u_x>=v_x>0,

    0<=sigma_4n
      <=kappa d^2 sum_x pi_x c_x/(c_x-kappa alpha)
      <=kappa d^2/(1-kappa/c_0).

The stationary boundary term remains B: the extra uniform bit cancels
from the ratio. For epsilon=delta/2 and
kappa<min(c_0/2,1/T,eta/2), the stated strict accuracy and rate bounds
follow. For T=0 the 1/T restriction is omitted.

Thus four times the source's state count and one fixed escape clock
suffice. Neither a growing maximum clock nor a growing state count is
needed for this counterconstruction.

## 4. Resource and interpretation qualifications

The orientation process has an exact nonconstant eigenmode with decay
rate kappa. Hence no source-uniform relaxation bound follows. This is a
worst-start relaxation statement, not a proof that every permitted way
to prepare the stationary law necessarily takes time 1/kappa.

B diverges as epsilon decreases, but it is specifically the KL between
stationary preparation and its parity image. It is not automatically a
thermodynamic preparation-work cost, a number of stored bits, or an
operational preparation time. For example, the orientation's relative
entropy to an unbiased bit is log 2-H(epsilon), which stays bounded by
log 2. Its divergence relative to its nearly opposite preparation can
nevertheless diverge. The root note's explicit parity-divergence meaning
should be retained whenever this quantity is described as preparation
information.

The construction also uses arbitrarily small switching rates and small
stationary weights. The fixed upper clock ceiling does not bound those
quantities, mixing, parameter precision, or preparation accuracy.

Every observed source label now represents several microscopic states,
and Theta fixes no individual orientation state. The construction does
not preserve a warranty that a resolved observed port is one microscopic
reset state fixed under reversal. Therefore it does not contradict the
native regenerative J floor. Its nontrivial hidden parity also excludes
it from the all-even metric-tree theorem. An observable counting all
microscopic bit or orientation jumps would be an additional interface;
it is absent from the specified memoryless readout.

The algebra proves the claimed collapse of the robust sustained-rate
floor for every finite-source coarse path law in this unrestricted
parity/preparation class. It does not produce one zero-rate irreducible
model with the exact full target law, establish a native physical parity,
or implement a low-heat physical simulator.

## 5. What an actual boundary budget would add

If an admissible model class instead supplies B<=B_max, the stationary
path identity and even-readout data processing give, for every finite observed grid
G in [0,T],

    sigma >= [D(p_G||p_G^reverse)-B_max]/T,

with the positive part understood. Lower semicontinuity passes this
obstruction to approximation neighborhoods whenever the observed
divergence strictly exceeds B_max. Thus a quantified parity-preparation
budget is mathematically different information from a state-count or
maximum-clock bound. This is an implication of the checked construction,
not a claim that such a budget has been acquired.

Here p_G^reverse is the law induced by the reversed path on G. For an
irregular grid, acquiring both laws uses the union of G and its reflection
T-G; reversing the list of symbols on G alone would be insufficient.

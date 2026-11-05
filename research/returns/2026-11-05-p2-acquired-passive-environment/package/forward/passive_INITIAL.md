# Passive forward acquisition: first substantive derivation

Use x'+V'(x)+m=f, z_lambda'=-lambda z_lambda+x', m=integral z dnu, nu>=0, nu total<=B, initial bath energy (1/2)integral z0^2 dnu<=E0. Let c be a fixed observed reference, command u(t) in [-A,A], u(0)=0, and use the actual finite-stiffness port

q(t)=c+V'(c)/k+u(t),   f=k(q-x).

No state-dependent ideal clamp or derivative feedforward is required. For x_cmd=c+u and e=x-x_cmd,

e'+k e+[V'(x_cmd+e)-V'(x_cmd)]+K*e' = -[u'+V'(c+u)-V'(c)+H0+K*u'],

where H0=integral exp(-lambda t) z0 dnu. Since |H0|<=sqrt(2BE0), ||K*u'||inf<=2BA for any globally bounded command (independently of number of cycles), and |u'|<=U, the right side is bounded by

D=sqrt(2BE0)+2BA+U+max{|V'(c+A)-V'(c)|,|V'(c-A)-V'(c)|}.

At a new maximum of e, the derivative-memory term is nonnegative because K is nonnegative decreasing. Thus the scalar maximum principle gives

||e||inf <= max{|e(0)|,D/(k+mu)}.

This comparison uses bounded variation of K, so no upper bound or moment of lambda is needed. The actual force obeys |f|<=|V'(c)|+k||e||inf. With initial alignment |e(0)|<=D/(k+mu), force stays bounded by |V'(c)|+D even as k is increased.

A quintic ramp S(v)=10v^3-15v^4+6v^5 has sup S'=15/8 and sup |S''|=10 sqrt(3)/3. With u=sign*A*S(t/h), q speed <=(15/8)A/h and q acceleration <=(10 sqrt(3)/3)A/h^2. Shrinking h is compatible with fixed speed and acceleration caps by shrinking A proportional to h^2, at a paid statistical and position-resolution cost.

Tracking-memory error after restarting a cycle at s is bounded by

||K*e'||inf <= [K(0)+K(t)+K(0)-K(t)]||e||inf <=2B||e||inf,

including the nonzero initial tracking error e(s). (A 3B bound is safe but loose.) The full hidden force remains bounded independently of cycle count: from bounded actual position |x-c|<=A+delta,

|m(t)| <=sqrt(2BE0)+2B(A+delta).

Therefore fresh-sign multiplication can cancel arbitrary retained bath offsets with bounded martingale increments; no hidden-state reset is needed. Remaining derivation: integrated bin residual, sensor and calibration errors, complete finite cost and feasibility conditions. The initial alignment and calibrated metrology must be explicitly paid rather than assumed exact.

## Improvement: exact finite-bin identity, no instantaneous position samples

Use a triangular test psi on [t,t+2w], height 1, rising on the first w and falling on the second. Position meters return the two box averages X_left and X_right over those w-wide bins. Then

(1/w) integral psi x' = (X_right-X_left)/w

exactly. Estimate the weighted force integral from fine force-bin averages of width d=w/n using midpoint weights. Since force is bounded by Fmax, the deterministic quadrature error is <=Fmax/n, with no force-derivative or lambda_max assumption. During the hold subtract the known constant V'(c+sign*A); the nonlinear subtraction error is <=omega_V'(delta), not a noisy nonlinear transformation of position readings.

The measured target is K_star(t)=integral exp(-lambda*t) c_h(lambda) d_w(lambda) dnu, where

d_w(lambda)=((1-exp(-lambda*w))/(lambda*w))^2,
c_h(lambda)=integral_0^h [S'(s/h)/h] exp(-lambda*(h-s)) ds.

Both filters are positive and <=1, so K_star is itself completely monotone with total height <=B. For the symmetric quintic ramp, mean ramp delay is h/2 and mean triangular-bin delay is w, giving the horizon-uniform smoothing bound

||K-K_star||_L1(0,T) <= B(h/2+w).

This is a genuine finite-bin protocol; no instantaneous derivative or pointwise meter has been assumed. With N fresh signs and M bins, retained-offset statistical error is <=(Mstar/A)*sqrt(2 log(2M/alpha)/N), and tracking/nonlinear/quadrature deterministic kernel bias is <=[2B*delta+omega_V'(delta)+Fmax/n+meter_bias]/A. Exact finite-bin noise variances and resource scaling follow in the full report.

# Pure-success/white-reset overlap power has both curvature signs

26 October 2026. Exact actual-source guard; no negative deficit.

Let R=C3 tensor C2, Y=b I3 tensor |0><0| with b>0, and let V_r u=u tensor (sqrt(r)|0>+sqrt(1-r)|1>), 0<=r<=1. Consider A_r=3d P_(Phi_Vr)+I3 tensor Y, d>0. This is precisely the pure maximally entangled success plus physically white reset family. The main/reset overlap power is r; its outside main Gram is d(1-r)I3 and visible main Gram is dr I3. The source trace n=3d+9b is independent of r.

Write eps=1-r. The changing input spectrum is one2x2 block

 M_r=[[b+3dr,3d sqrt(r eps)],[3d sqrt(r eps),3d eps]],

plus eight copies of b. The reference spectrum is three copies of

 R_r=[[3b+dr,d sqrt(r eps)],[d sqrt(r eps),d eps]].

The normalized WH output spectrum is three copies of

 O_r=[[b+dr,d sqrt(r eps)],[d sqrt(r eps),d eps]],

plus six copies of b. Thus the exact homogeneous deficit is

 Delta(r)=f(M_r)+3f(R_r)-6f(O_r)-4f(b)-(3d+9b)log3.

Each block has fixed positive trace and determinant linear in eps. Its small eigenvalue is therefore analytic at eps=0 with leading coefficients

 3db/(b+3d), 3db/(3b+d), db/(b+d),

respectively. Expanding the scalar entropy gives

 Delta(1-eps)=Delta(1)+C eps log eps+O(eps),

 C=3db[1/(b+3d)+3/(3b+d)-2/(b+d)]
  =12d^2 b(d-b)/[(b+d)(b+3d)(3b+d)].

The analytic eigenvalue expansions also receive the differentiated remainder:

 Delta''(r)=C/(1-r)+O(|log(1-r)|).

Consequently d>b gives strictly positive overlap-power curvature near r=1, whereas d<b gives strictly negative curvature. There is neither universal concavity nor universal convexity on this exact pure-success/white-reset overlap path. Normalizing by the constant n does not change these signs.

These sources are in the already-paid physical-CQ reset/scalar-compressed-resolvent class. The calculation only rules out a universal overlap-power shape reduction; it does not contradict value positivity, success-mass monotonicity, or a conditional coupled stationary equation.

## Exact normalized calibrations

Set d=p/3 and b=q/9, p+q=1. The normalized channel is

 E(rho)=p rho tensor P_s+q Tr(rho)(I3/3) tensor P_v,
 |<s,v>|^2=r.

The INPUT has one opening eigenvalue with coefficient pq/(q+9p); the REFERENCE has three opening eigenvalues with total coefficient pq. The three output openings contribute -2pq/(q+3p). Their sum is

 C(p)=pq[1+1/(q+9p)-2/(q+3p)].

At p=1/10, C=-1/100, proving negative curvature and a negative first overlap derivative near r=1. At p=1/2, C=1/20, proving positive curvature and positive first overlap derivative there. These rational calibrations eliminate any universal increasing, decreasing, convex, or concave shape claim for the common overlap power. They do not address sign of the actual value or conditional joint stationarity.

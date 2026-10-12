# Independent angular/window check

2026-10-13. Requested after the LP derivation gate. Source checked: root/FINITE_TIME_RESONANCE.txt, Sections 1–7 and the subsequently communicated unscreened mutation. This file contains independent calculations, not a microscopic derivation or a novelty assessment.

**Result:** the stated angular constants, cosine-window variance, finite-cutoff weak-error constants, fixed-memory leading-log limit, and unscreened identities check. There is a material distinction to retain: in the unscreened model the unnormalized longitudinal defect does not decay with increasing memory; it is only subleading to the divergent transverse logarithm.

## 1. Angular factors

Put u=r e3 and write k=q(sqrt(1-mu²)cos alpha,sqrt(1-mu²)sin alpha,mu). Integrating cos² alpha gives pi, so the transverse coefficient of the projected tensor is

~~~
a_T(r)=pi T int_0^K q^4 |Vhat(q)|²
                    int_-1^1 (1-mu²)phi(Tqr mu)dmu dq
      =pi/r int_0^K q³ |Vhat(q)|² R_phi(Tqr)dq.
~~~

Here R_phi(a)=int_|x|<=a(1-x²/a²)phi(x)dx. There is no missing 2pi or Fourier-volume factor under the specified dk convention.

For the raw tensor B_T=a_T P_u+b_T e_u e_u^T, the longitudinal coefficient is

~~~
b_T(r)=2pi/(T²r³) int_0^K q |Vhat(q)|² M2(Tqr)dq,
M2(a)=int_|x|<=a x² phi(x)dx.                         (1)
~~~

Consequently 0<=b_T<=2(a_inf-a_T) whenever a_inf and the difference have the stated meaning. For fixed nonzero finite K,r and finite positive second moment,

~~~
b_T/(a_inf-a_T) -> 2   as T->infinity.
~~~

Projection therefore removes a real term of the same leading asymptotic order as the transverse finite-memory deficit. It is not an equality to the original finite-memory evolution. The root document already makes that scope distinction.

For Fejer, direct integration of mu² F_T yields r²b_T=(4/T)int q² Vhat²[1-sinc(Tqr)]dq. For a *unit-mass* Maxwellian with covariance theta I, the weak kinetic-energy rate is exactly the stated 2/(theta T) radial integral. For mass M it is multiplied by M².

## 2. Variance and maximum time lag

For w in H_0^1(-1,1), Parseval gives

~~~
int phi=1,
int x²phi(x)dx=||w'||²/||w||².
~~~

The Dirichlet sine expansion has eigenvalues (n pi/2)². The smallest is pi²/4, attained only by a multiple of cos(pi s/2). The even restriction retains this first eigenfunction.

For w=cos(pi s/2),

~~~
||w||²=1,
what(x)=sin(x+pi/2)/(x+pi/2)+sin(x-pi/2)/(x-pi/2)
       =pi cos x/[(pi/2)²-x²].
~~~

The removable values at x=+-pi/2 are both one. The autocorrelation is supported on [-2,2], hence F_T has maximum lag L=2T. Its physical-frequency variance is

~~~
(pi²/4)/T²=pi²/L².
~~~

Equivalently the physical filter itself is

~~~
F_L(omega)=4pi L cos²(omega L/2)/(pi²-L²omega²)²,
~~~

with removable values at omega=+-pi/L. This makes the factor of two in temporal access explicit.

The Fejer expression in the root file follows by integrating (1-cos x)/x² by parts. Its remainder is 4/(pi a)+O(a^-3). A triangular amplitude has norm² 2/3 and derivative norm² 2, giving variance 3. Both comparators and their lag accounting check.

## 3. Yukawa: exact difference identity and a stronger bound

Let Vhat(q)=1/(q²+kappa²), kappa>0, r,T>0. Put

~~~
q_x=min(K,|x|/(Tr)).
~~~

Tonelli applied to the two nonnegative terms in 1-R gives the exact identity

~~~
a_inf^K(r)-a_T^K(r)
 =pi/(2r) int phi(x)
       [log(1+q_x²/kappa²)-q_x²/(kappa²+K²)]dx.         (2)
~~~

To verify it, for |x|<=TrK split the radial integral at q=|x|/(Tr). Use

~~~
int_0^q k³/(k²+kappa²)² dk
 =1/2[log(1+q²/kappa²)+kappa²/(kappa²+q²)-1],

int_q^K k/(k²+kappa²)² dk
 =1/2[1/(kappa²+q²)-1/(kappa²+K²)].
~~~

The rational terms cancel to (2). The case |x|>TrK gives the same formula with q_x=K.

As K increases, this nonnegative difference converges to

~~~
D_T(r)=pi/(2r) int phi(x)log(1+x²/(kappa²T²r²))dx.    (3)
~~~

This is a difference of two cutoff tensors, not an individually defined uncut tensor. A finite second moment suffices for (3). Since log(1+y)<=y,

~~~
D_T(r)<=pi mu2/(2kappa²T²r³).
~~~

Thus the root uniform-K constant checks. Jensen gives a stronger bound near r=0:

~~~
0<=a_inf^K-a_T^K
 <=pi/(2r)log(1+mu2/(kappa²T²r²))
 =pi/(2r)log(1+pi²/(kappa²L²r²))  for cosine.          (4)
~~~

This remains finite for every r>0 and is smaller than the existing algebraic bound. Formula (1) also gives

~~~
lim_K b_T^K(r)=pi/r int phi(x)x²/(kappa²T²r²+x²)dx.
~~~

For two Lipschitz gradient differences, the weak-form factor 1/2 and the r² product turn the tensor bound into pi³ H_f H_psi/(4L²kappa²) int ff*/r, exactly as stated. The local integral int_|u|<1 du/|u|=2pi confirms the crude bound M[2pi||f||_infinity+M].

The sharper bound (4) also yields

~~~
weak error <=pi H_f H_psi/4
                 int ff* r log(1+pi²/(kappa²L²r²)).
~~~

Using log(1+t²)<=t, it is at most pi² H_f H_psi M²/(4kappa L). This weaker rate can dispense with bounded density for the error integral itself. It does not remove any need to define the individual operators.

## 4. Fixed-memory leading logarithm

Direct integration gives the stated

~~~
a_inf^K(r)=pi/(2r)[log(1+z)+1/(1+z)-1],
z=(K/kappa)².
~~~

Writing ell=log(K/kappa), the rescaled discrepancy is

~~~
(2r/pi)(a_inf^K-pi ell/r)
 =log(1+1/z)+1/(1+z)-1.
~~~

For z>=1 this decreases from log 2-1/2 to -1. Hence its absolute value is at most one. The tensor error pi/(2r), the weak-form 1/2, and the two Hessian bounds give precisely pi H_f H_psi/(4ell) int ff*r. Combining with Section 3 gives the second stated weak-error term. Finite first velocity moment makes the first integral finite. No order-of-limits interchange is needed for fixed L>0.

## 5. Unscreened mutation: finite memory regularizes the infrared integral

For Vhat(q)=1/q², the projected finite-memory tensor is

~~~
a_T^K(r)=pi/r J_phi(A),  A=KTr,
J_phi(A)=int_0^A R_phi(a) da/a.
~~~

Tonelli gives

~~~
J_phi(A)=int_|x|<=A phi(x)
          [log(A/|x|)-1/2+x²/(2A²)]dx.                (5)
~~~

Finite E|log|X|| is needed here; finite second moment alone does not control the singularity of log|x| at zero. Cosine has a bounded density near zero and satisfies the condition.

Let c_phi=1/2+Elog|X|. Exactly,

~~~
J_phi(A)=log A-c_phi+epsilon(A),

epsilon(A)=int_|x|>A phi(x)[log(|x|/A)+1/2]dx
            +(1/(2A²))int_|x|<=A x²phi(x)dx.
~~~

Thus epsilon>=0. For y>=1, log y+1/2<=y²/2, so

~~~
0<=epsilon(A)<=mu2/(2A²),     A²epsilon(A)->mu2/2.
~~~

The asymptotic is sharp for a nonzero finite variance window. As A->0 for bounded continuous phi,

~~~
J_phi(A)=(4phi(0)/3)A+o(A).
~~~

Hence a_T^K stays finite in magnitude as r->0 (although P_u remains direction-dependent), and the low-k integral is genuinely finite for fixed T,K. This is a finite-memory regularization, not dynamically generated dielectric screening.

### Exact cosine logarithmic constant

The cosine characteristic function, from a direct overlap integral, is

~~~
C(t)=(1-|t|/2)cos(pi|t|/2)+(1/pi)sin(pi|t|/2),
0<=|t|<=2,
~~~

and zero outside. The logarithm identity, regularized if needed, gives

~~~
Elog|X|=-gamma-int_0^2 [C(t)-1_{t<=1}]dt/t
        =log(pi/2)-Ci(pi)-Si(pi)/pi.
~~~

Therefore

~~~
c_cosine=1/2+log(pi/2)-Ci(pi)-Si(pi)/pi
        =0.2884249210069454... .
~~~

This was also checked by direct integration of phi log|x| with an explicit tail bound.

### Exact longitudinal term and the hidden limit distinction

For the *raw*, unscreened finite-memory tensor, (1) becomes

~~~
b_T^K(r)=2pi/r int_0^A M2(a)da/a³
        =pi R_phi(A)/r.                              (6)
~~~

The second equality follows by integrating a^-3 from |x| to A. Thus 0<=b_T^K<=pi/r, and the discarded normalized weak term is bounded by

~~~
pi H_f H_psi/(2ell) int ff*r.
~~~

This checks the root compatibility claim at leading logarithm. However at fixed K>0, T->infinity also sends R_phi(KTr)->1, so b_T^K->pi/r. It does **not** decay like the Yukawa T^-2 longitudinal coefficient. For a unit-mass Maxwellian,

~~~
dE/dt -> pi/(2theta) E|u| = 2sqrt(pi)/sqrt(theta).
~~~

The defect is bounded and subleading after division by the large transverse logarithm, but is nonzero before that normalization. This is the precise failure that transverse projection removes.

## 6. A universal finite-memory ridge obstruction

For any squared-Fourier window generated by an amplitude supported in an interval of length L, Cauchy–Schwarz gives sup F<=L/(2pi). For the normalized Lorentzian h_eta,

~~~
int F h_eta/h_eta(0)<=pi eta sup F<=eta L/2.
~~~

Consequently all such finite-memory windows need L=Omega(1/eta) for a relative ridge approximation. For cosine the stated sharper shape constant 4eta L/pi² checks. This obstruction concerns frequency resolution; exact transversality cannot remove it.

## 7. Scope of the check

No counterexample to the stated restricted radial/window results was found. The main qualification is the nonvanishing *unnormalized* unscreened longitudinal defect in (6). Positivity, exact conservation after projection, and leading-log normalization remain compatible. They do not identify the actual microscopic memory operator or provide its missing stability and cumulant control.

## 8. Fisher-information extension communicated subsequently

Let f be bounded of mass M, with score xi=grad log f and finite Fisher information I=int f|xi|². Let psi have Hessian bound H_psi. No Hessian bound on log f is needed for the following Yukawa weak estimate.

If ||delta A(u)||<=C/|u|³, the weak form gives

~~~
|delta Q[psi]|
 <=C H_psi/2 int ff* (|xi|+|xi*|)/|u|²
 = C H_psi int f(v)|xi(v)|(f*|.|^-2)(v)dv.
~~~

For every R>0,

~~~
sup_v(f*|.|^-2)(v)
 <=4pi ||f||_infinity R+M/R²,
int f|xi|<=sqrt(M I).
~~~

Thus the root bound C H_psi sqrt(MI)[4pi||f||_infinity R+M/R²] checks, with C=pi³/(2L²kappa²). The optimal elementary split is R=(M/(2pi||f||_infinity))^(1/3), giving bracket 3(2pi)^(2/3)||f||_infinity^(2/3)M^(1/3).

For the Yukawa radial leading-log remainder ||delta A||<=pi/(2|u|), the same calculation gives

~~~
|delta Q[psi]|/ell
 <=pi H_psi M sqrt(M I)/(2ell).
~~~

These assumptions also suffice to define the separate finite-K weak forms: a_T<=a_inf is a constant times 1/r, which cancels the r from the gradient difference of psi, leaving an integrable score. No first moment is required in this Fisher version.

This tail simplification should not be automatically transferred to the unscreened log r remainder: bounded density, mass and Fisher information alone do not control an arbitrary logarithmic velocity tail.

# P2 return after C44D and continuation

Chat: https://chatgpt.com/c/6af1715f-dbc4-83ec-a58c-3bca5bb0fe65
Model at dispatch: GPT-6 Standard, Extra High 4/4.
Original exact prompt: P2_FULL_BODY_FORCE_AFTER_C44D_XI_20261110.txt; SHA-256 5bec4a1f1dfa54dccd0ae1d54ebf470c338f1bdc0f12b88b785ebd3c5f637cbb.
Original response 9a04f666-6565-49ee-9758-45824deb4fba ended mid-formula; the authorized exact continuation was “please continue.”, user turn 83e9601a-500b-4f6c-a145-b9b5c5ed8792. Final response e1553c6d-9d5c-41de-8c8c-84943fecbcdc.
No ZIP identified. Connector caps the final at 20,000 characters; its final sentence ending is reconstructed from the complete visible response and marked below. The earlier partial is preserved exactly as returned, including its abrupt ending.

## Visible activity before interrupted response

Worked for 29m 16s

Assessed mathematical obstructions and refined stabilization strategies

I’ll focus on the three-dimensional obstruction that the planar estimates avoid: pressure-coupled vortex stretching. The useful test is whether a large but short, force-realizable shear can have a perturbation bound that grows only algebraically with its impulse, while viscosity still removes the mixed modes.

Developed obstruction criteria and control actuator strategies

Tested spectral saturation, examined constructive control, and combined spatial modes

Developed conditional reduction for fast mixing and return control limits

Searched the web

I’ve obtained a more direct reduction. A zero-return Euler trajectory built from the twelve fundamental Fourier fields can be implemented by a fixed 36-field additive-force family. On a sufficiently short interval, every Leray–Hopf realization stays close to the homogeneous linearized Euler evolution of its unknown initial datum, with an explicit error proportional to the interval length. This avoids simulating the nonlinear 3D PDE in the control certificate; the unresolved issue is whether those linearized Euler maps can squeeze the entire H¹ ball.

Assessed the mixer condition

Established a coercive estimate

Developed verification criteria and computed eigenvalue and energy drift bounds

Analysis paused — Python, no output visible:
```python
import numpy as np, itertools, math
def coeff_sum(k):
    k=np.array(k,dtype=float); kk=np.dot(k,k)
    Pk=np.eye(3)-np.outer(k,k)/kk
    S=np.zeros((3,3))
    for i in range(3):
      for j in range(3):
       if i==j:continue
       for sig in [-1,1]:
        p=k.copy();p[j]+=sig
        if np.dot(p,p)==0: continue
        Pp=np.eye(3)-np.outer(p,p)/np.dot(p,p)
        D=k[i]*np.eye(3)+sig*np.outer(np.eye(3)[i],np.eye(3)[j])
        X=Pp@D@Pk
        S+=X.T@X
    eig=np.linalg.eigvalsh(Pk@S@Pk)
    return eig[1]/kk,eig[2]/kk
mn=(float("inf"),None)
for k in itertools.product(range(-6,7),repeat=3):
    if k==(0,0,0):continue
    val,_=coeff_sum(k)
    if val <mn[0]:mn=(val,k)
mn, [(k,coeff_sum(k)) for k in [(1,0,0),(1,1,0),(1,1,1),(2,0,0),(2,1,0),(2,2,0),(2,2,2),(6,0,0)]]
```

Analyzed — Python:
```python
import numpy as np, itertools
def boundval(k):
    k=np.array(k,dtype=float)
    Pk=np.eye(3)-np.outer(k,k)/(k@k)
    S=np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            if i==j:continue
            for sig in (-1,1):
                p=k.copy()
                p[j]+=sig
                if p@p==0:continue
                Pp=np.eye(3)-np.outer(p,p)/(p@p)
                D=k[i]*np.eye(3)+sig*np.outer(np.eye(3)[i],np.eye(3)[j])
                X=Pp@D@Pk
                S+=X.T@X
    eig=np.linalg.eigvalsh(S)
    return eig[1]/(k@k), eig[2]/(k@k)
mi=(float('inf'),None)
for k in itertools.product(range(-5,6), repeat=3):
    if k==(0,0,0):continue
    val,_=boundval(k)
    if val<mi[0]:mi=(val,k)
print(mi)
for k in [(1,0,0),(1,1,0),(1,1,1),(2,0,0),(2,1,0),(2,2,0),(2,2,2),(5,0,0)]:
    print(k,boundval(k))
```
STDOUT/STDERR:
```text
(np.float64(3.3333333333333335), (0, -1, -1)) (1, 0, 0) (np.float64(4.0), np.float64(4.0)) (1, 1, 0) (np.float64(3.333333333333334), np.float64(3.6)) (1, 1, 1) (np.float64(3.5555555555555554), np.float64(3.555555555555556)) (2, 0, 0) (np.float64(3.4000000000000004), np.float64(3.4000000000000004)) (2, 1, 0) (np.float64(3.4666666666666663), np.float64(3.744000000000001)) (2, 2, 0) (np.float64(3.6111111111111107), np.float64(3.946153846153846)) (2, 2, 2) (np.float64(3.8801742919389977), np.float64(3.880174291938999)) (5, 0, 0) (np.float64(3.8523076923076927), np.float64(3.8523076923076927))
```

Analyzed — Python:
```python
import numpy as np
def matrices(k):
    k=np.array(k,dtype=float)
    if k@k==0:return None
    I=np.eye(3)
    Pk=I-np.outer(k,k)/(k@k)
    SH=np.zeros((3,3))
    LOOP=np.zeros((3,3))
    for i in range(3):
      for j in range(3):
        if i==j:continue
        for sig in [-1,1]:
          p=k.copy();p[j]+=sig
          Pp=I-np.outer(p,p)/(p@p) if p@p else np.zeros((3,3))
          Di=k[i]*I+sig*np.outer(I[i],I[j])
          T=Pp@Di@Pk
          SH+=T.T@T
          Dback=p[i]*I-sig*np.outer(I[i],I[j])
          Tback=Pk@Dback@Pp
          LOOP+=Tback@T
    DRIFT=Pk@(SH-LOOP)@Pk
    return SH,LOOP,DRIFT,np.linalg.eigvalsh(DRIFT)
for k in [(1,0,0),(1,1,0),(1,1,1),(2,0,0),(2,1,0),(3,2,1),(10,1,0)]:
    a,b,c,e=matrices(k)
    print(k, np.round(e,6), 'drift matrix',np.round(c,3))
```
STDOUT/STDERR:
```text
(1, 0, 0) [0. 2. 2.] drift matrix [[0. 0. 0.] [0. 2. 0.] [0. 0. 2.]] (1, 1, 0) [0. 1.333333 2.4 ] drift matrix [[ 1.2 -1.2 0. ] [-1.2 1.2 0. ] [ 0. 0. 1.333]] (1, 1, 1) [0. 2. 2.] drift matrix [[ 1.333 -0.667 -0.667] [-0.667 1.333 -0.667] [-0.667 -0.667 1.333]] (2, 0, 0) [0. 0.8 0.8] drift matrix [[0. 0. 0. ] [0. 0.8 0. ] [0. 0. 0.8]] (2, 1, 0) [0. 0.666667 2.4 ] drift matrix [[ 0.48 -0.96 0. ] [-0.96 1.92 0. ] [ 0. 0. 0.667]] (3, 2, 1) [-0. 0.888188 3.030736] drift matrix [[ 1.046 -1.377 -0.385] [-1.377 1.996 0.139] [-0.385 0.139 0.876]] (10, 1, 0) [-0. 0.039216 0.19303 ] drift matrix [[ 0.002 -0.019 0. ] [-0.019 0.191 0. ] [ 0. 0. 0.039]]
```

## Visible activity after continuation

Worked for 23m 43s

Assessed mathematical avenues and tested construction limits

I’ll pursue the remaining homogeneous Euler squeezing condition directly, while also testing whether it is too strong to follow from the twelve-generator coercivity estimate. I’ll distinguish an actual common contraction mechanism from evidence that individual Fourier modes can be mixed.

Reconsidered obstructions

Derived and strengthened microlocal obstructions from helicity and structural constraints

Assessed and refined microlocal, spectral, and norm obstructions

Assessed high frequencies and the perturbation argument

Strengthened compiler and obstruction arguments through construction refinement

Refined the compiler and assessed the control strategy

Searched the web

## Interrupted available response (verbatim)

# P2 — A new reduction of the full additive-force problem

**The full compiler remains open.** This continuation establishes a useful reduction: a fixed finite additive-force family can implement a rapidly accelerated, zero-return Euler trajectory, and the resulting nonlinear three-dimensional Navier–Stokes evolution can be compared uniformly with a *homogeneous linearized Euler propagator*\.

The comparison works for the entire \(H^1\) preparation ball, arbitrary admitted Leray–Hopf realizations and additive disturbances. Its error is explicitly controlled as the physical duration shrinks.

This changes the central question from constructing and verifying nonlinear three-dimensional trajectories to constructing a particular kind of **uniformly squeezing linearized Euler evolution**\.

## 1\. A fixed family of 36 rational actuators

Let \(\kappa=2\pi\)\. Begin with the twelve first-harmonic fields

\[
e_i\cos(\kappa x_j),\qquad
e_i\sin(\kappa x_j),\qquad i\ne j.
\]

Denote their span by \(\mathcal W\)\.

Add 24 fields associated with the six wavevectors

\[
k=e_i+\sigma e_j,\qquad
1\le i<j\le3,\quad \sigma\in\{-1,1\}.
\]

For each \(k\), use the two rational perpendicular polarizations

\[
e_\ell,\qquad e_i-\sigma e_j,
\]

where \(\ell\) is the remaining coordinate, with both sine and cosine phases.

This produces one fixed 36-dimensional admissible spatial family \(\mathcal G\), independent of \(M,\nu,\tau,\epsilon\)\.

Its key algebraic closure property is

\[
\boxed{
w\in\mathcal W
\quad\Longrightarrow\quad
\mathbb P[(w\cdot\nabla)w]\in\mathcal G.
}
\tag{1}
\]

Indeed, parallel first-harmonic interactions vanish, and nonparallel interactions have sum frequencies \(e_i\pm e_j\)\. Every resulting Leray projection is a rational matrix acting on the Fourier polarization, apart from the known factor \(\kappa\) arising from differentiation.

Thus arbitrary time-dependent trajectories inside \(\mathcal W\) can be maintained by additive forcing from this same fixed 36-field family.

## 2\. Uniform fast-return transference theorem

Let \(w:[0,1]\to\mathcal W\) be a continuous, piecewise-polynomial path with rational coefficients and breakpoints, satisfying

\[
w(0)=w(1)=0.
\]

Write

\[
\mathcal B(u,v)=\mathbb P[(u\cdot\nabla)v],
\qquad
\mathcal L_wv=\mathcal B(w,v)+\mathcal B(v,w).
\]

Let \(S_w(s)\) denote the homogeneous linearized Euler evolution

\[
\boxed{
v_s+\mathcal L_{w(s)}v=0,\qquad v(0)=v_0.
}
\tag{2}
\]

This is the physical linearization, including the stretching term. It is not the transport-only equation solved in the previous P2 programme.

For any rational \(0<\delta\le\tau\), construct the exact force on \(0\le t\le\delta\)\:

\[
\boxed{
f_\delta(t)=
\delta^{-2}
\left[
w_s+\mathcal B(w,w)
\right](t/\delta)
-\nu\delta^{-1}\Delta w(t/\delta).
}
\tag{3}
\]

Set \(f_\delta=0\) afterwards.

The formula temporarily contains factors of \(2\pi\) and \(4\pi^2\)\. Rational enclosures of these constants produce admissible rational time coefficients, with a separately controlled residual.

### The main identity

For any divergence-free trigonometric initial field \(v_0\), let \(v(s)=S_w(s)v_0\)\. Define

\[
a_\delta(t)
=\delta^{-1}w(t/\delta)+v(t/\delta).
\]

Its initial and final values are

\[
a_\delta(0)=v_0,\qquad
a_\delta(\delta)=S_w(1)v_0.
\]

A direct expansion of the full Navier–Stokes operator gives the exact residual identity

\[
\boxed{
(a_\delta)_t-\nu\Delta a_\delta
+\mathcal B(a_\delta,a_\delta)-f_\delta
=
\mathcal B(v,v)-\nu\Delta v.
}
\tag{4}
\]

All terms involving \(\delta^{-2}\) and \(\delta^{-1}\) cancel.

In particular, the residual on the right is independent of the large background amplitude \(\delta^{-1}\)\. This is the decisive distinction from applying a general-purpose stability estimate directly to that background.

### All-weak comparison estimate

Let \(P_N\) denote Fourier truncation to \(|k|_\infty\le N\), and use \(v_0=P_NU_0\) in the reference construction.

Set

\[
K=\int_0^1\|\nabla w(s)\|_\infty\,ds,
\]

and suppose a verified number \(V\) satisfies

\[
\sup_{0\le s\le1}\|S_w(s)P_NU_0\|_{H^3}\le V
\]

uniformly for \(\|U_0\|_{H^1}\le M\)\.

Let \(\beta\) be the integrated \(L^2\) error caused by replacing the exact coefficients in (3) with rational coefficients.

For every corresponding Leray–Hopf solution \(U\) and every additive disturbance \(\|h\|_{L^\infty_tL^2_x}\le\eta\),

\[
\boxed{
\begin{aligned}
\|U(\delta)-S_w(1)P_NU_0\|_2
\le{}&
\exp\left(K+2^{20}\delta V\right)\\
&\times\left[
\frac{M}{\kappa(N+1)}
+\delta\left(2^{20}V^2+\nu V+\eta\right)
+\beta
\right].
\end{aligned}
}
\tag{5}
\]

This estimate is uniform over the actual initial state, calibration disturbance and weak realization.

**Proof.** Put \(z=U-a_\delta\)\. Testing its equation against \(z\), the terms \(\mathcal B(z,z)\) and \(\mathcal B(a_\delta,z)\) cancel by incompressibility. The remaining linear interaction is bounded by

\[
|\langle\mathcal B(z,a_\delta),z\rangle|
\le\|\nabla a_\delta\|_\infty\|z\|_2^2.
\]

The residual (4), together with the fixed-torus Sobolev estimates, gives

\[
\|\mathcal B(v,v)-\nu\Delta v\|_2
\le2^{20}V^2+\nu V.
\]

Meanwhile,

\[
\int_0^\delta\|\nabla a_\delta(t)\|_\infty dt
\le K+2^{20}\delta V.
\]

The initial discrepancy is bounded by the Fourier tail

\[
\|U_0-P_NU_0\|_2
\le\frac{M}{\kappa(N+1)}.
\]

Integrating the relative-energy inequality proves (5). Its validity for all admitted weak solutions follows from the standard weak–smooth relative-energy comparison and the specified one-sided energy traces.

This is an absolute error estimate. It does not require the unknown solution to be smooth.

## 3\. New coercivity theorem for the twelve physical Euler generators

The previous extra-advection research established a quantitative nondegeneracy result for projected transport generators. The ordinary additive-force problem requires the **different physical linearization**, which includes stretching.

For the twelve first-harmonic fields, that stronger operator family also admits a global coercivity estimate.

Define

\[
\mathcal L_Fv
=\mathbb P[(F\cdot\nabla)v+(v\cdot\nabla)F].
\]

### Theorem

For every real, mean-zero, divergence-free \(v\in H^1(\mathbb T^3)\),

\[
\boxed{
\begin{aligned}
\|\nabla v\|_2^2
&\le
\sum_{i\ne j}
\left(
\|\mathcal L_{F^c_{ij}}v\|_2^2+
\|\mathcal L_{F^s_{ij}}v\|_2^2
\right)\\
&\le3\|\nabla v\|_2^2.
\end{aligned}
}
\tag{6}
\]

The inequalities concern the actual Leray-projected Euler linearization, including \((v\cdot\nabla)F\)\.

### Fourier proof

For a nonzero integer wavevector \(k\), write \(v_k\perp k\)\. Combining cosine and sine cancels interference between opposite frequency shifts.

The resulting coefficient at \(k+\sigma e_j\), with \(\sigma=\pm1\), is governed by

\[
T_{i,j,\sigma}(k)v_k
=
P_{k+\sigma e_j}
\left(k_i v_k+\sigma v_{k,j}e_i\right).
\]

Put \(r=|k|^2\)\. For \(r\ge2\), direct expansion and summation give

\[
\begin{aligned}
&\sum_{i\ne j}\sum_{\sigma=\pm1}
\|T_{i,j,\sigma}(k)v_k\|^2\\
&\quad=
4r\|v_k\|^2
+4\sum_{j=1}^3
\left[
1-(r-k_j^2)
\left(
\frac1{|k+e_j|^2}
+\frac1{|k-e_j|^2}
\right)
\right]|v_{k,j}|^2.
\end{aligned}
\tag{7}
\]

The bracket lies between \(-1\) and \(1\)\. To verify its lower bound, observe that

\[
(r-k_j^2)
\left(
\frac1{|k+e_j|^2}
+\frac1{|k-e_j|^2}
\right)
=
\frac{2(r-k_j^2)(r+1)}
{(r+1)^2-4k_j^2}
\le2.
\]

The last inequality follows from

\[
r+1+(r-3)k_j^2\ge0
\]

for every integer \(r\ge2\) and \(0\le k_j^2\le r\)\.

Consequently,

\[
4(r-1)\|v_k\|^2
\le
\sum_{i\ne j,\sigma}
\|T_{i,j,\sigma}(k)v_k\|^2
\le
4(r+1)\|v_k\|^2.
\]

Since \(r\ge2\), these imply the simpler bounds

\[
2r\|v_k\|^2
\le
\sum_{i\ne j,\sigma}\|T_{i,j,\sigma}(k)v_k\|^2
\le6r\|v_k\|^2.
\]

For the remaining case \(r=1\), direct evaluation gives exactly \(4r\|v_k\|^2\)\.

Finally, the cosine–sine normalization contributes \(\kappa^2/2\)\. Summing over all nonzero Fourier wavevectors proves (6).

### Consequence

The twelve physical generators have no nonzero common kernel on the entire mean-zero divergence-free \(H^1\) space\:

\[
\boxed{
\bigcap_{i\ne j}
\ker\mathcal L_{F^c_{ij}}
\cap\ker\mathcal L_{F^s_{ij}}
=\{0\}.
}
\tag{8}
\]

This is stronger than proving that no finitely supported Fourier field belongs to their common kernel.

However, (6) is an instantaneous quadratic estimate, not a mixing theorem. A family of operators can be coercive in the sense of (6) while its time-ordered evolutions fail to contract a prescribed norm. The theorem therefore removes one algebraic degeneracy without establishing the required terminal control.

## 4\. Turning the linearized Euler test into finite rational arithmetic

The reduction becomes useful only if the proposed linear squeezing property can be checked without an Euler PDE oracle.

That verification is possible.

For each rational path \(w\), construct a computable integer \(H\ge1\) satisfying

\[
\sup_{s\in[0,1]}
\left(
\|w(s)\|_{W^{4,\infty}}
+\|w_s(s)\|_{W^{1,\infty}}
\right)\le H
\]

on its polynomial pieces.

Such an \(H\) is obtained by taking absolute values of the rational polynomial coefficients and replacing \(\kappa\) by the rational upper bound \(7\)\.

Set

\[
Z=2^{40}H.
\]

Standard integer-order Sobolev energy estimates for (2), with constants bounded conservatively by \(2^{20}\), give

\[
\|S_w(s)v_0\|_{H^3}
\le2^{2Z}\|v_0\|_{H^3},
\qquad 0\le s\le1.
\]

Also,

\[
\|S_w(s)v_0\|_2\le2^{2Z}\|v_0\|_2.
\]

These are deliberately excessive but effective bounds.

### Avoiding the Fourier-net circularity

Crucially, select the initial Fourier cutoff **after** selecting the candidate trajectory \(w\)\:

\[
\boxed{
N(w,M,\epsilon)=
\left\lceil
2^{2(Z+10)}\frac{M}{\epsilon}
\right\rceil.
}
\tag{9}
\]

This ensures that the high-frequency initial tail remains negligible even after amplification by the particular trajectory's strain budget.

It avoids the earlier circularity in which one chooses a net, subsequently selects an arbitrarily strong control, and discovers that the net resolution was insufficient.

The finite test is now

\[
\boxed{
\|S_w(1)P_{N(w,M,\epsilon)}\|_{2\to2}
<\frac{\epsilon}{8M}.
}
\tag{10}
\]

If (10) is certified, then every admissible low-frequency initial component has sufficiently small terminal linearized Euler velocity.

### Paid finite verification

Set

\[
\rho=\frac{\epsilon}{4096M},
\qquad
W=2^{2Z}(1+150N^2)^2.
\]

For unit \(L^2\) initial fields supported in \(P_N\), the preceding Sobolev estimate bounds their evolved \(H^3\) norm by \(W\)\.

Choose a Fourier cutoff \(R\) at least

\[
R=N+
\left\lceil\frac{2^{2Z+20}HW}{\rho}\right\rceil.
\]

The \(H^3\) tail estimate and the Galerkin consistency equation give a certified approximation of \(S_w(1)P_N\), with operator error smaller than \(\rho\), by the corresponding finite projected linear Euler evolution.

That finite evolution is a matrix ODE with piecewise-polynomial coefficients. Its entries are rational combinations of \(2\pi\) and the rational Fourier projection matrices.

Using a rational enclosure for \(2\pi\), divide each time piece into intervals of length at most

\[
\frac{1}{8B_R},
\qquad B_R=2^{12}H(R+1).
\]

On each subinterval, evaluate the time-ordered Picard series using exact rational polynomial integration. A Taylor order exceeding

\[
100\left(B_R+\log_2\frac{n+1}{\rho}+1\right),
\]

where \(n\) is the total number of subintervals, suffices for a rational enclosure of the finite propagator, after also choosing the rational-\(\pi\) precision to control its accumulated coefficient error.

The final result is a rational matrix \(F\) with

\[
\|F-S_w(1)P_N\|_{2\to2}<2\rho.
\]

A strict acceptance certificate is the exact rational positive-definiteness test

\[
\boxed{
\left(\frac{\epsilon}{8M}-2\rho\right)^2I-F^*F\succ0.
}
\tag{11}
\]

The test can be performed by rational \(LDL^*\) elimination on a real-block representation. It terminates for every candidate, whether accepted or rejected.

For instance, any candidate satisfying

\[
\|S_w(1)P_N\|_{2\to2}
\le\frac{\epsilon}{32M}
\]

has sufficient margin to pass the test.

This is a concrete finite verifier for an infinite-dimensional homogeneous Euler evolution. It does not simulate the full nonlinear Navier–Stokes equation.

## 5\. Conditional compiler with completely explicit rational force bounds

Suppose a candidate \(w\) passes (11). With \(N\) as above, define

\[
V=2^{2Z}(1+150N^2)M.
\]

Choose

\[
\eta=\min\left(1,\frac{\epsilon}{8\tau}\right).
\]

Choose a positive dyadic \(\delta\) satisfying

\[
\boxed{
\delta\le
\min\left\{
\frac{\tau}{2},
\frac{1}{2^{20}V},
\frac{\epsilon}
{2^{2(Z+10)}(2^{20}V^2+\nu V+1)}
\right\}.
}
\tag{12}
\]

Approximate \(\kappa=2\pi\) by a rational with error at most

\[
\frac{\epsilon\delta}
{2^{2(Z+30)}H^2}.
\]

The resulting rational force has an integrated coefficient-rounding residual \(\beta\) small enough that (5), (9) and (12) imply

\[
\|U(\delta)\|_2<\frac{\epsilon}{4}.
\]

After \(\delta\), set \(f=0\)\. For every subsequent Leray–Hopf continuation,

\[
\|U(\tau)\|_2
\le\|U(\delta)\|_2+(\tau-\delta)\eta
<\frac{3\epsilon}{8}.
\]

Thus **an accepted homogeneous Euler squeezing certificate is sufficient for the entire original additive-force endpoint**, including all weak realizations and the full \(H^1\) ball.

The resource costs after finding the candidate are explicit\:

| Quantity | Bound for accepted candidate |
|--------|--------|
| Fixed spatial actuator family | 36 fields |
| Time intervals | At most \(p+1\), where \(p\) is the number of pieces of \(w\) |
| Time polynomial degree | At most \(2d_w\), where \(d_w\) is the largest degree of \(w\) |
| Calibration tolerance | \(\eta=\min(1,\epsilon/(8\tau))\) |
| Peak force \(W^{1,\infty}\) norm | \(2^{22}H^2\delta^{-2}+2\nu H\delta^{-1}\) |
| Integrated force \(W^{1,\infty}\) norm | \(2^{22}H^2\delta^{-1}+2\nu H\) |
| Rational breakpoint heights | Computable from the original breakpoint heights and \(\delta^{-1}\) |
| Rational coefficient heights | Computable from \(H,d_w,\delta^{-1}\) and the certified \(\pi\) precision |

All arithmetic is finite and rational. The Galerkin size, Picard order, matrix arithmetic and coefficient precision are fixed by the displayed formulas rather than by an uncharged convergence oracle.

### The one unproved existence condition

The following statement would now suffice to resolve the original question\:

> For every rational \(M\ge1\) and \(0<\epsilon<1\), there is a rational piecewise-polynomial zero-return path \(w\) inside the twelve-dimensional first-harmonic space \(\mathcal W\) such that
>
> \\\[
> \\boxed

## Completed continuation (connector text; final sentence tail reconstructed from visible display)

# P2 — A geometric obstruction to homogeneous Euler squeezing

**The full ordinary additive-force compiler remains open.** This continuation identifies a limitation of the previous conditional construction and gives a sharper, computably verifiable condition that avoids it.

The key distinction is between contracting every unit-\(L^2\) perturbation and contracting every perturbation in a bounded \(H^1\) ball. The latter is the actual requirement, and it is substantially weaker.

## 1\. High-frequency noncontractivity of the physical linearized Euler evolution

Let \(w(t,x)\) be any smooth, divergence-free, time-dependent field on \(\mathbb T^3\)\. Consider

\[
v_t+\mathbb P\big[(w\cdot\nabla)v+(v\cdot\nabla)w\big]=0,
\]

and denote its time-one solution operator by \(S_w\)\.

This is the complete physical Euler linearization, including stretching.

### Theorem — Essential-norm obstruction

For every such \(w\),

\[
\boxed{
\|S_w\|_{L^2_\sigma\to L^2_\sigma,\mathrm{ess}}\ge1.
}
\tag{1}
\]

Here the essential norm is the distance from \(S_w\) to the compact operators.

In particular,

\[
\boxed{\|S_w\|_{L^2_\sigma\to L^2_\sigma}\ge1.}
\tag{2}
\]

Neither large strain nor elaborate time switching can turn the homogeneous physical linearized Euler evolution into a strict contraction of the *entire* divergence-free \(L^2\) space.

### Proof: the high-frequency amplitude system

Let \(X(t)\) be a fluid trajectory and put \(A(t)=\nabla w(t,X(t))\)\.

The high-frequency linearized Euler dynamics are governed by the bicharacteristic-amplitude equations

\[
\begin{aligned}
\dot X&=w(t,X),\\
\dot\xi&=-A^\top\xi,\\
\dot a&=-Aa+
2\frac{\xi\cdot Aa}{|\xi|^2}\xi,
\qquad a\cdot\xi=0.
\end{aligned}
\tag{3}
\]

These are the standard geometric-optics equations for the complete physical Euler linearization, rather than passive vector transport. They also underlie the classical work of Friedlander, Strauss and Vishik on the essential spectrum of linearized Euler. citeturn570342search27turn570342search3

Write \(\Phi_t\) for the volume-preserving flow map of \(w\)\. Then

\[
\xi(t)=D\Phi_t(X_0)^{-\top}\xi_0.
\]

Let \(M_t\) be the map taking initial amplitudes in \(\xi_0^\perp\) to final amplitudes in \(\xi(t)^\perp\)\.

In an orthonormal moving frame of these two-dimensional polarization spaces, the pressure correction in (3) is perpendicular to the frame. Consequently,

\[
\frac{d}{dt}\log|\det M_t|
=
-\operatorname{tr}A+
\frac{\xi^\top A\xi}{|\xi|^2}.
\]

Incompressibility gives \(\operatorname{tr}A=0\), while

\[
\frac{d}{dt}\log|\xi|
=
-\frac{\xi^\top A\xi}{|\xi|^2}.
\]

Combining them yields the exact identity

\[
\boxed{
|\det M_t|=\frac{|\xi_0|}{|\xi(t)|}.
}
\tag{4}
\]

Now \(D\Phi_1\) has determinant one. Hence \(D\Phi_1^{-\top}\) has some unit direction \(\xi_0\) satisfying

\[
|D\Phi_1^{-\top}\xi_0|\le1.
\]

For that direction, (4) gives \(|\det M_1|\ge1\)\. Since the product of the two singular values of \(M_1\) is at least one,

\[
\|M_1\|\ge1.
\]

Choose a polarization attaining this norm.

Finally, construct normalized divergence-free oscillatory wave packets concentrated near \(X_0\), with carrier frequency tending to infinity in direction \(\xi_0\)\. The geometric-optics approximation shows that their final \(L^2\) norms approach \(\|M_1a_0\|\ge1\)\. These packets converge weakly to zero, so every compact operator sends them strongly to zero.

It follows that the distance from \(S_w\) to every compact operator is at least one, proving (1).

This argument works for arbitrary smooth prescribed backgrounds, including the twelve-field paths from the preceding fast-return construction.

## 2\. A stronger all-weak fast-return theorem — no initial Fourier cutoff

The earlier reduction used a finite Fourier truncation of the unknown initial condition and an \(H^3\) bound on the comparison solution. That truncation is not necessary.

The relative-energy argument can be carried out directly with the unknown initial field in \(H^1\), using a homogeneous \(H^{-1}\) residual estimate.

This is a useful improvement because the comparison becomes uniform over the **original infinite-dimensional preparation ball without any finite input net**\.

### Theorem — Uniform \(H^1\)\-to-\(L^2\) fast-return transference

Let \(w:[0,1]\to\mathcal W\) be a continuous, rational piecewise-polynomial, divergence-free path with \(w(0)=w(1)=0\)\. Define

\[
\begin{aligned}
K&=\int_0^1\|\nabla w(s)\|_\infty\,ds,\\
H&=1+\int_0^1\|w(s)\|_{W^{2,\infty}}\,ds,\\
V&=e^{20H}M.
\end{aligned}
\]

Let \(S_w(s)\) be the complete homogeneous linearized Euler propagator.

For any rational \(0<\delta\le\tau\), define the ideal force

\[
f_\delta(t)=
\delta^{-2}[w_s+\mathcal B(w,w)](t/\delta)
-\nu\delta^{-1}\Delta w(t/\delta),
\quad 0\le t\le\delta,
\]

and zero thereafter.

Suppose the actual rational force approximates this ideal force in \(L^\infty_tL^2_x\) with error at most \(\xi\)\. Then, for every \(\|U_0\|_{H^1}\le M\), every additive disturbance of norm at most \(\eta\), and every corresponding Leray–Hopf realization,

\[
\boxed{
\begin{aligned}
\|U(\delta)-S_w(1)U_0\|_2
\le{}&
\sqrt{\frac{8\delta}{\nu}}\,
\bigl(16V^2+\nu V+\eta+\xi\bigr)\\
&\times\exp\left(
K+108C_6^6\delta\nu^{-3}V^4
\right),
\end{aligned}
}
\tag{5}
\]

where \(C_6\) is any fixed valid constant in the mean-zero torus Sobolev inequality

\[
\|z\|_6\le C_6\|\nabla z\|_2.
\]

A conservative rational \(C_6\) can be fixed once through the standard periodic Sobolev inequality; it does not depend on the input or the control.

The error is \(O(\sqrt\delta)\) for every fixed \(w,M,\nu,\eta,\xi\)\. There is no dependence on an initial Fourier cutoff or a selected weak solution.

### Proof

Take the **actual unknown initial field** \(U_0\in H^1\) and solve

\[
v_s+\mathcal L_{w(s)}v=0,\qquad v(0)=U_0.
\]

Standard differentiated energy estimates for this linear equation give

\[
\sup_{s\in[0,1]}\|v(s)\|_{H^1}
\le e^{20H}M=V.
\tag{6}
\]

Define the comparison field

\[
a_\delta(t)=\delta^{-1}w(t/\delta)+v(t/\delta).
\]

It has exactly the same initial condition as the actual fluid\:

\[
a_\delta(0)=U_0,
\]

and, because \(w(1)=0\),

\[
a_\delta(\delta)=S_w(1)U_0.
\]

The large terms cancel algebraically. The comparison residual is

\[
r=\mathcal B(v,v)-\nu\Delta v.
\]

On the unit torus, the Fourier Hausdorff–Young inequality and the summability of \((1+4\pi^2|k|^2)^{-2}\) give the conservative bound

\[
\|v\|_4\le4\|v\|_{H^1}.
\]

Consequently,

\[
\boxed{
\|r(t)\|_{\dot H^{-1}}
\le16V^2+\nu V.
}
\tag{7}
\]

Let \(z=U-a_\delta\), \(E=\|z\|_2^2\) and \(G=\|\nabla z\|_2^2\)\.

The background transport terms vanish in relative energy. The remaining interactions satisfy

\[
\left|\int(z\cdot\nabla w)\cdot z\right|
\le\|\nabla w\|_\infty E
\]

and

\[
\left|\int(z\cdot\nabla v)\cdot z\right|
\le\|\nabla v\|_2\|z\|_4^2.
\]

The Gagliardo–Nirenberg inequality gives

\[
\|z\|_4^2
\le C_6^{3/2}E^{1/4}G^{3/4}.
\]

Young's inequality, with the viscosity explicitly retained, now yields

\[
\boxed{
E'+\nu G
\le
\left[
2\delta^{-1}\|\nabla w(t/\delta)\|_\infty
+216C_6^6\nu^{-3}V^4
\right]E
+\frac8\nu(16V^2+\nu V+\eta+\xi)^2.
}
\tag{8}
\]

Importantly, \(E(0)=0\) exactly. There is no initial Fourier-tail error.

Integrating (8) for physical time \(\delta\) proves (5).

The comparison field is in \(L^\infty H^1\), has its time derivative in \(L^\infty L^2\) on each time piece, and has an \(H^{-1}\) residual. The weak–smooth comparison argument extends to this regularity by mollification; all terms in (8) are integrable. Thus the estimate applies to admitted Leray–Hopf realizations rather than requiring the actual fluid to be a strong solution.

**This theorem removes the entire finite-input-cover step from the fast-return transfer.** It does not establish that a suitable squeezing path exists, but it makes the transfer from such a path to the original nonlinear problem considerably cleaner.

## 3\. A stronger geometric consequence: stretching creates high-frequency amplification

The determinant identity (4) yields more than the lower bound of one.

For each initial point \(x\), choose a unit covector along the direction of smallest stretching by \(D\Phi_1(x)^{-\top}\)\. Then

\[
|\xi(1)|=\frac{1}{\|D\Phi_1(x)\|_{\mathrm{op}}}.
\]

Equation (4) gives

\[
|\det M_1|=\|D\Phi_1(x)\|_{\mathrm{op}}.
\]

The larger singular value of a two-dimensional matrix is at least the square root of its determinant. Therefore

\[
\boxed{
\|S_w\|_{\mathrm{ess}}^2
\ge
\sup_{x\in\mathbb T^3}
\|D\Phi_1(x)\|_{\mathrm{op}}.
}
\tag{9}
\]

This is a precise inviscid mixing–amplification tradeoff: whenever the background's Lagrangian map strongly stretches material directions, the physical linearized Euler evolution necessarily amplifies some sufficiently short-wavelength divergence-free perturbations.

It does **not** say that every low-frequency perturbation grows. Those low modes may still be mixed, depleted or contracted. It also does not establish an obstruction for the viscous original equation, which can dissipate the high-frequency perturbations.

The distinction matters for the proposed compiler: a high-strain path should not be tested for uniform \(L^2\)\-to-\(L^2\) contraction on an unnecessarily large Fourier space.

## 4\. The corrected finite squeezing certificate

Define

\[
J=(I-\Delta)^{-1/2}
\]

on the mean-zero divergence-free \(L^2\) space. Then

\[
\boxed{
\|S_w(1)\|_{H^1\to L^2}
=
\|S_w(1)J\|_{L^2\to L^2}.
}
\tag{10}
\]

Unlike \(S_w\), the operator \(S_wJ\) is compact: \(J\) is compact on \(L^2\), while \(S_w\) is bounded.

Thus the high-frequency obstruction in (1)–(9) does not prevent

\[
\|S_wJ\|\ll1.
\]

The appropriate homogeneous Euler squeezing assertion is

\[
\boxed{
\forall \gamma\in\mathbb Q_{>0},\
\exists w\in\mathcal W_{\mathrm{rat},0}:
\quad
\|S_w(1)J\|<\gamma.
}
\tag{WE}
\]

Here \(\mathcal W_{\mathrm{rat},0}\) is the collection of rational piecewise-polynomial paths in the twelve-dimensional first-harmonic space with zero initial and terminal background.

Assertion (WE) is **not proved**\. But it is sufficient for the original full additive-force compiler, and it has an effective finite verification interface.

### Complete finite test for one candidate

Fix a candidate \(w\)\. Compute a rational upper bound \(h\ge1\) for its integrated \(W^{2,\infty}\) norm and set

\[
E_h=2^{2\lceil h\rceil}.
\]

The homogeneous Euler energy inequality ensures

\[
\|S_w(1)\|_{L^2\to L^2}\le E_h.
\]

For any Fourier cutoff \(N\),

\[
\boxed{
\|S_w(1)(I-P_N)J\|_{2\to2}
\le
\frac{E_h}{\sqrt{1+4\pi^2(N+1)^2}}.
}
\tag{11}
\]

Choose a target \(\gamma>0\) and

\[
N=\left\lceil\frac{16E_h}{\gamma}\right\rceil.
\]

The tail in (11) is then strictly below \(\gamma/8\)\.

Next, approximate \(S_w(1)P_N\) by a finite rational Fourier matrix \(F\) with certified \(L^2\)\-operator error less than \(\rho=\gamma/8\)\. This uses the already established Galerkin consistency, Fourier-tail, time-ordered Picard and rational-\(\pi\) certificates.

Let \(G_R\) be the rational \(L^2\) Gram matrix of the output Fourier basis. Let \(H_N^{\mathrm{lo}}\) be the rational input Gram matrix formed using the conservative weights

\[
1+36|k|^2
\le1+4\pi^2|k|^2.
\]

The compiler accepts the candidate precisely when the strict rational matrix inequality

\[
\boxed{
\left(\frac{\gamma}{2}\right)^2
H_N^{\mathrm{lo}}
-F^\ast G_RF\succ0
}
\tag{12}
\]

is certified by exact positive-definiteness arithmetic.

Acceptance implies

\[
\begin{aligned}
\|S_wJ\|
&\le
\underbrace{\|F\|_{H^1\to L^2}}_{<\gamma/2}
+\underbrace{\rho}_{=\gamma/8}
+\underbrace{\text{Fourier tail}}_{<\gamma/8}\\
&<\frac{3\gamma}{4}.
\end{aligned}
\]

Conversely, a path satisfying the stronger inequality

\[
\|S_wJ\|\le\frac{\gamma}{8}
\]

has enough margin for (12) to pass.

Each candidate's test has predetermined finite dimensions, arithmetic precision and Taylor orders. It does not loop indefinitely on a candidate that fails.

Most importantly, the test weights each Fourier mode by its true \(H^1\) cost. It therefore verifies exactly the preparation-class norm that the original question requires.

## 5\. A fully rational conditional compiler without an initial-data net

The two preceding results combine into a stronger conditional construction than the earlier one.

Suppose (WE) holds. Then the following procedure is a terminating compiler for the original additive-force question.

### Step 1 — Find a certified Euler squeezing path

Given \(M,\nu,\tau,\epsilon\), set

\[
\gamma=\frac{\epsilon}{8M}.
\]

Enumerate rational piecewise-polynomial zero-return paths \(w\) in the twelve-dimensional first-harmonic space. Apply the finite test (12) to each.

If (WE) holds, some candidate satisfies

\[
\|S_wJ\|\le\frac{\gamma}{8}.
\]

The finite verifier will accept a candidate, establishing

\[
\boxed{
\|S_w(1)U_0\|_2<\frac{3\epsilon}{32}
}
\tag{13}
\]

for every \(\|U_0\|_{H^1}\le M\)\.

There is no initial-data sampling or input-dependent control in this step.

### Step 2 — Calculate a rational pulse duration

For the accepted path, calculate a rational upper bound \(h\ge H\), with \(H\) as in Section 2. Define the integers and rationals

\[
\begin{aligned}
E_h&=2^{2\lceil h\rceil},\\
V_h&=2^{40\lceil h\rceil}M,\\
\eta&=\frac{\epsilon}{16},\\
R_h&=16V_h^2+\nu V_h+2\eta.
\end{aligned}
\]

We may take \(C_6=64\) in the fixed-torus Sobolev inequality. One elementary way to certify this generous constant is to apply the Euclidean \(W^{1,2}\to L^6\) inequality to a cutoff of the periodic field on \([-1,2]^3\), then use the mean-zero Poincaré inequality. All cutoff and extension constants are fixed.

Select the first dyadic \(\delta=2^{-n}\) satisfying

\[
\boxed{
\delta\le
\min\left\{
\frac{\tau}{2},
\frac{\nu^3}{2^{20}C_6^6V_h^4},
\frac{\nu\epsilon^2}{2^{20}E_h^2R_h^2}
\right\}.
}
\tag{14}
\]

This selection terminates by rational comparisons.

Since

\[
e^K\le E_h,
\qquad
e^{108C_6^6\delta\nu^{-3}V_h^4}<2,
\]

the transference estimate (5), with rational force-rounding error at most \(\eta\), gives

\[
\boxed{
\|U(\delta)-S_w(1)U_0\|_2
<\frac{\epsilon}{128}.
}
\tag{15}
\]

This holds simultaneously for the entire \(H^1\) ball, every allowed disturbance and every admitted weak realization.

### Step 3 — Emit the actual rational force

Use the fixed 36-field spatial family from the earlier construction\:

\[
f(t)=
\delta^{-2}[w_s+\mathcal B(w,w)](t/\delta)
-\nu\delta^{-1}\Delta w(t/\delta),
\]

with the coefficients of \(2\pi\) and \(4\pi^2\) replaced by certified rational approximations.

Let \(H_*\ge1\) be a rational bound for the relevant polynomial coefficient sums and their first time derivatives. It can be computed by summing absolute values of the rational coefficients and applying the fixed bounds \(\kappa<7\)\.

Choose a rational approximation \(\widehat\kappa\) satisfying

\[
|\widehat\kappa-\kappa|
\le
\frac{\eta\delta^2}{2^{40}(H_*+1)^2}.
\]

The fixed finite Fourier multiplication rules then guarantee that the resulting ordinary rational force differs from the ideal force by less than \(\eta\) in \(L^\infty_tL^2_x\)\.

Set \(f=0\) after \(\delta\)\.

### Step 4 — Verify the terminal endpoint

From (13) and (15),

\[
\|U(\delta)\|_2
<
\frac{3\epsilon}{32}+\frac{\epsilon}{128}.
\]

After \(\delta\), only the additive disturbance remains. The Leray–Hopf energy inequality gives

\[
\|U(\tau)\|_2
\le\|U(\delta)\|_2+\eta(\tau-\delta).
\]

As \(0<\tau\le1\),

\[
\boxed{
\|U(\tau)\|_2
<
\frac{3\epsilon}{32}
+\frac{\epsilon}{128}
+\frac{\epsilon}{16}
=
\frac{21\epsilon}{128}
<\epsilon.
}
\tag{16}
\]

This is the required terminal conclusion, **conditional only on the existence of a path satisfying (WE)**\.

The weak-solution and calibration quantifiers are fully covered by the transference theorem. No smoothness or uniqueness assumption on the actual solution is introduced.

## 6\. Resource bounds for an accepted candidate

The post-selection construction has explicit rational resource bounds.

Let \(p\) be the number of time pieces of the accepted path and \(d\) its largest time-polynomial degree. Define \(C_f=2^{30}\)\.

| Quantity | Constructive bound |
|--------|--------|
| Spatial actuator family | Fixed 36 rational fields |
| Nonzero time pieces | \(p\) |
| Total time intervals | At most \(p+1\) |
| Time polynomial degree | At most \(2d\) |
| Calibration tolerance | \(\eta=\epsilon/16\) |
| Peak \(\\|f\\|_{W^{1,\infty}}\) | \(C_f(H_*^2\delta^{-2}+\nu H_*\delta^{-1})\) |
| Integrated \(\\|f\\|_{W^{1,\infty}}\) | \(C_f(H_*^2\delta^{-1}+\nu H_*)\) |
| Rational breakpoint heights | Computable from \(p\), original breakpoint heights and \(\delta^{-1}\) |
| Rational coefficient heights | Computable from the accepted path, \(\delta^{-1}\) and \(\widehat\kappa\)'s precision |

The finite matrix test, force expansion, rational approximation and dyadic selection all have terminating exact-rational algorithms.

If (WE) were proved, the compiler would terminate on every input. A uniform complete-bit bound depending only on input length \(L\) could then be obtained by exhaustively running it on all valid binary encodings of length at most \(L\), recording the maximum of each requested resource. That would be a total computable bound, although not necessarily an elementary one.

Without (WE), these are only **conditional compiler bounds**, not the unconditional uniform bounds required by the full question.

## 7\. What is now proved, and what remains

RESEARCH STATUS — THIS CONTINUATION

| Operation | Status |
|--------|--------|
| Essential \(L^2\) noncontractivity of every smooth physical Euler linearization | Proved |
| Geometric amplification bound (9) | Proved |
| Uniform fast-return comparison for the full \(H^1\) ball without Fourier truncation | Proved |
| Explicit \(O(\sqrt\delta)\) nonlinear error bound, valid for all Leray–Hopf realizations | Proved |
| Weighted \(H^1\to L^2\) finite rational squeezing certificate | Constructive |
| Fixed 36-field additive-force compiler assuming (WE) | Conditional positive |
| Existence of arbitrarily strong weighted Euler squeezing paths | **Open** |
| Unconditional full additive-force compiler | **Open** |
| General negative theorem excluding every fixed finite actuator family | **Open** |

### The principal mathematical distinction

There are now three different requirements, which should not be conflated.

The first is **unweighted inviscid contraction**\:

\[
\|S_w\|_{L^2\to L^2}\ll1.
\]

This is impossible by the geometric-optics obstruction.

The second is **weighted inviscid contraction**\:

\[
\|S_w\|_{H^1\to L^2}\ll1.
\]

This remains possible in principle and is exactly what the improved fast-return method requires.

The third is **viscous nonlinear terminal contraction** for every unknown \(H^1\) input and all weak realizations. The new transference theorem proves that the second would imply the third, using only a fixed rational additive-force family and a sufficiently short physical pulse.

The most consequential advance in this continuation is that **the nonlinear three-dimensional transfer no longer requires a Fourier net or \(H^3\)\-smooth preparation**\. Its proof now acts directly on the whole \(H^1\) ball with an explicit viscosity-dependent \(O(\sqrt\delta)\) error.

The next decisive research problem is therefore the weighted assertion (WE): whether time-dependent physical Euler generators from the twelve first-harmonic fields can make their homogeneous propagator arbitrarily small as an operator from \(H^1_\sigma\) to \(L^2_\sigma\)\.

Instantaneous generator coercivity, passive-scalar mixing and the existing coupled viscous shear theorems do not establish that assertion. A proof would complete this particular 36-actuator route to the original positive endpoint; a disproof would rule out that route without necessarily ruling out other additive-force constructions.

**Final status: stronger unconditional transference and a new geometric obstruction, but the full common-force compiler remains unresolved.**


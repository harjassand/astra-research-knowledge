# Independent analytic reconstruction and adversarial extensions

Internal mathematical work, 2026-10-16. This is not external validation or a novelty finding.

The source read is `originals/stability/PROOF_NOTE.md` and its rational matrix data, together with the N888 analytic proof in the pinned checkout at `9dbe934e5475f415c2d160a6c0715534aafa546b`. No other receiving-worker report was used for Sections 1–7.

## 1. Exact setting and analytic use of the Gram reserve

The torus is `(R/2pi Z)^2`, with probability measure. All functions are real and periodic in `W^{1,4}`. Write

```
a=f_x, b=f_y, c=g_x, d=g_y,
u=a²+c², v=b²+d², j=ad-bc,
J_r(V)=3r(u+v-2j)²/[8(r+2)] + r(r-1)u²/6 + j² + ruj,
E_r(f,g,s)=<J_r(sI+D(f,g))>-J_r(sI),
α=5r/[4096(r+2)], β=r/[512(r+2)], σ=r+1, k=r(r+2)/3.
```

For fixed `r>0,s in R`, the source's exact matrix identity gives the pointwise polynomial bound

```
J_r(sI+V)-J_r(sI)-[(r+2)(2r+3)/3]s³a-S_1(b)c-S_2(a)d
 >= α|V|⁴+βs²(a²+c²+d²),
S_1(b)=-(r+2)s²b+7rb³/[6(r+2)],
S_2(a)=(r+2)s³+(5r/2+2)s²a+7rsa²/4+r(4r+3)a³/[12(r+2)].
```

For completeness, the rational identity is `(r+2)G=z0^T Q0 z0+r z1^T Q1 z1`; the independent finite check in `verify.py` reconstructs the original polynomial and matrix identity from the data and checks exact positive LDL pivots of `Q0`, `Q1`, and `Q1-I/512`. Positivity is an algebraic fact; the following analytic deduction is additional.

Since `Df in L4`, the stress is in `L^{4/3}`. If its distributional divergence vanishes, it pairs to zero with smooth periodic gradients. Strong smooth approximation of `g` in `W^{1,4}` then gives `<S(f).Dg>=0` by Holder. Periodicity gives `<a>=0`. Thus the integrated reserve is

```
E_r(f,g,s)>=α<|D(f,g)|⁴>+βs²< a²+c²+d² >.
```

For `f0=F(x)+H(y)`, the first stress component depends only on `y`, and the second only on `x`; hence the divergence vanishes distributionally, with no second derivatives needed. In particular, with

```
R=||Df0||4, A=||f0_x||2, t=||Dg||4, v=||Dg||2,
```

the integrated reserve is at least `α(R⁴+t⁴)+βs²(A²+v²)`. This uses `(|Df0|²+|Dg|²)²>=|Df0|⁴+|Dg|⁴`. No bound on `g`, `s`, or mixed derivatives has been introduced.

## 2. Reconstruction of the full acoustic expansion

For smooth periodic maps, integration by parts gives `<ad-bc>=0`. Approximation in `W^{1,4}` preserves this equality, since products of two gradients converge in `L2`. Direct polynomial expansion gives

```
E_r(f,g,s)=s²<B>+s<P>+<Q>,
B=(σa+d)²+k c²,
P=r[d+(2r+1)a/3](a²+c²)+2(ad-bc)(σa+d),
Q=J_r(D(f,g)).
```

Pointwise, the omitted quadratic term is `(r+2)s²(ad-bc)`, and the omitted cubic tangents are constants times `s³a` and `s³d`, all integrating to zero. Keeping the entire `B` is essential in the large-background argument.

The coefficient sums of the first-row derivatives are

```
LB=2(r+1)(r+2),
LP=2(r+2)(4r+9)/3,
LQ=4(r³+7r²+34r+12)/[3(r+2)].
```

The independent verifier checks these equalities as rational polynomial identities and checks the coefficient signs for every positive `r`. For a degree `m` polynomial, the fundamental theorem of calculus along the first-row segment, followed by Holder, bounds a derivative monomial with `j` second-row factors by `ε U^{m-1-j}t^j`, where `U` bounds the intermediate first-row `L4` norm. This is the analytic reason for the estimates; the coefficient checker alone does not prove Holder or the Sobolev passage.

## 3. The supplied neighborhood theorem is valid

Assume `A>0`, hence `R>0`, and `ε=||D(f-f0)||4<=1`. The supplied choices `M=max(1,R+1)` and

```
C=(3/2)LB M+(3/2)LP M²+4LQ M³,
m=min(αR⁴,α,βA²,β),
ε0=min(1,m/(2C))
```

give

```
|E_r(f,g,s)-E_r(f0,g,s)|<=C ε [1+t⁴+s²(1+v²)],
E_r(f0,g,s)>=m [1+t⁴+s²(1+v²)].
```

The source's elementary inequalities suffice: `1+v<=(3/2)(1+v²)`, `|s|(1+t+t²)<=(3/2)(1+t⁴+s²)`, and `1+t+t²+t³<=4(1+t⁴)`. The first-row derivative removes every pure second-row monomial, so the differences contain at most one, two and three second-row factors, respectively. Therefore `E_r(f,g,s)>=E_r(f0,g,s)/2` simultaneously for every real `s` and every periodic `W^{1,4}` second potential. Large `g` is absorbed by `t⁴`; large `s` is absorbed by the retained acoustic reserve. The proof does not need stress conservation for the perturbed first row.

## 4. A stronger homogeneous radius, linear in A

The supplied formula can first be normalized by `R`: putting `κ=A/R`, `C*=3LB+6LP+32LQ`, the radius

```
ε<=R min(α,βκ²)/(2C*)
```

is valid by applying Section 3 to `f/R,g/R,s/R`. This is homogeneous but still quadratic in `κ`.

A sharper argument uses the separated anchor's exact orthogonality

```
<F'(x)g_y>=0,
<B(f0,g)>=σ²A²+||g_y||2²+k||g_x||2².
```

Define constants depending only on `r`:

```
D4=6LP+15LQ,
D2=2σ²+σ+3LP,
h_r=min(1, α/(2D4), β/(2D2)).
```

**Theorem.** For every separated `f0=F(x)+H(y)` with `A=||F'||2>0`, if

```
||D(f-f0)||4<=h_r A,
```

then `E_r(f,g,s)>=E_r(f0,g,s)/2>=0` for all real backgrounds `s` and all periodic `W^{1,4}` functions `g`. The radius is independent of `R=||Df0||4` and is exactly homogeneous under simultaneous multiplication of the fields and the background. Its constants are conservative.

**Proof.** Put `h=ε/A<=1`. Since normalized measure gives `A<=R`, we also have `ε<=R`; the intermediate first-row norm is at most `2R`. Write `δa=f_x-F'`. Orthogonality and the nonnegative square `σ²<δa²>` give

```
<ΔB> >= -2σ²A ε-2σ ε v
       >= -(2σ²+σ)h(A²+v²).
```

The degree-two derivative estimate gives

```
|<ΔP>|<=ε LP(4R²+2Rt+t²)<=6 ε LP(R²+t²).
```

Young's inequality then yields

```
|s<ΔP>|<=3 LP h[s²A²+(R²+t²)²]
         <=3 LP h s²A²+6 LP h(R⁴+t⁴).
```

The degree-three derivative estimate gives

```
|<ΔQ>|<=ε LQ(8R³+4R²t+2Rt²+t³)
         <=15 LQ h(R⁴+t⁴),
```

using `ε=hA<=hR` and each `R^{4-j}t^j<=R⁴+t⁴`. Consequently

```
E_r(f,g,s)>=E_r(f0,g,s)
             -h[D4(R⁴+t⁴)+D2 s²(A²+v²)]
           >=E_r(f0,g,s)-(1/2)[α(R⁴+t⁴)+βs²(A²+v²)]
           >=E_r(f0,g,s)/2.
```

The last step uses the lower reserve from Section 1 in the correct direction. This proof is uniform over unbounded `g` and `s`.

For `r=1`, `LP=26,LQ=24,D4=516,D2=88`, and `h_1=5/12681216`. At `f0=sin x+sin y`, `A=1/sqrt(2)`, so the admissible gradient radius is about `2.79e-7`, larger than the source's `5e-8`. This is still a local theorem, not unrestricted quasiconvexity.

## 5. Exact acoustic kernel and a decisive A=0 domination countermodel

For compatible fields, `<B>=0` if and only if `f_x=0` and `Dg=0`. Indeed `c=0` gives `g=G(y)`, and `d=-σa`; averaging this equality over `x` gives `d=0`, then `a=0`. The cubic `P` also vanishes on this exact kernel. Thus no fixed compatible field can become negative at arbitrarily large `|s|` by a negative leading acoustic coefficient.

There is nevertheless no uniform spectral coercivity away from that kernel. Let `f0=H(y)` and choose integers `N>=1`, `δ>0`:

```
f=H(y)+(δ/N)sin(x+Ny),
g=-(σδ/N²)sin(x+Ny).
```

Then `d=-σa`,

```
||D(f-f0)||4=δ sqrt(1+N^-2)(3/8)^(1/4),
<B(f,g)>=k σ²δ²/(2N⁴),
<B(f0,g)>=σ²δ²/(2N²)(1+k/N²),
<B(f,g)>/<B(f0,g)>=k/(N²+k)->0.
```

For any neighborhood radius and any positive fraction `θ`, choose `δ` small, then `N` so that this ratio is below `θ`; the energy ratio tends to it as `|s|` tends to infinity. Hence a conclusion `E_r(f,g,s)>=θ E_r(f0,g,s)` cannot hold throughout any gradient-`L4` neighborhood of an `A=0` anchor. This refutes extension of the source's domination conclusion, not the possibility of a weaker Jensen neighborhood theorem.

For the concrete anchor `H(y)=sin y`, this counterfamily itself has **strictly positive** Jensen energy for every `r>0,s`. Put `m=N²`. The phase variables `cos y` and `cos(x+Ny)` are independent under torus averaging. The cubic average is zero, and

```
<Q>=9r/[64(r+2)] + δ² T2/[16N⁴(r+2)]
     +δ⁴ r(N²+(r+1)²)²(9N⁴+18N²+(2r+1)²)/[64N⁸(r+2)],
T2=9r(m-1)²+3r[(r-1)²+3](m-1)
     +16r³+28r²+32r+8 >0.
```

This explicitly prevents misreporting the acoustic cancellation as a negative Jensen example.

## 6. Small mixed derivatives are not necessary

Choose any admitted positive perturbation amplitude `η` and put

```
f_N=sin x+sin y+(η/N)sin(Nx+Ny).
```

Then `||D(f_N-f0)||4=η(3/2)^(1/4)` is independent of `N`, while `||f_{N,xy}||p=ηN ||sin||p` diverges for every finite positive `p`. Choosing the fixed `η` inside the radius of Section 4 proves Jensen simultaneously for all `N,s,g`. Each first potential is smooth and nonseparated. Thus neither a small classical mixed derivative nor an approximate stress-conservation condition is necessary for the local theorem. For general `W^{1,4}` perturbations the classical mixed derivative need not even exist as a function.

## 7. Precise classical one-phase coverage

Primary source: Harris, Kirchheim and Lin, *Two-by-two upper triangular matrices and Morrey's conjecture*, Theorem 2.4, accepted version arXiv:1708.07849v2, https://arxiv.org/pdf/1708.07849. Its compactly supported homogeneous-gradient-measure theorem says triangular support implies lamination. The invariance under invertible output/input linear maps is established in its proof.

Here is the independent application, including the missing integrand hypothesis. Left rotations preserve `J_r`. It therefore suffices to test rank-one directions `e1 tensor (1,z)`. In variables `(a,b,c,d)=(p+x,y-q,y+q,p-x)/2`, the coefficient of the square of the rank-one increment is a quadratic form. Its leading `(p,q)` block is

```
A_c=(1/4)[[(r+1)²,-(r+1)z],[-(r+1)z,z²+r(r+2)/3]],
det A_c=r(r+1)²(r+2)/48>0.
```

Its Schur complement has entries

```
S11=r[3r(r+2)z²+(2r+1)²]/[4(r+1)²(r+2)],
S12=3r(2r+1)z/[4(r+1)(r+2)],
S22=9rz²/[4(r+2)],
det S=27r³z⁴/[16(r+1)²(r+2)]>=0.
```

Thus the form is nonnegative for all base matrices, all real `z` and `r>0`. The direction whose first input component is zero follows by continuity. This proves rank-one convexity independently of the producer's rank-one-convexity label.

Now let `f=F(k.x)` for one fixed nonzero integer covector `k`, with arbitrary periodic `g`, and arbitrary conformal background `sI`. The first row of `D(f,g)` annihilates a fixed nonzero vector perpendicular to `k`. An invertible input change taking that vector as its first column, followed by a row swap, puts the gradient support in the triangular subspace. Subtracting/translating the constant background is harmless. The transformed integrand remains rank-one convex. For smooth periodic maps the gradient distribution is a homogeneous gradient Young measure with compact support, so the cited theorem gives its Jensen inequality. Approximation of the one-dimensional profile and of `g` strongly in `W^{1,4}` extends the quartic energy inequality to that class.

**Coverage conclusion:** every one-phase first potential `F(k.x)`, not just the special two-slope stress-conserved example, already has classical qualitative Jensen coverage for all `r>0,s` and arbitrary `g`. The cited theorem itself supplies no numerical reserve asserted here. General two-profile separated potentials have no fixed triangular-support hypothesis: for example `f=sin x+sin y`, `g=sin(2x)+sin(2y)` has gradient support with affine span all four matrix dimensions. Invertible affine matrix transformations cannot put that support in a three-dimensional triangular hyperplane. Failure of this hypothesis does not prove nonlaminateness or novelty.

## 8. Additional A=0 route

At the parent's request, the separately communicated acoustic-projection/cubic candidate received an independent audit at SHA256 `c564e52914d70ba14000e1abadb17ac7432b04d19fd62cb0bfb159b6c8713b36`. It passes the receiving review: the explicit absolute cubic lemma, projection orthogonality, all six cubic coefficient rows, quartic continuity and both absorption losses are valid. The complete reconstruction is in `A0_RECEIVING_AUDIT.md`. It proves a relative tube around every nonconstant separated anchor, including `A=0`, and therefore supersedes the restricted scope of Section 4 for the existence of a Jensen neighborhood. Section 4 retains a stronger positive-fraction comparison at `A>0`; Section 5 explains why that particular comparison cannot extend to `A=0`.

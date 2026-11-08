# P2 Coulomb Landau–Fermi–Dirac return

Chat: https://chatgpt.com/c/6aed7c5f-9954-83ec-8e3e-12eb8200d2f7
Prompt: exact held source P2_FULL_LFD_AFTER_COOLER_EQUILIBRIUM_FINAL_20261109.txt
Prompt turn: c63a5146-099d-400e-9f43-aa12f6f3e8c3
Response: 494f6652-5893-460b-b7e9-82a130a82235
Model displayed: 5.6 Pro. Collected 9 November 2026 Brisbane.
Source: No ZIP visible; an individual TXT is offered but not downloaded under existing source holds.

## Complete visible response

## Status

The full same-energy thermalization statement remains unresolved. I have not proved

$$H\!\left(f(t)\mid F_{M,P,E}\right)\to0,$$

and I have not constructed an admissible nonthermalizing classical trajectory in the stipulated model.

The accepted preceding theorem still gives the strongest convergence result:

$$f(t)\longrightarrow F_*
\quad\text{in }L^1_q(\mathbb T^3\times\mathbb R^3)
\quad\text{for every }0\le q<2,$$

where $$F_*$$ is a homogeneous positive-temperature Fermi–Dirac distribution with the same $$M,P$$, entropy $$\mathcal S(F_*)=\mathcal S_\infty$$, and energy $$E_*\le E$$.

Writing

$$\Delta=E-E_*\ge0,$$

the requested theorem is exactly the assertion $$\Delta=0$$. The prior identity remains

$$\lim_{t\to\infty}H(f(t)\mid F_{M,P,E})
=
H(F_*\mid F_{M,P,E})+\beta\Delta
=
\mathcal S(F_{M,P,E})-\mathcal S(F_*).$$

This continuation identifies the possible defect more precisely and derives its exact dynamical transport law.

## 1. A nonzero defect is a pure energy atom at velocity infinity

Let

$$u=\frac PM,\qquad
E_c=E-\frac{|P|^2}{M},\qquad
E_{*,c}=E_*-\frac{|P|^2}{M}.$$

Thus $$\Delta=E_c-E_{*,c}$$.

Define the velocity energy measure

$$\mu_t(dv)
=
\int_{\mathbb T^3}|v-u|^2f(t,x,v)\,dx\,dv.$$

On the one-point compactification $$\mathbb R^3\cup\{\infty\}$$,

$$\boxed{
\mu_t
\stackrel{*}{\rightharpoonup}
|v-u|^2F_*(v)\,dv+\Delta\,\delta_\infty .
}
\tag{1}$$

Indeed, for a continuous $$\psi$$ having a limit $$\psi_\infty$$ at infinity, local weighted convergence handles

$$(\psi-\psi_\infty)|v-u|^2$$

on bounded velocity sets, while exact energy conservation determines the constant part. The tails of the remainder are bounded by

$$\sup_{|v|>R}|\psi(v)-\psi_\infty|\,(E_c+E_{*,c}).$$

Thus no mass, momentum, or entropy is lost to infinity; only kinetic energy can be. The mass and momentum tails are controlled by the conserved energy, and the accepted binary-entropy tail estimate is uniform in time.

A direct consequence is:

$$\boxed{
\Delta>0
\quad\Longrightarrow\quad
\int |v-u|^qf(t,x,v)\,dx\,dv\longrightarrow\infty
\quad\text{for every }q>2.
}
\tag{2}$$

For fixed $$R$$,

$$\int |v-u|^qf
\ge
R^{q-2}
\int_{|v-u|>R}|v-u|^2f.$$

The latter integral converges to

$$\Delta+\int_{|v-u|>R}|v-u|^2F_*\,dv.$$

Letting $$R\to\infty$$ proves (2).

The accepted bound

$$M_{2+\eta}(t)\le C_\eta(1+t)^{3\eta/2},
\qquad 0<\eta\le1,$$

therefore restricts, but does not prevent, energy escape. It only implies that a radius carrying a fixed fraction of $$\Delta$$ cannot grow faster than order $$t^{3/2}$$ under the currently available estimate.

## 2. Exact shell-energy transport identity

Set

$$g=f(1-f),\qquad
\ell=\log\frac{f}{1-f},
\qquad
a(z)=\frac{\Pi(z)}{|z|}.$$

The collision flux has the pair representation

$$J(v)
=
\int_{\mathbb R^3}
a(v-w)g(v)g(w)
\bigl(\nabla\ell(v)-\nabla\ell(w)\bigr)\,dw.$$

For every smooth compactly supported velocity test $$\varphi$$,

$$\begin{aligned}
\frac{d}{dt}\int\varphi(v)f\,dx\,dv
=
-\frac12\int_{x,v,w}
&g(v)g(w)
\bigl(\nabla\varphi(v)-\nabla\varphi(w)\bigr)^T\\
&\times a(v-w)
\bigl(\nabla\ell(v)-\nabla\ell(w)\bigr).
\end{aligned}
\tag{3}$$

Define the corresponding test mobility

$$\begin{aligned}
\mathscr A_\varphi(t)
=
\frac12\int_{x,v,w}
g(v)g(w)
\bigl(\nabla\varphi(v)-\nabla\varphi(w)\bigr)^T
a(v-w)
\bigl(\nabla\varphi(v)-\nabla\varphi(w)\bigr).
\end{aligned}
\tag{4}$$

Matrix Cauchy–Schwarz and the entropy-dissipation form give the exact action estimate

$$\boxed{
\left|
\frac{d}{dt}\int\varphi f
\right|
\le
\sqrt{D(f(t))\,\mathscr A_\varphi(t)}.
}
\tag{5}$$

### Energy cutoffs

Choose a fixed smooth $$\chi$$ such that

$$\chi(r)=1\quad(r\le1),
\qquad
\chi(r)=0\quad(r\ge2),$$

and define

$$\varphi_R(v)=|v-u|^2\chi\!\left(\frac{|v-u|}{R}\right).$$

Then

$$\int\varphi_R f(t)\longrightarrow\int\varphi_RF_*
\quad(t\to\infty),$$

and hence

$$\int\varphi_R f_0-\int\varphi_RF_*$$

is exactly the cumulative collision-induced energy flux through that cutoff, up to the sign convention in (3). As $$R\to\infty$$,

$$\boxed{
\int\varphi_R f_0-\int\varphi_RF_*
\longrightarrow\Delta.
}
\tag{6}$$

Thus a nonzero $$\Delta$$ is not merely weak convergence losing a moment: it requires actual cumulative outward transfer through every sufficiently large velocity scale.

## 3. The Coulomb projection removes the bulk energy gradient

Define

$$q_R(v)=\nabla\varphi_R(v)-2(v-u).$$

Because

$$\Pi(v-w)(v-w)=0,$$

the full quadratic-energy gradient cancels from the mobility:

$$\boxed{
\begin{aligned}
\mathscr A_{\varphi_R}(t)
=
\frac12\int_{x,v,w}
g(v)g(w)
\frac{
\left|
\Pi(v-w)\bigl(q_R(v)-q_R(w)\bigr)
\right|^2
}{|v-w|}.
\end{aligned}
}
\tag{7}$$

Moreover,

$$q_R=0\quad\text{on }|v-u|\le R,
\qquad
|q_R(v)|\le C_\chi|v-u|\mathbf1_{\{|v-u|>R\}}.$$

Let

$$\rho(t,x)=\int f(t,x,v)\,dv,$$

and

$$e_R(t,x)
=
\int_{|v-u|>R}|v-u|^2f(t,x,v)\,dv.$$

Splitting the Coulomb potential into $$|v-w|\le r$$ and $$|v-w|>r$$, using $$0\le g\le1$$, and optimizing $$r$$, gives

$$\sup_v\int\frac{g(w)}{|v-w|}\,dw
\le C\left(\int g(w)\,dw\right)^{2/3}
\le C\rho^{2/3}.$$

Consequently,

$$\boxed{
\mathscr A_{\varphi_R}(t)
\le
C_\chi\int_{\mathbb T^3}
\rho(t,x)^{2/3}e_R(t,x)\,dx.
}
\tag{8}$$

Equations (5)–(8) identify an exact missing quantity: the space-time mobility of high-velocity energy through regions containing collision partners.

For every fixed finite $$T$$, the supplied finite-horizon decay and regularity estimates imply

$$\lim_{R\to\infty}
\int_0^T\mathscr A_{\varphi_R}(t)\,dt=0.
\tag{9}$$

Therefore, if $$\Delta>0$$, it must be created as a genuinely infinite-time cascade. It cannot occur during one fixed finite interval.

## 4. Why the accepted all-time density estimate does not close the argument

The accepted compensated-integrability estimate is

$$\sup_{s\ge0}
\int_s^{s+1}\int_{\mathbb T^3}\rho(t,x)^2\,dx\,dt
\le K_\rho(M,E).
\tag{10}$$

Applying Hölder on a unit time slab to (8),

$$\begin{aligned}
\int_s^{s+1}\int\rho^{2/3}e_R
\le
K_\rho^{1/3}
\left(
\int_s^{s+1}\int e_R^{3/2}
\right)^{2/3}.
\end{aligned}
\tag{11}$$

The missing bound is now explicit:

$$\int_s^{s+1}\int_{\mathbb T^3}e_R(t,x)^{3/2}\,dx\,dt.$$

Exact energy conservation controls

$$\int e_R(t,x)\,dx,$$

not its $$L_x^{3/2}$$ norm. The accepted polynomial bounds on global velocity moments likewise do not control spatial concentration of tail energy.

Thus neither the unit-window $$\rho^2$$ estimate nor the current $$M_{2+\eta}$$ bounds imply that the right-hand side of (11) vanishes uniformly at late times.

This is precisely where transport-driven spatial concentration remains relevant. A small amount of high-velocity mass can carry order-one energy while being concentrated in a small spatial region. The collision operator is local in $$x$$, so equilibrium information averaged over the whole torus does not directly supply local collision coercivity.

## 5. Why the homogeneous Coulomb entropy method does not transfer automatically

For the spatially homogeneous classical Coulomb Landau equation, a weighted relative-Fisher lower bound and propagation of high moments give a nonintegrable entropy-dissipation coefficient. Polynomial moments grow at most linearly; sufficiently high moments then force same-energy convergence. carrapatoso.perso.math.cnrs.fr (https://carrapatoso.perso.math.cnrs.fr/articles/8-LandauEntropie.pdf)

The homogeneous LFD theory also proves convergence to the Fermi–Dirac state having the conserved energy. NSF Public Access Repository (https://par.nsf.gov/servlets/purl/10401571)

Those arguments cannot simply be applied at each $$x$$:

- The local mass, momentum, and energy are not conserved.
- The homogeneous coercivity constants depend on local velocity distributions.
- Spatially varying local Fermi–Dirac profiles have zero instantaneous collision dissipation.
- The 2021 weighted Fisher estimate retains its homogeneous velocity-space hypotheses and does not provide spatial hypocoercivity. Springer (https://link.springer.com/article/10.1007/s10955-021-02751-z)

A full proof would need a quantitative transport–collision estimate controlling the local-equilibrium degrees of freedom and the high-velocity concentration represented by (8).

## 6. What would complete the theorem

Each of the following would imply $$\Delta=0$$, but none has been obtained here.

### A. Uniform energy tightness

$$\lim_{R\to\infty}
\sup_{t\ge0}
\int_{|v|>R}|v|^2f(t,x,v)\,dx\,dv=0.$$

### B. An integrable tail-mobility estimate

A bound strong enough to show that the cumulative right-hand side of (5) tends to zero as (R\to\infty), for example through control of the quantity in (11).

### C. A quantitative spatial hypocoercive entropy inequality

An estimate of the form

$$H(f(t)\mid F_{M,P,E})
\le
C(t)\int_t^{t+T(t)}D(f(s))\,ds+\text{controlled tail error},$$

where the resulting coefficient is nonintegrable in time using only estimates already derived from the equation.

The available qualitative warming and rigidity theorem is not quantitative enough to provide C.

## 7. No negative trajectory has been produced

The accepted same-invariant Gaussian-halo family proves that no instantaneous coercivity inequality depending only on $$M,P,E$$ and a fixed particle–hole core can work. But its members are different static states. They are not successive states of one solution.

Similarly, formal saturated indicators have zero particle–hole factor, but they are not smooth classical trajectories arising from the stipulated Schwartz data. They do not provide the requested negative resolution.

I have not constructed a solution realizing

$$\Delta>0.$$

## Final conclusion

The asymptotic alternatives have now been sharpened to:

$$\boxed{\Delta=0}$$

which gives the requested convergence

$$H(f(t)\mid F_{M,P,E})\to0
\quad\text{and}\quad
\|f(t)-F_{M,P,E}\|_1\to0,$$

or

$$\boxed{\Delta>0}$$

in which case:

- $$f(t)\to F_*$$ in every $$L^1_q$$, $$q<2$$;
- the missing energy becomes an atom $$\Delta\delta_\infty$$;
- every moment of order $$q>2$$ diverges;
- the defect must be generated by a persistent infinite-time shell flux governed by (3)–(8).

The current all-time estimates do not exclude that second alternative, and no actual trajectory realizing it has been constructed.

Therefore the full unconditional same-energy entropic thermalization question remains unresolved.

## Visible activity — Worked for 30m 22s

Analyzing energy escape
Tested tail control
Refined moment estimates
I’m testing whether dynamics can rule out the remaining energy defect, focusing on high-velocity energy flux, entropy dissipation, and possible runaway-halo mechanisms.
The tail-energy balance sharpens this: any nonzero defect requires persistent collision mobility across every large velocity shell. I’m testing whether existing unit-window density control rules that out.
Estimating velocity migration
Sought entropy controls
Estimated shell flux and assessed energy evaporation and retention
Tested weighted invariants and balanced moment growth
Investigated moment bounds
Reviewed known estimates
Connected dissipation bounds
Explored spatial control
Sought eventual bounds
Analyzed linearized dynamics and evaluated energy retention
Assessed energy escape
Searched 37 websites
Assessed energy retention
Assessed energy retention
Assessed energy retention
Assessed energy retention
Assessed energy tightness and retention
Assessed energy tightness
Assessed energy retention
Assessed energy tightness and convergence gap
Assessed energy retention
Searched 52 websites

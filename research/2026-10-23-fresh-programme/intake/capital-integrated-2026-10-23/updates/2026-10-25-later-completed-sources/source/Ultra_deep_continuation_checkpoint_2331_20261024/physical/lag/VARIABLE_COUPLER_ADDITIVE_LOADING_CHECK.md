# Two variable-transformer couplers at one resonator tap

Bounded circuit algebra check, 24 October 2026. The numerical parameters are
the ones stated in the Y. Yin et al. transformer model: (L_1=L_2=480\,\mathrm{pH}),
(M=-138\,\mathrm{pH}), and a tunable (L_s\). The paper describes a quarter-wave
resonator coupled to a transmission line through this transformer/SQUID block;
its text also notes that the coupler bias slightly shifts the resonator
frequency ([primary source](https://arxiv.org/abs/1208.2950v1)). This note checks
the two-block shunt-loading extension algebraically; it is not a device model
validation.

## One block: impedance and passivity

With the secondary terminated in a real (R>0), the coupled-inductor equations
are

\[
V_p=sL_pI_p+sM_{\rm eff}I_s,\qquad
0=sM_{\rm eff}I_p+(R+sL_{\rm sec})I_s.
\]

Eliminating (I_s) gives

\[
Z_p(s)=sL_p-\frac{s^2M_{\rm eff}^2}{R+sL_{\rm sec}},\quad
L_p=L_{\rm sec}=480+L_s,\quad M_{\rm eff}=L_s-138
\]

with inductances in pH in the last two expressions. This is the Schur
complement of the two-coil impedance matrix loaded by (R). On the physical
sinusoidal axis (s=i\omega),

\[
\operatorname{Re} Z_p(i\omega)=
\frac{\omega^2M_{\rm eff}^2R}{R^2+\omega^2L_{\rm sec}^2}\ge0,
\]

so the sign of the reflected resistance is passive. The inductance matrix is
positive definite for every (L_s\ge0), since

\[
L_pL_{\rm sec}-M_{\rm eff}^2
=(480+L_s)^2-(L_s-138)^2
=618(342+2L_s)\;\mathrm{pH}^2>0.
\]

For (L_s=0), its eigen-inductances are 342 and 618 pH. At the cancellation
point (L_s=138\,\mathrm{pH}), (M_{\rm eff}=0), (L_p=L_{\rm sec}=618\,\mathrm{pH}),
and the impedance matrix has eigenvalues 618 pH, 618 pH. The terminated port
then sees exactly (Z_p=s(618\,\mathrm{pH})): its 50 ohm resistor has zero
coupling, but the primary winding remains an inductive branch.

## Two actual port blocks and the frequency shift

For separate hot-side and cold-side blocks attached in shunt at the same
resonator tap, the natural-mode equation is additive:

\[
Y_{\rm line}(s)+Z_{p,H}(s)^{-1}+Z_{p,C}(s)^{-1}=0,
\quad
Y_{\rm line}(s)=
\frac{\tanh(s(\ell-d)/v)+\coth(sd/v)}{Z_r}.
\tag{1}
\]

At (s=i\omega), the line term becomes the stated

\[
\frac{i}{Z_r}\left[\tan(k(\ell-d))-\cot(kd)\right].
\]

Equation (1), with analytic continuation in (s), is the loaded-mode pole
condition. When either block has (M_{\rm eff}\ne0), its real-axis input
admittance has positive real part, so the complex equation cannot vanish at
real (\omega); a loaded pole has complex frequency. For a real-frequency
response peak, use the zero of total susceptance and compute its linewidth
from the nonzero conductance. The displayed real-(k) expression must not be
mistaken for a lossless real-frequency root when the 50 ohm loads are coupled.

Both ports can be set to their zero-mutual point independently: choose
(L_{s,H}=L_{s,C}=138\,\mathrm{pH}). Then each branch is a shunt inductor
(618\,\mathrm{pH}), and their sum is a (309\,\mathrm{pH}) equivalent shunt
inductance. The resistor ports are decoupled, while the common resonator is
still loaded reactively.

That reactive load does not leave the bare resonance unchanged. For an explicit
example, take (Z_r=50\,\Omega), target bare frequency (f_0=6\,\mathrm{GHz}),
(\ell=v/(4f_0)), and (d=\ell/2). Without either coupler, the two line
segments are each (\lambda/8), so the bare condition is
(\tan(\pi/4)-\cot(\pi/4)=0) at 6 GHz. With (n) identical cancellation-point
branches the real, lossless mode equation becomes

\[
\tan x-\cot x=\frac{nZ_r}{2\pi f L_p},\quad
x=\frac{\pi f}{4f_0},\quad L_p=618\,\mathrm{pH}.
\]

Bisection gives (f=8.4803843\,\mathrm{GHz}) for one attached block and
(f=9.5604843\,\mathrm{GHz}) for two. Thus both ports can cancel their
resistive couplings at once in this ideal algebra, but the original resonator
frequency is not free. Retuning the line geometry can restore a chosen
frequency; that consumes a changed resonator length/geometry rather than
leaving the original mode untouched. For example, keeping (d=\lambda_0/8)
at 6 GHz and retuning only the open-side segment requires
(k(\ell-d)=\arctan(1+4.2922045)=1.3840411\), or
((\ell-d)=0.220277\lambda_0), instead of its original (0.125\lambda_0).

## Scope

This confirms additive susceptance/conductance for two independent transformer
branches in this lumped model and the ideal (M_{\rm eff}=0) algebra. It does
not show independent linewidth tuning away from cancellation, a fixed
resonator frequency, a finite distributed realization of all parasitics, a
thermal transport advantage, or a hardware-validated boundary condition.

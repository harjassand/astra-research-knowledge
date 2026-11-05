# First-principles construction, before nearest-literature comparison

Question: Can the complete worst-case hidden-preparation uncertainty be computed
from a measured forced response, even though that response does not identify a
hidden realization? The intended consequence is a realization-uniform, sharp
prediction and readiness calculus, not a new response-table controller.

## Mechanical memory class

Known observed parameters M, Gamma, mu > 0. Unknown real Hilbert bath H,
contraction-semigroup generator A, and bounded coupling vector b:

    xdot = v,
    M vdot = -mu x-Gamma v-<b,z>+f,
    zdot = A z+b v.

Storage is (mu x^2+M v^2+||z||^2)/2. Its derivative is at most
f v-Gamma v^2. The total initial state, including visible x,v, has energy <= E.
The memory kernel K(t)=<b,exp(tA)b> and the zero-state displacement response S
are fixed. All initial states and all such hidden realizations are admitted.

The representation deliberately retains the known visible law. It is narrower
than every passive LTI port, and does not infer it from a response fit.

## Conservative completion

A contraction semigroup has a unitary dilation preserving <b,T(t)z> for t>=0.
Dilate the bath while retaining the actual local Gamma damper and known M,mu.
The enlarged bath has exactly the same K, and every old initial state embeds
isometrically with the same subsequent visible path under every additive input.
The conservative completion is itself allowed. Thus the union of possible
visible initial-state effects over all compatible baths is exactly the energy
ball image of this completion. Dilation existence will be compared with primary
functional-model literature; it is not claimed invented here.

Normalize the full state by q=(sqrt(mu)x,sqrt(M)v,z). In the completion the full
generator L, input vector B, and displacement row C satisfy

    L+L*=-2 Gamma B B*,  L C*=-B,  C C*=1/mu.

Let h(t)=C exp(tL)B=S'(t). Differentiating exp((t-u)L)exp((s-u)L*) for t>=s gives

    exp(tL)exp(sL*) = exp((t-s)L)
                      -2 Gamma int_0^s exp((t-u)L)BB*exp((s-u)L*)du.

Also C exp(tL)C*=1/mu-S(t), by L C*=-B. Therefore the exact maximum completion
kernel of free displacement is

    Cmax(t,s)=1/mu-S(|t-s|)
             -2 Gamma int_0^min(t,s) h(t-u)h(s-u)du.             (A)

It is positive semidefinite because it is the Gram kernel of C exp(tL).
Every compatible original bath embeds into this kernel's physical realization.
This equation is a response-only description of maximum initial uncertainty.

## Exact finite-record minimax prediction

Subtract the known forced response from finite linear observations, leaving
y_i=<r_i,q0>. Let G_ij=<r_i,r_j>, c_i=<r_i,r_*>, d=||r_*||^2. For exact data:

    E_used = y^T G^dagger y / 2,
    center = c^T G^dagger y,
    radius = sqrt((2E-y^T G^dagger y)(d-c^T G^dagger c)).       (B)

Compatibility requires y in range(G), E_used<=E. Orthogonal projection of q0
onto span{r_i} proves (B); opposite normalized residual representers attain it.
The same projected state defines a center for an entire future path. Its exact
sup-path radius is the supremum of the pointwise radii, attained or approached
at a maximizing time. The physical conservative completion attains the bound,
so this is sharp over hidden realizations, not just over abstract functions.

Additive preparation controls do not change these representers when their
known forced contribution is subtracted. In the additive independent-noise
measurement model, they cannot improve hidden-state information at fixed
measurement times. Changing stiffness/coupling or performing an actual reset
changes the premise and can change that conclusion.

## Avoid differentiating acquired data

For a finite position box phi_i=1_[a_i,a_i+b_i]/b_i, put

    H_i(u)=[S(a_i+b_i-u)-S(a_i-u)]/b_i,

using S=0 on negative arguments. Integrating (A) against boxes gives

    G_ij=1/mu-int int phi_i(t)phi_j(s)S(|t-s|)dt ds
         -2 Gamma int H_i(u)H_j(u)du.                         (C)

The same formula includes a future position box as the target. It uses S and
finite differences, never an unobserved velocity or derivative oracle. For a
piecewise-linear acquired S, every term is piecewise-polynomial integration.

If ||S-S_hat||infinity<=eps on [0,L], let e_i=2 eps sqrt(L)/b_i and
Q=1/sqrt(2 Gamma mu). Young's inequality and int h^2<=1/(2 Gamma mu) give

    |G_ij-Ghat_ij| <= eps+2 Gamma [Q(e_i+e_j)+e_i e_j].        (D)

For p boxes and common entry bound beta, G<=Ghat+p beta I in Loewner order.
Any chosen linear predictor a has a certified physical error

    sqrt(2E * (-a,1)^T (Ghat+p beta I) (-a,1))
      + sum_i |a_i| eta_i,                                  (E)

where eta_i are finite readout-error bounds. This bound avoids inversion of an
uncertified small eigenvalue. Its best a is a finite convex problem. A supplied
rational a and outward square-root bound make its certificate elementary.

## Possible structural payoff to investigate

The conservative bath's spectral measure is fixed by the even extension of K.
A finite atomic measure gives finite-rank preparation uncertainty. An absorbing
Lorentzian response Be^(-a|t|), although its forced transfer is rational and
first order, gives a continuous measure and infinite-rank maximum uncertainty.
Thus forced-response order is not the relevant preparation dimension. The
rank/conditioning of the completion kernel is. This might supply a broad
classification; nearest existing system theory and optimal recovery may already
contain its essential theorem, which must be established before a novelty claim.

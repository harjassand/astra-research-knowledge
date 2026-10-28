# Independent challenge of the root condition-number-free receiver

Whole-read source: `../parent/full_white_ray/KAPPA_FREE.md` and its
baseline import `PROOF.md`, 28 October 2026. Accepted at their displayed
finite-dimensional mathematical scope. This is a review, not my construction.

I reconstructed the weighted-log coefficients using `N(R)=(I+3P)/4`
and `N(I-R)=3(I-P)/4`. They give exactly
`LP=log[(a+3c)(a+c/3)/(a+c)^2]` and
`LQ=log[(a+c/3)/sqrt(a(a+c))]`.
LP is nonnegative because the numerator exceeds its denominator by
4ac/3. LQ is nonnegative for c>=3a. Its global lower bound -c/(6a)
follows from derivative x(x+7)/[6(x+3)(x+1)] for x=c/a.
For c<3a the baseline is at least 3c^2/(280a); with c>=m this
pays the first-order negative part by `(140/9)(eps/m) h0(a)`.

The finite perturbation comparison is valid without commuting H and C:
`0<=NH<=I`, because N is positive and unital and H is a density.
Integral entropy increments plus operator-log monotonicity give the
source's L_eps bound. The extra P and Q log charges are each at most
2eps/a, and TrH=1 gives total additional deficit charge 2eps^2/a.
No pointwise entropy whitening or unproved mixture sign is used.

The scalar baseline also checks independently: its second derivative is
12(s-1)/[s(s+3)(3s+1)(s+1)]. On s<=1 use concavity and g(1)>5/8;
on s>=1 restrict the integral representation to t>=2s and use
g''(t)>=16/(35t^3). Thus g(s)>=(6/35)s/(1+s)^2.
Monotonicity of c/(a+c) yields the claimed m-only matrix baseline.

For a>=a0<=m, the finite charge divided by the baseline is at most
`(35/(3r))(eps/m)^2(1+m/a)^2`
`<= (140/(3r))(eps/a0)^2 <=35/(192r)`.
The first charge fraction is at most 140/(9*2^22); their sum is less
than one half, leaving the stated half-baseline. For a<=a0, the actual
combined perturbation K=epsH+aI has trace w=eps+9ra<10ra0 and leakage
at least ell0=min(ell,8/9), so the reviewed general-ray receiver applies
to K/w at its own finite radius. This proves both portions including
their common boundary. The ell=0 branch must stay separate, as stated.

The result therefore removes the upper eigenvalue/condition-number
acquisition from the all-white premise. It preserves a lower order
certificate C>=mI, the literal H/PSD and leakage inputs, and finite
matrix/bath access. The common-bath lift is inherited. Neither a global
source theorem nor a physical implementation or historical priority
follows. I did not independently rerun the root fixture compiler here;
the acceptance is of the proof and its constants, not a claimed fresh
fixture replay.

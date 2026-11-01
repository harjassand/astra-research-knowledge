# Controlling qualifications for the unchanged activated macro receiver

Original source: `../ACTIVATED_TO_MACRO_AND_POSITIVE_FRACTIONS.md`, SHA256
 e527fafdfe790fa753b4584fca338bf9e4aa37179643a1f1596e39b140cb99a0.
It is preserved unchanged. Independent reviewer `review_activated_macro_interface`
identified the following two exact scope qualifications; they are received here.
The final independent receipt/manifest will bind its own unchanged payloads.

1. The interval M in [delta N,delta N+1] describes a FIRST actual crossing from
   below delta N. If the allowed initial state already has M>=delta N, it is
   immediate macro entry and need not satisfy this upper bound. The positive
   fraction receiver only requires M>=delta N and the mass bound, so it applies
   to either case without any change of constants.
2. The actual short-window error in displayed equation (8) is

       10 exp(-kappa_delta N),
       kappa_delta=rho^2/[2(32+rho/3)],
       rho=eta exp(-100)/4.

   It requires N>=28exp(100)/eta. If one wants a prefactor-free form
   exp(-c_delta N), take c_delta=kappa_delta/2 and additionally impose
   N>=2log(10)/kappa_delta. The informal Section 1 prefactor-free wording must
   not be read as silently dropping this factor or threshold.

The full composition source
`../../rate2_uniform_removal_composition/UNIFORM_ACTUAL_REMOVAL_BLOCK.md`,
SHA256 a0e09b39c50c28365a1ed5a0fe04c71b003b9c5556ffe9b94202441f9ee4cb21,
already uses only the lower macro condition M>=delta N, retains the exact factor
10, and includes N>=28exp(100)/eta in its N_* threshold. It therefore needs no
numeric or logical change for these two qualifications. No additional recurrence
or stationary-moment conclusion is conferred by this receiving addendum.

# Rank-one balanced source: exact scalar Stieltjes bath interface

This is a reduction, not an entropy sign theorem. Let

 T=[d;sqrt(h)][d;sqrt(h)]*, x=||d||^2, Q>=0,
 M=[[Q+dd*,sqrt(h/2)d],[sqrt(h/2)d*,h/2]], M0=dd*+2Q,
 tau=x+h+2TrQ.

The actual balanced deficit is

 Delta(Q)=f(T)+f(M0)-2f(M)+tau log(2/3)+x log2,
 f(X)=TrXlogX.

For s>0 define r_Q(s)=d*(Q+sI)^(-1)d and a(s)=2s/(h+2s). Matrix determinant lemmas give

 det(M+sI)=det(Q+sI)(h/2+s)[1+a(s)r_Q(s)],
 det(M0+2sI)=2^b det(Q+sI)[1+r_Q(s)/2].

In particular, with k_s(r)=log(1+a(s)r)-log(1+r/2), two bath operators Q,Q0 on the same space satisfy the convergent exact difference identity

 Delta(Q)-Delta(Q0)
 =2Tr(Q-Q0)log(4/3)
   +2 integral_0^infinity [k_s(r_Q(s))-k_s(r_Q0(s))] ds.

To check the linear coefficient, use the logdet integral for f and a common upper cutoff R. Rescaling the M0 integral s=2t cancels the Q determinant integrals except

 2 integral_(R/2)^R log[det(Q+sI)/det(Q0+sI)]ds
 ->2Tr(Q-Q0)log2.

Adding the explicit tau log(2/3) difference gives the displayed log(4/3). The k differences decay O(s^-2), so their rescaling introduces no further boundary term. Individual integrals of k are not convergent and must not be used without regularization.

Taking Q0=0 is legitimate by continuity, with r_0(s)=x/s. The kernel derivative has the exact single sign change

 partial_r k_s=(a(s)-1/2)/[(1+a(s)r)(1+r/2)],

negative for s<h/2 and positive for s>h/2. Thus Q>=0 implies r_Q<=x/s but does not give a pointwise sign for the entropy correction. The positive linear trace payment and the known Q=0 deficit must both be retained.

This representation retains arbitrary bath noncommutativity through the scalar spectral measure of Q in d. It does not reduce Q to rank one, nor prove convexity or a moment-extremality principle for that measure.

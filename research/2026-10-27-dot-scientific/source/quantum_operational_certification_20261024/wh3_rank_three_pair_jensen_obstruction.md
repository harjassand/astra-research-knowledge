# Rank-three actual-source pair Jensen obstruction

The commuting-marginal rank-two anchored proof does not extend by replacing all rank-three output blocks with their scalar Rayleigh means.

Take psi=(|00>+|11>+|22>)/sqrt(3), P=|psi><psi| and

 A=P+|10><10|+|20><20|.

This is an exact rank-three projection, 0<=A<=I, A psi=psi. Its marginal is R=diag(7/3,1/3,1/3), commuting with R_P=I/3. It belongs to the proved projection class; it is not a target counterexample.

In the phase-covariant notation, X=P on the maximally correlated subspace, a10=a20=1, all other offdiagonal populations zero. The three output pair blocks of NA are

 K01=K02=1/2 [[1/3,-1/3],[-1/3,4/3]],
 K12=1/2 [[1/3,-1/3],[-1/3,1/3]].

The NP contribution on each block has weight 1/3 and unit vector v=(1,-1)/sqrt(2). Thus the weights in 2Tr NP log NA are 2/3. Unit-vector Rayleigh quotients are 7/12,7/12,1/3, respectively. Replacing each v*log K v by log(v*Kv) gives the lower certificate

 G=(1/3)log[(7/9)(1/9)(1/9)]
   -(2/3)log[(7/12)(7/12)(1/3)]
  =(1/3)log(256/343)<0.

All constants are exact. Therefore any aligned rank-three proof must retain or quantitatively pay at least part of the within-pair log Jensen gaps. This obstruction already occurs for a projection, where the known operator transport certifies the actual anchored sign.

## Useful exact reduction retained
For general Schmidt weights lambda_i>0 summing to one, X u=u with u_i=sqrt(lambda_i), and occupancy matrix M having M_kk=Xkk and M_kj=a_kj for k!=j, define s_k=sum_j lambda_j M_kj and r_j=sum_i M_ij. For the pair excluding k, its unnormalized vector has norm squared w_k=1-lambda_k, and

 v_ij* Kij v_ij = (1-2lambda_k+s_k)/2.

The unit-vector Rayleigh quotient is this expression divided by w_k. This identity removes offdiagonal X dependence from scalar means, but the example proves those means alone do not yield the desired universal sign.

## Quantitative gap repairs this obstruction (not a universal proof)

For a positive pair matrix K, unit v, m=<K>, variance sigma^2=<K^2>-m^2, and L>=||K||, the scalar tangent remainder gives

 log m-<log K> >= c(m,L) sigma^2,
 c(m,L)=[L/m-1-log(L/m)]/(L-m)^2.

To see the coefficient direction, set y=x/m and write (y-1-log y)/(y-1)^2=integral_0^1 t/[1+t(y-1)] dt, which decreases in y>0. Apply the resulting scalar bound to the spectral measure of K at v; the linear term averages to zero.

For each problematic block above, m=7/12, sigma^2=1/16, and L=3/4 is a strict spectral upper bound: L I-K has positive diagonals and determinant 1/48. Thus c=36[2/7-log(9/7)]. The two weights 2/3 contribute total c/12, giving

 g >= (1/3)log(256/343)+3[2/7-log(9/7)] > 1/200.

The last strict inequality is certified with exact rational 40-term atanh series and an explicit remainder in `wh3_rank_three_gap_payment_check.py/.json`; its value is about 0.00568190. This establishes an actual paid repair of the obstruction, while leaving the general aligned rank-three source problem open.

# A pair-blind source pair with incompatible continuous optimal controls

1 November 2026. Optional complementary construction. This does not replace the inherited path lower bound used for the main interaction-order theorem. The response model and its energy minimum are inherited from pinned Astra N1150/N1152; the five-control source pair and regret argument below are constructed in this investigation.

## Source pair

Let g=e1 and let B have diagonal one, B_(1j)=B_(j1)=3/10 for j=2,3,4,5, B_23=B_32=-4/5, B_45=B_54=4/5, with all other offdiagonal entries zero. Let B' exchange the two dark pairs (2,3) and (4,5), reversing which pair has the negative edge. Both satisfy B>=0, max B_ii=1 and |g_i|<=1.

Proof of PSD: the dark block is the direct sum of two matrices [[1,±4/5],[±4/5,1]], hence positive definite. The scalar Schur complement is

    1-(3/10)^2[2/(1-4/5)+2/(1+4/5)] =0.

The nullspace of B is spanned by

    v=(1,-3/2,-3/2,-1/6,-1/6),

and B' has the two pairs exchanged. In particular each has rank four.

Every complete command using at most two actuators gives identical F for B and B'. If actuator 1 is absent the response is zero; if it is present there is at most one dark actuator, and the relevant 2x2 principal matrix is identical. This covers unlimited precision, arbitrary pair doses and adaptive pair-only measurements.

## Uniform large-dose reduction, with a finite remainder

For dose delta>0 write u=delta*d with d>=0, sum d_i=1. The exact variational representation is

    F_B(delta*d)
      =min_{r:v^T r=1} [(r-g)^T B^+ (r-g)+delta*sum_i d_i r_i^2].

For all strictly positive d, define

    h_v(d)=1/[sum_i v_i^2/d_i],
    r_i^*=(v_i/d_i)/[sum_j v_j^2/d_j].

At a boundary with any d_i=0, set h_v(d)=0; since all v_i are nonzero, a feasible residual supported on that zero coordinate attains zero weighted energy. In all cases,

    delta*h_v(d) <= F_B(delta*d) <= delta*h_v(d)+100.       (1)

For the upper bound, write q_i=v_i r_i^*. These weights are nonnegative and sum to one. Put w_i=e_i/v_i-g. Then r^*-g=sum_i q_i w_i, so convexity of the B^+ quadratic form yields

    (r^*-g)^T B^+(r^*-g) <=max_i w_i^T B^+ w_i=100.

The five exact values are 0,100/81,100/81,100,100. They can be obtained by solving Bz=w with v^Tz=0 and taking w^Tz, without numerical pseudoinversion. The same constant works for B' by symmetry. Boundary points use one w_i directly. Thus (1) is uniform over the whole simplex, including data-dependent controls.

## Continuous optimal-value separation

With the source known, Cauchy--Schwarz gives

    max_d h_v(d)=1/(sum_i |v_i|)^2=9/169,

attained by d_i=|v_i|/(13/3). The two models favor different dark pairs.

A controller unable to distinguish the two sources must select one common distribution of commands. Each h_v is concave, because it is the infimum over r of linear functions sum d_i r_i^2. Randomizing commands cannot improve the worst-case expected reward beyond their mean command. Symmetrizing within pairs and exchanging the two pairs shows that the maximum of (h_v+h_v')/2 occurs with d_2=d_3=d_4=d_5=(1-d_1)/4. At such a command,

    h_v(d)=h_v'(d)=1/[1/d_1+(164/9)/(1-d_1)].

Optimizing this scalar expression gives

    max_d min(h_v,h_v')
      =max_d (h_v+h_v')/2
      =9/(3+2sqrt(41))^2
      =0.0360234165... .

Combining this identity with (1), any adaptive, randomized, pair-only acquisition/controller has worst-case expected continuous-control regret at least

    delta * [9/169-9/(3+2sqrt(41))^2] -100
      =0.0172310213...*delta -100.                        (2)

The criterion here is unpriced response maximization over the entire positive dose simplex. It is not merely a two-action menu. The bound becomes positive for delta>5803.49, so this example is a high-strength mathematical obstruction; it does not demonstrate an easy-to-measure small-dose advantage. At large dose, the asymptotically optimal common robust value is only about 67.6% of the known-source optimum. The low-support transcript remains exactly identical at every dose.

The exact five-control matrices are legitimate PSD response sources. A physical apparatus realizing them, finite source precision, control settling and measurement costs have not been acquired. This example establishes no hardware or historical-priority claim.

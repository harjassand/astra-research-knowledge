# Ordinary RLD versus SLD, and an exact finite-reference decision advantage

## Family and three distinct coefficients

Consider the three prepared qubit states sigma_j=(I+a P_j)/2, with P_j=X,Y,Z and 0<a<1. For this family:

- Ordinary scalar-reference RLD coefficient: a^2/(2-a^2).
- Ordinary scalar-reference SLD coefficient: a^2/2.
- Complete conditional RLD and complete SLD/MMSE erasure threshold: 2a^2/(3-a^2).

The last identification uses the separately audited operational radius theorem. RLD and SLD are not interchanged in the ordinary setting.

At a=3/5 these are respectively 9/41, 9/50, and 3/11. The erasure reveal probability q=6/25 lies strictly above both ordinary thresholds and below the complete threshold. Section 4 provides a fully finite, faithful, rational-complex three-level-reference witness against complete domination at this q.

## 1. Ordinary RLD calculation

Let p_i>0, sum p_i=1, and h_i real with sum h_i=0. The output baseline has Bloch vector a p, and output tangent is (a/2)sum h_i P_i. Put N=sum h_i^2, s=sum p_i^2, and E=sum h_i^2/p_i. The exact RLD cost is

g_RLD=a^2 N/(1-a^2 s).

Let L be the largest eigenvalue of C_p=diag(p)-pp^T. On the zero-sum tangent subspace, N/E<=L. This follows by normalizing the input form with diag(sqrt(p)); the nonzero compressed spectrum equals that of C_p.

Two elementary bounds hold: L<=Tr C_p=1-s, and L<=1/2. For the latter, Gershgorin gives maximum absolute row sum 2p_i(1-p_i)<=1/2. Therefore

(2-a^2)L=(2-2a^2)L+a^2 L
<=1-a^2+a^2(1-s)=1-a^2 s.

It follows that g_RLD/E<=a^2/(2-a^2). The boundary prior (1/2,1/2,0) and tangent (1,-1,0) attain this value; faithful approximants give the same supremum.

## 2. Ordinary SLD calculation and exact upper certificate

Use the SLD convention g_SLD(rho,H)=Tr H L, where rho L+L rho=2H. For the same p,h,

g_SLD=a^2 N+a^4(p dot h)^2/(1-a^2 s).

We prove

E>=2N+2(p dot h)^2/(1-s).

Since a^2/(1-a^2 s)<=1/(1-s), this immediately gives g_SLD<=a^2 E/2.

For the promised inequality, define

M=diag(1/p)-2I-2pp^T/(1-s),
Q=[[1,0],[0,1],[-1,-1]].

Every zero-sum h is Q u. Write s_2=p_1p_2+p_1p_3+p_2p_3>0. Direct exact algebra, using sum p_i=1, gives

det(Q^T M Q)=1/s_2,
(Q^T M Q)_11
=p_2(p_1+p_3)(p_1+p_3-3p_1p_3)/(p_1p_3 s_2).

The first diagonal is positive: if t=p_1+p_3<1, then p_1p_3<=t^2/4, hence t-3p_1p_3>=t(1-3t/4)>0. The determinant is positive too, proving Q^T M Q>0 for faithful p. The desired upper inequality follows.

At the boundary p=(1/2,1/2,0), h=(1,-1,0), one has p dot h=0 and N/E=1/2, giving g_SLD/E=a^2/2. Faithful approximants yield the exact ordinary supremum.

The pure-output endpoint a=1 was used only as an algebraic comparison in the inequality, not as a premise that the physical prepared states are singular. The theorem here assumes 0<a<1.

## 3. Complete coefficient for this family

For uniform dual p, the harmonic matrix is

M=(2/(1-a^2))[I-(a/3)(X+Y+Z)].

Its inverse has trace (1-a^2)/(1-a^2/3). The inverse itself is a primal center whose three costs agree. Consequently the exact complete coefficient is

1-Tr M^-1=2a^2/(3-a^2).

This concerns complete conditional RLD, and the audited signed-observable/flag argument identifies the complete SLD/MMSE erasure threshold with the same number. It does not equate the two ordinary coefficients.

## 4. Explicit faithful three-level-reference witness at a=3/5

All matrices below are rational-complex. Define

Q=[[2,1,-2],[2,-2,1]]/3,
s=(1/3,2/3,2/3),
v_i=Q e_i,
z_i=s_i v_i,
R_i=(v_i v_i^T+(1/1000)I_2)/(1+3/1000).

Then Q Q^T=I_2, Qs=0, sum R_i=I_2, and sum z_i=0. Put delta=1/1000 and

B_i=diag(R_i,delta/3),
H_i=[[0_(2x2),z_i],[z_i^T,0]],
t=1/10000.

Define two equally likely classical-input/reference states by their three blocks:

rho_(+,i)=(B_i+tH_i)/(2+delta),
rho_(-,i)=(B_i-tH_i)/(2+delta).

They are normalized and have the same reference marginal diag(I_2,delta)/(2+delta), since sum H_i=0. Every block is strictly positive. The exact Schur complements for either sign are

300336497/901012500000,
75133997/225405000000,
75133997/225405000000,

all positive. Thus no singular-baseline approximation is used in this finite witness.

## 5. Exact SLD and binary-MMSE advantage

Let A=sum_i sigma_i tensor R_i, S=(sum_i sigma_i)/3, and W=sum_i sigma_i tensor z_i. The input SLD cost for the unnormalized B_i,H_i is

E=4 sum_i z_i^T(R_i+(delta/3)I)^-1 z_i
 =160736960576000/40156261216081.

For the output, let Y solve A Y+delta Y S=W. Its SLD cost is N=4Tr W*Y, exactly

N=1039714052516080146741536000/1041596831773046513406650209.

The exact ratio is

N/E=1300817207217904824626075939212171
     /5216323183100407577419584686573254
   approximately 0.24937435077493467.

At q=6/25, its strictly positive margin is

N-qE=1569482950516109666032375720892601923840
      /41826634458520833563849108591730932810929.

The erasure-output SLD cost is exactly qE: the erased-reference tangent vanishes. For the equiprobable binary labels +1 and -1 and squared-error loss, the optimal explained variance is exactly t^2 g/(2+delta). Therefore the quantum-output experiment has a strictly smaller minimum mean-square error than erasure, by

t^2(N-qE)/(2+delta)>0.

This is an exact finite statistical decision advantage, not merely an asymptotic Fisher-information statement. It assumes access to the specified preparations and arbitrary allowed measurements; no laboratory implementation, hardware availability, or experimental sensitivity is asserted.

## Executable verification

Run the package runner or `python /path/to/archive/checks/finite_sld_witness.py`. It uses SymPy exact rational-complex arithmetic to solve the 8-by-8 vectorized Sylvester equation, verify the SLD margin, and check every physical positivity Schur complement. Its recorded output is `../checks/FINITE_SLD_WITNESS.json`. The ordinary SLD determinant certificate is checked separately by `../checks/verify_ordinary_coefficients.py`.

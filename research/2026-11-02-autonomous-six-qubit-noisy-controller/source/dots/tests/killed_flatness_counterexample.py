from fractions import Fraction as F
# P contains logical |0>,|1>; J=|outside><1|, H=0.
# At t=2 log 2: e^(-t/2)=1/2, e^(-t)=1/4.
rho=[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]
killed=[[F(1,2),F(1,4)],[F(1,4),F(1,8)]]
loss=1-killed[0][0]-killed[1][1]
deficit=[[rho[i][j]-killed[i][j] for j in range(2)] for i in range(2)]
det=deficit[0][0]*deficit[1][1]-deficit[0][1]*deficit[1][0]
assert loss==F(3,8) and det==F(-1,16)
# Actual state equals embedded killed state plus loss*|outside><outside|,
# so their trace distance is loss. Decode outside to logical |0>.
# Decoded error has trace norm sqrt(13)/4 > 2 loss = 3/4.
assert F(13,16)>(2*loss)**2
print('PASS necessary-hypothesis counterexample: PJP=0 but PJdaggerJP=|1><1|')
print('Logical deficit determinant =',det,'; lost trace =',loss)
print('Decoded error sqrt(13)/4 exceeds twice actual-minus-killed norm 3/4')

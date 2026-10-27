import sympy as S
T,P,k=S.symbols('T P k',positive=True)
O=P+(2+k)*T+(2+k)**2;R=P+3*T+9
FP=2/O-3/R;FT=2/(2+T)+2*(2+k)/O-9/R-1/(1+T+k)
Den=(2+T)*O*R*(1+T+k)
N=S.cancel((FT-k*FP)*Den)
pos=10*(T*T/4-P)+3*k*k*T**3+(4*P*k+6*k**3+18*(k-S.Rational(1,6))**2+9)*T*T+((P-1)**2+23)*T+(6*P*k*k+18*P*k+3*k**4+24*k**3+36*k*k+6*k)*T+2*P*P*k+2*P*k**3+14*P*k*k+22*P*k+6*k**4+30*k**3+30*k*k+24*k
assert S.expand(N-pos)==0
assert S.factor(-FP*O*R-(P+3*k*T+3*k*k+12*k-6))==0
print('PASS exact universal compensated pair score f_T-k f_P>0 under P<=T²/4')
print('PASS exact sign numerator for unique source f_P crossing')
print('Strictness is supplied by23T; no numerical sign premise')

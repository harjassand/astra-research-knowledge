# Imports exact construction and assertions; then computes exact loss moments.
from pathlib import Path
exec(Path(__file__).with_name('robust_sld_witness.py').read_text().split('result={')[0])
Ymat=s.Matrix(4,2,lambda i,j:u[j*4+i]);V=2*t*Ymat
M4out=s.factor((s.trace(A*(V*V.conjugate().T)**2)+delta*s.trace(T*(V.conjugate().T*V)**2))/norm)
M2out=s.factor(t*t*N/norm)
Vin=[2*t*(R+delta*I/3).inv()*z for R,z in zip(Rs,zs)]
M4in=s.factor(sum([s.trace(R*(v*v.T)**2)+delta*s.trace((v.T*v)**2)/3 for R,v in zip(Rs,Vin)])/norm)
M2src=s.factor(t*t*q*E/norm);M4src=q*M4in
stats={}
for name,m2,m4 in [('target',M2out,M4out),('erasure',M2src,M4src)]:
 mean=1-m2;second=1+2*m2-3*m4;var=s.factor(second-mean**2)
 stats[name]={'mean_exact':str(mean),'mean':float(mean),'second_moment_exact':str(second),'second_moment':float(second),'variance_exact':str(var),'variance':float(var),'observable_fourth_moment_exact':str(m4)}
# Exact spectral range and conservative variance/gap certificates.
for k in [1,2]:
 assert s.factor((s.Rational(43,100)**2*I-V.conjugate().T*V)[:k,:k].det())>0
assert all(s.factor((v.T*v)[0])<s.Rational(53,100)**2 for v in Vin)
vo=s.factor(4*M2out-3*M4out-M2out**2);vsr=s.factor(4*M2src-3*M4src-M2src**2)
assert vo+vsr<s.Rational(77,200)
assert gap>s.Rational(157,20000)

# Rational logarithm upper bounds proved by positive truncated exponential series.
# These certify sufficient integer counts, without floating-point log rounding.
v=s.Rational(77,200);g=s.Rational(157,20000);bound=s.Rational(53,25)
log20_upper=s.Rational(29957323,10000000)
log40_upper=s.Rational(36888795,10000000)
for log_upper,value in [(log20_upper,20),(log40_upper,40)]:
 assert sum(log_upper**k/s.factorial(k) for k in range(41))>value
assert 37973*g*g>2*(v+bound*g/3)*log20_upper
assert 185705*g*g>8*(v+bound*g/6)*log40_upper
fixture=json.loads(Path(__file__).with_name('LOSS_STATISTICS.json').read_text())
for arm in ['target','erasure']:
 for key in ['mean_exact','second_moment_exact','variance_exact','observable_fourth_moment_exact']:
  assert s.Rational(stats[arm][key])==s.Rational(fixture[arm][key])
print('PASS: exact loss moments, spectral ranges, and rational certificates for 37973/185705 sufficient trials per arm')

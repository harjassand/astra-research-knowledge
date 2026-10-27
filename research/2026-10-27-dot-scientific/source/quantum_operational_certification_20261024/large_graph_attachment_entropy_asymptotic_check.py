exec(open('gls_instrument_entropy_monotonicity_exact_failure.py').read().split('Y=block')[0])
A=m.diag([m.mpf(2)/5,1,2]);D=m.diag([1,2,4]);C=m.matrix([[1,m.mpf(1)/5,0],[m.mpf(1)/10,1,m.mpf(3)/10],[0,m.mpf(1)/5,1]])
Z=D*C**-1;G=C*D**-1*C.T;g=list(m.eigsy(G,eigvals_only=True))
ell=lambda a,b:m.log(a/b)/(a-b) if a!=b else 1/a
high=sum(1/x for x in g)/6+sum(ell(g[i],g[j]) for i in range(3) for j in range(i+1,3))/2
omega=m.matrix(9,1)
for i in range(3):omega[3*i+i]=1
base=omega*omega.T+kron(m.eye(3),A);low=kron(m.eye(3),Z)*base*kron(m.eye(3),Z.T)
flow=deficit(low);fbase=deficit(base);kcoef=min(m.eigsy(Z.T*Z,eigvals_only=True));pred=flow+high
print('low filtered deficit',m.nstr(flow,35));print('high BKM coefficient',m.nstr(high,35));print('predicted coefficient',m.nstr(pred,35));print('accepted coefficient',m.nstr(kcoef*fbase,35))
for t in [10,30,100,300,1000,3000]:
 t=m.mpf(t);Y=block(A+t*t*C*D**-1*C.T,t*C,t*C.T,D)
 omega=m.matrix(18,1)
 for i in range(3):omega[6*i+i]=1
 src=omega*omega.T+kron(m.eye(3),Y);dd=deficit(src);L=block(m.eye(3),-t*C*D**-1,m.matrix(0,3),m.matrix(0,3));kap=1/max(m.eigsy(L*L.T,eigvals_only=True))
 print('t',t,'scaled deficit',m.nstr(t*t*dd,30),'scaled accepted',m.nstr(t*t*kap*fbase,30),'coefficient discrepancy',m.nstr(t*t*dd-pred,15))
assert abs(t*t*dd-pred)<m.mpf('.02')
print('noncommuting large-attachment leading coefficient replay PASS')

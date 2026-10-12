import sympy as s
r=s.symbols('r')
t=1; d=1; U=1; n=4
out=0
for k in range(n+1):
 states=[v for v in range(2**n) if v.bit_count()==k]; N=len(states); idx={v:i for i,v in enumerate(states)}
 H=s.zeros(N); J=s.zeros(N)
 for v in states:
  i=idx[v]; spin=[1-2*((v>>a)&1) for a in range(n)]
  H[i,i]=U*sum(spin[a]*spin[(a+1)%n] for a in range(n))
  for a in range(n):
   b=(a+1)%n
   if ((v>>a)&1)!=((v>>b)&1):
    j=idx[v^(1<<a)^(1<<b)]
    H[j,i]-=t
    J[j,i]+=s.I*t*(1-2*((v>>a)&1))
 B=s.zeros(N*N); jvec=s.Matrix(list(J))
 for x in range(N):
  for y in range(N):
   row=x*N+y
   if x!=y: B[row,row]+=s.Rational((states[x]^states[y]).bit_count(),2)*d+r
   else:
    for z in range(N): B[row,z*N+z]+=s.Rational(1,N)
   for z in range(N):
    B[row,z*N+y]+=-s.I*H[x,z]
    B[row,x*N+z]+=s.I*H[z,y]
 if J.is_zero_matrix: response=0
 else:
  sol=s.linsolve((B,jvec)); v=next(iter(sol))
  response=s.factor((s.conjugate(jvec).T*s.Matrix(v))[0])
 print('sector',k,'unnormalized response',response,flush=True)
 out+=response
out=s.factor(out/(n*2**n)); print('f(r)=',out)
print('poles=',s.nroots(s.denom(out),maxsteps=500))
print('df(0)=',s.diff(out,r).subs(r,0)); print('f(0)=',out.subs(r,0))

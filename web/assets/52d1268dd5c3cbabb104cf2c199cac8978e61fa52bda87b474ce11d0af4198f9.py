import cmath, math, json
import numpy as np

def sectors(N):
    js=np.arange(N%2/2,N/2+1,1)
    logs=[]
    for j in js:
        logchoose=math.lgamma(N+1)-math.lgamma(N/2-j+1)-math.lgamma(N/2+j+1)
        logs.append(2*math.log(2*j+1)-math.log(N/2+j+1)+logchoose-N*math.log(2))
    w=np.exp(logs)
    return js,w

def tr_H(N,A,b):
    js,w=sectors(N)
    ans=0
    for j,p in zip(js,w):
        ms=np.arange(-j,j+1,1)
        ans+=p*np.mean(np.exp(-A*j*(j+1)/N-b*ms/math.sqrt(N)))
    return float(ans)

def tr_H_Weyl(N,A,b,k):
    js,w=sectors(N)
    kk=np.linalg.norm(k); q=kk/(2*math.sqrt(N)); z=b/(2*math.sqrt(N))
    t=cmath.cosh(z)*math.cos(q)-1j*(k[2]/kk)*cmath.sinh(z)*math.sin(q)
    eta=2*cmath.acosh(t)
    ans=0j
    for j,p in zip(js,w):
        character=cmath.sinh((2*j+1)*eta/2)/((2*j+1)*cmath.sinh(eta/2))
        ans+=p*math.exp(-A*j*(j+1)/N)*character
    return ans

def K(A,b):
    return (1+A/2)**(-1.5)*math.exp(b*b/(8+4*A))

rows=[]
for A,b in [(.2,1),(.5,2),(.8,.5)]:
    k=np.array([.7,-.4,1.1]); kk=np.linalg.norm(k)
    V=1/(4+2*A)
    limit=K(A,b)*cmath.exp(-V*kk*kk/2-1j*b*V*k[2])
    for N in [16,64,256,1024,4096]:
        cross=tr_H_Weyl(N,A,b,k)
        t=kk/math.sqrt(N)
        a=math.sin(t)/t; d=(math.sin(t)-t*math.cos(t))/(t*t)
        g=math.exp(-kk*kk/9)
        l2sq=(a*a+d*d)**N+g*g-2*g*(a*math.cos(t/3)+d*math.sin(t/3))**N
        rows.append(dict(N=N,A=A,b=b,weight_sum=float(sectors(N)[1].sum()),Z_N=tr_H(N,A,b),Z_limit=K(A,b),H2_N=tr_H(N,2*A,2*b),H2_limit=K(2*A,2*b),cross_real=cross.real,cross_imag=cross.imag,cross_limit_real=limit.real,cross_limit_imag=limit.imag,cross_error=abs(cross-limit),fixed_fourier_L2_sq=l2sq))
out=dict(status='exact finite-sector floating arithmetic; diagnostics only',rows=rows)
with open('work/agents/thermal_window/trace_lift_checks.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))

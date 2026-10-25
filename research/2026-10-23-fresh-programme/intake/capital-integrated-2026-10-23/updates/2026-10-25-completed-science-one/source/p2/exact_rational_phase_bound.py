"""Exact-rational full-Hilbert residual bound for three Morse code levels.

No floating point enters matrix construction, linear solving, residuals,
norm upper bounds or final error upper bounds. Decimal floats in JSON are
display only. All upper square roots are checked by integer squaring.
The standard rational upper bound 3.141592653589794 > pi is used.
"""
from __future__ import annotations
from fractions import Fraction as Q
from math import comb,factorial,isqrt
from pathlib import Path
import json,time

SCALE=10**12
PI_UPPER=Q(3141592653589794,10**15)


def sqrt_upper(x):
    assert x>=0
    z=isqrt((x.numerator*SCALE*SCALE)//x.denominator)
    if z*z*x.denominator<x.numerator*SCALE*SCALE:z+=1
    result=Q(z,SCALE)
    assert result*result>=x
    return result


def dot(x,y):return sum((a*b for a,b in zip(x,y)),Q(0))


def calculate(n,J=128,N=8):
    D=Q(1);eps=Q(1,N*N);omega=Q(2,N);offset=Q(1,2);c=omega/(offset+omega)
    size=N+J+4
    def native(m):
        pref=Q((2*N-2*m-1)*factorial(m),factorial(2*N-m-1))
        w=[]
        for j in range(N):
            total=0
            for ell in range(m+1):
                p=N-m-1+ell
                if p>=j:
                    total+=(-1)**ell*comb(2*N-m-1,m-ell)*factorial(p)//factorial(ell)*comb(p,j)
            w.append(Q((-1)**j*total))
        assert pref*dot(w,w)==1
        return pref,w
    native_data=[native(m) for m in range(N)]
    pref,w=native_data[n];v=w+[Q(0)]*(size-N)
    energies=[D-eps*Q(2*N-2*m-1,2)**2 for m in range(N)];E=energies[n]
    fd=[Q(2*j+1,2*N) for j in range(size)];fo=[-Q(j+1,2*N) for j in range(size-1)]
    hd=[D+eps*(-j+(j+1-N)*(2*j+1)-Q(1,4))-E for j in range(size)]
    ho=[-eps*(j+1-N)*(j+1) for j in range(size-1)]
    def tri(diag,off,x):
        out=[a*b for a,b in zip(diag,x)]
        for j,b in enumerate(off):out[j]+=b*x[j+1];out[j+1]+=b*x[j]
        return out
    def ff(x):return tri(fd,fo,x)
    def gg(x):return [a-c*b for a,b in zip(ff(x),ff(ff(x)))]
    assert not any(tri(hd,ho,v))
    assert all(dot(w,native_data[m][1])==0 for m in range(N) if m!=n)
    fv=ff(v);u1=[x/(offset+omega) for x in fv]
    for m in range(n):
        pm,wm=native_data[m];de=energies[m]-E
        scale=2*de*pm*dot(wm,fv[:N])/((offset-de)*(offset+omega))
        for j in range(N):u1[j]+=scale*wm[j]
    equation=[a-offset*b+d for a,b,d in zip(tri(hd,ho,u1),u1,gg(v))]
    assert not any(equation)
    chi=pref*dot(v,gg(u1));s=[a-chi*b for a,b in zip(gg(u1),v)]
    assert dot(v,s)==0
    u2=[Q(0)]*size
    for m in range(N):
        if m==n:continue
        pm,wm=native_data[m];scale=-pm*dot(wm,s[:N])/(energies[m]-E)
        for j in range(N):u2[j]+=scale*wm[j]
    assert dot(v,u2)==0
    # Exact symmetric tridiagonal solve in the continuum trial block.
    dd=[];rr=[]
    for j in range(J):
        d=hd[N+j];r=-s[N+j]
        if j:
            factor=ho[N+j-1]/dd[-1]
            d-=factor*ho[N+j-1];r-=factor*rr[-1]
        assert d>0
        dd.append(d);rr.append(r)
    x=[Q(0)]*J
    for j in range(J-1,-1,-1):x[j]=(rr[j]-(ho[N+j]*x[j+1] if j<J-1 else 0))/dd[j]
    for j in range(J):
        z=max(Q(0),min(Q(1),Q(2*j-J,J-2)))
        window=1-10*z**3+15*z**4-6*z**5
        u2[N+j]=x[j]*window
    residual=[a+b for a,b in zip(tri(hd,ho,u2),s)]
    r3=[a-chi*b for a,b in zip(gg(u2),u1)]
    norm=lambda z:sqrt_upper(pref*dot(z,z))
    a=norm(u1);b=norm(u2);rho=norm(residual);r=norm(r3);vn=norm(gg(v))
    gap=min([abs(e-E) for m,e in enumerate(energies) if m!=n]+[D-E])
    err=rho/gap;herr=abs(E)*err+rho
    verr=sqrt_upper(2*herr**2+(64*eps**2+Q(17,2)*eps*D)*err**2)
    gerr=c*verr/D+(1+2*c)*sqrt_upper(verr*err/D)+(1+c)*err
    return {'n':n,'J':J,'energy':E,'chi':chi,'a':a,'b_upper':b+err,
      'r3_upper':r+gerr,'rho_upper':rho,'Vn_upper':vn,'gap':gap}


def code_bound(columns,g):
    e=[x['energy'] for x in columns];chi=[x['chi'] for x in columns]
    weight=(e[1]-e[0])/(e[2]-e[0])
    curvature=chi[1]-(1-weight)*chi[0]-weight*chi[2]
    tau_upper=PI_UPPER/(4*abs(curvature));errors=[]
    for col in columns:
        a=col['a'];b=col['b_upper'];r=col['r3_upper'];ch=col['chi']
        error=2*sqrt_upper(g*g*a*a+g**4*b*b)
        error+=tau_upper*g*sqrt_upper(r*r+g*g*ch*ch*b*b)
        error+=5*g*col['Vn_upper'];errors.append(error)
    squared=sum((x*x for x in errors),Q(0));code=sqrt_upper(squared)
    return {'g':g,'tau_upper':tau_upper,'plateau_duration_upper':tau_upper/(g*g),
      'column_error_bounds':errors,'code_isometry_error_upper':code,
      'continuum_probability_upper':min(Q(1),squared),'exact_chi_curvature':curvature}


def encode(x):
    if isinstance(x,Q):return {'rational':str(x),'decimal_display':float(x)}
    if isinstance(x,list):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x


if __name__=='__main__':
    t=time.monotonic();cols=[calculate(n) for n in [2,4,6]]
    data={'columns':cols,'code_bounds':[code_bound(cols,Q(1,1000)),code_bound(cols,Q(1,10000))],
      'scope':'Exact rational matrix, trial resolvent, residual and norm upper bounds; display floats only.',
      'elapsed_seconds':time.monotonic()-t}
    Path(__file__).with_suffix('.json').write_text(json.dumps(encode(data),indent=2)+'\n')
    print(json.dumps(encode(data),indent=2))

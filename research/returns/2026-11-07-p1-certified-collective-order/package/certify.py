"""Exact certificates for attractive cubic networks.

Every function in this module uses rational arithmetic. Floating proposals
are supplied separately and have no authority over the certificate.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from exact import require, psd, up, sqrt_up, qbits, encode


def matvec(A,x):
    return [sum((a*b for a,b in zip(row,x)),Q(0)) for row in A]


def quadratic(A,x):
    return sum((a*b for a,b in zip(x,matvec(A,x))),Q(0))


def matrix_bound(A):
    return max((sum(map(abs,row),Q(0)) for row in A),default=Q(0))


def residual(T,beta,h,q):
    return [v+b*x**3-f for v,b,x,f in zip(matvec(T,q),beta,q,h)]


def energy(T,beta,h,q):
    return quadratic(T,q)/2+sum((b*x**4/4-f*x
        for b,f,x in zip(beta,h,q)),Q(0))


def connected_z(T):
    n=len(T)
    require(n>0 and all(len(row)==n for row in T))
    require(all(T[i][j]==T[j][i] for i in range(n) for j in range(n)))
    require(all(T[i][j]<=0 for i in range(n) for j in range(n) if i!=j),
            'Attractive sign contract failed')
    seen={0}
    while True:
        more={j for i in seen for j in range(n) if T[i][j]<0 and i!=j}
        if more<=seen:break
        seen|=more
    require(len(seen)==n,'Connectedness contract failed')


def ground_certificate(T,beta,h,q):
    connected_z(T)
    require(all(b>0 for b in beta) and all(f>=0 for f in h))
    require(all(x>=0 for x in q))
    if all(x==0 for x in q):
        require(all(f==0 for f in h) and psd(T),'Zero is not certified global')
        return {'method':'exact PSD and positive quartic', 'candidate':q,
                'energy':Q(0),'lower_energy':Q(0),'gap':Q(0),
                'amplitude_error_L2':Q(0),'status':'PASS'}
    require(all(x>0 for x in q),'This checker requires positive candidates')
    b=min(beta); z=[x*x for x in q]; F=residual(T,beta,h,q)
    grad=[f/(2*x) for f,x in zip(F,q)]
    # Minimize the exact strongly convex quadratic minorant over z>=0.
    minimizer=[max(Q(0),x-2*g/b) for x,g in zip(z,grad)]
    delta=[s-x for s,x in zip(minimizer,z)]
    gap=-sum((g*d+b*d*d/4 for g,d in zip(grad,delta)),Q(0))
    require(gap>=0)
    value=energy(T,beta,h,q)
    # ||q-q*||^4 <= 4 n gap / b, using exact upward square roots.
    radius=sqrt_up(sqrt_up(4*len(q)*gap/b))
    H=[[T[i][j]+(3*beta[i]*q[i]**2 if i==j else 0)
        for j in range(len(q))] for i in range(len(q))]
    return {'method':'strongly convex squared-amplitude lower bound',
            'candidate':q,'residual':F,'squared_amplitude_gradient':grad,
            'minorant_minimizer':minimizer,'energy':value,
            'lower_energy':value-gap,'gap':gap,'amplitude_error_L2':radius,
            'candidate_hessian_PSD':psd(H),'status':'PASS'}


def relative_bracket(T,beta,h,q):
    if all(x==0 for x in q):
        require(all(f==0 for f in h) and psd(T))
        return {'lower':q,'upper':q,'theta':Q(0),'status':'PASS'}
    connected_z(T);require(all(x>0 for x in q))
    theta=Q(1,1<<35)
    for _ in range(34):
        lower=[(1-theta)*x for x in q]
        upper=[(1+theta)*x for x in q]
        fl=residual(T,beta,h,lower);fu=residual(T,beta,h,upper)
        if max(fl)<=0 and min(fu)>=0:
            return {'lower':lower,'upper':upper,'theta':theta,
                    'lower_residual':fl,'upper_residual':fu,'status':'PASS'}
        theta*=2
    raise ValueError('Proposal did not yield a finite positive bracket')


def static_model(path):
    obj=json.loads(Path(path).read_text());r=obj['r']
    require(obj['certificate']['status']=='PASS')
    A=[list(map(Q,row)) for row in obj['A']]
    poles=list(map(Q,obj['poles']))
    residues=[[list(map(Q,row)) for row in R] for R in obj['residues']]
    require(all(l>=Q(obj['a']) for l in poles))
    require(all(psd(R) for R in residues))
    S=[[A[i][j]-sum((R[i][j]/l for R,l in zip(residues,poles)),Q(0))
        for j in range(r)] for i in range(r)]
    E=up(Q(obj['certificate']['operator_error']),30)
    return S,E,obj


def assembled_inputs(paths,calibration):
    models=[static_model(p) for p in paths]
    sizes=[len(v[0]) for v in models];n=sum(sizes)
    S=[[Q(0) for _ in range(n)] for _ in range(n)]
    d=[[Q(calibration) for _ in range(n)] for _ in range(n)]
    block_errors=[];start=0
    for M,E,_ in models:
        block_errors.append(E)
        for i in range(len(M)):
            for j in range(len(M)):
                S[start+i][start+j]=M[i][j]
                d[start+i][start+j]+=E
        start+=len(M)
    return S,d,max(block_errors)+calibration,block_errors


def outer_tasks(T,beta,h,d,beta_error,field_error):
    n=len(T)
    upperT=[[T[i][j]+d[i][j] for j in range(n)] for i in range(n)]
    lowerT=[[T[i][j]-d[i][j] for j in range(n)] for i in range(n)]
    lowerh=[f-e for f,e in zip(h,field_error)]
    upperh=[f+e for f,e in zip(h,field_error)]
    upperb=[b+e for b,e in zip(beta,beta_error)]
    lowerb=[b-e for b,e in zip(beta,beta_error)]
    require(all(x>=0 for x in lowerh) and min(lowerb)>0)
    connected_z(upperT);connected_z(lowerT)
    return (upperT,upperb,lowerh),(lowerT,lowerb,upperh)


def design(p,beta,h,W,Shat,sigma):
    n=len(p);require(all(x>0 for x in p))
    require(all(s in (-1,1) for s in sigma))
    wp=matvec(W,p)
    T=[[-W[i][j]+(wp[i]/p[i]+h[i]/p[i]-beta[i]*p[i]**2 if i==j else 0)
        for j in range(n)] for i in range(n)]
    connected_z(T)
    # T is in the q=Sigma*y coordinates; K is the physical port law.
    K=[[Shat[i][j]-sigma[i]*sigma[j]*T[i][j]
        for j in range(n)] for i in range(n)]
    require(all(v==0 for v in residual(T,beta,h,p)))
    return T,K


def robust_design_certificate(T,beta,h,p,d,beta_error,field_error,theta):
    require(0<theta<1)
    (Tl,bl,hl),(Tu,bu,hu)=outer_tasks(T,beta,h,d,beta_error,field_error)
    lower=[(1-theta)*x for x in p];upper=[(1+theta)*x for x in p]
    # Worst residual for a subsolution uses larger T,beta and smaller field.
    fl=residual(Tl,bl,hl,lower);fu=residual(Tu,bu,hu,upper)
    require(max(fl)<=0 and min(fu)>=0,'Robust pattern margin failed')
    return {'lower':lower,'upper':upper,'relative_radius':theta,
            'worst_lower_residual':fl,'worst_upper_residual':fu,
            'lower_margin':-max(fl),'upper_margin':min(fu),'status':'PASS'}


def max_fraction_bits(obj):
    if isinstance(obj,Q):return qbits(obj)
    if isinstance(obj,dict):return max((max_fraction_bits(v) for v in obj.values()),default=0)
    if isinstance(obj,(tuple,list)):return max((max_fraction_bits(v) for v in obj),default=0)
    return 0


def save(path,obj):
    Path(path).write_text(json.dumps(encode(obj),indent=2,sort_keys=True)+'\n')

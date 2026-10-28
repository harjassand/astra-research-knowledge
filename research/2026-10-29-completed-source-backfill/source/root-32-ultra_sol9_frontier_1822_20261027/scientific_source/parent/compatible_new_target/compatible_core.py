"""Actual compatible Fourier gradients with unregularized background deflation.

Exact target strings, including L+M=1e-10, are retained. Floating searches
produce candidates only. Exact Laurent-polynomial replay is separate.
"""
import pathlib,json,itertools,math
from fractions import Fraction as F
import numpy as np
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parent
TARGET=json.loads((ROOT/'TARGET.json').read_text())
EXACT_COEFF=list(map(F,TARGET['coefficients']))
SCALE=1/float(EXACT_COEFF[0])

def tensor():
    a,b,c,d=sp.symbols('a b c d');u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    bases=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
    poly=sp.Poly(sum(sp.Rational(x.numerator,x.denominator)*p for x,p in zip(EXACT_COEFF,bases)),a,b,c,d)
    coeff={e:F(int(z.p),int(z.q))for e,z in poly.terms()}
    t=np.empty((4,)*4)
    for inds in itertools.product(range(4),repeat=4):
        e=tuple(inds.count(i)for i in range(4));multiplicity=math.factorial(4)//math.prod(math.factorial(x)for x in e)
        t[inds]=float(coeff.get(e,F(0)))/multiplicity*SCALE
    return t,coeff
TENSOR,POLYNOMIAL=tensor()
COEFF=np.array(list(map(float,EXACT_COEFF)))*SCALE

def value(x):
    a,b,c,d=np.moveaxis(np.asarray(x),-1,0);u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    A,B,C,E,G,H,L,M,N=COEFF
    return A*u*u+B*v*v+C*u*v+E*w*w+G*u*w+H*v*w+L*q*u+M*q*v+N*q*w

def gradient(x):
    a,b,c,d=np.moveaxis(np.asarray(x),-1,0);u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    A,B,C,E,G,H,L,M,N=COEFF
    fu=2*A*u+C*v+G*w+L*q;fv=2*B*v+C*u+H*w+M*q;fw=2*E*w+G*u+H*v+N*q;fq=L*u+M*v+N*w
    return np.stack([2*a*fu+b*fw+d*fq,2*b*fv+a*fw-c*fq,2*c*fu+d*fw-b*fq,2*d*fv+c*fw+a*fq],axis=-1)

class FourierProblem:
    def __init__(self,frequencies,grid=None):
        self.frequencies=np.array(frequencies,dtype=int);self.m=len(frequencies)
        minimum=4*int(np.max(abs(self.frequencies)))+1
        self.grid=minimum if grid is None else max(minimum,int(grid))
        xy=np.array(list(np.ndindex(self.grid,self.grid)))*2*np.pi/self.grid
        phase=xy@self.frequencies.T
        profiles=np.stack([np.cos(phase),np.sin(phase)],axis=2)
        self.profiles=profiles
        self.units=self.frequencies/np.linalg.norm(self.frequencies,axis=1)[:,None]
        self.design=np.zeros((len(xy),self.m,2,2,4))
        for j,k in enumerate(self.units):
            self.design[:,j,:,0,:2]=profiles[:,j,:,None]*k
            self.design[:,j,:,1,2:]=profiles[:,j,:,None]*k
        self.design=self.design.reshape(len(xy),4*self.m,4)
        self.N=len(xy)

    def evaluate(self,p,details=False):
        norm=np.linalg.norm(p)
        if norm<1e-100:raise ValueError('zero Fourier input')
        q=p/norm;x=np.einsum('npi,p->ni',self.design,q)
        cov=x.T@x/self.N;h=12*np.einsum('ijkl,kl->ij',TENSOR,cov)
        b=np.mean(gradient(x),axis=0);c=float(np.mean(value(x)));m2=float(np.trace(cov))
        he=np.linalg.eigvalsh(h)
        assert he[0]>=.99*(SCALE/200000)*m2,(he,m2)
        background=-np.linalg.solve(h,b)
        gap=c+float(b@background)/2
        square=np.sum(x*x,axis=1);m4=float(np.mean(square*square));objective=gap/m4
        # Exact envelope derivative, expanded before averaging to avoid
        # subtracting two potentially large cubic background values.
        g=gradient(x)+12*np.einsum('ijkl,j,nk,nl->ni',TENSOR,background,x,x,optimize=True)
        linear=12*np.einsum('ijkl,j,k->il',TENSOR,background,background)
        g+=x@linear.T
        g=(g-objective*(4*square[:,None]*x))/m4
        gq=np.einsum('npi,ni->p',self.design,g)/self.N
        gp=(gq-q*np.dot(q,gq))/norm
        if not details:return objective,gp
        direct=float(np.mean(value(x+background))-value(background))
        determinant=x[:,0]*x[:,3]-x[:,1]*x[:,2]
        return {'objective_scaled':objective,'gap_scaled':gap,'original_gap':gap/SCALE,
            'fourth_moment':m4,'second_moment':m2,'c_scaled':c,'Schur_loss_scaled':-float(b@background)/2,
            'background':background.tolist(),'averaged_Hessian_eigenvalues_scaled':he.tolist(),
            'covariance_eigenvalues':np.linalg.eigvalsh(cov).tolist(),
            'mean_gradient_max':float(np.max(abs(np.mean(x,axis=0)))),
            'mean_determinant':float(np.mean(determinant)),
            'direct_gap_scaled':direct,'direct_deflation_difference':direct-gap,
            'gradient_norm':float(np.linalg.norm(gp)),
            'normalized_gradient_amplitudes':q.reshape(self.m,2,2).tolist(),
            'potential_amplitudes':(q.reshape(self.m,2,2)/np.linalg.norm(self.frequencies,axis=1)[:,None,None]).tolist(),
            'frequencies':self.frequencies.tolist(),'grid':self.grid}

def half_square(cutoff):
    return [(i,j)for i in range(cutoff+1)for j in range(-cutoff,cutoff+1)if i>0 or(i==0 and j>0)]

def derivative_check():
    problem=FourierProblem([(1,0),(0,1),(1,1),(1,-1)])
    p=np.random.default_rng(721).normal(size=16);v,g=problem.evaluate(p)
    eps=1e-6;fd=[]
    for i in range(len(p)):
        e=np.zeros_like(p);e[i]=eps
        fd.append((problem.evaluate(p+e)[0]-problem.evaluate(p-e)[0])/(2*eps))
    error=float(np.max(np.abs(np.array(fd)-g)));assert error<2e-6
    pure=np.zeros(16);pure[0]=1
    assert abs(problem.evaluate(pure)[0]-1)<1e-12
    return {'finite_difference_max_error':error,'pure_wave_objective_scaled':problem.evaluate(pure)[0],
        'L_plus_M_exact':str(EXACT_COEFF[6]+EXACT_COEFF[7])}

#!/usr/bin/env python3
"""Three targeted compatible negative searches after convex amplitude elimination.

Positive cubic periodic B-spline density, fixed exact phase and mass.
No finite positive output is a continuum bound. A negative output would need
independent continuum certification before being promoted.
"""
import json,time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parent
D=8
FLOOR=1e-4

def basis(points):
 h=2*np.pi/D
 t=(points[:,None]/h-np.arange(D)[None,:]+D/2)%D-D/2
 a=np.abs(t);sgn=np.sign(t)
 b=np.where(a<1,(4-6*a*a+3*a**3)/6,np.where(a<2,(2-a)**3/6,0.))
 db=np.where(a<1,sgn*(-12*a+9*a*a)/6,np.where(a<2,-sgn*(2-a)**2/2,0.))/h
 assert np.max(np.abs(b.sum(axis=1)-1))<1e-13
 assert np.max(np.abs(db.sum(axis=1)))<1e-13
 return b,db

def grid(order):
 z,w=leggauss(order);h=2*np.pi/D
 one=np.ravel((np.arange(D)[:,None]+(z[None,:]+1)/2)*h)
 ww=np.tile(w/(2*D),D)
 bx,dx=basis(one)
 B=np.einsum("xi,yj->xyij",bx,bx).reshape(len(one)**2,D*D)
 X=np.einsum("xi,yj->xyij",dx,bx).reshape(len(one)**2,D*D)
 Y=np.einsum("xi,yj->xyij",bx,dx).reshape(len(one)**2,D*D)
 x,y=np.meshgrid(one,one,indexing="ij")
 return [B,X,Y,np.outer(ww,ww).ravel()],x.ravel(),y.ravel()

def phase(name,x,y):
 if name=="shear_control":
  return np.cos(2*x),np.ones_like(y)
 if name=="separable_fold":
  return np.cos(x),np.cos(y)
 if name=="crossed_fold":
  return np.cos(x)*np.sin(y),np.sin(x)*np.cos(y)
 raise ValueError(name)

def evaluate_factory(name,order):
 mats,x,y=grid(order);B,X,Y,w=mats
 kx,ky=phase(name,x,y)
 def fn(c,grad=True):
  rho=B@c; a=(X@c)/(4*rho);b=(Y@c)/(4*rho)
  u=a*a+kx*kx;v=b*b+ky*ky;q=a*ky-b*kx
  z=u+v-2*q
  gf=3*z*z+(35/24)*u*u+q*q-2.5*q*u
  f=float(np.dot(w,rho*gf))
  if grad:
   ga=12*z*(a-ky)+(35/6)*u*a+2*q*ky-2.5*ky*u-5*a*q
   gb=12*z*(b+kx)-2*q*kx+2.5*kx*u
   gradient=B.T@(w*(gf-a*ga-b*gb))+X.T@(w*ga/4)+Y.T@(w*gb/4)
   return f,gradient
  return f
 return fn,B

def simplex_projection(v):
 """Euclidean projection onto coefficient floor and sum D^2."""
 z=v-FLOOR;mass=D*D*(1-FLOOR)
 u=np.sort(z)[::-1]
 css=np.cumsum(u)-mass
 eligible=np.flatnonzero(u-css/np.arange(1,len(u)+1)>0)
 j=eligible[-1]
 threshold=css[j]/(j+1)
 return np.maximum(z-threshold,0)+FLOOR

def solve(fn,initial):
 """Spectral projected gradient with Armijo descent, bounded by 1500 steps."""
 c=initial.copy();f,g=fn(c);alpha=1.
 ledger=[]
 for iteration in range(1500):
  gap=float(np.dot(g,c-FLOOR)-D*D*(1-FLOOR)*np.min(g))
  if iteration%100==0:ledger.append({"iteration":iteration,"objective":f,"FW_gap":gap})
  if gap<1e-8:return c,f,g,iteration,ledger,"FW gap below tolerance"
  direction=simplex_projection(c-alpha*g)-c
  slope=np.dot(g,direction)
  if slope>=-1e-16:return c,f,g,iteration,ledger,"projected direction numerically stationary"
  step=1.
  for backtrack in range(50):
   trial=c+step*direction
   ft,gt=fn(trial)
   if ft<=f+1e-4*step*slope:break
   step*=.5
  else:return c,f,g,iteration,ledger,"line search exhausted"
  dc=trial-c;dg=gt-g
  denom=np.dot(dc,dg)
  alpha=float(np.clip(np.dot(dc,dc)/denom,1e-8,1e5)) if denom>0 else 1.
  c,f,g=trial,ft,gt
 return c,f,g,1500,ledger,"bounded iteration limit"

results=[]
for name in ["shear_control","separable_fold","crossed_fold"]:
 fn,B=evaluate_factory(name,6)
 start=time.time();initial=np.ones(D*D)
 direction=np.sin(np.arange(D*D));direction-=direction.mean()
 delta=1e-6
 derivative=(fn(initial+delta*direction,False)-fn(initial-delta*direction,False))/(2*delta)
 assert abs(derivative-np.dot(fn(initial)[1],direction))<1e-5
 coefficients,f,g,iterations,ledger,message=solve(fn,initial)
 gap=float(np.dot(g,coefficients-FLOOR)-(D*D*(1-FLOOR))*np.min(g))
 refined,_=evaluate_factory(name,10)
 fine=refined(coefficients,False)
 rec={"phase":name,"density_basis":"periodic cardinal cubic B-splines",
  "knots_per_axis":D,"coefficient_floor":FLOOR,
  "mass_mean":float(coefficients.mean()),"initial_energy":float(fn(initial)[0]),
  "final_energy_quadrature6":f,"reevaluation_quadrature10":fine,
  "finite_convex_program_FW_gap":max(0.,gap),
  "finite_convex_program_lower_bound":f-max(0.,gap),
  "message":message,"iterations":iterations,"iteration_ledger":ledger,
  "seconds":time.time()-start,
  "coefficient_min":float(coefficients.min()),"coefficient_max":float(coefficients.max()),
  "sample_density_min":float((B@coefficients).min()),
  "sample_density_max":float((B@coefficients).max()),
  "coefficients":coefficients.tolist(),
  "scope":"Compatible continuous fields and analytic density positivity; quadrature/optimization exploratory only."}
 results.append(rec)
 out={"scope":"Three targeted negative searches. No positive result certifies continuum positivity.",
      "results":results}
 (ROOT/"concentrated_density_search.json").write_text(json.dumps(out,indent=2)+"\n")
 print({k:v for k,v in rec.items() if k!="coefficients"},flush=True)

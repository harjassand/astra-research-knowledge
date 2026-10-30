"""Search the unrestricted-minor-support obstruction via an analytic cut family.

For diagonal bases, the best off-diagonal positive-determinant cut is minimized
analytically, not acquired by a pointwise oracle. Negative cuts are ordinary
diagonal directions. A positive result is only accepted after exact replay.
NumPy only; no numerical optimizer package or network.
"""
import json,math,time
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent

def pars(tau):
    return (1-3*tau*tau)/(1+3*tau*tau),4-12*tau/(1+3*tau*tau)

def gap(theta,logw,beta,r):
    w=np.exp(np.clip(logw,-20,20));x=np.cos(theta);y=np.sin(theta)
    C=4*r-2
    f=1+w**4+C*w*w+4*beta*(w**3-w)
    ga=4+2*C*w*w+4*beta*(-3*w+w**3)
    gd=-4*w**3-2*C*w+4*beta*(1-3*w*w)
    haa=12+2*C*w*w-24*beta*w
    had=-4*C*w+12*beta*(1-w*w)
    hdd=12*w*w+2*C+24*beta*w
    c2=(haa*x*x+2*had*x*y+hdd*y*y)/2
    c1=ga*x+gd*y
    lower=-(c2-c1*c1/(4*f))/w
    upper=4*np.sqrt(np.maximum(0,1-4*beta*beta*x*x*y*y))+4*beta*(x*x-y*y)+8*(r-1)*x*y
    return lower-upper

def nelder_mead(x0,beta,r,steps=300):
    ss=np.array([x0,np.array(x0)+[.03,0],np.array(x0)+[0,.05]],dtype=float)
    ff=np.array([float(gap(*x,beta,r)) for x in ss])
    for _ in range(steps):
        order=np.argsort(ff)[::-1];ss=ss[order];ff=ff[order]
        mid=(ss[0]+ss[1])/2
        refl=mid+(mid-ss[2]);fr=float(gap(*refl,beta,r))
        if fr>ff[0]:
            ex=mid+2*(refl-mid);fe=float(gap(*ex,beta,r))
            ss[2],ff[2]=(ex,fe) if fe>fr else (refl,fr)
        elif fr>ff[1]:ss[2],ff[2]=refl,fr
        else:
            co=mid+.5*(ss[2]-mid);fc=float(gap(*co,beta,r))
            if fc>ff[2]:ss[2],ff[2]=co,fc
            else:
                ss[1:]=ss[0]+.5*(ss[1:]-ss[0]);ff[1:]=[float(gap(*x,beta,r)) for x in ss[1:]]
        if np.max(np.abs(ss-ss[0]))<1e-10:break
    ii=int(np.argmax(ff));return ss[ii],float(ff[ii])

def search(tau):
    beta,r=pars(tau)
    tt=np.linspace(-math.pi/2,math.pi/2,401)[:,None]
    ww=np.linspace(-5,5,401)[None,:]
    values=gap(tt,ww,beta,r)
    best=sorted(np.ndenumerate(values),key=lambda xx:xx[1],reverse=True)[:12]
    candidates=[nelder_mead([float(tt[i,0]),float(ww[0,j])],beta,r) for (i,j),_ in best]
    point,value=max(candidates,key=lambda xx:xx[1])
    theta,logw=map(float,point);x,y=math.cos(theta),math.sin(theta)
    z=math.sqrt((2*(x*x+y*y)-4*beta*x*y)/(2*(x*x+y*y)+4*beta*x*y))
    return {'tau':tau,'beta':beta,'r':r,'base_ratio_y_over_x':y/x,
            'Rplus_c_over_minus_b':z,'Rminus_minus_d_over_a':math.exp(logw),
            'normalized_support_cut_gap':value,'theta':theta,'logw':logw}

if __name__=='__main__':
    start=time.time()
    ans=[search(tau) for tau in (1/30,1/6,1/5,1/4,.3,.32,.33)]
    (HERE/'pc_cut_search_result.json').write_text(json.dumps({'search':ans,'seconds':time.time()-start},indent=2)+'\n')
    print(json.dumps(ans,indent=2))

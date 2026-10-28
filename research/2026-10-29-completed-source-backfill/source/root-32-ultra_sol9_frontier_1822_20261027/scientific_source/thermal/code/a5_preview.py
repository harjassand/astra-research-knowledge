"""Full-state, numerical five-angle A5-sector p4/p6 feasibility preview.

No trace or mode-count output from this float64 file is a certified input.
This is the parent-requested diagnostic before any cyclotomic acquisition.
"""
import json,time,math
import numpy as np
import scipy.linalg as la
from acquire_cycle_moments import cycle,ROOT

def spectra(n):
    angles=[0.,np.pi,2*np.pi/3,2*np.pi/5,4*np.pi/5]
    out=[[]for t in angles]
    for mag in range(2*n+1):
        h,words=cycle(n,mag,'I');p,_=cycle(n,mag,'P')
        if not len(words):continue
        ds=np.array([math.prod(1/math.sqrt(math.comb(4,int(x)))for x in w)for w in words])
        physical=h.toarray()*ds[:,None]/ds[None,:]/2
        exchange=(h-p).toarray()*ds[:,None]/ds[None,:]/4
        diagonal=physical-exchange;up=np.triu(exchange);down=np.tril(exchange,-1)
        for k,t in enumerate(angles):
            vals=la.eigvalsh(diagonal+np.exp(1j*t)*up+np.exp(-1j*t)*down,check_finite=False)
            out[k].extend(vals.tolist()*(1 if mag==0 else 2))
    assert all(len(es)==5**n for es in out)
    return [np.array(x)for x in out]

def project(z):
    phi=(1+math.sqrt(5))/2;phip=(1-math.sqrt(5))/2
    i,p,c,f,g=z
    return {'1':(i+15*p+20*c+12*f+12*g)/60,
            '3':(3*i-15*p+12*phi*f+12*phip*g)/60,
            '3prime':(3*i-15*p+12*phip*f+12*phi*g)/60,
            '4':(4*i+20*c-12*f-12*g)/60,
            '5':(5*i+15*p-20*c)/60}

def main():
    start=time.monotonic();raw={p:spectra(p)for p in [4,6]}
    data=json.loads((ROOT/'results/scalar_loop_certificate.json').read_text());rows=[]
    dims={'1':1,'3':3,'3prime':3,'4':4,'5':5}
    for b,bname in [(1.5,'3/2'),(3.,'3'),(6.,'6')]:
        theta=next(x['theta_J_lower']for x in data['rows']if x['beta_exact']==bname)
        moments={p:project([float(np.exp(-b*es).sum()/5**p)for es in raw[p]])for p in raw}
        radii={};tau=0;chosen={}
        for ir in dims:
            options=[]
            for p in [4,6]:
                mass=moments[p][ir]-(theta**p if ir=='1'else 0.)
                radius=max(0.,mass)**(1/p);options.append((radius,p,mass))
            radius,p,mass=min(options);radii[ir]=radius;chosen[ir]=p
            tau+=dims[ir]*(radius/theta)**256
        item={'beta':b,'scalar_theta':theta,'moments':moments,'radii':radii,
              'radius_over_theta':{k:r/theta for k,r in radii.items()},
              'selected_moments':chosen,'relative_loop_tail_proposal':tau,
              'scope':'NUMERICAL_PREVIEW_ONLY_NO_ACCEPTED_INCREMENT'}
        rows.append(item);print(json.dumps(item),flush=True)
    result={'status':'NUMERICAL_A5_FIVE_ANGLE_FEASIBILITY','rows':rows,'seconds':time.monotonic()-start}
    (ROOT/'results/a5_preview.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()

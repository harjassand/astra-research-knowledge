"""Finite diagnostic of rational graded hats; not proof or formal certification."""
from pathlib import Path
import json
import numpy as np

cases = [
    ('uniform', lambda x: np.full_like(x, .5), .5, .5, 0.),
    ('linear', lambda x: .5*(1+.8*x), .1, .9, .4),
    ('cusp', lambda x: (1+np.abs(x))/3, 1/3, 2/3, 1/3),
    ('sine', lambda x: .5*(1+.6*np.sin(np.pi*x)), .2, .8, .3*np.pi),
]
z, w = np.polynomial.legendre.leggauss(80)
results=[]
for name, rho, minimum, maximum, lipschitz in cases:
    for J in [4,8,16,32,64]:
        s=np.arange(J+1)/J
        nodes=-1+6*s*s-4*s*s*s
        mass=np.zeros(J+1)
        moment=np.zeros(J+1)
        fmean={theta:np.zeros(J+1) for theta in [-1.,-.1,.01,.5,1.]}
        integrals={theta:0. for theta in fmean}
        raw={theta:np.exp(theta*z) for theta in fmean}
        norm={theta:np.dot(w,rho(z)*raw[theta]) for theta in fmean}
        for k in range(J):
            a,b=nodes[k:k+2]
            x=(a+b)/2+(b-a)/2*z
            measure=(b-a)/2*w*rho(x)
            left=(b-x)/(b-a)
            right=(x-a)/(b-a)
            for j,hat in [(k,left),(k+1,right)]:
                mass[j]+=np.dot(measure,hat)
                moment[j]+=np.dot(measure,hat*x)
                for theta in fmean:
                    fmean[theta][j]+=np.dot(measure,hat*np.exp(theta*x))/norm[theta]
        centroids=moment/mass
        B=4*maximum/minimum+3*lipschitz/(2*minimum)
        ratio=float(np.max(np.abs(centroids-nodes))*J*J/B)
        x=np.linspace(-1,1,20001)
        k=np.searchsorted(nodes,x,side='right')-1
        k=np.clip(k,0,J-1)
        bary=(x-nodes[k])/(nodes[k+1]-nodes[k])
        max_defect=0.
        for theta in fmean:
            local=fmean[theta]/mass
            kf=(1-bary)*local[k]+bary*local[k+1]
            truth=np.exp(theta*x)/norm[theta]
            C=np.exp(2)*(B+45/8)*abs(theta)
            max_defect=max(max_defect,float(np.max(np.abs(kf-truth))*J*J/C))
        results.append(dict(reference=name,J=J,normalization=float(mass.sum()),
                            centroid_bound_ratio=ratio,defect_bound_ratio=max_defect))
assert all(abs(x['normalization']-1)<1e-9 for x in results)
assert all(x['centroid_bound_ratio']<=1+1e-8 for x in results)
assert all(x['defect_bound_ratio']<=1+1e-8 for x in results)
out=dict(status='finite numerical diagnostics passed; not a proof',fixtures=results,
         max_centroid_ratio=max(x['centroid_bound_ratio'] for x in results),
         max_defect_ratio=max(x['defect_bound_ratio'] for x in results))
Path(__file__).with_name('scalar_diagnostics.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='fixtures'}))

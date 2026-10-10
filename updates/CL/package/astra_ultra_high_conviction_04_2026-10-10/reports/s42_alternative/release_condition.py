"""Positive-time conditioning of the independent release functions.

Even supplied direct couplings and exact leading subtraction are assumed here.
This is a favorable conditioning diagnostic, not an end-to-end acquisition test.
"""
import json
import numpy as np
import mpmath as mp

def basis_value(c, tau, arithmetic):
    sqrt,log=arithmetic.sqrt,arithmetic.log
    m=len(c)
    vals=[]
    def oriented(i,j):
        a=2*c[i]**2; b=2*c[j]**2
        u=sqrt(1+b*tau); v=sqrt(1+a*tau)
        ratio=a/b; aa=1-ratio
        coeff=3*aa**2/(4*b*sqrt(ratio))
        integral=(u*v*(2*ratio*u*u+5*aa)-(2*ratio+5*aa))/(4*b)
        integral+=coeff*log((sqrt(ratio)*u+v)/(sqrt(ratio)+1))
        h=(1+a*tau)**(-arithmetic.mpf(3)/2) if arithmetic is mp else (1+a*tau)**(-1.5)
        return (c[i]*c[j]/3+c[i]**3*c[j]*integral)*h
    for i in range(m):
        for j in range(i,m):
            vals.append(oriented(i,j)+(oriented(j,i) if j!=i else 0))
    return vals


def main():
    records=[]
    for family in ('bounded_range','integer','geometric'):
        for m in range(2,13):
            if family=='bounded_range':
                c=np.linspace(0.7,1.3,m)
            elif family=='integer':
                c=np.arange(1,m+1,dtype=float)
            else:
                c=2.0**(np.arange(m)/2)
            tau=np.r_[0,np.geomspace(1e-5/c.max()**2,1e3/c.min()**2,500)]
            mat=np.array([basis_value(c,t,np) for t in tau])
            norms=np.linalg.norm(mat,axis=0)
            s=np.linalg.svd(mat/norms,compute_uv=False)
            records.append(dict(family=family,hidden_nodes=m,unknowns=m*(m+1)//2,
                                column_normalized_condition=float(s[0]/s[-1]),
                                singular_min=float(s[-1]),singular_max=float(s[0])))
    
    # Recompute selected small cases with 70-digit arithmetic to distinguish real
    # ill-conditioning from floating-point quadrature or cancellation artifacts.
    mp.mp.dps=70
    for m in (2,3,4,5,6):
        c=[mp.mpf('0.7')+mp.mpf('0.6')*i/(m-1) for i in range(m)]
        tau=[mp.mpf(0)]+[mp.power(10,mp.mpf(-5)+mp.mpf(8)*i/119) for i in range(120)]
        mat=mp.matrix([basis_value(c,t,mp) for t in tau])
        for col in range(mat.cols):
            norm=mp.sqrt(sum(mat[row,col]**2 for row in range(mat.rows)))
            for row in range(mat.rows): mat[row,col]/=norm
        s=mp.svd(mat,compute_uv=False)
        smallest=s[s.rows-1]
        records.append(dict(family='bounded_range_70digits',hidden_nodes=m,
                            unknowns=m*(m+1)//2,
                            column_normalized_condition=mp.nstr(s[0]/smallest,18),
                            singular_min=mp.nstr(smallest,18),
                            singular_max=mp.nstr(s[0],18)))
        print(json.dumps(records[-1]),flush=True)
    
    with open(__file__.replace('.py','_results.json'),'w') as f:
        json.dump(records,f,indent=2)
    print(json.dumps(records,indent=2))


if __name__ == "__main__":
    main()

"""Independent coordinate-to-table check for archive minima 1, 7 and 16.

Coordinates are the first sixteen fixed 38-line records, streamed from the
preserved official archive. Only selected records are used. No basin labels
are inferred for any other node.
"""
from pathlib import Path
import itertools,json,time
import numpy as np
from scipy.special import sph_harm_y
from scipy.spatial import cKDTree

HERE=Path(__file__).resolve().parent
def isometries(x,tol=2e-6):
    # Map an independent ordered basis of centered atom vectors to every
    # triple with matching Gram entries; verify all 38 mapped atom positions.
    x=x-x.mean(axis=0)
    triples=np.array(list(itertools.combinations(range(len(x)),3)))
    det=np.abs(np.linalg.det(x[triples]))
    a=triples[det.argmax()]
    ref=x[a]
    gram=ref@ref.T
    norms=np.sum(x*x,axis=1)
    candidates=[np.flatnonzero(np.abs(norms-gram[k,k])<tol) for k in range(3)]
    tree=cKDTree(x)
    maps=set()
    for i,j,k in itertools.product(*candidates):
        target=x[[i,j,k]]
        if np.max(np.abs(target@target.T-gram))>tol: continue
        q=np.linalg.solve(ref,target)
        if np.max(np.abs(q@q.T-np.eye(3)))>tol: continue
        distances,perm=tree.query(x@q)
        if distances.max()<tol and len(set(perm))==len(x): maps.add(tuple(perm))
    return len(maps)

def inspect(x):
    n=len(x); energy=0.; h=np.zeros((3*n,3*n)); grad=np.zeros((n,3)); bonds=[]
    for i in range(n):
        for j in range(i+1,n):
            v=x[i]-x[j]; r2=float(v@v); inv=1/r2; r6=inv**3
            energy+=4*(r6*r6-r6)
            a=24*r6*inv*(1-2*r6)
            d=(672*inv**8-192*inv**5)*np.outer(v,v)+a*np.eye(3)
            si=slice(3*i,3*i+3); sj=slice(3*j,3*j+3)
            h[si,si]+=d; h[sj,sj]+=d; h[si,sj]-=d; h[sj,si]-=d
            grad[i]+=a*v; grad[j]-=a*v
            if r2<1.391**2: bonds.append(v/np.sqrt(r2))
    eig=np.linalg.eigvalsh(h)
    x=x-x.mean(axis=0)
    inertia=np.eye(3)*np.sum(x*x)-x.T@x
    v=np.array(bonds); theta=np.arccos(np.clip(v[:,2],-1,1)); phi=np.arctan2(v[:,1],v[:,0])
    q={}
    for l in (4,6):
        lm=np.array([np.mean(sph_harm_y(l,m,theta,phi)) for m in range(-l,l+1)])
        q[f"Q{l}_cutoff_1.391"]=float(np.sqrt(4*np.pi/(2*l+1)*np.sum(np.abs(lm)**2)))
    return {"computed_LJ_energy":energy,"max_gradient_absolute":float(np.max(np.abs(grad))),
            "near_zero_hessian_eigenvalues":eig[:6].tolist(),"first_positive_hessian_eigenvalue":float(eig[6]),
            "computed_log_product_positive_hessian":float(np.log(eig[6:]).sum()),
            "computed_inertia_eigenvalues":np.linalg.eigvalsh(inertia).tolist(),
            "verified_point_group_isometry_count":isometries(x),"bond_count":len(bonds),**q}

def main():
    st=time.perf_counter()
    minima=np.load(HERE/"audited_tables.npz")["minima"]
    coords=np.loadtxt(HERE/"coordinate_first16.raw").reshape(16,38,3)
    result={}
    for identifier in (1,7,16):
        x=inspect(coords[identifier-1]); row=minima[identifier-1]
        x.update({"archive_id":identifier,"table_energy":float(row[0]),"table_hessian_log_product":float(row[1]),
                  "table_point_group_order":int(row[2]),"table_inertia":row[3:].tolist(),
                  "energy_difference":x["computed_LJ_energy"]-float(row[0]),
                  "hessian_log_difference":x["computed_log_product_positive_hessian"]-float(row[1])})
        result[str(identifier)]=x
    result["seconds"]=time.perf_counter()-st
    (HERE/"COORDINATE_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()

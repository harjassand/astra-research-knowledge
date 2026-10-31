"""Raw-input noncommuting monotone Gaussian capacity compiler (candidate)."""
from pathlib import Path
from fractions import Fraction as F
from time import perf_counter
import hashlib, json, sys
import sympy as sp

PARENT=Path(__file__).resolve().parents[1]
EXPECTED="8ff7aeebe56217463b7976b389d9931c3952a5f4e51f1f3b55d8f54e27652131"
if hashlib.sha256((PARENT/"capacity.py").read_bytes()).hexdigest()!=EXPECTED:
    raise RuntimeError("accepted parent arithmetic source changed")
sys.path.insert(0,str(PARENT))
from capacity import Unknown, rat, strict_positive_int, Integrator, interval_json, fraction_string


def decode(raw):
    if type(raw) is not dict or set(raw)!={"n","terms"}:
        raise Unknown("raw schema")
    n=raw["n"]
    if type(n) is not int or n<3 or type(raw["terms"]) is not list:
        raise Unknown("dimension/terms")
    terms={}
    for rec in raw["terms"]:
        if type(rec) is not dict or set(rec)!={"powers","coefficient"}:
            raise Unknown("term schema")
        p=rec["powers"]
        if type(p) is not list or len(p)!=n or any(type(k)is not int or k<0 for k in p):
            raise Unknown("exponent vector")
        p=tuple(p);a=rat(rec["coefficient"])
        if p in terms or not a or sum(p)>10:
            raise Unknown("duplicate, zero or excess degree")
        terms[p]=a
    if not terms or max(map(sum,terms))!=10:
        raise Unknown("degree-ten family required")
    return n,terms


def encode_terms(n,terms):
    return {"n":n,"terms":[{"powers":list(p),"coefficient":str(a)} for p,a in sorted(terms.items(),reverse=True) if a]}


def aligned_terms(H1,H2,j=0):
    n=H1.rows; terms={}
    def add(i,k,yp,a):
        if not a:return
        p=[0]*n;p[j]=yp;p[i]+=1;p[k]+=1;p=tuple(p)
        terms[p]=terms.get(p,0)+a
        if not terms[p]:del terms[p]
    for i in range(n):
        if i!=j:add(i,i,0,sp.Rational(1,2))
        for k in range(i,n):
            mul=sp.Rational(1,2) if i==k else sp.Integer(1)
            for yp,a in [(0,1),(2,-2),(4,1)]:add(i,k,yp,mul*a*H1[i,k])
            for yp,a in [(0,1),(2,-4),(4,6),(6,-4),(8,1)]:add(i,k,yp,mul*a*H2[i,k])
    return terms


def fixture(m,rotate=False):
    if m%2:raise ValueError("even fixture m")
    n=m+1;H1=sp.zeros(n);H2=sp.zeros(n)
    for r in range(m//2):
        i=1+2*r;t=sp.Rational(r,8*m)
        H1[i,i]=sp.Rational(1,2)+t;H1[i+1,i+1]=sp.Rational(3,4)+t
        H1[i,i+1]=H1[i+1,i]=sp.Rational(1,16)
        H2[i,i]=sp.Rational(1,4)+t;H2[i+1,i+1]=sp.Rational(1,2)+t
    if not rotate:return encode_terms(n,aligned_terms(H1,H2))
    xs=sp.symbols(f"x0:{n}");x=sp.Matrix(xs);u=sp.Matrix(range(1,n+1))
    Q=sp.eye(n)-2*u*u.T/u.dot(u);ell=Q[:,0];Pi=ell*ell.T
    H1=Q*H1*Q.T;H2=Q*H2*Q.T;s=(x.T*Pi*x)[0]
    expr=sp.expand(((x.T*(sp.eye(n)-Pi)*x)[0]+(1-s)**2*(x.T*H1*x)[0]+(1-s)**4*(x.T*H2*x)[0])/2)
    return encode_terms(n,dict(sp.Poly(expr,*xs).terms()))


def components(*matrices):
    n=matrices[0].rows; unseen=set(range(n));out=[]
    while unseen:
        todo=[unseen.pop()];comp=[]
        while todo:
            i=todo.pop();comp.append(i)
            near=[j for j in unseen if any(M[i,j]!=0 for M in matrices)]
            for j in near:unseen.remove(j);todo.append(j)
        out.append(sorted(comp))
    return out


def psd(M,strict=False):
    """Exact symmetric Schur elimination with zero-diagonal guard."""
    if M!=M.T:return False
    A=sp.MutableDenseMatrix(M)
    while A.rows:
        if any(A[i,i]<0 for i in range(A.rows)):return False
        inds=[i for i in range(A.rows) if A[i,i]>0]
        if not inds:return not strict and A==sp.zeros(A.rows)
        k=inds[0]
        if k:A.row_swap(0,k);A.col_swap(0,k)
        v=A[1:,0];A=sp.MutableDenseMatrix(A[1:,1:]-v*v.T/A[0,0])
    return True


def psd_by_graph(M,strict=False):
    return all(psd(M.extract(c,c),strict) for c in components(M))


def norm_upper(M,max_doublings=128):
    if M==sp.zeros(M.rows):return sp.Integer(0),1
    u=sp.Integer(1)
    for k in range(max_doublings+1):
        if psd_by_graph(u*sp.eye(M.rows)-M):return u,k+1
        u*=2
    raise Unknown("spectral upper certificate budget exhausted")


def energy_matrix(terms,n,yp,j):
    M=sp.zeros(n)
    for p,a in terms.items():
        if p[j]!=yp or sum(p)!=yp+2:continue
        rem=list(p);rem[j]=0;inds=[i for i,k in enumerate(rem) for _ in range(k)]
        if len(inds)!=2:raise Unknown("quadratic extraction")
        i,k=inds
        if i==k:M[i,i]+=2*a
        else:M[i,k]+=a;M[k,i]+=a
    return M


def acquire(raw):
    start=perf_counter();n,terms=decode(raw);m=n-1
    top=[p for p in terms if sum(p)==10]
    candidates=[j for j in range(n) if min(p[j] for p in top)==8]
    fast=False
    if len(candidates)==1:
        j=candidates[0];H2=energy_matrix(terms,n,8,j)
        H1=energy_matrix(terms,n,4,j)-6*H2
        if aligned_terms(H1,H2,j)==terms:
            u=sp.eye(n)[:,j];Pi=u*u.T;fast=True
    if not fast:
        xs=sp.symbols(f"x0:{n}");x=sp.Matrix(xs)
        def hom(d):return sp.Poly.from_dict({p:a for p,a in terms.items() if sum(p)==d},xs).as_expr()
        Q=sp.hessian(hom(2),xs);ns=Q.nullspace()
        if len(ns)!=1:raise Unknown("quadratic nullspace is not unique")
        u=ns[0];u=u/next(a for a in u if a);Pi=u*u.T/u.dot(u);s=(x.T*Pi*x)[0]
        q2,r2=sp.div(2*hom(10),s**4,*xs)
        q1,r1=sp.div(2*hom(6),s**2,*xs)
        if r1!=0 or r2!=0 or sp.Poly(q1,*xs).total_degree()!=2 or sp.Poly(q2,*xs).total_degree()!=2:
            raise Unknown("matrix polynomial quotient failure")
        H2=sp.hessian(q2,xs)/2;H1=sp.hessian(q1,xs)/2-6*H2
        got=sp.Poly.from_dict(terms,xs)
        expected=((x.T*(sp.eye(n)-Pi)*x)[0]+(1-s)**2*(x.T*H1*x)[0]+(1-s)**4*(x.T*H2*x)[0])/2
        if sp.Poly(got.as_expr()-expected,*xs)!=sp.Poly(0,*xs):raise Unknown("full polynomial identity")
    if H1!=H1.T or H2!=H2.T or H1*u!=sp.zeros(n,1) or H2*u!=sp.zeros(n,1):
        raise Unknown("physical fiber identity")
    if not psd_by_graph(H1+Pi,True) or not psd_by_graph(H2):
        raise Unknown("fiber positivity")
    u1,tr1=norm_upper(H1);u2,tr2=norm_upper(H2)
    t=sp.Symbol("t");dp=sp.Poly(1,t);blocks=components(H1,H2)
    for c in blocks:
        dd=(sp.eye(len(c))+t*H1.extract(c,c)+t*t*H2.extract(c,c)).det()
        dp*=sp.Poly(dd,t)
    coeff=[dp.nth(i) for i in range(dp.degree()+1)]
    if coeff[0]!=1 or any(c<=0 for c in coeff):raise Unknown("determinant coefficient certificate")
    tail_det=(H1+Pi).det()
    if tail_det<=0:raise Unknown("tail determinant")
    comm=H1*H2-H2*H1
    return {"schema":"monotone_matrix_acquisition.v1","n":n,"m":m,
            "direction":[str(a) for a in u],"direction_norm_squared":str(u.dot(u)),
            "H1":[[str(a) for a in H1.row(i)] for i in range(n)],
            "H2":[[str(a) for a in H2.row(i)] for i in range(n)],
            "u1":str(u1),"u2":str(u2),"norm_tests":tr1+tr2,
            "determinant_coefficients":[str(c) for c in coeff],"determinant_degree":dp.degree(),
            "tail_det_H1":str(tail_det),"tail_exponent_physical_m":m,
            "commutator_squared_frobenius":str(sum(a*a for a in comm)),
            "raw_terms":len(terms),"route":"aligned_full_dictionary" if fast else "quadratic_nullspace_projector_full_identity",
            "acquired_joint_component_sizes":[len(c) for c in blocks],
            "seconds":perf_counter()-start}


def new_integrator(acq,p,max_points,max_bits):
    ii=Integrator(None,p,[F(c) for c in acq["determinant_coefficients"]],max_points,max_bits)
    # Physical Gaussian dimension is NOT the determinant polynomial degree.
    # The tail uses A>=v H1 and det_+(H1), independently of rank(H2).
    ii.m=acq["m"];ii.leading=F(acq["tail_det_H1"])
    return ii


def certify(raw,beta=F(1),quad_relative=F(1,100),max_grid=131072,
            max_points=524288,max_cutoff=65536,max_precision=16384,max_product_bits=2000000):
    if type(beta)is not F or beta<=0 or type(quad_relative)is not F or quad_relative<=0:
        raise Unknown("exact positive external task")
    for name,value in [("grid",max_grid),("points",max_points),("cutoff",max_cutoff),("precision",max_precision),("bits",max_product_bits)]:
        strict_positive_int(value,name)
    if max_grid<64 or max_cutoff<2:raise Unknown("initial budget")
    start=perf_counter();acq=acquire(raw);m=acq["m"];p=max(192,8*m+128)
    if p>max_precision:raise Unknown("precision budget")
    ii=new_integrator(acq,p,max_points,max_product_bits)
    seed=ii.monotone_integral(F(1),F(5,4),32,0)[0]
    if seed<=0:raise Unknown("unresolved seed")
    T=F(2)
    while ii.tail(T)>quad_relative*seed/8:
        T*=2
        if T>max_cutoff:raise Unknown("cutoff budget")
    N=64
    while True:
        if N>max_grid or N*(2*int(T)+1)>max_points:raise Unknown("total grid budget")
        aa=ii.monotone_integral(F(1,2),F(1),N,0)
        bb=ii.monotone_integral(F(1),T,2*N*int(T-1),0)
        mass=(aa[0]+bb[0],aa[1]+bb[1]+ii.tail(T))
        rr=ii.monotone_integral(F(0),F(1,2),N,1);res=(2*rr[0],2*rr[1])
        if min(mass+res)>0 and mass[1]*res[1]<=(1+quad_relative)*mass[0]*res[0]:break
        N*=2
    factor=1+(2*F(acq["u1"])+4*F(acq["u2"]))/beta
    free=(1/(beta*mass[1]*res[1]),1/(beta*mass[0]*res[0]))
    full=(free[0]/factor,free[1])
    return {"schema":"monotone_matrix_capacity.v1","acquisition":acq,
            "beta":fraction_string(beta),"b":"1/2","observable":"cap_mu(A,B)/mu(A)",
            "basins":"u.x <= -sqrt(u.u)/2 and u.x >= sqrt(u.u)/2",
            "factor":fraction_string(factor),"mass":interval_json(mass),"resistance":interval_json(res),
            "free_energy_rate":interval_json(free),"full_rate":interval_json(full),
            "N":N,"T":str(T),"precision_bits":p,"tail_upper":fraction_string(ii.tail(T)),
            "exact_points":len(ii.cache),"horner_multiply_adds":ii.polynomial_multiply_adds,
            "max_determinant_rational_bits":ii.max_integer_bits,"seconds":perf_counter()-start}


def verify(raw,certificate,**external_task):
    """Sound incomplete receiver, paying the entire adaptive construction again."""
    expected=certify(raw,**external_task)
    if type(certificate)is not dict:raise Unknown("certificate schema")
    for k in ["schema","beta","b","observable","basins","factor","N","T","precision_bits","tail_upper"]:
        if type(certificate.get(k))is not type(expected[k]) or certificate.get(k)!=expected[k]:raise Unknown("external task or interval binding: "+k)
    got=certificate.get("acquisition")
    if type(got)is not dict:raise Unknown("acquisition record")
    for k,v in expected["acquisition"].items():
        if k!="seconds" and (type(got.get(k))is not type(v) or got.get(k)!=v):raise Unknown("raw acquisition binding: "+k)
    for name in ["mass","resistance","free_energy_rate","full_rate"]:
        if type(certificate.get(name))is not dict:raise Unknown("interval record")
        for side in ["lower","upper"]:
            if certificate[name].get(side)!=expected[name][side]:raise Unknown("exact interval mismatch")
    return {"status":"PASS","scope":"recomputed exact raw-input acquired full-fiber capacity ratio",
            "m":expected["acquisition"]["m"],"determinant_degree":expected["acquisition"]["determinant_degree"]}


def main():
    results=[]
    for m in [2,4,16,32,64]:
        raw=fixture(m);out=certify(raw);results.append(out)
        print(json.dumps({"m":m,"degree":out["acquisition"]["determinant_degree"],
                          "commutator_norm2":out["acquisition"]["commutator_squared_frobenius"],
                          "factor":out["factor"],"low":out["full_rate"]["lower_display"],
                          "high":out["full_rate"]["upper_display"],"seconds":out["seconds"]}),flush=True)
    Path("results.json").write_text(json.dumps(results,indent=2))
    raw=fixture(4,True);out=certify(raw)
    Path("rotated_fixture.json").write_text(json.dumps({"raw":raw,"certificate":out},indent=2))
    print("rotated",out["acquisition"]["raw_terms"],out["factor"],out["seconds"],flush=True)

if __name__=="__main__":main()

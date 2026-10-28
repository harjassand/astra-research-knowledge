"""Entire isotropic ROC/QC cone at each chosen contact transform; no t grid."""
from pathlib import Path
source=Path(__file__).with_name('acquire.py').read_text()
# Reuse only the exact feature compiler/helpers; no previous solve is run.
prefix=source.split('columns=[];metadata=[];seen=set();start=time.monotonic()')[0]
exec(compile(prefix,str(Path(__file__).with_name('acquire.py')),'exec'))
OUT=Path(__file__).resolve().parent/'full_cone';OUT.mkdir(exist_ok=True)
centers=[s.zeros(2),A,-A,2*A,s.diag(0,2),s.diag(2,0),s.diag(s.Rational(1,2),s.Rational(3,2)),s.diag(s.Rational(3,2),s.Rational(1,2)),s.Matrix([[0,1],[1,0]])]
maps=[(p,n,r,0) for p,n,r in product([s.Rational(1,2),1,2],[s.Rational(1,2),1,2],[0,2])]
maps += [(s.Rational(8,21),s.Rational(21,4),r,0) for r in [0,2]]
maps += [(s.Rational(21,8),s.Rational(4,21),r,0) for r in [0,2]]
maps += [(1,s.Rational(21,4),r,0) for r in [0,2]]
maps += [(s.Rational(8,21),1,r,0) for r in [0,2]]
columns=[[],[],[]];metadata=[];seen=set();now=time.monotonic()
for (p,n,ir,jr),center in product(maps,centers):
    P=s.diag(p,1)*rot[ir];N=rot[jr]*s.diag(n,1);B=P*(X-center)*N
    tt=sum(z*z for z in B);qq=B.det()
    polys=[s.Poly(s.expand(z),*x) for z in [tt*tt,tt*qq,qq*qq]]
    norm=sum(abs(c) for e,c in polys[0].terms() if sum(e)==4)
    vecs=[breg(z.as_expr()/norm) for z in polys];key=tuple(np.concatenate(vecs))
    if key in seen:continue
    seen.add(key)
    for j in range(3):columns[j].append(vecs[j])
    metadata.append({'P':[str(v) for v in P],'S':[str(v) for v in N],'center':[str(v) for v in center],'normalization':str(norm)})
D=[np.stack(c,axis=1) for c in columns];n=len(metadata)
print('compiled',n,'full isotropic cones',time.monotonic()-now,flush=True)
(OUT/'DICTIONARY.json').write_text(json.dumps({'models':metadata,'rows':rows,'features':features},indent=2)+'\n')
np.savez(OUT/'COMPILED.npz',D0=D[0],D1=D[1],D2=D[2],G=G.toarray(),S=S.toarray())
m=s.Integer(197);beta=(m*m-1)/(m*m+1)
target=T*T+12*q*q+4*beta*q*xx
control=s.Rational(101,100)*T*T-s.Rational(9,4)*q*T
qv=np.array([float(s.Poly(q,*x).coeff_monomial(e)) for e in rows]);report=[]
for label,poly in [('QC_control',control),('target',target)]:
    gr=cp.Variable(105);k=cp.Variable();rho=cp.Variable()
    aa=cp.Variable(n,nonneg=True);bb=cp.Variable(n);cc=cp.Variable(n)
    ww=(8/3)*(cc+2*aa);R=cp.reshape(S@gr,(14,14),order='C')
    eq=G@gr+k*qv+D[0]@aa+D[1]@bb+D[2]@cc==breg(poly)
    constraints=[R-rho*np.eye(14)>>0,rho<=1,bb<=4*aa,bb>=-4*aa,
                 cp.SOC(aa+ww,cp.vstack([2*bb,aa-ww]),axis=0),eq]
    problem=cp.Problem(cp.Maximize(rho-1e-10*cp.sum(aa+ww)),constraints);start=time.monotonic()
    problem.solve(solver='CLARABEL',max_iter=180,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
    out={'label':label,'status':problem.status,'scope':'NUMERICAL_POINT_CONTACT_ONLY','models':n,'seconds':time.monotonic()-start,'margin':None if rho.value is None else float(rho.value)}
    if gr.value is not None:
        out.update(equality_error=float(np.max(np.abs(eq.violation()))),selector=float(k.value),total_a=float(sum(aa.value)))
        np.savez(OUT/(label+'.npz'),gram=R.value,k=k.value,rho=rho.value,a=aa.value,b=bb.value,c=cc.value,dual=eq.dual_value)
    report.append(out);print(json.dumps(out),flush=True)
    (OUT/'ACQUISITION.json').write_text(json.dumps(report,indent=2)+'\n')

"""Change the diffusion representation before judging heat insufficiency.

Find a positive anisotropic diffusion and a closed polynomial correction
for a fixed ROC quartic. Finite numerical feasibility is only a proposal.
"""
from pathlib import Path
root=Path(__file__).resolve().parents[1];ss=(root/'work/hessian_heat_sos.py').read_text();ns={'__file__':str(root/'work/hessian_heat_sos.py'),'__name__':'heat_linear_helpers'};exec(ss[:ss.index('class HeatModel:')],ns);globals().update({k:v for k,v in ns.items() if k not in ('__name__','__file__')});start=time.perf_counter();rd=np.zeros((3,60,15))
for l,P in enumerate(m.monomials):
 HH=[[b.diff(b.diff(P,i),j) for j in range(3)] for i in range(3)]
 for ii,(aa,cc) in enumerate(((0,0),(0,1),(1,1))):
  B=[[{} for _ in range(4)] for _ in range(4)]
  for q1,q2 in (((pi1,pi1),) if ii==0 else ((pi2,pi2),) if ii==2 else ((pi1,pi2),(pi2,pi1))):
   for i in range(3):
    for j in range(3):B[q1[i]][q2[j]]=b.add(B[q1[i]][q2[j]],HH[i][j])
  for pw in qa:
   for i in range(4):
    for j in range(i,4):rd[ii,index[pw,i,j],l]=float(B[i][j].get(pw,0))*(1 if i==j else 2)
src=json.loads((root/'work/hessian_heat_sos.json').read_text());records=[]
for row in src['records']:
 if row.get('maximum_Gram_margin',0)>0:continue
 hh=np.array(row['quartic_coefficients']);G=cp.Variable((12,12),symmetric=True);om=cp.Variable(18);D=cp.Variable((2,2),symmetric=True);margin=cp.Variable();target=rd[0]@hh*D[0,0]+rd[1]@hh*D[0,1]+rd[2]@hh*D[1,1];constraints=[cp.reshape(gc.reshape(60,144)@cp.reshape(G,(144,),order='C'),(60,),order='C')==target+oc@om,closure@om==0,G-margin*np.eye(12)>>0,D-R(1,10000)*np.eye(2)>>0,cp.trace(D)==1];prob=cp.Problem(cp.Maximize(margin),constraints)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-11,max_iter=500);rec={'name':row['name'],'status':prob.status,'margin':None if margin.value is None else float(margin.value),'diffusion':None if D.value is None else D.value.tolist(),'Gram':None if G.value is None else G.value.tolist(),'closed_two_form':None if om.value is None else om.value.tolist()}
 except cp.error.SolverError as err:rec={'name':row['name'],'status':'SOLVER_FAILED','error':str(err)}
 records.append(rec);print(json.dumps({k:v for k,v in rec.items() if k not in ('Gram','closed_two_form')}),flush=True)
(root/'work/hessian_anisotropic_heat.json').write_text(json.dumps({'records':records,'seconds':time.perf_counter()-start,'scope':__doc__},indent=2)+'\n')

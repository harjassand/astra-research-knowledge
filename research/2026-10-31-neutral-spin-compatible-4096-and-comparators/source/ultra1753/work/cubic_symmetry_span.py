"""Exact symmetry orbit of the globally QC C0 stabilizer."""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
import importlib.util,json,sys
root=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('compat',root/'outputs/gradient_compatibility/receive.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);d=g.gauge();b=g.b;ca=g.ca;r=g.r;F,C0,T=r.m.acquired();qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());ac=json.loads((root/'outputs/acoustic_capacity/certificate.json').read_text());op=list(map(lambda row:list(map(R,row)),qc['normal_form_operator']));jet=list(map(lambda row:list(map(R,row)),ac['jet_operator_on_normal_basis']));Q=ca.mm(jet,op)
A=[b.var(4,i) for i in range(4)];GA=[[R(0)]*4 for _ in range(4)]
for i,(j,s) in enumerate(zip((3,2,1,0),(1,-1,1,-1))):GA[i][j]=R(s)
rots=[(R(1),R(0)),(R(0),R(1)),(R(3,5),R(4,5)),(R(-4,5),R(3,5))];rows=[];polys=[];metadata=[]
for gamma,(x,y) in product((0,1),rots):
 UA=[[x,0,-y,0],[0,x,0,-y],[y,0,x,0],[0,y,0,x]]
 if gamma:UA=ca.mm(UA,GA)
 images=[b.add(*(b.scale(p,c) for p,c in zip(A,row))) for row in UA];C=r.compose(C0,images,4);assert r.compose(F,images,4)==F and r.compose(T,images,4)==T;polys.append(C);rows.append([C.get(tuple(pw),R(0)) for pw in d['powers']]);metadata.append({'Gamma':gamma,'rotation':list(map(str,(x,y)))})
J=ca.transpose(rows);Z=ca.mm(Q,J);rank=b.rank(Z);print('symmetry charge rank',rank,flush=True)
out={'orbit_parameters':metadata,'cubic_coefficient_rows':[[str(v) for v in row] for row in rows],'charge_matrix':[[str(v) for v in row] for row in Z],'charge_rank':rank,'governing_nu':4096}
if rank==8:
 Zi,_=ca.solve_range(Z,[[R(int(i==j)) for j in range(8)] for i in range(8)]);P=ca.scale(ca.mm(ca.transpose(Zi),Zi),8*4096);b.pd(P);opJ=ca.mm(op,J);Jtrans=[row for row in opJ[:4]]
 # Translate orbit moments back to the minimal coefficient gauge. This
 # offset affects the quadratic block, but never its eight correlations.
 EU=ca.mm(d['charge_representatives'],Z);delta=ca.add(J,ca.scale(EU,-1));tm=d['translations'];TT=ca.mm(ca.transpose(tm),tm);tg,_=ca.solve_range(TT,ca.mm(ca.transpose(tm),delta));assert ca.mm(tm,tg)==delta
 out.update({'charge_inverse':[[str(v) for v in row] for row in Zi],'QC_quadratic_coefficient_Gram':[[str(v) for v in row] for row in P],'translation_offsets':[[str(v) for v in row] for row in tg],'all_eight_modes_have_orbit_QC_stabilization':True})
 print('rough sufficient charge-Gram size',max(float(abs(v)) for row in P for v in row),flush=True)
(root/'work/cubic_symmetry_span.json').write_text(json.dumps(out,indent=2)+'\n')

import sympy as s,json
from pathlib import Path
root=Path(__file__).parent;f=json.loads((root/'fixture.json').read_text());D=s.Integer(f['denominator'])
rho=[[s.Matrix(f['real_numerators'][l][i])/D+s.I*s.Matrix(f['imag_numerators'][l][i])/D for i in range(3)]for l in range(2)]
I=s.eye(2);sig=[(I+s.Rational(3,5)*P)/2 for P in [s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]];q=s.Rational(1,5)
for blocks in rho:
 assert sum(s.trace(b) for b in blocks)==1
 for b in blocks:
  assert b==b.conjugate().T
  for A in [b-I/1000,s.Rational(3,5)*I-b]:assert A[0,0]>0 and s.factor(A.det())>0
B=[(p+m)/2 for p,m in zip(*rho)];H=[(p-m)/2 for p,m in zip(*rho)]
assert sum(s.trace(h) for h in H)==0

def sld(B,H):
 n=B.rows
 assert n==2
 b0=s.trace(B)/2;h0=s.trace(H)/2;Bd=B-b0*s.eye(2);Hd=H-h0*s.eye(2)
 l0=s.cancel((b0*h0-s.trace(Bd*Hd)/2)/(b0*b0-s.trace(Bd*Bd)/2))
 L=(l0*s.eye(2)+(Hd-l0*Bd)/b0).applyfunc(s.cancel)
 assert (B*L+L*B-2*H).applyfunc(s.simplify)==s.zeros(2)
 return s.factor(s.trace(H*L)),L
input_costs=[];Lin=[]
for b,h in zip(B,H):g,L=sld(b,h);input_costs.append(g);Lin.append(L)
gi=sum(input_costs);gr,Lr=sld(sum(B,s.zeros(2)),sum(H,s.zeros(2)))
Bo=sum([s.kronecker_product(S,b) for S,b in zip(sig,B)],s.zeros(4));Ho=sum([s.kronecker_product(S,h) for S,h in zip(sig,H)],s.zeros(4));rf=json.loads((root/'receiver.json').read_text());Lo=(s.Matrix(rf['real_numerators'])+s.I*s.Matrix(rf['imag_numerators']))/rf['denominator'];go=s.factor(2*s.trace(Ho*Lo)-s.trace(Bo*Lo*Lo));gs=q*gi+(1-q)*gr;gap=s.factor(go-gs)
assert gap>s.Rational(1,200)
result={'target_fixed_receiver_risk_reduction':str(go),'source_explained_variance':str(gs),'input_SLD':str(gi),'reference_SLD':str(gr),'gap_exact':str(gap),'gap_decimal':float(gap),'target_fixed_receiver_risk':float(1-go),'source_MMSE':float(1-gs),'eigenvalue_bounds':['1/1000','3/5'],'reference_marginals_equal':sum(rho[0],s.zeros(2))==sum(rho[1],s.zeros(2)),'target_receiver':'fixed rational Hermitian observable, not asserted exactly optimal','all_assertions':'PASS'}
assert json.loads((root/'FIXED_RECEIVER_CERTIFICATE.json').read_text()) == result, 'Exact receiver fixture mismatch';print(json.dumps(result,indent=2))

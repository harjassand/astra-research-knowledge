"""Independent finite-matrix regression; not a proof of the uniform-N theorem."""
import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
I2=np.eye(2,dtype=complex); X2=np.array([[0,1],[1,0]],complex);Y2=np.array([[0,-1j],[1j,0]],complex);Z2=np.diag([1.,-1.]);Sm=np.array([[0,1],[0,0]],complex)
def at(n, pairs):
 a=np.array([[1.]],complex)
 for i in range(n):a=np.kron(a,pairs.get(i,I2))
 return a
norm=lambda a:float(np.linalg.norm(a,2))
rows=[]
for n in range(2,6):
 d=2**n;I=np.eye(d,dtype=complex)
 Hs=[.17*at(n,{i:Z2})+.09*at(n,{i:X2}) for i in range(n)]
 Hs += [.11*at(n,{i:X2,i+1:Y2}) for i in range(n-1)]
 Js=[.3*at(n,{i:Sm})+.07*at(n,{i:Z2}) for i in range(n)]
 Ds=[(-1)**i*.23*at(n,{i:Z2})-.04*I for i in range(n)]
 H=sum(Hs);Delta=sum(Ds)
 gates=[]
 for parity in range(2):
  gates.append([((.42 if i%3 else -.71),at(n,{i:X2,i+1:X2})+.2*at(n,{i:Z2})) for i in range(parity,n-1,2)])
 gates.append([((.35 if i%2 else -.26),at(n,{i:Y2})) for i in range(n)])
 XX=sum(w*A for layer in gates for w,A in layer)
 def Lc(O):
  v=1j*(H@O-O@H)
  for J in Js:
   G=J.conj().T@J;v+=J.conj().T@O@J-(G@O+O@G)/2
  return v
 def K(O):return Lc(O)-(Delta@O+O@Delta)/2
 def yy(u):
  Y=I.copy()
  for layer in gates:
   for w,A in layer:Y=Y@expm(u*w*A/2)
  return Y
 max_formula=0.;ratios=[];values={}
 for u in [.08,.04,.02,-.04,1.e-4,-1.e-4,0.]:
  Y=yy(u);Yi=np.linalg.inv(Y);G=Y.conj().T@Y
  B=Yi.conj().T@K(G)@Yi
  R=np.zeros_like(B)
  for J in Js:
   Ju=Y@J@Yi;Gu=Y@(J.conj().T@J)@Yi
   R+=Ju.conj().T@Ju-(Gu+Gu.conj().T)/2
  for He in Hs:
   Hu=Y@He@Yi;R+=1j*(Hu.conj().T-Hu)
  for De in Ds:
   Du=Y@De@Yi;R-=(Du+Du.conj().T)/2
  max_formula=max(max_formula,norm(B-R));values[u]=B
  if abs(u)>.001:ratios.append(norm(B+Delta-u*Lc(XX))/(n*u*u))
 first=norm((values[1.e-4]-values[-1.e-4])/2.e-4-Lc(XX))
 # Actual conservative physical generator tilted by a noncommuting positive S.
 S=expm(.08*sum(at(n,{i:Z2}) for i in range(n))+.03*at(n,{0:X2}))
 Si=np.linalg.inv(S)
 Jt=[S@J@Si for J in Js]
 K0=-1j*H-sum(J.conj().T@J for J in Js)/2
 Kt=S@K0@Si
 Dt=-(sum(J.conj().T@J for J in Jt)+Kt.conj().T+Kt)
 Ht=(Kt.conj().T-Kt)/(2j)
 def Lct(O):
  v=1j*(Ht@O-O@Ht)
  for J in Jt:
   GG=J.conj().T@J;v+=J.conj().T@O@J-(GG@O+O@GG)/2
  return v
 def Lw(O):return Si@Lc(S@O@S)@Si
 rng=np.random.default_rng(n);a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));O=(a+a.conj().T)/2
 tiltres=norm(Lw(O)-Lct(O)+(Dt@O+O@Dt)/2)
 u=.04;Y=yy(u);Yi=np.linalg.inv(Y);YS=Y@S;YSi=np.linalg.inv(YS);G=Y.conj().T@Y;W=S@G@S
 phys=YSi.conj().T@Lc(W)@YSi
 Bt=Yi.conj().T@(Lct(G)-(Dt@G+G@Dt)/2)@Yi
 pres=norm(phys-Bt)
 assert max_formula<2e-12 and first<1e-7 and pres<2e-12 and tiltres<2e-12
 rows.append({'N':n,'matrix_dimension':d,'signed_Delta_min':float(np.linalg.eigvalsh(Delta).min()),'signed_Delta_max':float(np.linalg.eigvalsh(Delta).max()),'exact_formula_max_residual':max_formula,'central_first_derivative_residual':first,'remainder_over_N_u2':ratios,'physical_YS_order_residual':pres,'tilted_conservative_GKLS_residual':tiltres})
out={'scope':'Unequal signed weights, noncommuting color layers, nonzero Hamiltonian, nonnormal jumps and indefinite total killing; finite algebra diagnostic only. Uniform cone proof is in receipt.','checks':rows}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

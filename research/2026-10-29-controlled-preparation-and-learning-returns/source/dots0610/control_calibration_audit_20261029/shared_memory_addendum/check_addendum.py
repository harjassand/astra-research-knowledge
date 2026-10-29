import pathlib, runpy, numpy as np, json
ROOT=pathlib.Path(__file__).resolve().parent
a=runpy.run_path(str(ROOT/'author_replay/check_shared_memory_v3.py'))
Es,Ds,N=a['Es'],a['Ds'],a['N']
I=np.eye(2);Z=np.diag([1.,-1.]);X=np.array([[0.,1.],[1.,0.]]);Y=np.array([[0.,-1j],[1j,0.]])
rst=[np.outer(I[:,0],I[:,f]) for f in range(2)]
errs=[]
for use_source in (False,True):
 target=[np.kron(Z if use_source else I,r) for r in rst]
 A=[d@(N if use_source else np.eye(32))@e for d in Ds for e in Es]
 mx=0.
 for j in range(4):
  for k in range(4):
   B=np.zeros((4,4));B[j,k]=1
   actual=sum(t@B@t.conj().T for t in A)
   expected=sum(t@B@t.conj().T for t in target)
   mx=max(mx,float(np.linalg.norm(actual-expected)))
 assert mx<1e-12;errs.append(mx)
for P in (I,X,Y,Z):
 A=P.conj().T@Z@P
 assert np.linalg.norm(np.kron(A.conj(),A)-np.kron(Z,Z))<1e-12
rng=np.random.default_rng(202610290450);maxgap=0.
for t in range(200):
 c=np.array([2.,9.6,1.]);w=np.exp(rng.normal(size=3));lam=np.sqrt(w*c);lam/=sum(lam)
 optimum=sum(np.sqrt(w*c))**2
 assert abs(sum(w*c/lam)-optimum)<1e-10
 for _ in range(10):
  test=rng.dirichlet(np.ones(3))
  assert sum(w*c/test)>=optimum-1e-10
out={'all_checks_passed':True,'full_logical_bath_matrix_unit_checks':32,'roundtrip_and_service_superoperator_residuals':errs,'all_four_Pauli_conjugations_preserve_AdZ':True,'weighted_role_optimization_cases':200,'random_comparisons':2000,'asymptotic_unweighted_coefficient':float((np.sqrt(2)+2*np.sqrt(2.4)+1)**2)}
(ROOT/'check_addendum.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

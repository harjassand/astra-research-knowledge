import numpy as np,sympy as sp,json
from scipy.linalg import expm
from pathlib import Path
PTH=Path(__file__).parent
I=np.eye(2);paulis=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def kron(*xs):
 r=np.array([[1.]])
 for x in xs:r=np.kron(r,x)
 return r
def permutation_swap(a,b,n):
 U=np.zeros((2**n,2**n))
 for j in range(2**n):
  bits=list(format(j,f'0{n}b'));bits[a],bits[b]=bits[b],bits[a];U[int(''.join(bits),2),j]=1
 return U
s=np.array([0,1,-1,0])/np.sqrt(2);v0=np.kron(s,s);v1=np.zeros(16);v1[[3,12]]=1/np.sqrt(3);v1[[5,6,9,10]]=-1/np.sqrt(12);V=np.column_stack([v0,v1]);P=V@V.T;S12=permutation_swap(0,1,4);S23=permutation_swap(1,2,4)
J=[sum(kron(*[a if i==j else I for i in range(4)]) for j in range(4))/2 for a in paulis]
assert max(np.linalg.norm(a@V) for a in J)<1e-14
rng=np.random.default_rng(1093)
def herm(n):
 A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return (A+A.conj().T)/2
U=np.eye(48,dtype=complex);UC=np.eye(2,dtype=complex);UM=np.eye(3,dtype=complex)
for dt in [.13,.27,.41]:
 Hm=herm(3);Bs=[herm(3)*7 for _ in range(3)];Hc=rng.normal()*S12+rng.normal()*S23
 H=kron(Hc,np.eye(3))+kron(np.eye(16),Hm)+sum(kron(j,b) for j,b in zip(J,Bs))
 U=expm(-1j*dt*H)@U;UC=expm(-1j*dt*(V.T@Hc@V))@UC;UM=expm(-1j*dt*Hm)@UM
E=kron(V,np.eye(3));memory_res=np.linalg.norm(U@E-E@kron(UC,UM),2)
# Actual eight-spin independent-block support check.
V8=kron(V,V);S_A=permutation_swap(0,1,8);S_B=permutation_swap(4,5,8);cross=permutation_swap(3,4,8)
zz=np.linalg.norm(V8.T@S_A@S_B@V8-kron(paulis[2],paulis[2]))
# A single boundary exchange really leaks product code despite preserving global singlet.
leak=float(np.linalg.norm((np.eye(256)-V8@V8.T)@expm(-.31j*cross)@V8[:,0])**2)
# finite oscillator thermal magnitudes and joint reference state full-loop.
N=60;a=np.diag(np.sqrt(np.arange(1,N)),1);num=a.T@a;T=2*np.pi;forces=[-.5,0,0,.5]
blocks=[expm(-1j*T*(num+f*(a+a.T))) for f in forces]
return_res=max(np.linalg.norm((u-np.exp(1j*2*np.pi*f*f)*np.eye(N))[:,:6],2) for u,f in zip(blocks,forces))
psi=rng.normal(size=(4,N,3))+1j*rng.normal(size=(4,N,3));psi[:,6:,:]=0;psi/=np.linalg.norm(psi)
after=np.stack([u@psi[i] for i,u in enumerate(blocks)]);ideal=np.stack([np.exp(1j*2*np.pi*f*f)*psi[i] for i,f in enumerate(forces)]);correlated_res=np.linalg.norm(after-ideal)
t=T+.13;nbar=.8;r=nbar/(nbar+1);rho=np.diag((1-r)*r**np.arange(N));f,g=-.5,.5;uf=expm(-1j*t*(num+f*(a+a.T)));ug=expm(-1j*t*(num+g*(a+a.T)));observed=abs(np.trace(uf@rho@ug.conj().T));expected=np.exp(-(2*nbar+1)*(f-g)**2*abs(1-np.exp(-1j*t))**2/2)
# Analytic symbolic pair example.
sym_s=sp.Matrix([1,-1])/sp.sqrt(2);sym_t=sp.Matrix([1,1])/sp.sqrt(2);X=sp.Matrix([[0,1],[1,0]]);Z=sp.diag(1,-1);out=sp.I*(2*Z+sp.sqrt(5)*X)*sym_s/3;assert sp.simplify(out-(2*sp.I*sym_t-sp.I*sp.sqrt(5)*sym_s)/3)==sp.zeros(2,1)
result={'three_segment_memory3_factorization_operator_residual':float(memory_res),'eight_spin_pair_product_ZZ_residual':float(zz),'cross_boundary_exchange_product_code_leakage':leak,'oscillator_cutoff':N,'audited_fock_levels':6,'low_energy_full_loop_operator_residual':float(return_res),'logical_oscillator_reference_correlated_state_residual':float(correlated_res),'thermal_coherence_observed':float(observed),'thermal_coherence_formula':float(expected),'thermal_difference':float(abs(observed-expected)),'exact_pair_symbolic_identity':True}
assert memory_res<1e-12 and zz<1e-12 and return_res<1e-12 and correlated_res<1e-12 and abs(observed-expected)<1e-12 and leak>0
(PTH/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

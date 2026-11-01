"""Exact monotone-envelope checks for composition; not independent review."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
u=10**20;N=u*u;m=u//20000;k=m//2;delta=Q(1,10**12);r=Q(1,1000)
checks=0
def ck(x):
 global checks
 assert x;checks+=1
ck(N>=10**8*(m+1)**2)
ck(m>=Q(u,40000));ck(k>=Q(m,4));ck(k>=Q(u,160000));ck(k<=delta*N)
# Each surplus below is increasing in u>=10^20 by its displayed derivatives.
ck(Q(N,4)-49*Q(u,20000)-48>=0);ck(Q(u,2)-Q(49,20000)>0)
ck(Q(3,4)-delta>=101*4*r)
ck(8*m+10**12+Q(256*N,k)+Q(1,N)+5<1+10**8*u)
ck(Q(256*N,k)<=40960000*u)
ck(Q(8,20000)+Q(10**12,u)+Q(6,u)+40960000<10**8)
ck(1+10**8*u<=Q(N,256));ck(Q(u,128)-10**8>0)
ck(Q(1,256)-Q(1,64)*Q(2,3)<=-Q(1,256))
ck(Q(3,4)+Q(1,64)==Q(49,64));ck(Q(49,64)<Q(15,16))
ck(Q(7,8)*Q(65,64)+Q(1,64)==Q(463,512));ck(Q(463,512)<Q(15,16))
# Failure exponents from source floors and all probability prefactors.
ck(Q(1,480000)>Q(1,10**6));ck(Q(1,160000)>Q(1,10**6))
ck(Q(101,100)+1+1+8+1+10+1+1<32)
# Conditional consumer can use a genuinely small positive tilt; no tail claim here.
D=100000001;theta=Q(1,10**16)
ck(4*D*theta<Q(1,10**6))
files={
'growth':root.parent/'rate2_uniform_initial_growth/UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md',
'activation':root.parent/'rate2_uniform_activation/UNIFORM_ACTIVATION_OR_REMOVAL.md',
'macro_interface':root.parent/'rate2_activated_macro_interface/ACTIVATED_TO_MACRO_AND_POSITIVE_FRACTIONS.md',
'interior':root.parent/'rate2_paid_interior_removal/PAID_INTERIOR_REMOVAL.md'}
expected={'growth':'90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e','activation':'c1d2ed0820d4f92ea236dcb27eab1cd29e27665f9b1a2e826617cc34e3c3fda8','macro_interface':'e527fafdfe790fa753b4584fca338bf9e4aa37179643a1f1596e39b140cb99a0','interior':'a8e0bd383b053021f72e8197986581c87878046cdeaa7570536e44f5cf71a1cf'}
for key,p in files.items():ck(hashlib.sha256(p.read_bytes()).hexdigest()==expected[key])
result={'status':'PASS_AUTHOR_EXACT_COMPOSITION_ENVELOPES_NOT_INDEPENDENT_REVIEW','exact_checks':checks,'dependency_sha256':expected,'proof_sha256':hashlib.sha256((root/'UNIFORM_ACTUAL_REMOVAL_BLOCK.md').read_bytes()).hexdigest(),'consumer_parameters':{'a':'1/2','delta_remove':'1/16','p':32,'c':'1/1000000','D':D,'d0':1},'uncomputed_costs':['interior n0(epsilon) and c(epsilon), supplied by separate interior component','huge finite Nstar from explicit component constants']}
(root/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

#!/usr/bin/env python3
"""Replay all Phase D exact claims using the Python standard library only.

Requires the authorized original frozen cube certificate and original stdlib
verifier in ../ppt_cube_chain_sol. It does not import numpy, sympy or a solver.
"""
import hashlib, importlib.util, json, sys, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ppt_cube_chain_sol'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('cube_stdlib',SOURCE/'verify_cube_stdlib.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
FROZEN_HASH='256745ff4887eadb653a8fdb416ccb15e91051756065396eb58d11761173d961'

def load(name):return json.loads((HERE/name).read_text())
def digest(name):return hashlib.sha256((HERE/name).read_bytes()).hexdigest()
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def scale(a,c):return [[c*x for x in r] for r in a]
def diag(xs):return [[x*int(i==j) for j in range(len(xs))] for i,x in enumerate(xs)]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]

def reconstruct():
    qs=[[[v.BLOCKS[j][r][i] for j in range(4)] for i in range(4)] for r in range(6)]
    ts=[]
    for q in qs:
      for r in qs:
        ts.append([[q[a][i]*r[b][j]-q[b][i]*r[a][j]+(
                    q[a][j]*r[b][i]-q[b][j]*r[a][i] if i!=j else 0)
                    for i,j in v.SYMS] for a,b in v.WEDS])
    a0=[[sum(k[a][i]*k[b][j] for k in ts) for i in range(10) for j in range(10)]
        for a in range(6) for b in range(6)]
    assert all(a0[a*6+b][i*10+j]==a0[b*6+a][i*10+j]==a0[a*6+b][j*10+i]
               for a in range(6) for b in range(6) for i in range(10) for j in range(10))
    return ts,a0,[2 if i==j else 1 for i,j in v.SYMS]

def target(a0,d,p,q):
    den=p*p+q*q
    un=scale(ident(10),den)
    un[0][0]=un[4][4]=q*q-p*p;un[0][4]=2*p*q;un[4][0]=-2*p*q
    assert v.matmul(un,v.transpose(un))==scale(ident(10),den*den)
    ud=v.matmul(un,diag(d))
    m=v.matmul(v.matmul(v.matmul(v.matmul(a0,v.kron(ud,ud)),v.transpose(a0)),v.kron(v.K,v.K)),a0)
    j=[[m[a*6+b][i*10+j0] for j0 in range(10) for b in range(6)] for i in range(10) for a in range(6)]
    assert j==v.transpose(j)
    assert all(j[i*6+a][j0*6+b]==j[j0*6+a][i*6+b]==j[i*6+b][j0*6+a]
               for i in range(10) for j0 in range(10) for a in range(6) for b in range(6))
    return j,den*den

def pd(a):
    assert a==v.transpose(a)
    n=len(a);b=[r[:] for r in a];prev=1
    for k in range(n):
        pivot=b[k][k]
        if pivot<=0:return False,k+1,pivot
        if k==n-1:break
        for i in range(k+1,n):
          for j in range(i,n):
            z=b[i][j]*pivot-b[i][k]*b[k][j]
            assert z%prev==0
            b[i][j]=b[j][i]=z//prev
        for i in range(k+1,n):b[i][k]=b[k][i]=0
        prev=pivot
    return True,n,pivot

def determinant_mod(a,prime):
    b=[[x%prime for x in row] for row in a];n=len(b);value=1
    assert all(len(r)==n for r in b)
    for k in range(n):
        pivot=next((i for i in range(k,n) if b[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:b[k],b[pivot]=b[pivot],b[k];value=-value
        x=b[k][k];value=value*x%prime;inv=pow(x,-1,prime)
        for i in range(k+1,n):
            f=b[i][k]*inv%prime
            for j in range(k+1,n):b[i][j]=(b[i][j]-f*b[k][j])%prime
            b[i][k]=0
    return value%prime

def rank_mod(a,prime):
    b=[[x%prime for x in row] for row in a];rows=len(b);cols=len(b[0]);rank=0
    for k in range(cols):
        pivot=next((i for i in range(rank,rows) if b[i][k]),None)
        if pivot is None:continue
        b[rank],b[pivot]=b[pivot],b[rank];inv=pow(b[rank][k],-1,prime)
        for i in range(rank+1,rows):
            f=b[i][k]*inv%prime
            for j in range(k,cols):b[i][j]=(b[i][j]-f*b[rank][j])%prime
        rank+=1
        if rank==rows:break
    return rank

def check_rank(ts,d):
    z=load('phase_d_rank_certificate.json')
    prime=z['prime'];assert prime==1009
    assert all(prime%k for k in range(2,32))
    basis=[ts[i] for i in z['source_kraus_basis_indices']]
    assert z['source_kraus_basis_indices']==[p*6+q for p in range(6) for q in range(p+1,6)]
    assert all(ts[p*6+p]==[[0]*10 for _ in range(6)] for p in range(6))
    assert all(ts[p*6+q]==scale(ts[q*6+p],-1) for p in range(6) for q in range(p+1,6))
    basis_columns=[[t[a][i] for t in basis] for a in range(6) for i in range(10)]
    constraints=[[t[a][i] for t in basis] for a in range(6) for i in (0,4)]
    assert rank_mod(basis_columns,prime)==15 and rank_mod(constraints,prime)==11
    assert rank_mod(z['annihilator_coefficients'],prime)==4
    ls=[]
    for cs in z['annihilator_coefficients']:
        l=[[sum(cs[k]*basis[k][a][i] for k in range(len(basis))) for i in range(10)] for a in range(6)]
        assert all(l[a][i]==0 for a in range(6) for i in (0,4))
        ls.append(l)
    assert ls==z['annihilator_matrices']
    rows=[]
    for a,b,c in z['selected_product_indices']:
        r=v.matmul(v.matmul(v.matmul(v.matmul(ls[a],diag(d)),v.transpose(ts[b])),v.K),ts[c])
        rows.append([x for row in r for x in row])
    assert rows==z['minor_rows_exact_integer'] and len(rows)==60
    determinant=determinant_mod(rows,prime);assert determinant!=0
    kappa=sum(x*x for cs in z['annihilator_coefficients'] for x in cs)
    tau=sum(x*x for row in rows for x in row)
    assert kappa==42 and tau==8974168593985584
    return {'rank_mod_prime':60,'prime':prime,'determinant_mod_prime':determinant,
            'annihilators_exactly_reconstructed':len(ls),
            'kraus_space_dimension':15,'two_column_constraint_rank':11,'annihilator_space_dimension':4,
            'annihilator_coefficient_frobenius_squared':kappa,
            'fixed_Gram_trace':tau,
            'uniform_eigenvalue_lower_bound':'1/[42*(8974168593985584)^59]',
            'uniform_claim':'J(M_F) strictly positive for every complex2x2 block F on coordinates0,4, identity on other8'}

def bh(j,side):
    e=6;d=10
    def s(i):return 1 if i%2==0 else -1
    if side=='output':
        pt=[[sum(j[i*e+a][k*e+a] for a in range(e)) for k in range(d)] for i in range(d)]
        return [[pt[i][k]*int(a==b)-j[i*e+a][k*e+b]-s(a)*s(b)*j[i*e+(b^1)][k*e+(a^1)]
                 for k in range(d) for b in range(e)] for i in range(d) for a in range(e)]
    assert side=='reference'
    pt=[[sum(j[i*e+a][i*e+b] for i in range(d)) for b in range(e)] for a in range(e)]
    return [[pt[a][b]*int(i==k)-j[i*e+a][k*e+b]-s(i)*s(k)*j[(k^1)*e+a][(i^1)*e+b]
             for k in range(d) for b in range(e)] for i in range(d) for a in range(e)]

def check_correction(name,j,den2,j0,cert):
    z=load('phase_d_correction_'+name+'.json')
    local=v.kron(cert['x_numerator'],cert['y_numerator'])
    residual=v.matmul(v.matmul(local,sub(j,scale(j0,den2))),v.transpose(local))
    rd=cert['rational_target_trace']*cert['filter_denominator']**4*den2
    bd=cert['output_denominator'];assert z['corrected_output_denominator']==rd*bd
    cs=[[[residual[i*6+a][i*6+b] for b in range(6)] for a in range(6)] for i in range(10)]
    ps=[]
    for i in range(10):
      for k in range(i+1,10):
        r=[[residual[i*6+a][k*6+b] for b in range(6)] for a in range(6)]
        assert r==v.transpose(r);ps.append(r);cs[i]=sub(cs[i],r);cs[k]=sub(cs[k],r)
    cs+=ps;checks=[]
    for i,r in enumerate(cs):
        old=cert['output_numerators'][i]
        num=[[old[a][b]*rd+r[a][b]*bd for b in range(6)] for a in range(6)]
        assert num==z['corrected_output_numerators'][i]
        checks.append(pd(num)[0])
    qv=cert['input_denominator']
    assert cert['input_numerators'][:10]==[[qv*int(i==j) for j in range(10)] for i in range(10)]
    assert cert['input_numerators'][10:55]==[[qv*(int(k==i)+int(k==j)) for k in range(10)]
                        for i in range(10) for j in range(i+1,10)]
    # The displayed elementary residual correction proves equality. Verify it
    # independently on every block, not by trusting the saved result string.
    out=[[0]*60 for _ in range(60)]
    for vec,corr in zip(cert['input_numerators'][:55],cs):
      for i in range(10):
        for k in range(10):
          for a in range(6):
            for b in range(6):out[i*6+a][k*6+b]+=vec[i]*vec[k]*corr[a][b]
    assert out==scale(residual,qv*qv)
    assert all(checks)==z['all_corrected_strict_pd']
    return {'all_corrected_strict_pd':all(checks),'failed_atom_indices':[i for i,c in enumerate(checks) if not c]}

def main():
    if not __debug__:raise RuntimeError('Run without -O or -OO')
    before=time.monotonic();protocol=load('phase_d_preregistration.json');report=load('phase_d_results.json')
    assert digest('phase_d_preregistration.json')==report['protocol_sha256']
    raw=(SOURCE/'cube_separable_certificate.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==FROZEN_HASH==report['original_certificate_sha256']
    cert=json.loads(raw);v.verify(SOURCE/'cube_separable_certificate.json')
    ts,a0,d=reconstruct();rank=check_rank(ts,d);j0,den0=target(a0,d,0,1)
    assert j0==v.rational_model()[0] and den0==1
    assert len(report['samples'])==len(protocol['samples_p_q'])==7
    out=[];witness_count=0
    for sample,pq in zip(report['samples'],protocol['samples_p_q']):
        p,q=pq;assert [sample['p'],sample['q']]==pq
        name=f'p{p}_q{q}';j,den2=target(a0,d,p,q)
        z=load('phase_d_target_'+name+'.json')
        assert z['choi_numerator']==j and z['denominator']==den2
        assert digest('phase_d_target_'+name+'.json')==sample['target_sha256']
        assert pd(j)[0]
        assert len(sample['witness_tests'])==4
        for result,(side,filtered) in zip(sample['witness_tests'],[('output',False),('output',True),('reference',False),('reference',True)]):
            assert (result['side'],result['frozen_filter'])==(side,filtered)
            filt=v.kron(ident(10),cert['y_numerator']) if side=='output' else v.kron(cert['x_numerator'],ident(6))
            jf=v.matmul(v.matmul(filt,j),v.transpose(filt)) if filtered else j
            h=bh(jf,side);hname=f'phase_d_bh_{name}_{side}_{int(filtered)}.json'
            assert load(hname)['operator_numerator']==h and digest(hname)==result['operator_sha256']
            assert pd(h)[0] and result['exact']['strict_pd'] and result['negative_vector'] is None
            witness_count+=1
        correction=check_correction(name,j,den2,j0,cert)
        assert digest('phase_d_correction_'+name+'.json')==sample['frozen_400_atom_attempt']['certificate_sha256']
        assert correction['all_corrected_strict_pd']==sample['frozen_400_atom_attempt']['all_corrected_strict_pd']
        out.append({'p':p,'q':q,'cube_corner_choi':'strictly positive',
                    'BH_tests_strictly_positive':4,'frozen_correction':correction})
    result={'status':'ALL_EXACT_PHASE_D_CLAIMS_REPLAYED','arithmetic':'Python stdlib integers only',
            'analytic_rank':rank,'positive_BH_tests':witness_count,'samples':out,
            'nonzero_sample_separability':'UNKNOWN','universal_PPT_cube':'UNKNOWN',
            'elapsed_seconds':time.monotonic()-before}
    (HERE/'phase_d_stdlib_replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

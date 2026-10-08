#!/usr/bin/env python3
"""Finite preregistered rotations and independently exact certificates.

Numerical eigenvalues are diagnostics only. Exact statements are certified
using Python integers. Sympy is used only to discover rational annihilators;
their identities and modular full-rank witness are checked with integers.
No candidate or family is chosen after seeing the test outcomes.
"""
import hashlib, importlib.util, json, math, sys, time
from pathlib import Path
import numpy as np
import sympy as sp

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ppt_cube_chain_sol'
sys.dont_write_bytecode=True
FROZEN_HASH='256745ff4887eadb653a8fdb416ccb15e91051756065396eb58d11761173d961'
spec=importlib.util.spec_from_file_location('cube_stdlib',SOURCE/'verify_cube_stdlib.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def save(path,data):
    path.write_text(json.dumps(data,separators=(',',':'))+'\n')
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def scale(a,c):return [[c*x for x in r] for r in a]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def diag(xs):return [[x*int(i==j) for j in range(len(xs))] for i,x in enumerate(xs)]

def kraus_model():
    qs=[[[v.BLOCKS[j][r][i] for j in range(4)] for i in range(4)] for r in range(6)]
    ts=[]
    for q in qs:
      for r in qs:
        matrix=[]
        for a,b in v.WEDS:
            row=[]
            for i,j in v.SYMS:
                value=q[a][i]*r[b][j]-q[b][i]*r[a][j]
                if i!=j:value+=q[a][j]*r[b][i]-q[b][j]*r[a][i]
                row.append(value)
            matrix.append(row)
        ts.append(matrix)
    a0=[[sum(k[a][i]*k[b][j] for k in ts) for i in range(10) for j in range(10)]
        for a in range(6) for b in range(6)]
    assert all(a0[a*6+b][i*10+j]==a0[b*6+a][i*10+j]==a0[a*6+b][j*10+i]
               for a in range(6) for b in range(6) for i in range(10) for j in range(10))
    return ts,a0,[2 if i==j else 1 for i,j in v.SYMS]

def rotation_numerator(p,q):
    den=p*p+q*q
    un=scale(ident(10),den)
    un[0][0]=un[4][4]=q*q-p*p
    un[0][4]=2*p*q;un[4][0]=-2*p*q
    assert v.matmul(un,v.transpose(un))==scale(ident(10),den*den)
    return un,den

def target(a0,d,p,q):
    un,den=rotation_numerator(p,q)
    ud=v.matmul(un,diag(d))
    # Flattening is row-major. Ad_UD is represented by UD tensor UD.
    m=v.matmul(v.matmul(v.matmul(v.matmul(a0,v.kron(ud,ud)),v.transpose(a0)),v.kron(v.K,v.K)),a0)
    j=[[m[a*6+b][i*10+j0] for j0 in range(10) for b in range(6)]
       for i in range(10) for a in range(6)]
    assert j==v.transpose(j)
    # Both outer A0 factors enforce the two partial transpose invariances.
    assert all(j[i*6+a][j0*6+b]==j[j0*6+a][i*6+b]==j[i*6+b][j0*6+a]
               for i in range(10) for j0 in range(10) for a in range(6) for b in range(6))
    return j,den*den

def strict_pd(a):
    """One Bareiss elimination yields all leading principal minors exactly."""
    assert a==v.transpose(a)
    n=len(a);b=[r[:] for r in a];previous=1;bits=[];minor_hash=hashlib.sha256()
    for k in range(n):
        pivot=b[k][k]
        minor_hash.update(str(pivot).encode()+b'\n')
        bits.append(abs(pivot).bit_length())
        if pivot<=0:
            return {'strict_pd':False,'first_nonpositive_leading_minor_order':k+1,
                    'first_nonpositive_minor':str(pivot),'leading_minor_sha256_prefix':minor_hash.hexdigest()}
        if k==n-1:break
        for i in range(k+1,n):
            for j in range(i,n):
                z=b[i][j]*pivot-b[i][k]*b[k][j]
                assert z%previous==0
                b[i][j]=b[j][i]=z//previous
        for i in range(k+1,n):b[i][k]=b[k][i]=0
        previous=pivot
    return {'strict_pd':True,'leading_minor_orders':n,'leading_minor_sha256':minor_hash.hexdigest(),
            'max_minor_bits':max(bits),'determinant':str(pivot)}

def bh(j,d,e,side):
    def sig(i):return 1 if i%2==0 else -1
    if side=='output':
        partial=[[sum(j[i*e+a][k*e+a] for a in range(e)) for k in range(d)] for i in range(d)]
        return [[partial[i][k]*int(a==b)-j[i*e+a][k*e+b]
                 -sig(a)*sig(b)*j[i*e+(b^1)][k*e+(a^1)]
                 for k in range(d) for b in range(e)] for i in range(d) for a in range(e)]
    partial=[[sum(j[i*e+a][i*e+b] for i in range(d)) for b in range(e)] for a in range(e)]
    return [[partial[a][b]*int(i==k)-j[i*e+a][k*e+b]
             -sig(i)*sig(k)*j[(k^1)*e+a][(i^1)*e+b]
             for k in range(d) for b in range(e)] for i in range(d) for a in range(e)]

def eig_diagnostic(j):
    # Normalize before float conversion; integer trace is positive for all tests.
    tr=v.tr(j)
    assert tr>0
    nf=np.array([[x/tr for x in r] for r in j],dtype=float)
    eig,vec=np.linalg.eigh(nf)
    return {'min_eigenvalue_over_trace':float(eig[0]),'max_eigenvalue_over_trace':float(eig[-1])},vec[:,0]

def annihilator_certificate(ts,d):
    # Discovery is a rational nullspace, followed by independently checked exact
    # identities. Zero/redundant Kraus matrices are removed before discovery.
    flats=sp.Matrix.hstack(*[sp.Matrix([x for r in t for x in r]) for t in ts])
    independent=list(flats.rref()[1]);basis=[ts[i] for i in independent]
    constraints=sp.Matrix([[t[a][i] for t in basis] for a in range(6) for i in (0,4)])
    nulls=constraints.nullspace();cs=[];ls=[]
    for col in nulls:
        den=sp.ilcm(*[x.q for x in col]);c=[int(x*den) for x in col]
        g=math.gcd(*c);c=[x//g for x in c]
        l=[[sum(c[k]*basis[k][a][i] for k in range(len(basis))) for i in range(10)] for a in range(6)]
        assert all(l[a][i]==0 for a in range(6) for i in (0,4))
        cs.append(c);ls.append(l)
    prime=1009;elimination=[];selected=[];selected_vectors=[]
    # Mod p gives a sufficient exact rank witness. We retain every selected
    # product, its indices, exact Kraus coefficients and the 60x60 minor.
    for a,l in enumerate(ls):
      ld=v.matmul(l,diag(d))
      for b,tb in enumerate(ts):
        mid=v.matmul(v.matmul(ld,v.transpose(tb)),v.K)
        for c,tc in enumerate(ts):
            product=v.matmul(mid,tc);flat=[x for r in product for x in r]
            row=[x%prime for x in flat]
            for pivot,base in elimination:
                factor=row[pivot]
                if factor:row=[(x-factor*y)%prime for x,y in zip(row,base)]
            pivot=next((i for i,x in enumerate(row) if x),None)
            if pivot is None:continue
            inv=pow(row[pivot],-1,prime);row=[x*inv%prime for x in row]
            elimination.append((pivot,row));selected.append([a,b,c]);selected_vectors.append(flat)
            if len(selected)==60:break
        if len(selected)==60:break
      if len(selected)==60:break
    data={'schema':'parameter_independent_kraus_span_v1','prime':prime,
          'source_kraus_basis_indices':independent,'annihilator_coefficients':cs,
          'annihilator_matrices':ls,'selected_product_indices':selected,
          'minor_rows_exact_integer':selected_vectors,'rank_mod_prime':len(selected),
          'claim':('J(M_t) has full rank60 for every real t' if len(selected)==60 else 'Full-rank obstruction not obtained')}
    save(HERE/'phase_d_rank_certificate.json',data)
    return {k:data[k] for k in ('prime','source_kraus_basis_indices','rank_mod_prime','claim')}|{'annihilator_dimension':len(ls)}

def frozen_correction(j,den2,j0,cert):
    x=cert['x_numerator'];y=cert['y_numerator'];local=v.kron(x,y)
    residual=v.matmul(v.matmul(local,sub(j,scale(j0,den2))),v.transpose(local))
    lhs_den=cert['rational_target_trace']*cert['filter_denominator']**4*den2
    out_den=cert['output_denominator']
    coords=[[[residual[i*6+a][i*6+b] for b in range(6)] for a in range(6)] for i in range(10)]
    pair=[]
    for i in range(10):
      for k in range(i+1,10):
        block=[[residual[i*6+a][k*6+b] for b in range(6)] for a in range(6)]
        assert block==v.transpose(block)
        pair.append(block)
        coords[i]=sub(coords[i],block);coords[k]=sub(coords[k],block)
    qv=cert['input_denominator']
    expected=[[qv*(int(k==i)+int(k==j0)) for k in range(10)] for i in range(10) for j0 in range(i+1,10)]
    assert cert['input_numerators'][10:55]==expected
    corrections=coords+pair;new_nums=[];checks=[]
    for index,corr in enumerate(corrections):
        old=cert['output_numerators'][index]
        new=[[old[a][b]*lhs_den+corr[a][b]*out_den for b in range(6)] for a in range(6)]
        new_nums.append(new);checks.append(strict_pd(new))
    common_den=lhs_den*out_den
    data={'schema':'frozen_atom_exact_residual_v1','corrected_atom_count':55,
          'unchanged_atoms':list(range(55,400)),'corrected_output_denominator':common_den,
          'corrected_output_numerators':new_nums,'strict_pd_checks':checks,
          'all_corrected_strict_pd':all(c['strict_pd'] for c in checks),
          'target_denominator':den2}
    # Check the correction identity directly in all 3600 entries.
    reconstructed=[[0]*60 for _ in range(60)]
    for vec,corr in zip(cert['input_numerators'][:55],corrections):
      for i in range(10):
        for k in range(10):
          for a in range(6):
            for b in range(6):reconstructed[i*6+a][k*6+b]+=vec[i]*vec[k]*corr[a][b]
    assert reconstructed==scale(residual,qv*qv)
    data['correction_identity']='exactly checked all3600 entries'
    return data

def main():
    start=time.monotonic()
    protocol=json.loads((HERE/'phase_d_preregistration.json').read_text())
    raw=(SOURCE/'cube_separable_certificate.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==FROZEN_HASH
    cert=json.loads(raw)
    v.verify(SOURCE/'cube_separable_certificate.json')
    ts,a0,d=kraus_model();j0,den0=target(a0,d,0,1)
    assert den0==1 and (j0,v.tr(j0))==(v.rational_model()[0],cert['rational_target_trace'])
    rank=annihilator_certificate(ts,d)
    print('analytic_rank',json.dumps(rank),flush=True)
    report={'schema':protocol['schema'],'protocol_sha256':hashlib.sha256((HERE/'phase_d_preregistration.json').read_bytes()).hexdigest(),
            'original_certificate_sha256':FROZEN_HASH,'analytic_rank':rank,'samples':[]}
    for p,q in protocol['samples_p_q']:
        name=f'p{p}_q{q}';j,den2=target(a0,d,p,q)
        jhash=save(HERE/f'phase_d_target_{name}.json',{'p':p,'q':q,'denominator':den2,'choi_numerator':j})
        diag_info,_=eig_diagnostic(j)
        sample={'p':p,'q':q,'target_sha256':jhash,'target_denominator':den2,
                'choi_numerical':diag_info,'choi_exact':strict_pd(j),'witness_tests':[]}
        for side,filtered in [('output',False),('output',True),('reference',False),('reference',True)]:
            filt=v.kron(ident(10),cert['y_numerator']) if side=='output' else v.kron(cert['x_numerator'],ident(6))
            jf=v.matmul(v.matmul(filt,j),v.transpose(filt)) if filtered else j
            h=bh(jf,10,6,side)
            hhash=save(HERE/f'phase_d_bh_{name}_{side}_{int(filtered)}.json',{'side':side,'frozen_filter':filtered,'operator_numerator':h})
            info,vec=eig_diagnostic(h);exact=strict_pd(h)
            negative=None
            if info['min_eigenvalue_over_trace']<0:
                iv=[int(round(x*protocol['numerical_negative_vector_rounding_scale'])) for x in vec]
                value=sum(iv[i]*h[i][k]*iv[k] for i in range(60) for k in range(60))
                negative={'vector':iv,'expectation_numerator':value,'certified_negative':value<0}
            sample['witness_tests'].append({'side':side,'frozen_filter':filtered,'operator_sha256':hhash,
                    'numerical':info,'exact':exact,'negative_vector':negative})
        corr=frozen_correction(j,den2,j0,cert)
        chash=save(HERE/f'phase_d_correction_{name}.json',corr)
        sample['frozen_400_atom_attempt']={'certificate_sha256':chash,'all_corrected_strict_pd':corr['all_corrected_strict_pd'],
             'failed_atom_indices':[i for i,c in enumerate(corr['strict_pd_checks']) if not c['strict_pd']],
             'status':'EXACT_SEPARABILITY_CERTIFICATE' if corr['all_corrected_strict_pd'] else 'SUFFICIENT_DECOMPOSITION_FAILED_NOT_ENTANGLEMENT'}
        report['samples'].append(sample)
        save(HERE/'phase_d_results.json',report)
        print('sample',p,q,'BHmin',[c['numerical']['min_eigenvalue_over_trace'] for c in sample['witness_tests']],
              'BH_PD',[c['exact']['strict_pd'] for c in sample['witness_tests']],
              'frozen_sep',corr['all_corrected_strict_pd'],flush=True)
    report['elapsed_seconds']=time.monotonic()-start
    report['universal_cube_claim']='UNKNOWN'
    save(HERE/'phase_d_results.json',report)
    print('completed',report['elapsed_seconds'],flush=True)

if __name__=='__main__':main()

"""Exact local receiver for arbitrary coherent perturbations, no reference search."""
from pathlib import Path
from time import perf_counter
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent

def matrix_json(M):
    return [[[str(s.re(z)),str(s.im(z))] for z in M.row(i)] for i in range(M.rows)]

def load_matrix(a):
    return s.Matrix([[s.Rational(z[0])+s.I*s.Rational(z[1]) for z in row] for row in a])

def pd_pivots(A):
    A=A.copy()
    piv=[]
    for k in range(A.rows):
        p=A[k,k]
        assert p>0
        piv.append(str(p))
        for i in range(k+1,A.rows):
            for j in range(k+1,A.cols):
                A[i,j]=s.cancel(A[i,j]-A[i,k]*A[k,j]/p)
    return piv

def main():
    start=perf_counter()
    raw=(HERE/'CHANNELS.json').read_bytes(); ch=json.loads(raw)
    rawq=(HERE/'SYNTHESIS.json').read_bytes(); source=json.loads(rawq)
    qr=source['ordered_source']['quantum_receiver']
    primitive=[load_matrix(M) for M in qr['primitive']]
    E=[load_matrix(M) for M in qr['E']];F=[load_matrix(M) for M in qr['F']]
    I=s.eye(2);sx=s.Matrix([[0,1],[1,0]]);sy=s.Matrix([[0,-s.I],[s.I,0]]);sz=s.diag(1,-1)
    n=4;m=s.Rational(1,8);M=s.Rational(3,8);delta=s.Rational(3,200);lam=s.Rational(1,2)
    L=s.zeros(4)
    for i,j in [(0,1),(1,2),(2,3)]:
        L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
    C=s.Matrix([[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]])
    restriction=C.T*(L-lam*(s.eye(4)-s.ones(4)/4))*C
    piv=pd_pivots(restriction)
    alpha=s.cancel(delta*m*lam/(2*M**2)); assert alpha==s.Rational(1,300)
    eta=s.Rational(1,10_000_000);tau=eta/7
    budgets=[]
    K=s.Rational(0)
    for name in ['P','Q']:
        for y,row in enumerate(ch[name]):
            r=sum(s.Rational(a) for a in row.values())
            k=4*2/m+2*n/(m*r)+2/m**2
            budgets.append({'channel':name,'row':y,'mass':str(r),'baseline_floor':str(m*r),'Lipschitz':str(k)})
            assert eta<=m*r/2
            K+=k
    assert K*eta<alpha/2
    Ep=[a.copy() for a in E];Fp=[a.copy() for a in F]
    Ep[0]+=tau*sx;Ep[1]-=tau*sx
    Fp[0]+=tau*sz;Fp[1]-=tau*sz
    D=load_matrix(qr['rho_plus'])-I/2
    basis=s.Matrix([[1,sig[0],sig[1],sig[2]] for sig in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]])
    def coefficients(A):
        return [s.simplify(s.trace(A)/2+4*sum(z*s.trace(A*p)/2 for z,p in zip(sig,[sx,sy,sz])))
                for sig in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
    negative=[]; candidate={};success={}
    for name,rows,base in [('E',Ep,E),('F',Fp,F)]:
        assert sum(rows,s.zeros(2))==I
        table=[]
        for y,(A,B) in enumerate(zip(rows,base)):
            assert A==A.conjugate().T and A[0,0]>0 and s.det(A)>0
            co=coefficients(A); diff=coefficients(A-B)
            assert all(abs(z)<=eta for z in diff)
            assert sum((z*M0 for z,M0 in zip(co,primitive)),s.zeros(2))==A
            for i,z in enumerate(co):
                if z<0:negative.append([name,y,i,str(z)])
            table.append(list(map(str,co)))
        success[name]=s.simplify((1+sum(abs(s.simplify(s.trace(A*D))) for A in rows))/2)
        candidate[name]={'effects':[matrix_json(A) for A in rows],'primitive_coefficients':table}
    assert negative
    robust_guess=s.Rational(1,640)-23*eta/16
    assert robust_guess>0 and success['F']>success['E']
    out={'source_channels_sha256':hashlib.sha256(raw).hexdigest(),
         'synthesis_sha256':hashlib.sha256(rawq).hexdigest(),
         'input_contract':{'primitive_bounds':[str(m),str(M)],'delta':str(delta),'graph_lambda':str(lam)},
         'graph_restricted_matrix':[[str(z) for z in restriction.row(i)] for i in range(3)],
         'graph_LDL_pivots':piv,'alpha':str(alpha),'eta':str(eta),'effect_opnorm_radius':str(tau),
         'row_budgets':budgets,'K':str(K),'K_eta':str(K*eta),'remaining_coercivity':str(alpha-K*eta),
         'uniform_guessing_reversal_lower':str(robust_guess),
         'candidate':candidate,'negative_primitive_coefficients':negative,
         'candidate_guessing':{k:str(v) for k,v in success.items()},
         'candidate_guessing_reversal':str(success['F']-success['E']),
         'cost':{'compile_seconds':perf_counter()-start,'reference_dimensions_tested':0,'SDPs':0},
         'scope':'full affine POVM-pair neighbourhood; arbitrary finite reference; no physical qualification'}
    (HERE/'NEIGHBOURHOOD.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['alpha','eta','K','K_eta','remaining_coercivity','uniform_guessing_reversal_lower','cost']}))

if __name__=='__main__': main()

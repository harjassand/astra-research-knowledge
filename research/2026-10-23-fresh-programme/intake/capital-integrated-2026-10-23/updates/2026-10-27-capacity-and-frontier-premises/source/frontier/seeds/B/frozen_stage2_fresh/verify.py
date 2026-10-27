"""Exact finite replica opposition check; no endpoint distillation witness."""
from itertools import permutations, combinations, product
from collections import Counter
from pathlib import Path
import json
import sympy as s


def require(ok, message):
    if not bool(ok):
        raise RuntimeError(message)


def kron(mats):
    out=s.ones(1)
    for mat in mats:
        out=s.kronecker_product(out,mat)
    return out


def physical_perm(words,perm):
    """P sends each replica label r to perm[r]."""
    out=s.zeros(len(words))
    index={w:j for j,w in enumerate(words)}
    for j,w in enumerate(words):
        y=[0]*4
        for r in range(4):
            y[perm[r]]=w[r]
        out[index[tuple(y)],j]=1
    return out


def transposition(a,b):
    p=list(range(4));p[a],p[b]=p[b],p[a]
    return tuple(p)


def cycles(perm):
    seen=set();out=[]
    for i in range(4):
        if i in seen:
            continue
        j=i;length=0
        while j not in seen:
            seen.add(j);length+=1;j=perm[j]
        out.append(length)
    return tuple(sorted(out,reverse=True))


def local_rep(words,W):
    gram=W.T*W
    require(gram.det()>0,'positive physical Gram metric')
    inverse=gram.inv()
    reps={}
    for perm in permutations(range(4)):
        physical=physical_perm(words,perm)
        rep=inverse*W.T*physical*W
        require(physical*W==W*rep,'local representation exact physical intertwiner')
        require(rep.T*gram*rep==gram,'local representation metric unitarity')
        reps[perm]=rep
    return gram,reps


def tensor_word(size,digits):
    out=s.zeros(size**3,1)
    out[digits[0]*size**2+digits[1]*size+digits[2]]=1
    return out


def symword(size,digits):
    return sum((tensor_word(size,x) for x in set(permutations(digits))),s.zeros(size**3,1))


def invariant_sector(gram,reps,V,expected_eigenvalue,expected_characters,label):
    metric=kron([gram]*3)
    inner=V.T*metric*V
    require(inner.det()>0,label+' independent vectors with positive Gram matrix')
    left=inner.inv()*V.T*metric
    size=gram.rows
    K=s.zeros(size**3)
    for a,b in combinations(range(4),2):
        f=reps[transposition(a,b)]
        K+=kron([f-s.eye(size)/2]*3)/6
    require(K.T*metric==metric*K,label+' physical self-adjoint K')
    require(K*V==expected_eigenvalue*V,label+' negative K eigenspace')
    density=V*left/V.cols
    require(density*density==density/V.cols,label+' normalized orthogonal-projector identity')
    require(s.trace(density)==1,label+' trace one')
    require(s.trace(density*K)==expected_eigenvalue,label+' exact objective')
    characters={}
    reduced={}
    for perm,rep in reps.items():
        global_rep=kron([rep]*3)
        small=left*global_rep*V
        require(global_rep*V==V*small,label+' invariant sector')
        character=s.trace(small)/V.cols
        typ=cycles(perm)
        require(character==expected_characters[typ],label+' every permutation character')
        require(global_rep*density==density*global_rep,label+' invariant normalized projector')
        characters[typ]=character
        if perm in [transposition(0,1),transposition(1,2),transposition(2,3)]:
            reduced[str(perm)]=[[str(x) for x in row] for row in small.tolist()]
    cartan = None
    if label == '[22]':
        w=V[:,0]
        f12=kron([reps[transposition(0,1)]]*3)
        f34=kron([reps[transposition(2,3)]]*3)
        colswap=kron([reps[(2,3,0,1)]]*3)
        antisym=s.zeros(size**3)
        for perm,rep in reps.items():
            sign=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
            antisym+=sign*kron([rep]*3)/24
        require(f12*w == -w and f34*w == -w,'Cartan column antisymmetries')
        require(colswap*w == w,'Cartan symmetric column exchange')
        require(antisym*w == s.zeros(size**3,1),'Cartan removal of exterior-four component')
        B=kron([reps[transposition(0,2)]-s.eye(size)/2]*3)
        cartan=s.factor((w.T*metric*B*w)[0]/(w.T*metric*w)[0])
        require(cartan==-s.Rational(3,8),'exact first-Cartan-level negative control')
    return {'dimension':V.cols,'objective':str(expected_eigenvalue),'cartan_degree_two_objective':str(cartan),
            'characters':{str(k):str(v) for k,v in characters.items()},
            'adjacent_transpositions':reduced}


def exact_four_replica_state():
    # A physical four-qubit one-excitation representation of S4 [31].
    words31=[tuple(int(i==j) for i in range(4)) for j in range(4)]
    W31=s.Matrix([[int(i==j)-int(i==3) for j in range(3)] for i in range(4)])
    G31,rep31=local_rep(words31,W31)
    v0=4*tensor_word(3,(0,0,0))-symword(3,(0,0,1))-symword(3,(0,0,2))+symword(3,(0,1,1))+symword(3,(0,2,2))
    v1=4*tensor_word(3,(1,1,1))-symword(3,(1,1,0))-symword(3,(1,1,2))+symword(3,(1,0,0))+symword(3,(1,2,2))
    v2=sum((tensor_word(3,(j,j,j)) for j in range(3)),s.zeros(27,1))
    chars31={(1,1,1,1):1,(2,1,1):s.Rational(1,3),(2,2):-s.Rational(1,3),(3,1):0,(4,):-s.Rational(1,3)}
    out31=invariant_sector(G31,rep31,s.Matrix.hstack(v0,v1,v2),-s.Rational(13,24),chars31,'[31]')
    # Exact physical spin-zero S4 [22] representation, inside binary coordinates.
    words22=[x for x in product(range(2),repeat=4) if sum(x)==2]
    def pairing(pair_list):
        out=s.zeros(len(words22),1)
        for j,w in enumerate(words22):
            coefficient=1
            for a,b in pair_list:
                coefficient*=int((w[a],w[b])==(0,1))-int((w[a],w[b])==(1,0))
            out[j]=coefficient
        return out
    W22=s.Matrix.hstack(pairing([(0,1),(2,3)]),pairing([(0,2),(1,3)]))
    require(W22==s.Matrix([[0,1],[1,0],[-1,-1],[-1,-1],[1,0],[0,1]]),'displayed physical singlet pairing columns')
    G22,rep22=local_rep(words22,W22)
    w0=3*tensor_word(2,(0,0,0))-symword(2,(0,0,1))+symword(2,(0,1,1))
    w1=tensor_word(2,(0,0,0))+tensor_word(2,(1,1,1))
    chars22={(1,1,1,1):1,(2,1,1):0,(2,2):1,(3,1):-s.Rational(1,2),(4,):0}
    out22=invariant_sector(G22,rep22,s.Matrix.hstack(w0,w1),-s.Rational(9,8),chars22,'[22]')
    weights=[s.Rational(5,16),s.Rational(9,16),s.Rational(2,16)]
    require(sum(weights)==1 and all(x>0 for x in weights),'positive normalized direct-sum state')
    moments={}
    for perm in permutations(range(4)):
        typ=cycles(perm)
        observed=weights[0]+weights[1]*chars31[typ]+weights[2]*chars22[typ]
        expected=s.Rational(2)**(len(typ)-4)
        require(observed==expected,'every full S4 flat-rank-two moment')
        moments[str(typ)]=str(observed)
    objective=weights[0]/8-weights[1]*s.Rational(13,24)-weights[2]*s.Rational(9,8)
    require(objective==-s.Rational(13,32),'negative relaxed objective')
    return {'replicas':4,'physical_sites':3,'binary_physical_support':True,
            'sector_31':out31,'sector_22':out22,'weights':[str(x) for x in weights],
            'all_24_permutation_moments_checked':True,'moments':moments,'objective':str(objective),
            'padded_objective':'-13 / 2**(n+2), n >= 3',
            'interpretation':'A PSD relaxation state, not an admissible negative Werner witness.'}


def binary_zero_checks():
    eps=s.Matrix([[0,1],[-1,0]])
    J=kron([eps]*3)
    require(J*J == -s.eye(8),'odd spin-flip square')
    def q_binary(C):
        value=0
        for mask in range(8):
            traced=[i for i in range(3) if mask&(1<<i)]
            keep=[i for i in range(3) if i not in traced]
            partial=s.zeros(2**len(keep))
            for a in range(8):
                aa=[(a>>(2-i))&1 for i in range(3)]
                for b in range(8):
                    bb=[(b>>(2-i))&1 for i in range(3)]
                    if any(aa[i]!=bb[i] for i in traced):continue
                    ai=sum(aa[i]*2**(len(keep)-j-1) for j,i in enumerate(keep))
                    bi=sum(bb[i]*2**(len(keep)-j-1) for j,i in enumerate(keep))
                    partial[ai,bi]+=C[a,b]
            value+=(-s.Rational(1,2))**len(traced)*s.trace(partial.conjugate().T*partial)
        return s.simplify(value)
    examples=[]
    for entries in [[1,0,1,s.I,0,2,0,1],[1,s.I,2,1-s.I,0,-1,2*s.I,1]]:
        u=s.Matrix(entries);v=J*u.conjugate();norm=s.simplify((u.conjugate().T*u)[0])
        require((u.conjugate().T*v)[0]==0,'Kramers-pair orthogonality')
        P=((u*u.conjugate().T+v*v.conjugate().T)/norm).applyfunc(s.simplify)
        require((P*P-P).applyfunc(s.simplify)==s.zeros(8) and s.simplify(s.trace(P))==2,'complex quaternionic rank-two projection')
        require((J*P.T*J.inv()-P).applyfunc(s.simplify)==s.zeros(8),'spin-flip invariant projection')
        q=q_binary(P)
        require(q==0,'complex quaternionic zero by independent partial traces')
        examples.append(str(q))
    P=s.zeros(8);P[0,0]=1;P[3,3]=1
    positive=q_binary(P)
    require(positive==s.Rational(1,2),'positive coherent control span 000,011')
    return {'complex_quaternionic_zero_values':examples,'positive_projection_value':str(positive),
            'all_degree_spanning_step':'Proved analytically in CARTAN.md, not inferred from these examples.'}


def rigidity_and_scaling():
    # Piecewise rounding inequality, with the two ranges proved directly.
    z=s.symbols('z',nonnegative=True)
    low=s.factor(4*z*(s.Rational(1,2)-z)-z)
    high=s.factor(4*z-1)
    require(s.expand(low-z*(1-4*z))==0,'low-eigenvalue rounding factor')
    require(high==4*z-1,'high-eigenvalue rounding factor')
    require(4*s.sqrt(s.Rational(1,64))==s.Rational(1,2),'rounding trace threshold')
    require(16*s.sqrt(s.Rational(1,64))==2,'uniform trace-distance bound')
    require(16*(1+1/s.sqrt(2))<32,'dimension-independent q Lipschitz constant')
    n=s.symbols('n',integer=True,positive=True)
    require(s.simplify(12*9**n/(12*18**n)-2**(-n))==0,'de Finetti diagonal scaling')
    require(s.simplify(2**(-n)*s.Rational(3,2)**n-s.Rational(3,4)**n)==0,'objective error scaling')
    degree=s.symbols('k',integer=True,positive=True)
    dimension=s.symbols('D',integer=True,positive=True)
    ratio=degree**2*(degree**2-1)/((degree+dimension-1)*(degree+dimension-2)**2*(degree+dimension-3))
    paired=(degree+1)/(degree+dimension-1)*(degree/(degree+dimension-2))**2*(degree-1)/(degree+dimension-3)
    require(s.cancel(ratio-paired)==0,'Cartan dimension-ratio factorization')
    require(s.simplify(16*3**n*s.Rational(3,2)**n/(16*9**n)-2**(-n))==0,'Cartan diagonal error scaling')
    return {'full_trace_norm_de_finetti_delta':'min(2, 12 * 9**n / m)',
            'rigidity_constant':16,'q_lipschitz_constant':32,
            'm_diagonal':'ceil(12 * 18**n)',
            'error_diagonal':'32*sqrt(2)*2**(-n/2) + (3/4)**n',
            'cartan_degree_diagonal':'ceil(16 * 9**n)',
            'cartan_error_diagonal':'2**(-n)',
            'all_copy_bound_proved':False}


if __name__=='__main__':
    result={'exact_opposition':exact_four_replica_state(),'rigidity':rigidity_and_scaling(),'binary_zero_controls':binary_zero_checks(),
            'scope':'Exact finite replica algebra and complete hierarchy convergence; the full all-copy target remains unresolved.'}
    rendered=json.dumps(result,indent=2)
    print(rendered)
    Path(__file__).with_name('verification.json').write_text(rendered+'\n')

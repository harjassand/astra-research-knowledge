import sympy as sp
from itertools import combinations
from math import gcd
import json
from pathlib import Path

I = sp.I

def pauli_mul_word(a,b):
    phase=0; out=[]
    tab={('I','I'):(0,'I'),('I','X'):(0,'X'),('I','Y'):(0,'Y'),('I','Z'):(0,'Z'),
         ('X','I'):(0,'X'),('Y','I'):(0,'Y'),('Z','I'):(0,'Z'),('X','X'):(0,'I'),
         ('Y','Y'):(0,'I'),('Z','Z'):(0,'I'),('X','Y'):(1,'Z'),('Y','X'):(3,'Z'),
         ('Y','Z'):(1,'X'),('Z','Y'):(3,'X'),('Z','X'):(1,'Y'),('X','Z'):(3,'Y')}
    for x,y in zip(a,b):
        p,z=tab[x,y]; phase=(phase+p)%4; out.append(z)
    return phase,tuple(out)

def gamma_words(n=4):
    out=[]
    for k in range(n):
        pre=('Z',)*k; suf=('I',)*(n-k-1)
        out.append(pre+('X',)+suf); out.append(pre+('Y',)+suf)
    out.append(('Z',)*n)
    return out

GAM=gamma_words()
def e_basis(k):
    # E_A=i^(k(k-1)/2) Gamma_{a1}...Gamma_{ak}, Hermitian.
    for A in combinations(range(9),k):
        ph=0; w=('I',)*4
        for a in A:
            p,w=pauli_mul_word(w,GAM[a]); ph=(ph+p)%4
        ph=(ph+k*(k-1)//2)%4
        yield A,ph,w

def apply_word(word,bits):
    # word order qubit 0..3; 0-based bits
    out=bits; phase=1
    for q,p in enumerate(word):
        bit=(bits>>q)&1
        if p=='X': out ^= (1<<q)
        elif p=='Y': out ^= (1<<q); phase *= I*(1 if bit==0 else -1)
        elif p=='Z': phase *= (1 if bit==0 else -1)
    return out,sp.simplify(phase)

def triple_apply(term,idx):
    # term is (phase, words by factor)
    ph=term[0]; out=0
    for f,w in enumerate(term[1]):
        b=(idx>>(4*f))&15
        bo,p=apply_word(w,b); ph*=p
        out |= bo << (4*f)
    return out,sp.simplify(ph)

def h_terms():
    out={k:[] for k in range(1,5)}
    for k in range(1,5):
        for A,ph,w in e_basis(k):
            # E_A^T has the same scalar and gains (-1) for each Y under transpose.
            pt=(ph+2*(w.count('Y')%2))%4
            # Coefficient multiplying Pauli words for E_A^T tensor E_A.
            c=I**(pt+ph)
            assert sp.simplify(c).is_real
            # two receiver terms
            out[k].append((sp.simplify(c),(w,w,('I',)*4)))
            out[k].append((sp.simplify(c),(w,('I',)*4,w)))
    return out

HT=h_terms()

def c_action(q,bits,create=True):
    # JW c_q^dag maps 0->1; c_q maps 1->0.
    bit=(bits>>q)&1
    if create and bit: return None
    if not create and not bit: return None
    phase=(-1)**sum((bits>>j)&1 for j in range(q))
    out=bits^(1<<q)
    return out,sp.Integer(phase)

def simple_action(alpha, bits, dual=False):
    # Single-spinor action for alpha=(i,i+1) difference, or i=3 short root.
    if alpha==3:
        # For the B4 spinor, E_{e4}=(Gamma_7-i Gamma_8)Gamma_9/2
        # is bare local raising on the fourth qubit (the JW prefix cancels).
        bit=(bits>>3)&1
        if not dual:
            return None if bit else (bits^(1<<3),sp.Integer(1))
        return None if not bit else (bits^(1<<3),sp.Integer(-1))
    i=alpha
    # E_{e_i-e_{i+1}} = c_i^dagger c_{i+1}; apply annihilate j then create i
    if not dual:
        a=c_action(i+1,bits,False)
        if a is None:return None
        b=c_action(i,a[0],True)
        if b is None:return None
        return b[0],sp.Integer(a[1]*b[1])
    # negative transpose: reverse every nonzero matrix edge with negative coefficient
    # Find primal preimage by reversing target state transitions: ref input has bit i=1,j=0.
    if ((bits>>i)&1)==0 or ((bits>>(i+1))&1)==1:return None
    src=bits^(1<<i)^(1<<(i+1))
    forward=simple_action(alpha,src,False)
    assert forward is not None and forward[0]==bits
    return src,-forward[1]

def weight2(idx):
    # U* x U x U: doubled weight = -h(ref)+h(b1)+h(b2), h=2bit-1.
    ans=[]
    for q in range(4):
        br=(idx>>q)&1; b1=(idx>>(4+q))&1; b2=(idx>>(8+q))&1
        ans.append((1-2*br)+(2*b1-1)+(2*b2-1))
    return tuple(ans)

def target(r):
    return tuple(3 if i<r else 1 for i in range(4))

def make_highest(r):
    wt=target(r)
    states=[x for x in range(4096) if weight2(x)==wt]
    pos={x:i for i,x in enumerate(states)}
    rows=[]
    for a in range(4):
        destwt=list(wt)
        if a<3: destwt[a]+=2; destwt[a+1]-=2
        else: destwt[3]+=2
        destwt=tuple(destwt)
        dest=[x for x in range(4096) if weight2(x)==destwt]
        dpos={x:i for i,x in enumerate(dest)}
        M=sp.zeros(len(dest),len(states))
        for col,x in enumerate(states):
            # reference dual + outputs primal
            for f in range(3):
                b=(x>>(4*f))&15
                ans=simple_action(a,b,dual=(f==0))
                if ans is not None:
                    y,p=ans
                    z=(x&~(15<<(4*f))) | (y<<(4*f))
                    if z in dpos: M[dpos[z],col]+=p
        rows.append(M)
    stacked=sp.Matrix.vstack(*rows)
    ker=stacked.nullspace()
    N=sp.Matrix.hstack(*ker)
    return states,N,stacked

def act_h(k, states, vec):
    # vec indexed by highest-weight computational states, return full sparse dict
    out={}
    for col,x in enumerate(states):
        cv=vec[col]
        if cv==0: continue
        for term in HT[k]:
            y,p=triple_apply(term,x)
            out[y]=out.get(y,0)+cv*p
    return {x:sp.simplify(v) for x,v in out.items() if sp.simplify(v)!=0}

def act_swap(states,vec):
    out={}
    for col,x in enumerate(states):
        cv=vec[col]
        if cv==0: continue
        # output factors 1 and 2 swap four-bit blocks
        y=(x&15)|(((x>>8)&15)<<4)|(((x>>4)&15)<<8)
        out[y]=out.get(y,0)+cv
    return out

def coeff_matrix(states,N,act):
    # N has one column per basis vector, with coordinates on states. act(j)->full dict.
    # solve coefficients using pivot rows of N
    piv=[]
    for rr in range(N.rows):
        trial=piv+[rr]
        if N[trial,:].rank()>len(piv): piv.append(rr)
        if len(piv)==N.cols: break
    assert len(piv)==N.cols
    P=N[piv,:]
    Pinv=P.inv()
    A=sp.zeros(N.cols,N.cols)
    statepos={x:i for i,x in enumerate(states)}
    for j in range(N.cols):
        out=act([N[i,j] for i in range(N.rows)])
        vals=sp.Matrix([out.get(states[i],0) for i in piv])
        A[:,j]=Pinv*vals
        # verify all rows using full support, including outside the highest weight (should preserve)
        for x,v in out.items():
            if x not in statepos: assert sp.simplify(v)==0, ('outside target',x,v)
        predicted=N*A[:,j]
        for i,x in enumerate(states):
            assert sp.simplify(predicted[i]-out.get(x,0))==0, ('preservation failed',j,i)
    return A

def restrict_subspace(A,T):
    # coordinate matrix on invariant range(T)
    piv=[]
    for rr in range(T.rows):
        trial=piv+[rr]
        if T[trial,:].rank()>len(piv): piv.append(rr)
        if len(piv)==T.cols: break
    P=T[piv,:]
    return P.inv()*(A*T)[piv,:]

def gram_schmidt_orthonormal(G):
    n=G.rows
    E=sp.zeros(n,n)
    for j in range(n):
        v=sp.eye(n)[:,j]
        for i in range(j):
            vi=E[:,i]
            v=v-vi*(vi.T*G*v)[0]
        norm=sp.simplify((v.T*G*v)[0])
        E[:,j]=v/sp.sqrt(norm)
    return E

VERTICES = [
    sp.Matrix([1, 0, 0, 14]),
    sp.Matrix([0, 1, 7, 7]),
    sp.Matrix([1, 4, 4, 6]),
]
TRACE_COEFF = sp.Matrix([9, 36, 84, 126])


def primitive_ray(v):
    den = sp.ilcm(*(q.q for q in v))
    z = [int(q * den) for q in v]
    common = 0
    for q in z:
        common = gcd(common, abs(q))
    return tuple(q // common for q in z)


def support_cone_rays(winner):
    # alpha >= 0 and (v_winner-v_other).alpha >= 0.
    rows = [sp.eye(4).row(j) for j in range(4)]
    rows.extend((VERTICES[winner] - VERTICES[j]).T
                for j in range(3) if j != winner)
    rays = set()
    for active in combinations(range(len(rows)), 3):
        M = sp.Matrix.vstack(*(sp.Matrix(rows[j]) for j in active))
        if M.rank() != 3:
            continue
        ker = M.nullspace()
        if len(ker) != 1:
            continue
        q = ker[0]
        if all((row*q)[0] >= 0 for row in rows):
            pass
        elif all((row*(-q))[0] >= 0 for row in rows):
            q = -q
        else:
            continue
        rays.add(primitive_ray(q))
    return rays


def principal_minors(M):
    out = []
    for size in range(1, M.rows + 1):
        for inds in combinations(range(M.rows), size):
            det = sp.simplify(M.extract(inds, inds).det())
            out.append((inds, det))
    return out


def main():
    # On the highest-weight space of each T_r, the invariant Hamiltonian is a
    # (5-r)-by-(5-r) multiplicity matrix.  Resolve the output swap first.
    blocks = {}
    irreducible_dims = [16, 128, 432, 768, 672]
    swap_dims = {}
    total_dimension = 0
    for r in range(5):
        states, N, _ = make_highest(r)
        if N.cols != 5-r:
            raise AssertionError((r, len(states), N.cols))
        H = [coeff_matrix(states, N, lambda v, k=k: act_h(k, states, v))
             for k in range(1, 5)]
        S = coeff_matrix(states, N, lambda v: act_swap(states, v))
        G = N.T*N
        if S*S != sp.eye(N.cols):
            raise AssertionError(("swap involution", r, S))
        if sum(irreducible_dims[r]*(5-r) for r in range(5)) != 4096:
            raise AssertionError("Spin(9) triple decomposition dimensions")
        total_dimension += irreducible_dims[r]*(5-r)
        for eps in (1, -1):
            vecs = (S-eps*sp.eye(N.cols)).nullspace()
            if not vecs:
                continue
            T = sp.Matrix.hstack(*vecs)
            A = [restrict_subspace(q, T) for q in H]
            Gp = T.T*G*T
            E = gram_schmidt_orthonormal(Gp)
            # Exact orthonormal coordinates; every resulting matrix is real
            # symmetric because the physical H_k is Hermitian.
            Ao = [sp.simplify(E.T*Gp*q*E) for q in A]
            for q in Ao:
                if q != q.T or any(z.is_real is False for z in q):
                    raise AssertionError(("not real symmetric", r, eps, q))
            if sp.simplify(E.T*Gp*E-sp.eye(T.cols)) != sp.zeros(T.cols):
                raise AssertionError(("orthonormalization", r, eps))
            blocks[(r, eps)] = Ao
            swap_dims[(r, eps)] = T.cols
        print(f"T_{r}: dim={irreducible_dims[r]}, multiplicity={5-r}, "
              f"swap(+/-)=({swap_dims.get((r,1),0)}/{swap_dims.get((r,-1),0)})",
              flush=True)
        for eps in (1, -1):
            if (r, eps) in blocks:
                print(f"  swap {eps:+d}")
                for k, q in enumerate(blocks[(r, eps)], 1):
                    print(f"    H{k}={q}")

    if total_dimension != 4096:
        raise AssertionError(("dimension", total_dimension))
    sym_dim = sum(irreducible_dims[r]*swap_dims.get((r,1),0) for r in range(5))
    anti_dim = sum(irreducible_dims[r]*swap_dims.get((r,-1),0) for r in range(5))
    if (sym_dim, anti_dim) != (2176, 1920):
        raise AssertionError(("swap dimensions", sym_dim, anti_dim))

    # Independently enumerate the three support cones' extreme rays.
    rays_by_cone = [support_cone_rays(j) for j in range(3)]
    union = set().union(*rays_by_cone)
    expected_union = {
        (1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
        (0,0,1,1),(0,2,0,1),(0,7,5,6),(7,0,2,1),
        (0,1,1,0),(3,0,1,0),
    }
    if union != expected_union:
        raise AssertionError(("support cone rays", [sorted(x) for x in rays_by_cone],
                              sorted(union), sorted(expected_union)))
    if tuple(map(len, rays_by_cone)) != (6, 6, 7):
        raise AssertionError(("per-cone ray counts", tuple(map(len, rays_by_cone))))
    for j, cone in enumerate(rays_by_cone):
        print(f"support cone L{j} rays: {sorted(cone)}", flush=True)

    # The orbit calculation supplies S_can=max_i v_i.alpha as a symbolic
    # input.  At each ray, certify Tr(Q)+S_can-H_Q >= 0 in every irreducible
    # and both output-swap signs by all exact principal minors.
    ray_records = []
    for ray in sorted(union):
        alpha = sp.Matrix(ray)
        scores = [(v.T*alpha)[0] for v in VERTICES]
        S_can = max(scores)
        bound = (TRACE_COEFF.T*alpha)[0] + S_can
        record = {"ray": list(ray), "support_values": [str(q) for q in scores],
                  "support": str(S_can), "bound": str(bound), "blocks": []}
        for key, mats in blocks.items():
            Hmix = sp.zeros(mats[0].rows)
            for ak, mat in zip(alpha, mats):
                Hmix += ak*mat
            gap = sp.simplify(bound*sp.eye(Hmix.rows)-Hmix)
            mins = principal_minors(gap)
            bad = [(inds, val) for inds, val in mins if val.is_nonnegative is False]
            if bad:
                print("EXACT_VIOLATION", ray, key, "bound", bound, "gap", gap,
                      "negative_minors", bad)
                raise AssertionError(("ray PSD failure", ray, key, bad))
            if any(val.is_nonnegative is None for _, val in mins):
                raise AssertionError(("undecided principal minor", ray, key, mins))
            record["blocks"].append({
                "r": key[0], "swap_sign": key[1],
                "gap_matrix": [[str(sp.simplify(gap[i,j])) for j in range(gap.cols)]
                               for i in range(gap.rows)],
                "principal_minors": [
                    {"indices_0_based": list(inds), "determinant": str(val)}
                    for inds, val in mins
                ],
            })
        print(f"ray {ray}: exact PSD in all {len(blocks)} swap/isotypic blocks; "
              f"support={S_can}, bound={bound}", flush=True)
        ray_records.append(record)

    # Full-isotropic normalization check: H=sum_{k=1}^4 H_k has top 270.
    isotropic_max = sp.S(0)
    for key, mats in blocks.items():
        Hmix = sum(mats, sp.zeros(mats[0].rows))
        roots = Hmix.eigenvals()
        largest = max(roots)
        isotropic_max = max(isotropic_max, largest)
    if isotropic_max != 270:
        raise AssertionError(("isotropic normalization", isotropic_max))
    output = Path(__file__).with_name("spin9_fullstar_certificate.json")
    data = {
        "status": "PASS",
        "scope": "Spin(9) invariant Q=sum_{k=1}^4 alpha_k Pi_k, alpha_k>=0",
        "normalization": "tau=Tr/16; Hermitian form basis T_A=i^(k(k-1)/2) Gamma_A",
        "irreducible_dims": irreducible_dims,
        "swap_multiplicities": {f"{r},{eps:+d}": n for (r,eps), n in swap_dims.items()},
        "blocks": {
            f"{r},{eps:+d}": [
                [[str(sp.simplify(M[i,j])) for j in range(M.cols)]
                 for i in range(M.rows)] for M in mats
            ] for (r,eps), mats in blocks.items()
        },
        "support_vertices": [[int(x) for x in v] for v in VERTICES],
        "trace_coefficients": [int(x) for x in TRACE_COEFF],
        "support_cone_rays": [[list(ray) for ray in sorted(cone)] for cone in rays_by_cone],
        "ray_psd_certificates": ray_records,
        "full_isotropic_star_max": str(isotropic_max),
        "full_dimension": total_dimension,
        "swap_sector_dimensions": {"symmetric": sym_dim, "antisymmetric": anti_dim},
    }
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(f"exact matrix/principal-minor certificate saved: {output}")
    print("CERTIFICATE PASS: exact cone rays; exact all-block PSD; "
          "full isotropic top=270; both swap signs retained.")

if __name__=='__main__': main()

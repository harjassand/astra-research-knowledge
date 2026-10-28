#!/usr/bin/env python3
"""Acquire and count hidden growing matrix multiplication from raw Boolean ANF.

Input contains only original bit count and squarefree monomial masks.
No field, grouping, invertible slice, matrix units or small width is supplied.
"""
from pathlib import Path
import itertools, math, sys, time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_field_root'))
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from field_descent import (bits,xor_all,linear_apply,compose,flat,unflat,span,
    solve,nullspace_rows,kernel_columns,tensor_pairs,acquire_field,extract_anf,
    polynomial_value)
from binary_modules import identity,inverse,basis,matrix_basis,hom_basis,module_isomorphism
from zero_product_pair import zero_product_pair_from_ranks
from annihilating_sources import annihilating_cubic_from_ranks
from matrix_kloosterman import (Field,charpoly,factor_polynomial,pmul,
    primary_columns,matrix_kloosterman_from_primary,cubic_zero_source_from_ranks,
    matrix_kloosterman_pair_rank_one_from_data)
from nilpotent_pair_counter import nilpotent_pair_from_alternating_ranks,strings_from_source_ranks
from rank_hom_resummation import even_string_kloosterman,one_sided_even_kloosterman
from cyclic_endpoint_cubic import cubic_from_primary_and_cyclic_ranks
from polynomial_nilpotent_pair import polynomial_nilpotent_pair
from cubic_joint_height import cubic_polynomial_from_primary_and_cyclic_ranks


def add(A,B): return [x^y for x,y in zip(A,B)]
def transpose(A):
    return [sum(((c>>i)&1)<<j for j,c in enumerate(A)) for i in range(len(A))]


def derivations(poly,n):
    pair=tensor_pairs(poly,n)
    rows=[(pair[j][k]<<(n*i))^(pair[i][k]<<(n*j))^(pair[i][j]<<(n*k))
          for i,j,k in itertools.combinations(range(n),3)]
    return [unflat(v,n) for v in nullspace_rows(rows,n*n)]


def hidden_groups(poly,n):
    if n%3: raise ValueError('input count is not three equal blocks')
    D=derivations(poly,n)
    columns=[sum(flat(add(compose(C,E),compose(E,C)),n)<<(n*n*j)
                 for j,E in enumerate(D)) for C in D]
    coeffs=kernel_columns(columns)
    df=[flat(E,n) for E in D]
    Z=[unflat(linear_apply(df,c),n) for c in coeffs]
    if not Z: raise ValueError('derivation Lie center is zero')
    A=matrix_basis([identity(n)]+Z,n)
    while True:
        B=matrix_basis(A+[compose(C,E) for C in Z for E in A],n)
        if len(B)==len(A): A=B; break
        A=B
        if len(A)>n: raise ValueError('oversized grouping algebra')
    if any(compose(C,E)!=compose(E,C) for C in A for E in A):
        raise ValueError('grouping algebra is not commutative')
    af=[flat(E,n) for E in A]
    frob=[solve(af,flat(compose(E,E),n)) for E in A]
    if any(v is None for v in frob) or len(span(frob))!=len(A):
        raise ValueError('grouping algebra is not reduced')
    fixed=kernel_columns([v^(1<<i) for i,v in enumerate(frob)])
    if len(fixed)!=3: raise ValueError('grouping algebra does not have three field factors')
    idems=[unflat(linear_apply(af,linear_apply(fixed,m)),n) for m in range(1,8)]
    d=n//3
    primitive=[E for E in idems if len(span(E))==d]
    if len(primitive)!=3 or xor_all(flat(E,n) for E in primitive)!=flat(identity(n),n):
        raise ValueError('grouping factors are not three equal primitive summands')
    if any(any(compose(primitive[i],primitive[j]))
           for i in range(3) for j in range(3) if i!=j):
        raise ValueError('grouping idempotents are not orthogonal')
    P=sum([basis(E) for E in primitive],[])
    if len(span(P))!=n: raise AssertionError('groups do not span original input')
    grouped=extract_anf(lambda x:polynomial_value(poly,linear_apply(P,x)),n)
    slices=[[0]*d for _ in range(d)]
    for mask in grouped:
        if mask.bit_count()!=3: continue
        i,j,k=bits(mask)
        if not(i<d<=j<2*d<=k): raise ValueError('tensor not trilinear on acquired groups')
        slices[i][j-d]^=1<<(k-2*d)
    if len(span([flat(S,d) for S in slices]))!=d: raise ValueError('slice map has a radical')
    return grouped,slices,P,dict(derivation_dimension=len(D),
        derivation_center_dimension=len(Z),group_algebra_dimension=len(A),
        group_idempotents_enumerated=8,original_bits=n,block_bits=d)


def adjoint_pairs(slices,d):
    rows=[]
    for S in slices:
        SR=transpose(S)
        for j in range(d):
            for i in range(d):
                rows.append(sum(1<<(d*k+i) for k in bits(S[j])) ^
                            (SR[i]<<(d*d+d*j)))
    result=nullspace_rows(rows,2*d*d); mask=(1<<(d*d))-1
    return ([unflat(v&mask,d) for v in result],[unflat(v>>(d*d),d) for v in result])


def polynomial_power(p,e,F):
    out=[1]
    while e:
        if e&1: out=pmul(out,p,F)
        p=pmul(p,p,F); e>>=1
    return out


def reduced_charpoly(cp,t,F):
    """Unique monic t-th root in F[T], including even t, fully verified."""
    v=t&-t; s=v.bit_length()-1
    if any(c for i,c in enumerate(cp) if i%v):
        raise ValueError('regular characteristic polynomial not a Frobenius power')
    p=[F.pow(cp[i],1<<((-s)%F.a)) for i in range(0,len(cp),v)]
    u=t//v; target=list(reversed(p)); r=[1]
    for j in range(1,t+1):
        power=polynomial_power(r,u,F)
        r.append(target[j]^(power[j] if j<len(power) else 0))
    result=list(reversed(r))
    if polynomial_power(result,t,F)!=cp:
        raise ValueError('regular characteristic polynomial has no required monic root')
    return result


class AcquiredMatrixAlgebra:
    def __init__(self,slices):
        self.d=d=len(slices)
        P,Q=adjoint_pairs(slices,d)
        self.stats=dict(adjoint_dimension=len(P))
        H=hom_basis(Q,P,d,d); hf=[flat(E,d) for E in H]; sf=[flat(E,d) for E in slices]
        if len(H)!=d or any(solve(hf,v) is None for v in sf):
            raise ValueError('slice space is not full acquired intertwiner space')
        S=module_isomorphism(Q,P,d,self.stats)
        if S is None or solve(sf,flat(S,d)) is None:
            raise ValueError('acquired slice space has no invertible slice')
        self.slice=S; self.slice_input=solve(sf,flat(S,d)); Sinv=inverse(S)
        self.A=[compose(T,Sinv) for T in slices]; af=[flat(A,d) for A in self.A]
        self.one=solve(af,flat(identity(d),d))
        if self.one is None: raise ValueError('normalized slices omit identity')
        self.table=[[solve(af,flat(compose(A,B),d)) for B in self.A] for A in self.A]
        if any(v is None for row in self.table for v in row):
            raise ValueError('normalized slices not closed under multiplication')
        self.left=self.table
        self.right=[[self.table[i][j] for i in range(d)] for j in range(d)]
        comm=[sum((self.table[i][j]^self.table[j][i])<<(d*j) for j in range(d))
              for i in range(d)]
        self.center=kernel_columns(comm); self.a=a=len(self.center)
        if not a or d%a: raise ValueError('invalid algebra center dimension')
        try:
            self.h,self.field_columns,self.field_module_basis=acquire_field(
                [self.left_matrix(c) for c in self.center],d)
        except (ValueError,AssertionError) as e:
            raise ValueError('algebra center is not a field') from e
        self.F=F=Field(self.h)
        if F.a!=a: raise AssertionError('field acquisition dimension mismatch')
        self.D=D=d//a; self.t=t=math.isqrt(D)
        if t<2 or t*t!=D: raise ValueError('central dimension is not a matrix square >=4')
        envelope=[flat(compose(L,R),d) for L in self.left for R in self.right]
        self.envelope_rank=len(span(envelope))
        if self.envelope_rank!=d*d//a: raise ValueError('bimodule envelope does not certify simplicity')
        self.phi=module_isomorphism(self.left,self.A,d,self.stats)
        if self.phi is None: raise ValueError('slice module not isomorphic to regular module')
        self.Y=compose(inverse(self.phi),S)
        trace_coeffs=[]
        for i in range(d):
            rc=reduced_charpoly(charpoly(self.field_left_matrix(1<<i),F),t,F)
            trace_coeffs.append(F.trace(rc[-2]))
        self.trace_mask=sum(c<<i for i,c in enumerate(trace_coeffs))
        self.gram=[sum(self.trace(self.table[i][j])<<i for i in range(d)) for j in range(d)]
        if len(span(self.gram))!=d: raise ValueError('reduced trace pairing degenerate')
        self.Z=[solve(self.gram,row) for row in transpose(self.phi)]
        if len(span(self.Y))!=d or len(span(self.Z))!=d: raise AssertionError('singular acquired isotopy')
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    if self.trace(self.mul(self.mul(1<<i,self.Y[j]),self.Z[k])) != ((slices[i][j]>>k)&1):
                        raise AssertionError('trace-coordinate tensor identity failed')
        self.stats.update(field_degree=a,field_modulus=self.h,matrix_rank=t,algebra_bits=d,
            bimodule_envelope_rank=self.envelope_rank,tensor_coefficients_verified=d**3,
            supplied_invertible_slices=0,supplied_matrix_units=0)

    def mul(self,x,y): return xor_all(linear_apply(self.table[i],y) for i in bits(x))
    def left_matrix(self,x): return [self.mul(x,1<<j) for j in range(self.d)]
    def is_unit(self,x): return len(span(self.left_matrix(x)))==self.d
    def trace(self,x): return (self.trace_mask&x).bit_count()&1

    def reduced_rank(self,x):
        rank=len(span(self.left_matrix(x)))
        if rank%(self.a*self.t): raise AssertionError('nonintegral reduced rank')
        return rank//(self.a*self.t)

    def relative_trace(self,x):
        return reduced_charpoly(charpoly(self.field_left_matrix(x),self.F),self.t,self.F)[-2]

    def field_left_matrix(self,x):
        cols=[solve(self.field_columns,self.mul(x,b)) for b in self.field_module_basis]
        if any(c is None for c in cols): raise AssertionError('lost field coordinates')
        mask=(1<<self.a)-1
        return [[(c>>(self.a*i))&mask for c in cols] for i in range(self.D)]

    def source(self,linear_mask,variable_map):
        inv=inverse(variable_map)
        functional=sum(((linear_mask&c).bit_count()&1)<<i for i,c in enumerate(inv))
        answer=solve(self.gram,functional)
        if answer is None: raise AssertionError('source trace-dual solution failed')
        return answer

    def primary_data(self,x):
        M=self.field_left_matrix(x); cp=reduced_charpoly(charpoly(M,self.F),self.t,self.F)
        data=[]
        for g,multiplicity in factor_polynomial(cp,self.F):
            columns=primary_columns(M,g,self.t*multiplicity,self.F)
            if any(c%self.t for c in columns): raise AssertionError('invalid regular primary multiplicities')
            data.append(dict(irreducible=g,multiplicity=multiplicity,
                             jordan_columns=[c//self.t for c in columns]))
        return cp,data

    def full_pair_count(self,A,B,require_polynomial=False):
        """Intrinsic exact pair count, uniformly polynomial in rank and field degree."""
        cp,data=self.primary_data(self.mul(A,B))
        regular=[p for p in data if p['irreducible']!=[0,1]]
        u=sum((len(p['irreducible'])-1)*p['multiplicity'] for p in regular)
        v=self.t-u
        kr,regmeta=matrix_kloosterman_from_primary(regular,u,self.h)
        x=A;y=B;ar=[];br=[]
        for length in range(1,2*self.t+2):
            ar.append(self.reduced_rank(x)-u);br.append(self.reduced_rank(y)-u)
            x=self.mul(x,B if length%2 else A)
            y=self.mul(y,A if length%2 else B)
        ranks=[[v],[v]]
        for length in range(1,2*v+2):
            ranks[0].append(br[length-1] if length%2 else ar[length-1])
            ranks[1].append(ar[length-1] if length%2 else br[length-1])
        parts=strings_from_source_ranks(v,ranks)
        even=all(length%2==0 for length,color in parts)
        one_sided=len({color for length,color in parts if length%2==0})<=1
        if even:
            nilmeta={}
            kn=even_string_kloosterman(parts,1<<self.a,nilmeta)
            nilmeta.update(strings=parts,max_chain_length=max((l for l,c in parts),default=0))
        elif one_sided:
            nilmeta={}
            kn=one_sided_even_kloosterman(parts,1<<self.a,nilmeta)
            nilmeta.update(strings=parts,max_chain_length=max((l for l,c in parts),default=0))
        else:
            nilmeta={};kn=polynomial_nilpotent_pair(parts,1<<self.a,nilmeta)
            nilmeta.update(strings=parts,max_chain_length=max((l for l,c in parts),default=0))
        value=(1<<(self.a*u*v))*kr*kn
        route=('even-string Hall resummation' if even else
               'one-sided odd-string Hall resummation' if one_sided else
               'full polynomial two-height pair aggregation')
        return value,dict(route=route,
            regular_rank=u,nilpotent_rank=v,regular=regmeta,nilpotent=nilmeta,
            reduced_product_charpoly=cp,
            complexity='polynomial in a,t; unrestricted acquired string types and height')

    def full_cubic_normalized(self,A,B,C):
        """Full affine-source sum from intrinsic algebra invariants only."""
        cp,data=self.primary_data(self.mul(self.mul(A,C),B))
        arrows=[B,C,A];ranks=[]
        for source in range(3):
            current=self.one;row=[self.t]
            for length in range(1,3*self.t+2):
                current=self.mul(arrows[(source+length-1)%3],current)
                row.append(self.reduced_rank(current))
            ranks.append(row)
        zeros,meta=cubic_polynomial_from_primary_and_cyclic_ranks(data,self.t,self.h,ranks,0)
        signed=2*zeros-(1<<(3*self.d))
        if signed%(1<<self.d):raise AssertionError('missing matrix-fiber normalization')
        meta.update(route='full polynomial cyclic-height aggregation',reduced_product_charpoly=cp)
        return signed//(1<<self.d),meta


def shift_anf(poly,offset):
    out=set()
    for mask in poly:
        optional=mask&offset; sub=optional
        while True:
            m=mask^sub
            if m in out: out.remove(m)
            else: out.add(m)
            if not sub: break
            sub=(sub-1)&optional
    return out


def acquire_center(poly,slices,d,allow_within=False):
    targets=[0,0,0]
    for mask in poly:
        if mask.bit_count()!=2: continue
        i,j=bits(mask)
        if i//d==j//d:
            if allow_within:continue
            raise ValueError('within-group quadratic outside translated matrix family')
        if i<d<=j<2*d: targets[2]^=1<<(d*i+j-d)
        elif i<d and j>=2*d: targets[1]^=1<<(d*i+j-2*d)
        else: targets[0]^=1<<(d*(i-d)+j-2*d)
    columns=[[flat(S,d) for S in slices],
        [sum(slices[i][j]<<(d*i) for i in range(d)) for j in range(d)],
        [sum(((slices[i][j]>>k)&1)<<(d*i+j) for i in range(d) for j in range(d)) for k in range(d)]]
    offsets=[solve(c,t) for c,t in zip(columns,targets)]
    if any(x is None for x in offsets): raise ValueError('quadratic remainder is not a tensor translation')
    offset=sum(x<<(d*i) for i,x in enumerate(offsets)); centered=shift_anf(poly,offset)
    if any(m.bit_count()==2 and (not allow_within or len({i//d for i in bits(m)})>1)
           for m in centered): raise AssertionError('center left forbidden quadratic coefficients')
    return centered,offset


def compile_raw_matrix_trace(poly,n,allow_subexponential=False):
    start=time.perf_counter(); poly=set(poly)
    if n<=0 or any(not isinstance(m,int) or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('input is not a degree-at-most-three Boolean ANF')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices); d=algebra.d
    centered,offset=acquire_center(grouped,slices,d)
    linears=[sum((1<<i) if (1<<(d*j+i)) in centered else 0 for i in range(d)) for j in range(3)]
    sources=[algebra.source(linears[0],identity(d)),algebra.source(linears[1],algebra.Y),
             algebra.source(linears[2],algebra.Z)]
    constant=int(0 in centered); mask=(1<<d)-1
    def reconstructed(v):
        X=v&mask; Y=linear_apply(algebra.Y,(v>>d)&mask); Z=linear_apply(algebra.Z,(v>>(2*d))&mask)
        w=algebra.mul(algebra.mul(X,Y),Z)
        for a,x in zip(sources,(X,Y,Z)): w^=algebra.mul(a,x)
        return algebra.trace(w)^constant
    if extract_anf(reconstructed,n)!=centered: raise AssertionError('full polynomial identity failed')
    zero=next((j for j,x in enumerate(sources) if not x),None)
    annihilating=not any(algebra.mul(sources[(i+1)%3],sources[i])
                        for i in range(3))
    if annihilating:
        rotation=0;cp=None
        gap,backend=annihilating_cubic_from_ranks(algebra.t,algebra.a,
                *[algebra.reduced_rank(x) for x in sources])
        gap*=(-1)**constant
    elif zero is not None:
        rotation=(zero+1)%3; A,B,C=sources[rotation:]+sources[:rotation]; assert C==0
        gap,backend=cubic_zero_source_from_ranks(algebra.t,algebra.a,algebra.reduced_rank(A),
            algebra.reduced_rank(B),algebra.reduced_rank(algebra.mul(B,A)))
        gap*=(-1)**constant; cp=None
    else:
        found=False
        for rotation in range(3):
            A,B,C=sources[rotation:]+sources[:rotation]
            if algebra.is_unit(A) and algebra.is_unit(C):
                argument=algebra.mul(algebra.mul(A,C),B); cp,data=algebra.primary_data(argument)
                K,backend=matrix_kloosterman_from_primary(data,algebra.t,algebra.h)
                found=True; break
        if not found:
            for rotation in range(3):
                A,B,C=sources[rotation:]+sources[:rotation]
                if not algebra.is_unit(C): continue
                D=algebra.mul(C,B); ra,rd=algebra.reduced_rank(A),algebra.reduced_rank(D)
                AD,DA=algebra.mul(A,D),algebra.mul(D,A)
                rad,rda=algebra.reduced_rank(AD),algebra.reduced_rank(DA)
                if not AD or not DA:
                    K,backend=zero_product_pair_from_ranks(algebra.t,algebra.a,ra,rd,rad,rda)
                elif min(ra,rd)<=1:
                    K,backend=matrix_kloosterman_pair_rank_one_from_data(algebra.t,algebra.h,
                        ra,rd,algebra.relative_trace(AD),rad,rda)
                else:continue
                cp=None; found=True; break
        if not found:
            for rotation in range(3):
                A,B,C=sources[rotation:]+sources[:rotation]
                if algebra.is_unit(C):
                    pair_result=algebra.full_pair_count(A,algebra.mul(C,B),
                                                       require_polynomial=not allow_subexponential)
                    if pair_result is None:continue
                    K,backend=pair_result
                    cp=None;found=True;break
        if not found:
            K,backend=algebra.full_cubic_normalized(*sources)
            cp=None;found=True;rotation=0
        if not found:
            raise ValueError('sources outside certified matrix counting branches')
        gap=(-1)**constant*(1<<d)*K
    if abs(gap)>(1<<n) or gap&1: raise AssertionError('invalid exact count reconstruction')
    stats.update(algebra.stats)
    stats.update(raw_monomials=len(poly),coefficient_probes=1+n+n*(n-1)//2+n*(n-1)*(n-2)//6,
        affine_offset=offset,source_rotation=rotation,reduced_argument_charpoly=cp,backend=backend,
        enumerated_boolean_inputs=0,seconds=time.perf_counter()-start)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)


def compile_raw_matrix_trace_subexponential(poly,n):
    """Legacy entry point, now served by the complete polynomial backend."""
    return compile_raw_matrix_trace(poly,n,allow_subexponential=True)

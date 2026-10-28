#!/usr/bin/env python3
"""Polynomial joint endpoint/height transfer for a nilpotent three-cycle.

Uses the proved two-height singular-pair Hall identity. Endpoint profiles
are never enumerated separately. Fixedly many bounded counters are carried
through descending original chain lengths.
"""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from cyclic_endpoint_cubic import cyclic_dimensions,NilpotentCubicCounter,cyclic_strings_from_source_ranks
from matrix_kloosterman import Field,matrix_kloosterman_from_primary

def merge(items):
    """Deterministic comparison-sort aggregation, no hash-table assumption."""
    if not items:return []
    items.sort(key=lambda item:item[0]);out=[];old=items[0][0];weight=0
    for key,value in items:
        if key!=old:out.append((old,weight));old=key;weight=0
        weight+=value
    out.append((old,weight));return out

def pair_category(length,color):
    if length<=0:return None
    kept=[(color-j)%3 for j in range(length) if (color-j)%3!=1]
    if not kept:return None
    pair_color=0 if kept[0]==0 else 1;k=len(kept)
    category=pair_color if k%2 else 2+pair_color
    return (k+1)//2,category

def nilpotent_cubic_joint(parts,q,statistics=None):
    if type(q) is not int or q<2 or q&(q-1):raise ValueError('binary field order required')
    parts=tuple(tuple(x) for x in parts)
    if any(type(l) is not int or l<1 or c not in (0,1,2) for l,c in parts):
        raise ValueError('positive colored chain lengths required')
    dims=cyclic_dimensions(parts,3)
    if len(set(dims))!=1:raise ValueError('balanced three-cycle required')
    n=dims[0];limit=3*n
    multiplicities=[[0]*3 for _ in range(limit+1)]
    for l,c in parts:multiplicities[l][c]+=1
    gaussian=[[0]*(limit+1) for _ in range(limit+1)];gaussian[0][0]=1
    powers=[q**i for i in range(limit+1)]
    for i in range(1,limit+1):
        gaussian[i][0]=gaussian[i][i]=1
        for j in range(1,i):gaussian[i][j]=gaussian[i-1][j-1]+powers[j]*gaussian[i-1][j]
    gl=[1]
    for i in range(1,limit+1):gl.append(gl[-1]*powers[i-1]*(powers[i]-1))
    longer=[0]*(limit+1);total=0
    for l in range(limit,0,-1):
        longer[l]=total;total+=multiplicities[l][(l+1)%3]
    categories={(l,c):pair_category(l,c) for l in range(limit+1) for c in range(3)}
    # State: deleted top, deleted socle, longer retained socles,
    # four current columns, four next-height pending columns,
    # pair image heights c_(j+1),d_(j+1). A temporary 14th coordinate
    # holds top-shortened terminal-zero strings inside each block.
    states=[((0,)*13,1)];transitions=0;peak_states=1;peak_records=1
    height=(max((l for l,c in parts),default=0)+2)//3
    for j in range(height,0,-1):
        states=[((key[0],key[1],key[2],
                  *tuple(key[3+i]+key[7+i] for i in range(4)),
                  0,0,0,0,key[11],key[12],0),weight) for key,weight in states]
        for l in (3*j,3*j-1,3*j-2):
            if l>limit:continue
            emitted=[];top_color=(l+1)%3;original=multiplicities[l];eligible=original[top_color]
            for key,weight in states:
                kt,ks,socle_longer=key[:3];pending_top=key[13]
                for u in range(eligible+1):
                    if kt+u>n:continue
                    top_weight=gaussian[eligible][u]*q**(u*(longer[l]-kt))
                    socle_count=original[0]-(u if top_color==0 else 0)+pending_top
                    for v in range(socle_count+1):
                        if ks+v>n:continue
                        factor=top_weight*gaussian[socle_count][v]*q**(v*socle_longer)
                        cols=list(key[3:7]);pending=list(key[7:11])
                        def emit(length,color,count):
                            if not count:return
                            category=categories[length,color]
                            if category is None:return
                            half,kind=category
                            if half==j:cols[kind]+=count
                            elif half==j-1:pending[kind]+=count
                            else:raise AssertionError(('nonlocal height',j,length,color,half))
                        for color in (1,2):
                            removed=u if color==top_color else 0
                            emit(l,color,original[color]-removed)
                            emit(l-1,color,removed)
                        emit(l,0,socle_count-v);emit(l-1,2,v)
                        new=(kt+u,ks+v,socle_longer+socle_count-v,
                             *cols,*pending,key[11],key[12],u if top_color==0 else 0)
                        emitted.append((new,weight*factor));transitions+=1
            peak_records=max(peak_records,len(emitted));states=merge(emitted)
            peak_states=max(peak_states,len(states))
        emitted=[]
        for key,weight in states:
            if key[13]:raise AssertionError('top shortening crossed a three-length block')
            a,b,e,f=key[3:7];cn,dn=key[11:13]
            for c in range(cn,min(a,b)+1):
                dc=c-cn
                first=gaussian[a-cn][dc]*gaussian[b-cn][dc]*gl[dc]
                for d in range(dn,min(e,f)+1):
                    dd=d-dn
                    exponent=(c+cn*(a+b+e+f-cn)+d+dn*(e+f-dn)
                              +d*(a+b-c-cn))
                    if exponent<0:raise AssertionError('negative local exponent')
                    factor=first*gaussian[e-dn][dd]*gaussian[f-dn][dd]*gl[dd]*q**exponent
                    emitted.append((key[:11]+(c,d),weight*factor));transitions+=1
        peak_records=max(peak_records,len(emitted));states=merge(emitted)
        peak_states=max(peak_states,len(states))
    total=0;leaves=0
    for key,weight in states:
        kt,ks=key[:2];a,b=key[3:5];c=key[11]
        if kt!=ks or a!=b or c!=a:continue
        if any(key[7:11]):raise AssertionError('nonempty height-zero pending state')
        r=n-kt;o=a
        exponent=n*n+n*kt+r*(r-1)//2-o*(o+1)//2
        if exponent<0:raise AssertionError('negative global exponent')
        total+=(-1 if (r+o)%2 else 1)*q**exponent*weight;leaves+=1
    if statistics is not None:
        statistics.update(matrix_size=n,field_degree=q.bit_length()-1,
            transfer_heights=height,generated_transitions=transitions,
            peak_states=peak_states,peak_transition_records=peak_records,final_strata=leaves,
            state_coordinates=14,enumerated_endpoint_profiles=0,
            enumerated_subspaces=0,enumerated_field_elements=0,
            uniform_polynomial_time=True)
    return total

def cubic_polynomial_from_primary_and_cyclic_ranks(primary_data,matrix_rank,field_h,
                                                  source_color_ranks,constant=0):
    """Complete polynomial intrinsic interface, preserving original inputs."""
    F=Field(field_h);n=matrix_rank
    if constant not in (0,1):raise ValueError('binary constant')
    if sum((len(p['irreducible'])-1)*p['multiplicity'] for p in primary_data)!=n:
        raise ValueError('primary dimensions')
    regular=[p for p in primary_data if list(p['irreducible'])!=[0,1]]
    u=sum((len(p['irreducible'])-1)*p['multiplicity'] for p in regular);v=n-u
    Kreg,regmeta=matrix_kloosterman_from_primary(regular,u,field_h)
    nil_ranks=[[r-u for r in row] for row in source_color_ranks]
    parts=cyclic_strings_from_source_ranks([v,v,v],nil_ranks,3)
    stats={};nil=nilpotent_cubic_joint(parts,F.q,stats)
    signed=F.q**(u*u+3*u*v)*Kreg*nil;N=3*F.a*n*n
    actual=(-1)**constant*signed
    if ((1<<N)+actual)%2:raise ArithmeticError('nonintegral Boolean count')
    return ((1<<N)+actual)//2,dict(route='full polynomial cyclic-height aggregation',
        original_inputs=N,matrix_rank=n,field_degree=F.a,regular_dimension=u,
        nilpotent_dimension=v,nilpotent_strings=parts,
        nilpotent_max_chain=max((l for l,c in parts),default=0),
        core_signed_sum=signed,signed_sum=actual,constant=constant,
        regular_backend=regmeta,nilpotent_backend=stats,uniform_polynomial_time=True,
        complexity='O((a+1)^2 (t+1)^24 + (at+1)^8) bit operations; conservative')

def cubic_polynomial_all_sources(A,B,C,field_h=3,constant=0):
    """Complete polynomial count on explicitly described field matrices."""
    from matrix_kloosterman import mmul,rref,charpoly,factor_polynomial,primary_columns,eye
    F=Field(field_h);n=len(A)
    if len(B)!=n or len(C)!=n or any(len(row)!=n for row in A+B+C):
        raise ValueError('coefficient shape')
    D=mmul(mmul(A,C,F),B,F);primary=[]
    for g,b in factor_polynomial(charpoly(D,F),F):
        primary.append(dict(irreducible=g,multiplicity=b,jordan_columns=primary_columns(D,g,b,F)))
    ranks=[];arrows=[B,C,A]
    for source in range(3):
        current=eye(n);row=[n]
        for k in range(1,3*n+2):
            current=mmul(arrows[(source+k-1)%3],current,F)
            row.append(len(rref(current,F)[1]))
        ranks.append(row)
    return cubic_polynomial_from_primary_and_cyclic_ranks(primary,n,field_h,ranks,constant)

def checks():
    from cyclic_endpoint_cubic import cyclic_string_types
    begun=time.perf_counter();rows=[]
    for q,nmax in ((2,3),(4,3),(8,2)):
        count=0;peak=0;transitions=0
        for n in range(nmax+1):
            for parts in cyclic_string_types(n):
                stats={};got=nilpotent_cubic_joint(parts,q,stats)
                old=NilpotentCubicCounter(q).count_signed(parts)
                assert got==old,(q,parts,got,old)
                peak=max(peak,stats['peak_states']);transitions+=stats['generated_transitions'];count+=1
        rows.append(dict(q=q,max_dimension=nmax,types=count,peak_states=peak,total_transitions=transitions))
        print(json.dumps(rows[-1]),flush=True)
    data=dict(status='all joint transfers match the independent endpoint recursion',checks=rows,
        seconds=time.perf_counter()-begun)
    Path(__file__).with_name('cubic_joint_height_results.json').write_text(json.dumps(data,indent=2)+'\n')
    return data

if __name__=='__main__':checks()

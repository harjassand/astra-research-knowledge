#!/usr/bin/env python3
"""Acquired self-adjoint central blocks; no commuting-projector assumption."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_trace_frontier','work_matrix_root','work_norm_slice_agent')]
from projector_quadratic_fibers import (polar_rows,affine_solutions,apply_binary,
    compose_quadratic,quadratic_gap,independent_basis,linear_kernel)
from acquired_planar_quadratic_fibers import binary_rows
from rectangle_tensor_admissibility import hyperdet

def pack(A,n):return sum(x<<(n*j) for j,x in enumerate(A))
def unpack(x,n):return [(x>>(n*j))&((1<<n)-1) for j in range(n)]
def product(A,B):return [apply_binary(A,x) for x in B]
def transpose(A):return binary_rows(A,len(A))
def xor_terms(parts):
    out=set()
    for terms in parts:out.symmetric_difference_update(terms)
    return out

def algebra_basis(generators,n):
    pivots={};basis=[]
    def insert(value):
        reduced=value
        while reduced:
            j=reduced.bit_length()-1
            if j in pivots:reduced^=pivots[j]
            else:pivots[j]=reduced;basis.append(value);return
    insert(pack([1<<i for i in range(n)],n));index=0;products=0
    while index<len(basis):
        A=unpack(basis[index],n);index+=1
        for G in generators:insert(pack(product(A,G),n));products+=1
    return basis,products

def local_information(quadratics,columns):
    d=len(columns);mons=[1<<j for j in range(d)]+[(1<<i)|(1<<j) for i in range(d) for j in range(i)]
    pos={m:i for i,m in enumerate(mons)};pivots={};basis=[];coefficients=[]
    for terms in quadratics:
        local=compose_quadratic(set(terms)-{0},0,columns)
        value=sum(1<<pos[m] for m in local);representation=0
        while value:
            j=value.bit_length()-1
            if j in pivots:
                row,label=pivots[j];value^=row;representation^=label
            else:
                bit=1<<len(basis);basis.append(local)
                pivots[j]=(value,representation^bit);representation=bit;break
        coefficients.append(representation)
    emission=[sum(((c>>j)&1)<<i for i,c in enumerate(coefficients)) for j in range(len(basis))]
    return basis,emission

def acquire_central_blocks(source_anf,quadratics,n,maximum_local_information=3):
    started=time.perf_counter();source=set(source_anf);quadratics=list(map(set,quadratics))
    if any(m<0 or m.bit_length()>n or m.bit_count()>2 for terms in [source]+quadratics for m in terms):
        raise ValueError('explicit binary quadratics required')
    B0=polar_rows(source,n);inverse=[]
    for i in range(n):
        solved=affine_solutions([(row,int(j==i)) for j,row in enumerate(B0)],n)
        if solved is None or solved[1]:raise ValueError('nonsingular source polar required')
        inverse.append(solved[0])
    operators=[product(inverse,polar_rows(terms,n)) for terms in quadratics]
    algebra,products=algebra_basis(operators,n);width=n*n;commutators=[]
    for value in algebra:
        A=unpack(value,n);packed=0
        for j,G in enumerate(operators):packed|=(pack(product(A,G),n)^pack(product(G,A),n))<<(width*j)
        commutators.append(packed)
    center=[apply_binary(algebra,c) for c in linear_kernel(commutators,width*len(operators))]
    equations=[]
    for value in center:
        Z=unpack(value,n);B0Z=product(B0,Z)
        equations.append((pack(product(Z,Z),n)^value)|((pack(B0Z,n)^pack(transpose(B0Z),n))<<width))
    idempotents=[apply_binary(center,c) for c in linear_kernel(equations,2*width)]
    blocks=[[1<<i for i in range(n)]]
    for value in idempotents:
        E=unpack(value,n)
        if product(E,E)!=E or product(B0,E)!=transpose(product(B0,E)):
            raise AssertionError('invalid self-adjoint central idempotent')
        refined=[]
        for columns in blocks:
            images=[apply_binary(E,x) for x in columns]
            left=independent_basis(images);right=independent_basis(x^y for x,y in zip(columns,images))
            if len(left)+len(right)!=len(columns):raise AssertionError('central split is not a direct sum')
            if left:refined.append(left)
            if right:refined.append(right)
        blocks=refined
    if sum(map(len,blocks))!=n or len(independent_basis(x for b in blocks for x in b))!=n:
        raise AssertionError('manufactured coordinates are not bijective')
    for i,left in enumerate(blocks):
        for right in blocks[:i]:
            for polar in [B0]+[polar_rows(f,n) for f in quadratics]:
                if any((x&apply_binary(polar,y)).bit_count()%2 for x in left for y in right):
                    raise AssertionError('cross-block quadratic coupling survived')
    records=[]
    for columns in blocks:
        information,emission=local_information(quadratics,columns)
        if len(information)>maximum_local_information:raise ValueError('acquired central block exceeds local-information budget')
        records.append(dict(columns=columns,input_bits=len(columns),
            source_anf=sorted(compose_quadratic(source-{0},0,columns)),
            information_anf=[sorted(f) for f in information],emission_columns=emission,information_rank=len(information)))
    commute=all(product(A,B)==product(B,A) for i,A in enumerate(operators) for B in operators[:i])
    return dict(input_bits=n,marked_quadratics=len(quadratics),blocks=records,
        source_constant=int(0 in source),output_constant=sum(int(0 in f)<<i for i,f in enumerate(quadratics)),
        generated_algebra_dimension=len(algebra),center_dimension=len(center),
        self_adjoint_idempotent_dimension=len(idempotents),algebra_products=products,
        original_relative_operators_commute=commute,source_orthogonal_verified=True,
        supplied_decomposition=False,enumerated_idempotents=0,seconds=time.perf_counter()-started)

def acquire_paired_ports(certificate):
    import networkx as nx
    blocks=certificate['blocks'];active=[i for i,b in enumerate(blocks) if b['information_rank']]
    if any(blocks[i]['information_rank']!=3 for i in active):raise ValueError('three active ports per block required')
    occurrences={}
    for i in active:
        for mask in range(1,8):
            value=apply_binary(blocks[i]['emission_columns'],mask)
            occurrences.setdefault(value,[]).append(i)
    if any(len(indices)>2 for indices in occurrences.values()):raise ValueError('a port line belongs to more than two blocks')
    lines=sorted(v for v,indices in occurrences.items() if len(indices)==2)
    if len(independent_basis(lines))!=len(lines):raise ValueError('shared lines are not independent edge syndromes')
    vertex={block:j for j,block in enumerate(active)};edges=[tuple(vertex[i] for i in occurrences[v]) for v in lines]
    if len(set(tuple(sorted(e)) for e in edges))!=len(edges):raise ValueError('simple acquired graph required')
    records=[]
    for i in active:
        b=blocks[i];incident=[e for e,v in enumerate(lines) if i in occurrences[v]]
        if len(incident)!=3:raise ValueError('intersections do not supply three local ports')
        coordinates=[];rows=binary_rows(b['emission_columns'],certificate['marked_quadratics'])
        for e in incident:
            solved=affine_solutions([(row,(lines[e]>>j)&1) for j,row in enumerate(rows)],3)
            if solved is None or solved[1]:raise AssertionError('nonunique local port coordinates')
            coordinates.append(solved[0])
        inverse=[]
        for k in range(3):
            solved=affine_solutions([(row,int(j==k)) for j,row in enumerate(binary_rows(coordinates,3))],3)
            if solved is None or solved[1]:raise ValueError('shared lines do not form a local basis')
            inverse.append(solved[0])
        forms=[xor_terms(b['information_anf'][j] for j in range(3) if inverse[j]>>k&1) for k in range(3)]
        G=[]
        for mask in range(8):
            terms=set(b['source_anf'])^xor_terms(forms[j] for j in range(3) if mask>>j&1)
            G.append(quadratic_gap(terms,b['input_bits']))
        T=[]
        for point in range(8):
            value=sum(g*(-1 if (point&mask).bit_count()%2 else 1) for mask,g in enumerate(G))
            if value%8:raise AssertionError('nonintegral local signed fiber')
            T.append(value//8)
        records.append(dict(block_index=i,incident_edges=incident,port_quadratics=[sorted(f) for f in forms],
            tensor=T,gaussian_probes=G,hyperdeterminant=hyperdet(T)))
    graph=nx.Graph();graph.add_nodes_from(range(len(active)));graph.add_edges_from(edges)
    planar,embedding=nx.check_planarity(graph)
    if not planar:raise ValueError('acquired tensor graph is nonplanar')
    embedding.check_structure()
    return dict(vertices=len(active),edges=[list(e) for e in edges],edge_syndrome_columns=lines,
        vertices_data=records,rotation={str(v):list(embedding.neighbors_cw_order(v)) for v in graph},
        unobserved_blocks=[i for i,b in enumerate(blocks) if not b['information_rank']],
        graph_supplied=False,ports_supplied=False,gaussian_evaluations=8*len(active))

def parity_n1077_genericity(graph,require_nonzero=True):
    """Exact CP-edge genericity for an already verified even-parity chart.

    If q_v,e(x,y)=a*x²-b*y², CP directions solve a*y²-b*x²=0.
    Neighbor pairings are all nonzero exactly when a_v*a_w-b_v*b_w!=0.
    This is an admission check, not a generic non-parity gauge compiler.
    """
    data=graph['vertices_data'];tests=[]
    for record in data:
        T=record['tensor']
        if any(T[x] for x in range(8) if x.bit_count()%2) or not record['hyperdeterminant']:
            raise ValueError('an even-parity nonsingular chart is required for this exact check')
    for e,(v,w) in enumerate(graph['edges']):
        pair=[]
        for vertex in (v,w):
            record=data[vertex];T=record['tensor'];port=record['incident_edges'].index(e)
            others=[i for i in range(3) if i!=port]
            a=T[0]*T[(1<<others[0])|(1<<others[1])]
            b=T[(1<<port)|(1<<others[0])]*T[(1<<port)|(1<<others[1])]
            pair.append((a,b))
        determinant=pair[0][0]*pair[1][0]-pair[0][1]*pair[1][1]
        if not determinant and require_nonzero:raise ValueError('a CP edge pairing vanishes: outside generic N1077 admission')
        tests.append(determinant)
    return dict(all_hyperdeterminants_nonzero=True,all_CP_edge_pairings_nonzero=all(tests),
        compatible_parity_gauges_verified=True,edge_resultants=tests,
        gauge_chart='identity in acquired port coordinates')

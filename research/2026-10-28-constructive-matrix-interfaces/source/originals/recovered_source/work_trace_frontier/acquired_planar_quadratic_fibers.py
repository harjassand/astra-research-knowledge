#!/usr/bin/env python3
"""Acquire a planar cubic parity code and count its signed quadratic fiber.

The input is an ordinary Boolean DAG plus a quadratic source.  No graph,
embedding, gauge, latent variables or decomposition is supplied to the
compiler.  It reuses the verified reversible/projector acquisition, discovers
vertex stars in the acquired code's rowspace, obtains a planar embedding,
builds explicit even-parity K4 matchgates and performs an exact Pfaffian.

This is a restricted recognizer, with explicit rejection; it is not a general
polynomial #SAT algorithm or a new FKT theorem.  NetworkX 3.5 is the only
nonstandard dependency and is used solely for planarity/rotation acquisition.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from math import gcd
import sys

HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
sys.path[:0]=[str(HERE),'/tmp/astra_planarity_deps']
from projector_quadratic_fibers import (acquire_projector_blocks,
    acquire_reversible_terminal_and, invert_terminal, affine_solutions,
    apply_binary, quadratic_gap, prepared_program, validate_trace_program)


def xor_basis(vectors):
    pivots={}
    for vector in vectors:
        while vector:
            p=vector.bit_length()-1
            if p in pivots:vector^=pivots[p]
            else:pivots[p]=vector;break
    return [pivots[p] for p in sorted(pivots,reverse=True)]


def in_span(vector,basis):
    for row in basis:
        p=row.bit_length()-1
        if vector>>p&1:vector^=row
    return vector==0


def binary_rows(columns,height):
    return [sum(((column>>i)&1)<<j for j,column in enumerate(columns)) for i in range(height)]


def acquire_cubic_cycle_code(columns,mark_count):
    """Find all rowspace words of weight <=3 and verify the vertex-star claim.

    Acceptance itself proves ker(C) is this graph's binary cycle space.
    Completeness is claimed only for simple 3-edge-connected cubic graphs
    having no non-vertex cut of size three.  There is no promise to recognize
    all graphic codes, nor a supplied incidence basis or rotation system.
    """
    import networkx as nx
    e=len(columns)
    if e<3:raise ValueError('no acquired cubic cycle-code graph')
    if any(type(c) is not int or c<0 or c.bit_length()>mark_count for c in columns):
        raise ValueError('invalid binary emission columns')
    rows=binary_rows(columns,mark_count);basis=xor_basis(rows);stars=[];tests=0
    for size in (1,2,3):
        for support in combinations(range(e),size):
            word=sum(1<<j for j in support);tests+=1
            if in_span(word,basis):
                if size!=3:raise ValueError('acquired code has a cut of size one or two')
                stars.append(word)
    incidences=[[] for _ in range(e)]
    for v,star in enumerate(stars):
        for j in range(e):
            if star>>j&1:incidences[j].append(v)
    if any(len(vs)!=2 for vs in incidences):
        raise ValueError('low-weight rowspace words do not give exactly two stars per edge')
    star_basis=xor_basis(stars)
    if len(star_basis)!=len(basis) or not all(in_span(row,star_basis) for row in basis):
        raise ValueError('acquired stars do not span the complete code rowspace')
    edges=[tuple(vs) for vs in incidences]
    if len(set(edges))!=e:raise ValueError('this recognizer admits simple acquired graphs only')
    graph=nx.Graph();graph.add_nodes_from(range(len(stars)));graph.add_edges_from(edges)
    planar,embedding=nx.check_planarity(graph)
    if not planar:raise ValueError('acquired parity graph is nonplanar')
    embedding.check_structure()
    return dict(vertices=len(stars),edges=[list(edge) for edge in edges],stars=stars,
        row_rank=len(basis),cycle_dimension=e-len(basis),rowspace_membership_tests=tests,
        rotation={str(v):list(embedding.neighbors_cw_order(v)) for v in graph},
        connected_components=nx.number_connected_components(graph),
        acquired_planar=True,graph_supplied=False,embedding_supplied=False,
        planarity_backend='NetworkX '+nx.__version__+' check_planarity')


def acquire_pfaffian_orientation(vertices,edges):
    """Solve and independently check clockwise-odd face equations over F2."""
    import networkx as nx
    edges=[tuple(sorted(edge)) for edge in edges]
    if len(set(edges))!=len(edges):raise ValueError('simple gadget graph required')
    index={edge:i for i,edge in enumerate(edges)}
    graph=nx.Graph();graph.add_nodes_from(range(vertices));graph.add_edges_from(edges)
    planar,embedding=nx.check_planarity(graph)
    if not planar:raise ValueError('expanded matchgate graph failed planarity')
    embedding.check_structure();equations=[];checked_faces=[];component_faces=[]
    for component in nx.connected_components(graph):
        marked=set();faces=[]
        for u in sorted(component):
            for v in embedding.neighbors_cw_order(u):
                if (u,v) not in marked:faces.append(embedding.traverse_face(u,v,marked))
        edge_count=sum(graph.degree(v) for v in component)//2
        if len(component)-edge_count+len(faces)!=2:raise ValueError('rotation Euler check failed')
        if len(component)%2:raise ValueError('odd gadget component')
        component_faces.append(len(faces))
        for face in faces[1:]:
            row=0;rhs=1
            for u,v in zip(face,face[1:]+face[:1]):
                row^=1<<index[tuple(sorted((u,v)))];rhs^=int(u>v)
            equations.append((row,rhs));checked_faces.append(face)
    solved=affine_solutions(equations,len(edges))
    if solved is None:raise ValueError('clockwise-odd orientation equations inconsistent')
    orientation=solved[0]
    for face in checked_faces:
        parity=0
        for u,v in zip(face,face[1:]+face[:1]):
            arrow=(orientation>>index[tuple(sorted((u,v)))])&1
            parity^=arrow^int(u>v)
        if parity!=1:raise AssertionError('orientation face parity verification failed')
    return dict(orientation=orientation,edges=edges,face_equations=len(equations),
        component_face_counts=component_faces,verified_faces=len(checked_faces),
        rotation={str(v):list(embedding.neighbors_cw_order(v)) for v in graph})


def pfaffian_integer(matrix):
    """Fraction-free skew elimination; exact divisions checked at every step.

    The update is the Pfaffian Pluecker/Bareiss identity.  Its entries are
    Pfaffians of minors; row/column pivot permutations preserve this invariant.
    """
    n=len(matrix)
    if n%2 or any(len(row)!=n for row in matrix):raise ValueError('even square skew matrix required')
    if any(matrix[i][i] or any(matrix[i][j]!=-matrix[j][i] for j in range(i)) for i in range(n)):
        raise ValueError('matrix is not skew-symmetric')
    if not n:return dict(pfaffian=1,updates=0,maximum_entry_bits=1)
    A=[list(row) for row in matrix];sign=1;previous=1;updates=0;bits=1
    for k in range(0,n-1,2):
        pivot_index=next((j for j in range(k+1,n) if A[k][j]),None)
        if pivot_index is None:return dict(pfaffian=0,updates=updates,maximum_entry_bits=bits)
        if pivot_index!=k+1:
            A[k+1],A[pivot_index]=A[pivot_index],A[k+1]
            for row in A:row[k+1],row[pivot_index]=row[pivot_index],row[k+1]
            sign=-sign
        pivot=A[k][k+1]
        if k==n-2:return dict(pfaffian=sign*pivot,updates=updates,maximum_entry_bits=max(bits,abs(pivot).bit_length()))
        for i in range(k+2,n):
            aki=A[k][i];ak1i=A[k+1][i]
            for j in range(i+1,n):
                numerator=pivot*A[i][j]-aki*A[k+1][j]+A[k][j]*ak1i
                value,remainder=divmod(numerator,previous)
                if remainder:raise AssertionError('non-exact fraction-free Pfaffian division')
                A[i][j]=value;A[j][i]=-value;updates+=1
                bits=max(bits,abs(value).bit_length())
        previous=pivot
    raise AssertionError('unreachable Pfaffian state')


def matching_orientation_sign(matching,orientation,edge_index):
    pairs=[tuple(sorted(pair)) for pair in matching];parity=0
    for i,(a,b) in enumerate(pairs):
        parity^=1^((orientation>>edge_index[(a,b)])&1)
        for c,d in pairs[:i]:parity^=int(a<c<b<d or c<a<d<b)
    return -1 if parity else 1


def planar_even_parity_sum(graph,weights,allow_zero_selected=False):
    """Exact sum over even edge configurations, with full signed prefactor."""
    vertices=graph['vertices'];original_edges=graph['edges']
    if len(weights)!=len(original_edges):raise ValueError('edge weight inventory mismatch')
    weights=[tuple(map(Fraction,table)) for table in weights]
    if any(len(table)!=2 or not table[0] or (not table[1] and not allow_zero_selected)
           for table in weights):
        raise ValueError('this matchgate chart requires a nonzero unselected weight; '
                         'selected zeros require the explicit pinning extension')
    incidents=[[] for _ in range(vertices)]
    for j,(u,v) in enumerate(original_edges):incidents[u].append(j);incidents[v].append(j)
    if any(len(es)!=3 for es in incidents):raise ValueError('trivalent acquired graph required')
    ports={};gadget_weights={};reference=[]
    def put(a,b,weight):
        edge=tuple(sorted((a,b)))
        if edge in gadget_weights:raise AssertionError('duplicate matchgate edge')
        gadget_weights[edge]=Fraction(weight)
    for v,es in enumerate(incidents):
        for port,e in enumerate(es):ports[(v,e)]=4*v+port
        for port in range(3):put(4*v+port,4*v+3,1)
        for i,j in combinations(range(3),2):put(4*v+i,4*v+j,Fraction(1,3))
        reference.extend(((4*v,4*v+3),(4*v+1,4*v+2)))
    prefactor=Fraction(1)
    for j,(u,v) in enumerate(original_edges):
        w0,w1=weights[j];prefactor*=w0
        put(ports[(u,j)],ports[(v,j)],w1/w0)
    edges=sorted(gadget_weights);oriented=acquire_pfaffian_orientation(4*vertices,edges)
    edge_index={edge:i for i,edge in enumerate(edges)}
    reference_sign=matching_orientation_sign(reference,oriented['orientation'],edge_index)
    denominator=1
    for weight in gadget_weights.values():denominator=denominator*weight.denominator//gcd(denominator,weight.denominator)
    n=4*vertices;matrix=[[0]*n for _ in range(n)]
    for j,(u,v) in enumerate(edges):
        entry=gadget_weights[(u,v)]*denominator
        if entry.denominator!=1:raise AssertionError('matrix denominator was not cleared')
        value=entry.numerator*(1 if oriented['orientation']>>j&1 else -1)
        matrix[u][v]=value;matrix[v][u]=-value
    elimination=pfaffian_integer(matrix)
    answer=prefactor*reference_sign*Fraction(elimination['pfaffian'],denominator**(n//2))
    return dict(value=answer,matchgate_vertices=n,matchgate_edges=len(edges),
        pfaffian_matrix_denominator=denominator,reference_matching_sign=reference_sign,
        scaled_pfaffian=elimination['pfaffian'],pfaffian_updates=elimination['updates'],
        pfaffian_maximum_entry_bits=elimination['maximum_entry_bits'],
        face_equations=oriented['face_equations'],verified_faces=oriented['verified_faces'],
        component_face_counts=oriented['component_face_counts'],
        prefactor_numerator=prefactor.numerator,prefactor_denominator=prefactor.denominator,
        cycle_configurations_enumerated=0,orientation=oriented['orientation'])


def planar_projector_target_fiber(certificate,target):
    columns=certificate['emission_columns'];m=certificate['marked_quadratics'];e=len(columns)
    value=target^certificate['output_constant'];rows=binary_rows(columns,m)
    solution=affine_solutions([(row,(value>>i)&1) for i,row in enumerate(rows)],e)
    if solution is None:
        return dict(status='empty_fiber',fiber_weight=0,quadratic_gauss_evaluations=0,
            coset_points_evaluated=0)
    graph=acquire_cubic_cycle_code(columns,m)
    offset=solution[0];weights=[];queries=0;prefactor=1-2*certificate['source_constant']
    for block in certificate['unobserved_blocks']:
        prefactor*=quadratic_gap(block['source_anf'],block['input_bits']);queries+=1
    for block in certificate['blocks']:
        Z=quadratic_gap(block['source_anf'],block['input_bits'])
        W=quadratic_gap(set(block['source_anf'])^set(block['information_anf']),block['input_bits'])
        if (Z+W)%2 or (Z-W)%2:raise AssertionError('nonintegral local response')
        weights.append([(Z+W)//2,(Z-W)//2]);queries+=2
    total=prefactor
    for table in weights:total*=sum(table)
    swapped=[list(reversed(table)) if offset>>j&1 else list(table) for j,table in enumerate(weights)]
    fkt=planar_even_parity_sum(graph,swapped);weighted=fkt.pop('value')*prefactor
    if weighted.denominator!=1:raise AssertionError('nonintegral original quadratic fiber')
    return dict(status='counted',fiber_weight=weighted.numerator,total_response=total,
        quadratic_gauss_evaluations=queries,local_tables=weights,graph_certificate=graph,
        coset_offset=offset,coset_dimension=len(solution[1]),coset_points_evaluated=0,
        swapped_edge_indices=[j for j in range(e) if offset>>j&1],
        unobserved_source_prefactor=prefactor,fkt_certificate=fkt)


def count_planar_reversible_response(source_anf,program):
    reversible=acquire_reversible_terminal_and(program)
    certificate=acquire_projector_blocks(source_anf,reversible['initial_quadratics'],reversible['input_bits'])
    target=invert_terminal(reversible);fiber=planar_projector_target_fiber(certificate,target)
    total=fiber.get('total_response');extra=int(total is None)
    if total is None:total=quadratic_gap(source_anf,reversible['input_bits'])
    return dict(status='counted',weighted_gap=total-2*fiber['fiber_weight'],
        reversible_certificate=reversible,projector_certificate=certificate,fiber_certificate=fiber,
        accepted_initial_register_value=target,inverted_terminal_states=1,
        original_input_assignments_enumerated=0,auxiliary_independent_inputs=0,
        complete_quadratic_summary_cube_enumerated=False,
        total_quadratic_gauss_evaluations=fiber['quadratic_gauss_evaluations']+extra)


def count_planar_resonant_program(program,field_h):
    sys.path.insert(0,str(ROOT/'work_ring_count_agent'))
    from circuit_field_packing import BinaryField
    from resonant_two_trace_boundary import response_constants
    F=BinaryField(field_h);a=F.n;validate_trace_program(program,2*a)
    source={(1<<i)|(1<<(a+j)) for i in range(a) for j in range(a) if F.trace(F.mul(1<<i,1<<j))}
    result=count_planar_reversible_response(source,program)
    result.update(field_polynomial=field_h,field_degree=a,source_D=[[0,F.eta],[1,1]],
        original_independent_bits=12*a,counted_domain_size=1<<(12*a))
    _,B,delta=response_constants(F.q);evaluate,_,_=prepared_program(program,2*a)
    gap=B*result['weighted_gap']+delta*(1-2*evaluate(0));domain=1<<(12*a)
    if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid native-domain count')
    result.update(gap=gap,ones=(domain-gap)//2,zeros=(domain+gap)//2)
    return result

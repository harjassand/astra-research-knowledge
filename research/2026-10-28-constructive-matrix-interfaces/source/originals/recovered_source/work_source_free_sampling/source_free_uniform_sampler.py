#!/usr/bin/env python3
"""Exact uniform samples from an acquired source-free product fiber.

All arithmetic is in the acquired binary algebra and its actual modules.
No field generator, polynomial factorization, or full matrix-unit system is constructed.
Randomized preprocessing and sampling have proved expected polynomial cost.
This is a consumer of a checked restricted-family certificate, not general SAT.
"""
from pathlib import Path
import random,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_multiprimary_audit','work_trace_frontier')]
from adjoint_matrix_product_counter import (BinaryCoordinates,apply_binary,
    unpack,affine_solutions,linear_kernel,independent_basis,gaussian_binomial)
from raw_bilinear_product_counter import bilinear_product_target_fiber


def equations_from_columns(columns,target,height):
    return [(sum(((value>>i)&1)<<j for j,value in enumerate(columns)),
        (target>>i)&1) for i in range(height)]


class AcquiredProductFiberSampler:
    def __init__(self,split,certificate,target,rng=None):
        begun=time.perf_counter();self.split=split;self.C=certificate
        self.rng=rng if rng is not None else random.SystemRandom()
        self.fiber=bilinear_product_target_fiber(certificate,target)
        self.population=self.fiber['population'];self.target=target
        self.stats=dict(corner_random_trials=0,corner_splits=0,
            stabilizer_trials=0,full_rank_input_trials=0,samples=0,
            field_generators_constructed=0,polynomials_factored=0,
            connecting_matrix_units_constructed=0,original_assignments_enumerated=0)
        if not self.population:
            self.stats['preprocessing_seconds']=time.perf_counter()-begun
            return
        C=certificate;self.U=C['left_dimension'];self.V=C['right_dimension']
        self.M=C['output_dimension'];self.a=C['field_degree']
        self.p=C['left_matrix_rows'];self.d=C['inner_dimension'];self.r=C['right_matrix_columns']
        self.k=self.fiber['matrix_target_rank'];self.y=self.fiber['target_output_coordinates']
        self.algebra=C['nucleus_certificate'];self.table=self.algebra['multiplication_table']
        self.K=len(self.table);self.one=self.algebra['unit_coordinates']
        self.input_ops=[unpack(x,self.U) for x in C['nucleus_input_operators']]
        self.output_ops=[unpack(x,self.M) for x in C['nucleus_output_operators']]
        self.forms=[split['cross_matrices'][i] for i in C['output_basis_mark_indices']]
        self.P=self.target_projection()
        if self.matrix_rank(self.P)!=self.k or self.mul(self.P,self.P)!=self.P:
            raise AssertionError('target-image projector certificate failed')
        self.complement_primitives=self.primitive_decomposition(self.one^self.P)
        self.projections=[self.P]
        for e in self.complement_primitives:self.projections.append(self.projections[-1]^e)
        if self.projections[-1]!=self.one:raise AssertionError('corner projections do not exhaust the unit')
        images=[self.mul(self.one^self.P,self.mul(1<<j,self.P)) for j in range(self.K)]
        self.stabilizer_basis=linear_kernel(images,self.K)
        self.strata=[]
        for s in range(self.k,min(self.p,self.d)+1):
            onto=1
            for j in range(s):onto*=((1<<(self.a*self.d))-(1<<(self.a*j)))
            weight=gaussian_binomial(self.p-self.k,s-self.k,self.a)*onto*(1<<(self.a*self.r*(self.d-s)))
            self.strata.append((s,weight))
        if sum(w for _,w in self.strata)!=self.population:
            raise AssertionError('sampling strata do not sum to the certified count')
        self.stats['primitive_projection_ranks']=[self.matrix_rank(e) for e in self.complement_primitives]
        self.stats['stabilizer_binary_dimension']=len(self.stabilizer_basis)
        self.stats['preprocessing_seconds']=time.perf_counter()-begun

    def mul(self,x,y):
        return apply_binary([apply_binary(row,y) for row in self.table],x)

    def output_action(self,A,y):
        return apply_binary([apply_binary(op,y) for op in self.output_ops],A)

    def input_action(self,A,u):
        return apply_binary([apply_binary(op,u) for op in self.input_ops],A)

    def matrix_rank(self,A):
        columns=[self.output_action(A,1<<i) for i in range(self.M)]
        rank,remainder=divmod(len(independent_basis(columns)),self.a*self.r)
        if remainder:raise AssertionError('operator rank has wrong module multiplicity')
        return rank

    def input_rank(self,u):
        orbit=[apply_binary(A,u) for A in self.input_ops]
        rank,remainder=divmod(len(independent_basis(orbit)),self.a*self.p)
        if remainder:raise AssertionError('input orbit has wrong simple-module dimension')
        return rank

    def target_projection(self):
        images=[apply_binary(A,self.y) for A in self.output_ops]
        annihilator=linear_kernel(images,self.M)
        equations=equations_from_columns(images,self.y,self.M)
        for h in annihilator:
            equations.extend(equations_from_columns([self.mul(h,1<<j)
                for j in range(self.K)],0,self.K))
        solved=affine_solutions(equations,self.K)
        if solved is None:raise AssertionError('target-image projection equations inconsistent')
        P=solved[0]
        if self.output_action(P,self.y)!=self.y or any(self.mul(h,P) for h in annihilator):
            raise AssertionError('target-image projection equations were not preserved')
        return P

    def primitive_decomposition(self,E):
        """Las Vegas primitive corners using only central Frobenius equations."""
        h=self.matrix_rank(E)
        if h==0:return []
        if h==1:return [E]
        corner=BinaryCoordinates(self.mul(E,self.mul(1<<i,E)) for i in range(self.K)).basis
        if len(corner)!=self.a*h*h:raise AssertionError('corner algebra has wrong dimension')
        center=[self.mul(E,z) for z in self.algebra['center_basis']]
        if len(independent_basis(center))!=self.a:raise AssertionError('corner center lost field degree')
        while True:
            self.stats['corner_random_trials']+=1
            A=apply_binary(corner,self.rng.getrandbits(len(corner)))
            commutative=BinaryCoordinates();power=E
            while True:
                added=False
                for z in center:
                    if commutative.insert(self.mul(z,power)) is not None:added=True
                if not added:break
                power=self.mul(power,A)
            basis=commutative.basis
            fixed=linear_kernel([self.mul(z,z)^z for z in basis],self.K)
            if len(fixed)<2:continue
            F=next((apply_binary(basis,v) for v in fixed
                if apply_binary(basis,v) not in (0,E)),None)
            if F is None:raise AssertionError('nontrivial Boolean center has no nontrivial basis idempotent')
            if self.mul(F,F)!=F or self.mul(E,F)!=F or self.mul(F,E)!=F:
                raise AssertionError('acquired corner split failed exact identity checks')
            self.stats['corner_splits']+=1
            return self.primitive_decomposition(F)+self.primitive_decomposition(E^F)

    def sample_local(self):
        if not self.population:raise ValueError('cannot sample an empty target fiber')
        draw=self.rng.randrange(self.population)
        for s,weight in self.strata:
            if draw<weight:break
            draw-=weight
        else:raise AssertionError('integer stratum draw out of range')
        Q=self.projections[s-self.k]
        while True:
            self.stats['stabilizer_trials']+=1
            A=apply_binary(self.stabilizer_basis,self.rng.getrandbits(len(self.stabilizer_basis)))
            if self.matrix_rank(A)==self.p:break
        AQ=self.mul(A,Q)
        while True:
            self.stats['full_rank_input_trials']+=1
            u=self.input_action(AQ,self.rng.getrandbits(self.U))
            if self.input_rank(u)==s:break
        columns=[sum(((u&H[j]).bit_count()%2)<<i for i,H in enumerate(self.forms))
            for j in range(self.V)]
        solved=affine_solutions(equations_from_columns(columns,self.y,self.M),self.V)
        if solved is None:raise AssertionError('sampled target-containing image gave no right factor')
        offset,kernel=solved
        if len(kernel)!=self.a*self.r*(self.d-s):
            raise AssertionError('right-factor affine kernel has wrong dimension')
        v=offset^apply_binary(kernel,self.rng.getrandbits(len(kernel)))
        if apply_binary(columns,v)!=self.y:raise AssertionError('sample does not have requested target')
        self.stats['samples']+=1
        return dict(left=u,right=v,rank=s,local_assignment=u|(v<<self.U))

    def sample(self):
        local=self.sample_local()
        x=self.split['affine_offset']^apply_binary(self.split['coordinate_columns'],local['local_assignment'])
        local['assignment']=x
        return local


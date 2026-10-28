#!/usr/bin/env python3
"""Manufacture coordinates and sample an acquired rank-one-dual Hom slice.

Unlike the counting consumer, this sampler deliberately constructs matrix
units. They are acquired with proved expected polynomial cost, never supplied.
The field is the actual binary center, without a chosen field generator.
"""
from pathlib import Path
import random,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_source_free_sampling','work_partition_free_agent',
    'work_matrix_root','work_multiprimary_audit')]
from rank_one_slice_sampler import *
from rank_one_dual_counter import acquire_rank_one_dual,rank_one_slice_target
from unsaturated_bilinear_counter import rectangular_unpack
from source_free_uniform_sampler import AcquiredProductFiberSampler,equations_from_columns
from adjoint_matrix_product_counter import unpack,independent_basis


class AcquiredCenterField:
    def __init__(self,algebra):
        self.a=algebra.a;self.q=1<<self.a;self.basis=algebra.algebra['center_basis']
        coordinates=BinaryCoordinates(self.basis);self.one=coordinates.coordinates(algebra.one)
        self.table=[[coordinates.coordinates(algebra.mul(x,y)) for y in self.basis] for x in self.basis]
    def mul(self,x,y):return apply_binary([apply_binary(row,y) for row in self.table],x)
    def power(self,x,e):
        result=self.one
        while e:
            if e&1:result=self.mul(result,x)
            x=self.mul(x,x);e>>=1
        return result
    def inv(self,x):
        if not x:raise ValueError('zero field inverse')
        return self.power(x,self.q-2)


class ManufacturedMatrixCoordinates:
    mul=AcquiredProductFiberSampler.mul
    output_action=AcquiredProductFiberSampler.output_action
    matrix_rank=AcquiredProductFiberSampler.matrix_rank
    primitive_decomposition=AcquiredProductFiberSampler.primitive_decomposition
    def __init__(self,C,rng):
        self.C=C;N=C['nucleus'];self.N=N;self.rng=rng
        self.a=N['field_degree'];self.p=N['left_matrix_rows'];self.d=N['inner_dimension']
        self.r=N['right_matrix_columns'];self.U=N['left_dimension'];self.M=N['output_dimension']
        self.algebra=N['nucleus_certificate'];self.table=self.algebra['multiplication_table']
        self.K=len(self.table);self.one=self.algebra['unit_coordinates']
        self.output_ops=[unpack(x,self.M) for x in N['nucleus_output_operators']]
        self.input_ops=[unpack(x,self.U) for x in N['nucleus_input_operators']]
        self.stats=dict(corner_random_trials=0,corner_splits=0,matrix_unit_system_constructed=True,
            field_generator_constructed=False,original_assignments_enumerated=0)
        atoms=self.primitive_decomposition(self.one)
        if len(atoms)!=self.p:raise AssertionError('wrong number of primitive matrix idempotents')
        self.e=atoms[0];self.forward=[];self.backward=[]
        for atom in atoms:
            a=next(self.mul(atom,self.mul(1<<j,self.e)) for j in range(self.K)
                if self.mul(atom,self.mul(1<<j,self.e)))
            corner=BinaryCoordinates(self.mul(self.e,self.mul(1<<j,atom)) for j in range(self.K)).basis
            images=[self.mul(x,a) for x in corner]
            solved=affine_solutions(equations_from_columns(images,self.e,self.K),len(corner))
            if solved is None or solved[1]:raise AssertionError('connecting inverse was not unique')
            b=apply_binary(corner,solved[0])
            if self.mul(b,a)!=self.e or self.mul(a,b)!=atom:raise AssertionError('matrix units do not compose')
            self.forward.append(a);self.backward.append(b)
        self.F=AcquiredCenterField(self)
        self.input_columns=self.module_coordinates(self.input_ops,self.U,self.d)
        self.output_columns=self.module_coordinates(self.output_ops,self.M,self.r)
        self.input_inverse=BinaryCoordinates(self.input_columns)
        self.output_inverse=BinaryCoordinates(self.output_columns)
        self.hom_columns=[]
        for packed in C['hom_basis']:
            H=rectangular_unpack(packed,self.M,self.U);word=0
            for j in range(self.d):
                probe=apply_binary(self.input_columns,self.F.one<<(self.a*j))
                image=self.output_inverse.coordinates(apply_binary(H,probe))
                if image>>(self.a*self.r):raise AssertionError('Hom map violates acquired matrix-unit coordinates')
                word|=image<<(self.a*self.r*j)
            self.hom_columns.append(word)
        self.hom_inverse=BinaryCoordinates(self.hom_columns)
        if len(self.hom_inverse.basis)!=self.a*self.d*self.r:
            raise AssertionError('Hom coordinate reconstruction is not bijective')
        self.right_inverse=BinaryCoordinates(C['right_embedding_columns'])
    def action(self,ops,A,v):return apply_binary([apply_binary(op,v) for op in ops],A)
    def module_coordinates(self,ops,dimension,multiplicity):
        candidates=independent_basis(self.action(ops,self.e,1<<i) for i in range(dimension))
        span=BinaryCoordinates();basis=[];Z=self.algebra['center_basis']
        for v in candidates:
            if contains(span,v):continue
            basis.append(v)
            for z in Z:span.insert(self.action(ops,z,v))
        if len(basis)!=multiplicity or len(span.basis)!=self.a*multiplicity:
            raise AssertionError('natural simple-module coordinate dimension failed')
        columns=[self.action(ops,a,self.action(ops,z,v))
            for a in self.forward for v in basis for z in Z]
        if len(BinaryCoordinates(columns).basis)!=dimension:
            raise AssertionError('manufactured full-module coordinates are not invertible')
        return columns
    def matrix(self,word,rows,columns):
        return [unpack_vector(self.F,word>>(self.a*columns*i),columns) for i in range(rows)]
    def word(self,matrix):return pack_vector(self.F,[x for row in matrix for x in row])
    def reverse_matrix(self,packed):
        D=rectangular_unpack(packed,self.U,self.M);rows=[]
        for j in range(self.r):
            probe=apply_binary(self.output_columns,self.F.one<<(self.a*j))
            image=self.input_inverse.coordinates(apply_binary(D,probe))
            if image>>(self.a*self.d):raise AssertionError('reverse Hom map violates matrix units')
            rows.append(unpack_vector(self.F,image,self.d))
        return rows


def common_vector(F,matrices,mode):
    vectors=[row for D in matrices for row in (D if mode=='row' else transpose(D))]
    v=next((x for x in vectors if any(x)),None)
    if v is None:return None
    pivot=next(i for i,x in enumerate(v) if x);inv=F.inv(v[pivot])
    for row in vectors:
        scale=F.mul(row[pivot],inv)
        if any(x!=F.mul(scale,y) for x,y in zip(row,v)):return None
    return v


class AcquiredRankOneSliceSampler:
    def __init__(self,split,certificate,target,affine_hom_offset=None,rng=None):
        begun=time.perf_counter();self.split=split;self.C=certificate;self.target=target
        # An acquired affine slice has already shifted the left input.  Its
        # native reconstruction is distinct from the polar split's initial
        # coordinates, even when the Hom offset lies outside the right image.
        if affine_hom_offset is None:
            affine_hom_offset=certificate.get('affine_hom_offset',0)
        self.offset=affine_hom_offset;self.rng=rng if rng is not None else random.SystemRandom()
        reconstruction_keys=('original_affine_input_offset','original_input_coordinate_columns')
        if any(key in certificate for key in reconstruction_keys):
            if not all(key in certificate for key in reconstruction_keys):
                raise ValueError('incomplete acquired affine input reconstruction')
            self.original_offset=certificate[reconstruction_keys[0]]
            self.original_columns=certificate[reconstruction_keys[1]]
        else:
            self.original_offset=split['affine_offset']
            self.original_columns=split['coordinate_columns']
        self.native_target_reconstruction=(affine_hom_offset==certificate.get('affine_hom_offset',0))
        checked=acquire_rank_one_dual(certificate)
        self.count=rank_one_slice_target(checked,target,affine_hom_offset)
        self.population=self.count['population'];self.stats=dict(samples=0)
        if not self.population:return
        C=certificate;N=C['nucleus'];self.coords=ManufacturedMatrixCoordinates(C,self.rng)
        Q=self.coords;F=Q.F;self.F=F;self.p=Q.p;self.d=Q.d;self.r=Q.r
        rhs=target^N['output_constant'];self.y=sum(((rhs>>i)&1)<<j for j,i in enumerate(N['output_basis_mark_indices']))
        self.Z=Q.matrix(Q.output_inverse.coordinates(self.y),self.p,self.r)
        if not C['codimension']:
            self.mode='unrestricted';self.stats['preprocessing_seconds']=time.perf_counter()-begun;return
        dual=[Q.reverse_matrix(D) for D in C['dual_reverse_matrices']]
        row=common_vector(F,dual,'row');column=common_vector(F,dual,'column')
        if row is not None:
            self.mode='row';self.change=complete_basis(F,[row],self.d)
            self.change_inverse=inverse(F,self.change);self.target_matrix=self.Z
            width=F.a*self.r
        elif column is not None:
            self.mode='column';self.change=transpose(complete_basis(F,[column],self.r),self.r)
            self.change_inverse=inverse(F,self.change);self.target_matrix=matmul(F,self.Z,self.change,self.r)
            width=F.a*self.d
        else:raise AssertionError('checked rank-one dual has neither common row nor common image')
        restrictions=[0]*C['codimension']
        for i in range(self.d):
            for j in range(self.r):
                for ell in range(F.a):
                    Y=[[0]*self.r for _ in range(self.d)];Y[i][j]=1<<ell
                    original=self.original_Y(Y);h=Q.hom_inverse.coordinates(Q.word(original))
                    phase=[(lam&h).bit_count()%2 for lam in C['right_annihilator_basis']]
                    selected=(i==0 if self.mode=='row' else j==0)
                    if not selected:
                        if any(phase):raise AssertionError('character did not reduce to its acquired row or column')
                    else:
                        bit=F.a*(j if self.mode=='row' else i)+ell
                        for k,value in enumerate(phase):restrictions[k]|=value<<bit
        equations=[(row,(lam&affine_hom_offset).bit_count()%2)
            for row,lam in zip(restrictions,C['right_annihilator_basis'])]
        solved=affine_solutions(equations,width)
        if solved is None:raise AssertionError('nonempty Hom translate has empty vector projection')
        self.T=BinaryAffine(*solved,width)
        if self.mode=='row':weights=row_constraint_categories(F,self.target_matrix,self.d,self.T)[2]
        else:weights=column_constraint_weights(F,self.target_matrix,self.d,self.T)[3]
        if sum(w for w,c in weights)!=self.population:
            raise AssertionError('independent vector-stratum count disagrees with rank-one character count')
        self.stats.update(mode=self.mode,affine_vector_dimension=len(solved[1]),
            vector_width=width,codimension=C['codimension'],preprocessing_seconds=time.perf_counter()-begun,
            coordinate_acquisition=Q.stats)
    def original_Y(self,Y):
        if self.mode=='row':return matmul(self.F,self.change_inverse,Y,self.r)
        if self.mode=='column':return matmul(self.F,Y,self.change_inverse,self.r)
        return Y
    def sample(self):
        if not self.population:raise ValueError('cannot sample an empty target fiber')
        F=self.F;Q=self.coords
        if self.mode=='row':
            X,Y,N=sample_row_restricted(F,self.target_matrix,self.d,self.T,self.rng)
            X=matmul(F,X,self.change,self.d);Y=self.original_Y(Y)
        elif self.mode=='column':
            X,Y,N=sample_column_restricted(F,self.target_matrix,self.d,self.T,self.rng)
            Y=self.original_Y(Y)
        else:X,Y=sample_product(F,self.Z,self.d,self.rng)
        if matmul(F,X,Y,self.r)!=self.Z:raise AssertionError('original product target changed')
        u=apply_binary(Q.input_columns,Q.word(X));h=Q.hom_inverse.coordinates(Q.word(Y))
        v=Q.right_inverse.coordinates(h^self.offset)
        H=rectangular_unpack(apply_binary(self.C['hom_basis'],h),Q.M,Q.U)
        if apply_binary(H,u)!=self.y:raise AssertionError('actual binary Hom evaluation disagrees')
        local=u|(v<<Q.U)
        x=self.original_offset^apply_binary(self.original_columns,local)
        self.stats['samples']+=1
        return dict(assignment=x,left=u,right=v,full_hom_coordinates=h,
            affine_hom_offset=self.offset,local_assignment=local,
            native_target_reconstruction=self.native_target_reconstruction)


#!/usr/bin/env python3
"""Exact rational cover test for antipodal Hopf contact caps.

Geometric coverage is conditional on independent contact certificates.
An uncovered direction is not a non-QC witness. No floating point is used.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from pathlib import Path
import argparse
import json

def dot(x,y):return sum(xx*yy for xx,yy in zip(x,y))
def cross(x,y):
    return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def threshold(radius_squared):
    rr=Q(radius_squared)
    assert 0<=rr<=1
    return 1-2*rr+rr*rr/2
def solve3(rows,rhs):
    cs=(cross(rows[1],rows[2]),cross(rows[2],rows[0]),cross(rows[0],rows[1]))
    det=dot(rows[0],cs[0])
    if not det:return None
    return tuple(sum(rhs[j]*cs[j][i] for j in range(3))/det for i in range(3))
def common_null(normals):
    for x,y in combinations(normals,2):
        v=cross(x,y)
        if dot(v,v):return v
    for e in [(Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(1))]:
        v=cross(normals[0],e)
        if dot(v,v):return v
    raise AssertionError('nonzero unit normal expected')
def verify_caps(patches):
    if not patches:return {'status':'NO_PATCHES','covers_sphere':False}
    normals=[]; kappas=[]
    for patch in patches:
        nn=tuple(Q(v) for v in patch['hopf_normal'])
        assert len(nn)==3 and dot(nn,nn)==1
        kk=threshold(patch['radius_squared'])
        if kk<=0:
            return {'status':'GEOMETRY_COVER_PASS','covers_sphere':True,
                    'reason':'one orbit radius covers all directions','contact_certificates_checked':False}
        normals.append(nn);kappas.append(kk)
    triples=[ids for ids in combinations(range(len(normals)),3)
             if dot(normals[ids[0]],cross(normals[ids[1]],normals[ids[2]]))]
    if not triples:
        v=common_null(normals)
        assert all(dot(nn,v)==0 for nn in normals)
        return {'status':'UNCOVERED_NULL_DIRECTION','covers_sphere':False,
                'unnormalized_direction':list(map(str,v)),'direction_norm_squared':str(dot(v,v)),
                'normalization':'v/sqrt(norm_squared)','contact_certificates_checked':False}
    vertices=set();candidates=0
    for ids in triples:
        rows=[normals[ii] for ii in ids]
        for signs in product((-1,1),repeat=3):
            candidates+=1
            vv=solve3(rows,[sign*kappas[ii] for sign,ii in zip(signs,ids)])
            assert vv is not None
            if all(abs(dot(nn,vv))<=kk for nn,kk in zip(normals,kappas)):
                vertices.add(vv)
    assert vertices
    vmax=max(vertices,key=lambda vv:dot(vv,vv))
    maxnorm=dot(vmax,vmax)
    result={'status':'GEOMETRY_COVER_PASS' if maxnorm<=1 else 'UNCOVERED_RADIAL_DIRECTION',
            'covers_sphere':maxnorm<=1,'caps':len(normals),'candidate_systems':candidates,
            'vertices':len(vertices),'maximum_vertex_norm_squared':str(maxnorm),
            'maximizing_vertex':list(map(str,vmax)),
            'thresholds':list(map(str,kappas)),'contact_certificates_checked':False}
    if maxnorm>1:
        assert all(dot(nn,vmax)**2<kk*kk*maxnorm for nn,kk in zip(normals,kappas))
        result['uncovered_direction']='maximizing_vertex/sqrt(maximum_vertex_norm_squared)'
    return result

def controls():
    axes=[(1,0,0),(0,1,0),(0,0,1)]
    half=[{'hopf_normal':list(map(str,nn)),'radius_squared':'1/4'} for nn in axes]
    quarter=[{'hopf_normal':list(map(str,nn)),'radius_squared':'1/16'} for nn in axes]
    good,bad,one=verify_caps(half),verify_caps(quarter),verify_caps(half[2:])
    assert good['covers_sphere'] and good['maximum_vertex_norm_squared']=='867/1024'
    assert not bad['covers_sphere'] and bad['maximum_vertex_norm_squared']=='604803/262144'
    assert not one['covers_sphere'] and one['status']=='UNCOVERED_NULL_DIRECTION'
    assert not verify_caps([])['covers_sphere']
    return {'three_half_radius_orbits':good,'three_quarter_radius_orbits':bad,
            'one_identity_orbit':one,'empty':verify_caps([]),
            'scope':'GEOMETRY_ONLY_CONDITIONAL_ON_VERIFIED_CONTACT_PATCHES'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,help='JSON list of independently certified patches')
    args=parser.parse_args()
    result=verify_caps(json.loads(args.input.read_text())) if args.input else controls()
    if not args.input:
        Path(__file__).with_name('COVER_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

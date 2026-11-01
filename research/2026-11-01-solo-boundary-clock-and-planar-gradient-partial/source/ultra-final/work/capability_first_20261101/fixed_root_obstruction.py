"""Exact periodic P1 geometry and feasible occurrence weights for Section 7."""
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path


def gradient(vertices):
    values = [int(x%4==0 and y%4==0) for x,y in vertices]
    (x0,y0),(x1,y1),(x2,y2)=vertices
    dx1,dy1,dx2,dy2=x1-x0,y1-y0,x2-x0,y2-y0
    det=dx1*dy2-dy1*dx2
    v1,v2=values[1]-values[0],values[2]-values[0]
    # Integer vertex coordinates are quarter-unit physical coordinates.
    return F(4*(v1*dy2-dy1*v2),det),F(4*(dx1*v2-v1*dx2),det)


def main():
    triangles=[];edge_faces=defaultdict(list);normals={}
    for x in range(4):
        for y in range(4):
            for tri in [[(x,y),(x+1,y),(x,y+1)],
                        [(x+1,y+1),(x,y+1),(x+1,y)]]:
                index=len(triangles);triangles.append((tri,gradient(tri)))
                for k,l in [(0,1),(1,2),(2,0)]:
                    u,v=tri[k],tri[l]
                    key=tuple(sorted(((u[0]%4,u[1]%4),(v[0]%4,v[1]%4))))
                    edge_faces[key].append(index)
                    normals[key]='x' if u[0]==v[0] else 'y' if u[1]==v[1] else 'd'
    assert len(triangles)==32 and len(edge_faces)==48
    assert all(len(v)==2 for v in edge_faces.values())
    assert all(sum(g[j] for _,g in triangles)==0 for j in [0,1])
    active_edge=((0,0),(0,1))
    occurrences=[];pairs=[]
    for key,faces in edge_faces.items():
        for group in {'x':[0,1],'y':[0,2],'d':[1,2]}[normals[key]]:
            pair=[]
            for face in faces:
                weight=F(1,192)
                if key==active_edge:
                    gx=triangles[face][1][0]
                    assert gx in [-4,0]
                    sign=1 if gx==-4 else -1
                    weight+=(1 if group==0 else -1)*sign*F(1,384)
                pair.append(len(occurrences))
                occurrences.append((group,face,weight))
            pairs.append(pair)
    assert len(occurrences)==192 and len(pairs)==96
    assert all(sum(occurrences[i][2] for i in pair)==F(1,96) for pair in pairs)
    assert all(sum(w for _,face,w in occurrences if face==f)==F(1,32) for f in range(32))
    assert min(w for _,_,w in occurrences)==F(1,384)
    roots=[]
    for group in range(3):
        assert sum(w for j,_,w in occurrences if j==group)==F(1,3)
        roots.append(tuple(3*sum(w*triangles[f][1][axis] for j,f,w in occurrences if j==group)
                           for axis in [0,1]))
    assert roots==[(-F(1,32),F(0)),(F(1,32),F(0)),(F(0),F(0))]
    support=[tuple(g/F(1024) for g in grad) for _,grad in triangles]
    low,high=min(g[0] for g in support),max(g[0] for g in support)
    assert roots[0][0]<low and roots[1][0]>high
    result=dict(periodic_grid=4,physical_triangles=32,physical_edges=48,
                occurrences=192,pair_constraints=96,face_constraints=32,
                all_weights_strictly_positive=True,
                submold_roots=[[str(c) for c in g] for g in roots],
                w_scale='1/1024',w_gradient_x_interval=[str(low),str(high)],
                exact_obstruction='The stated fixed submold roots are outside the convex hull of the actual target gradients.',
                scope='Obstruction to the fixed-root Section 7 construction; not a planar Morrey counterexample.')
    path=Path('outputs/capability_first_20261101/fixed_root.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

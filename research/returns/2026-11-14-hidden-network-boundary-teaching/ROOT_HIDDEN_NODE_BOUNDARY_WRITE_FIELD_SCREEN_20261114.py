"""Original conditional hidden-node learning diagnostic, no producer execution.

Six vertices: four drive/read ports, a reference, and ONE inaccessible interior
vertex. Seven positive resistors. The write law dr/dt=(pressure drop)^3, gate,
retention, sources and quasistatic assumptions are INTRODUCED, not a material.
"""
from fractions import Fraction as F
from pathlib import Path
import json

EDGES = [(0,2),(1,3),(0,5),(1,5),(2,5),(3,5),(5,4)]
PATTERNS = [(-1,-1,-1,-1),(-1,-1,-1,0),(-1,-1,-1,1),
            (-1,-1,0,-1),(-1,-1,0,0),(-1,-1,0,1),(-1,0,-1,-1)]


def write_drops(r,boundary):
    p=list(boundary)
    # Only the hidden vertex is free during writing. All five exterior ports
    # are pressure-controlled, one gauge redundant. No hidden clamp is added.
    neighbors=[0,1,2,3,4]
    g=[1/r[i] for i in range(2,7)]
    hidden=sum(x*p[j] for x,j in zip(g,neighbors))/sum(g)
    p.append(hidden)
    return [p[a]-p[b] for a,b in EDGES]


def rate(r,p):return [d**3 for d in write_drops(r,p)]


def det(a):
    a=[list(row) for row in a];out=F(1)
    for j in range(len(a)):
        k=next((k for k in range(j,len(a)) if a[k][j]),None)
        if k is None:return F(0)
        if k!=j:a[k],a[j]=a[j],a[k];out=-out
        q=a[j][j];out*=q
        for k in range(j+1,len(a)):
            f=a[k][j]/q
            for l in range(j,len(a)):a[k][l]-=f*a[j][l]
    return out


def rank(columns):
    a=[list(row) for row in zip(*columns)];i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[k],a[i]=a[i],a[k];q=a[i][j];a[i]=[x/q for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                q=a[k][j];a[k]=[x-q*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i


def solve(a,b):
    a=[list(row)+[x] for row,x in zip(a,b)]
    for j in range(len(a)):
        k=max(range(j,len(a)),key=lambda k:abs(a[k][j]));a[k],a[j]=a[j],a[k]
        q=a[j][j];a[j]=[x/q for x in a[j]]
        for k in range(len(a)):
            if k!=j:
                q=a[k][j];a[k]=[x-q*y for x,y in zip(a[k],a[j])]
    return [row[-1] for row in a]


def read_map(r):
    # Inputs0/1 and reference4 fixed, outputs2/3 plus interior5 floating.
    free=[2,3,5];matrix=[[0.0]*3 for _ in free]
    for (a,b),rr in zip(EDGES,r):
        g=1/float(rr)
        for x,y in ((a,b),(b,a)):
            if x in free:
                i=free.index(x);matrix[i][i]+=g
                if y in free:matrix[i][free.index(y)]-=g
    columns=[]
    for driven in (0,1):
        rhs=[0.0]*3
        for (a,b),rr in zip(EDGES,r):
            for x,y in ((a,b),(b,a)):
                if x in free and y==driven:rhs[free.index(x)]+=1/float(rr)
        columns.append(solve(matrix,rhs)[:2])
    return [list(row) for row in zip(*columns)]


def integrate(r,p,duration,steps):
    r=list(r);dt=duration/steps
    for _ in range(steps):
        k1=rate(r,p)
        k2=rate([x+dt*y/2 for x,y in zip(r,k1)],p)
        k3=rate([x+dt*y/2 for x,y in zip(r,k2)],p)
        k4=rate([x+dt*y for x,y in zip(r,k3)],p)
        r=[x+dt*(a+2*b+2*c+d)/6 for x,a,b,c,d in zip(r,k1,k2,k3,k4)]
        assert min(r)>0
    return r


def main():
    initial=[F(1)]*7
    fields=[[F(x) for x in q]+[F(0)] for q in PATTERNS]
    cubic_columns=[rate(initial,p) for p in fields]
    linear_columns=[write_drops(initial,p) for p in fields]
    determinant=det(list(zip(*cubic_columns)))
    assert determinant==F(4536,1953125)
    assert rank(linear_columns)==4
    assert rank(cubic_columns)==7
    v=[F(1),F(0),F(0),F(0),F(0)]
    w=[F(0),F(0),F(1),F(0),F(0)]
    old_fields=[[a+b for a,b in zip(v,w)],[-a+b for a,b in zip(v,w)],[-b for b in w]]
    first_order=[sum(t*c[e] for t,c in zip((1,1,2),[rate(initial,p) for p in old_fields])) for e in range(7)]
    assert first_order==list(map(F,[-6,0]))+[F(-96,125),F(-6,125),F(24,125),F(-6,125),F(6,125)]
    finite=[]
    for duration,steps in [(0.01,32),(0.001,8),(0.001,16),(0.001,32),(0.0001,32)]:
        r=[1.0]*7
        for p,mult in zip(old_fields,(1,1,2)):
            r=integrate(r,list(map(float,p)),duration*mult,steps)
        finite.append({"pulse_time":duration,"RK4_steps_each_phase":steps,"final_r":r,
                       "normalized_increment":[(x-1)/duration for x in r],"read_map":read_map(r)})
    refinement=max(abs(x-y) for x,y in zip(finite[1]['final_r'],finite[3]['final_r']))
    assert refinement<1e-10
    assert max(abs(x-float(y)) for x,y in zip(finite[-1]['normalized_increment'],first_order))<0.002
    result={
        "status":"INTRODUCED_MODEL_NOT_PHYSICAL_VALIDATION_OR_NOVELTY_CLAIM",
        "edges":EDGES,"ports":[0,1,2,3,4],"hidden_vertex":5,
        "initial_resistances":[1]*7,"initial_read_map":read_map(initial),
        "old_three_field_first_order_increment":list(map(str,first_order)),
        "max_unintended_increment_over_selected":float(max(abs(x) for x in first_order[1:])/6),
        "boundary_patterns_first_four_ports_reference_zero":PATTERNS,
        "linear_write_field_rank":rank(linear_columns),"cubic_write_field_rank":rank(cubic_columns),
        "exact_cubic_field_determinant":str(determinant),
        "local_consequence":"In this specified smooth positive-resistance model, seven reversible boundary vector fields span all seven state directions at the declared initial state. The inverse-function theorem gives local state reachability. This is not a global, robust, efficient or boundary-observed learning controller.",
        "finite_three_field_runs":finite,"RK4_refinement_max_state_difference":refinement,
        "limitations":["The previous exact edge-selective pulse construction leaks into hidden edges even with only one interior node.","Full frozen-state rank is a constructive opening, not proof of global teachability or useful-function training under noise.","The seven field vectors are evaluated at known simulator state; no hidden state is granted to a physical controller.","Known reversible cubic adaptation and a global mode gate are assumptions, not qualified memory, rheology, valves, mechanics or sensors.","No write-state potential, complete source work, rate calibration, finite-bandwidth plant, fabrication, life, scalability or whole-system advantage is supplied.","One graph and initial state do not prove a family-level physical principle or establish90-level scientific consequence."],
    }
    output=Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"output":str(output),"hidden_leak_ratio":result['max_unintended_increment_over_selected'],
                      "linear_rank":result['linear_write_field_rank'],"cubic_rank":result['cubic_write_field_rank'],
                      "determinant":str(determinant),"refinement_max_error":refinement},indent=2))


if __name__=='__main__':main()

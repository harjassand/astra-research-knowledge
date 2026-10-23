"""Exact low-rank proposal, input-error bridge, and actual-input witness."""
from fractions import Fraction as F
from exact_ops import action,frob2,rotate,core_graph,core_rows


def build(local_builder,M=96,N=2,epsilon=F(1,1000)):
    n0,edges=core_graph(2,6); q=5; X=core_rows(n0,q)
    X[1]=rotate([F(1),F(0),F(0),F(0),F(0)])
    selected=None; Ylocal=None; original_local=None
    c=(1-epsilon*epsilon)/(1+epsilon*epsilon); ss=2*epsilon/(1+epsilon*epsilon)
    for v in range(1,n0):
        for rep in range(N):
            ids=list(range(len(X),len(X)+M)); edges.update((v,i) for i in ids)
            edges.update((ids[j],ids[j+1]) for j in range(M-1))
            if v==1:
                small=[[F(1),F(0),F(0)]]
                original=[X[v]]
                for j in range(M):
                    z=([F(1),F(0)],[F(0),F(1)],[F(3,5),F(4,5)])[j%3]
                    small.append([F(0),c*z[0],c*z[1]])
                    r=rotate([F(0),c*z[0],c*z[1],ss,F(0)])
                    X.append(r);original.append(r)
                if selected is None:selected=[v]+ids;Ylocal=small;original_local=original
            else:X.extend(core_rows(M,q))
    local=local_builder(Ylocal,1)
    kind='flow' if local['flow_ratio_squared']>=local['local_ratio_squared'] else 'local'
    B=local[kind+'_entries']; D={tuple(sorted((selected[i],selected[j]))):a for (i,j),a in B.items() if a}
    Y=action(len(X),q,D,X); A2=frob2(Y)
    projected=[rotate(r+[F(0),F(0)]) for r in Ylocal]
    delta=[[a-b for a,b in zip(x,y)] for x,y in zip(original_local,projected)]
    E2=frob2(delta)
    projected_action=action(M+1,q,B,projected)
    perturb_action=action(M+1,q,B,delta)
    Bf2=sum((1 if i==j else 2)*a*a for (i,j),a in B.items())
    assert frob2(perturb_action)<=Bf2*E2
    op2=local[kind+'_operator_lower_squared'] if kind=='flow' else local['local_operator_squared']
    return {'schema':'astra.cone_core_witness.v1','kind':'low_projection',
      'n':len(X),'q':q,'edges':sorted(edges),'X':X,'D':D,
      'selected_vertices':selected,'projected_rows':projected,
      'projection_error_squared':E2,'projected_action_squared':frob2(projected_action),
      'perturbation_action_squared':frob2(perturb_action),'local_frobenius_squared':Bf2,
      'parameters':{'M':M,'N':N,'epsilon':epsilon},'local_witness_kind':kind,
      'action_squared':A2,'operator_lower_squared':op2,'ratio_lower_squared':op2/A2}

"""Independent exact contact audit with boundary-only labeled source controls.

Each replica has the SAME unknown bulk clockwise/counterclockwise rates u,v.
Only its gateway motion, boundary injection/removal, and common contact strength
are controlled. Particles are not hard-core here: co-location triggers a uniform
reaction removing both particles. Reaction events may be marked/observed.
"""
import itertools, json
import sympy as s

u,v=s.symbols('u v',positive=True)
A1,B1,A2,B2,alpha1,beta1,alpha2,beta2,kappa=s.symbols(
    'A1 B1 A2 B2 alpha1 beta1 alpha2 beta2 kappa',nonnegative=True)
m=3;n=m+2

def single(A,B):
    Q=s.zeros(n)
    Q[0,1]=A;Q[1,0]=B
    for i in range(2,n):
        Q[1,i]=Q[i,1]=1
        Q[i,2+(i-2+1)%m]=u
        Q[i,2+(i-2-1)%m]=v
    for i in range(n):Q[i,i]=-sum(Q.row(i))
    return Q

positions=list(range(-1,n)) # -1 denotes absence, not a hidden physical site.
states=list(itertools.product(positions,repeat=2));idx={z:i for i,z in enumerate(states)}
L=s.zeros(len(states));reaction=s.zeros(len(states));Q=[single(A1,B1),single(A2,B2)]
for znum,z in enumerate(states):
    for p in range(2):
        i=z[p]
        if i==-1:
            w=list(z);w[p]=0;L[znum,idx[tuple(w)]] += [alpha1,alpha2][p]
        else:
            for j in range(n):
                if j==i:continue
                w=list(z);w[p]=j;L[znum,idx[tuple(w)]] += Q[p][i,j]
            if i==0:
                w=list(z);w[p]=-1;L[znum,idx[tuple(w)]] += [beta1,beta2][p]
    if z[0]==z[1] and z[0]>=0:
        reaction[znum,idx[(-1,-1)]]=kappa
        reaction[znum,znum]=-kappa
    L[znum,znum]=-sum(L.row(znum))

labels=[]
for i,j in states:
    if i<2 and j<2:c=('outside',i,j)
    elif i<2:c=('left',i)
    elif j<2:c=('right',j)
    else:c=('both',(j-i)%m)
    labels.append(c)
classes=list(dict.fromkeys(labels));P=s.zeros(len(states),len(classes))
for i,c in enumerate(labels):P[i,classes.index(c)]=1
representatives=[labels.index(c) for c in classes]
checks={};quotients={}
for name,M in [('motion_and_boundary_sources',L),('marked_contact_reaction',reaction)]:
    MP=M*P;MB=MP[representatives,:]
    assert (MP-P*MB).applyfunc(s.simplify)==s.zeros(*MP.shape)
    assert (MB.diff(u)-MB.diff(v)).applyfunc(s.simplify)==s.zeros(*MB.shape)
    assert M*s.ones(M.rows,1)==s.zeros(M.rows,1)
    assert MB.subs({u:1,v:1})==MB.subs({u:s.Rational(19,10),v:s.Rational(1,10)})
    checks[name]='PASS'
    quotients[name]=[[str(s.factor(x)) for x in MB.row(i)] for i in range(MB.rows)]

# Extra output marks at the physical boundary: injection, removal, and each
# particle's jumps across the sole gateway edge. Marked transition kernels
# (offdiagonals only) must separately preserve the same quotient.
for p in range(2):
    for old,new,rate,kind in [(-1,0,[alpha1,alpha2][p],'injection'),
                             (0,-1,[beta1,beta2][p],'removal'),
                             (0,1,[A1,A2][p],'gateway_departure'),
                             (1,0,[B1,B2][p],'gateway_return')]:
        J=s.zeros(len(states))
        for a,z in enumerate(states):
            if z[p]==old:
                w=list(z);w[p]=new;J[a,idx[tuple(w)]]=rate
        JP=J*P;JB=JP[representatives,:]
        assert JP==P*JB
        checks[f'replica_{p+1}_{kind}_mark']='PASS'
# Reaction-jump-only kernel and no-reaction killed generator also intertwine.
J=s.zeros(len(states))
for a,z in enumerate(states):
    if z[0]==z[1] and z[0]>=0:J[a,idx[(-1,-1)]]=kappa
assert J*P==P*(J*P)[representatives,:]
checks['reaction_jump_mark']='PASS'
observations=[(int(i==0),int(j==0)) for i,j in states]
for c in classes:assert len({observations[a] for a,z in enumerate(labels) if z==c})==1
checks['labeled_boundary_occupancy_factors_through_partition']='PASS'

print(json.dumps({'full_state_count':len(states),'quotient_state_count':len(classes),
'common_bulk_rates':['u','v'],'controls':['A1','B1','A2','B2','alpha1','beta1','alpha2','beta2','kappa'],
'initial_condition':'both absent; alternatively any common projected initial law',
'checks':checks,'quotient_labels':classes,'quotient_generators':quotients,
'scope':'same unknown bulk rates on both replicas; no interior addressing or independent bulk clock control; full boundary/reaction event records and nonexplosive nonanticipating boundary feedback'},indent=2))

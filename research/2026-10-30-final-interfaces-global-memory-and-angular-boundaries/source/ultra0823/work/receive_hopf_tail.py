
def univar(p):
    out={}
    for e,c in p.items():
        if e[2] or e[3]:continue
        out[e[1]]=out.get(e[1],R(0))+c/4
    return {(e,):c for e,c in out.items() if c}

def determinant_poly(matrix):
    from itertools import permutations
    n=len(matrix);ans={}
    for perm in permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term={(0,):R(sign)}
        for i,j in enumerate(perm):term=mul(term,matrix[i][j])
        ans=add(ans,term)
    return ans

def primitive_univar(p):
    from math import gcd
    if not p:return {}
    den=lcm(*(c.denominator for c in p.values()));g=0
    vals={e:int(c*den) for e,c in p.items()}
    for c in vals.values():g=gcd(g,abs(c))
    return {e:R(c//g) for e,c in vals.items()}

def polynomial_rem(p,q):
    p=dict(p);dq=max(e[0] for e in q);lq=q[dq,]
    while p and max(e[0] for e in p)>=dq:
        dp=max(e[0] for e in p);co=p[dp,]/lq
        for (j,),v in q.items():
            key=(dp-dq+j,);p[key]=p.get(key,R(0))-co*v
            if not p[key]:del p[key]
    return p

def root_count(p):
    seq=[primitive_univar(p),primitive_univar(diff(p,0))]
    while seq[-1]:
        rem=primitive_univar(scale(polynomial_rem(seq[-2],seq[-1]),-1))
        if not rem:break
        seq.append(rem)
    def variations(infinity):
        signs=[]
        for pp in seq:
            degree=max(e[0] for e in pp);co=pp[degree,]
            signs.append((1 if co>0 else -1)*(-1 if infinity<0 and degree%2 else 1))
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variations(-1)-variations(1)

def rank(matrix):
    a=[list(row) for row in matrix];i=0
    for j in range(len(a[0])):
        pivot=next((k for k in range(i,len(a)) if a[k][j]),None)
        if pivot is None:continue
        a[i],a[pivot]=a[pivot],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i

def evaluate(poly,point):return sum((co*__import__('math').prod(x**e for x,e in zip(point,pw)) for pw,co in poly.items()),R(0))

def main():
    start=time.perf_counter();cert=json.loads((HERE/'certificate.json').read_text());ray=cert['ray'];K=list(map(R,ray['K_coefficients']))
    A=[var(4,i) for i in range(4)];T=add(*(mul(x,x) for x in A));T2=mul(T,T)
    X=add(mul(A[0],A[0]),mul(A[2],A[2]),scale(mul(A[1],A[1]),-1),scale(mul(A[3],A[3]),-1))
    Y=scale(add(mul(A[0],A[1]),mul(A[2],A[3])),2)
    Z=scale(add(mul(A[0],A[3]),scale(mul(A[1],A[2]),-1)),2)
    forms=[mul(X,X),scale(mul(X,Y),2),scale(mul(X,Z),2),mul(Y,Y),scale(mul(Y,Z),2),mul(Z,Z)]
    F=add(*(scale(f,k) for f,k in zip(forms,K)));HF=[[diff(diff(F,i),j) for j in range(4)] for i in range(4)]
    HR=[[univar(p) for p in row] for row in HF];signs=[]
    for size in range(1,5):
        pp=determinant_poly([row[:size] for row in HR[:size]]);power=min(e[0] for e in pp)
        rest={(e[0]-power,):c for e,c in pp.items()}
        assert power%2==0 and root_count(rest)==0 and rest.get((0,),0)>0
        signs.append({'minor':size,'zero_power':power,'remaining_degree':max(e[0] for e in rest)})
    assert [s['zero_power'] for s in signs]==[0,0,0,2]
    A0=list(map(R,ray['A0']));Hbasis=[[[univar(diff(diff(f,i),j)) for j in range(4)] for i in range(4)] for f in forms]
    face=[]
    for i in range(4):face.append([sum(HB[i][j].get((0,),R(0))*A0[j] for j in range(4)) for HB in Hbasis])
    face.append([sum(A0[i]*HB[i][j].get((1,),R(0))*A0[j] for i in range(4) for j in range(4)) for HB in Hbasis])
    assert rank(face)==5 and all(sum(x*k for x,k in zip(row,K))==0 for row in face)
    u,l,p,n,q,r=K;assert l*(p*p-q*q)+(n-u)*p*q!=0
    normal=[literal(x,3) for x in cert['normal_form']];av=[var(3,i) for i in range(3)]+[{(0,0,0):R(1)}]
    for i in range(5):
        row=[]
        for HB in Hbasis:
            if i<4:row.append(add(*(scale(av[j],HB[i][j].get((0,),R(0))) for j in range(4))))
            else:row.append(add(*(scale(mul(av[k],av[j]),HB[k][j].get((1,),R(0))) for k in range(4) for j in range(4))))
        assert not add(*(mul(x,y) for x,y in zip(row,normal)))
    nv=[evaluate(x,A0[:3]) for x in normal];ratio=K[0]/nv[0];assert [x*ratio for x in nv]==K
    jac=[[evaluate(diff(normal[i],j),A0[:3]) for j in range(3)] for i in range(6)]
    nu,nl,np_,nn,nq,nr=nv;rotation=[-2*nl,nu-nn,-nq,2*nl,np_,0]
    assert rank([row+[rotation[i],nv[i]] for i,row in enumerate(jac)])==5
    P=[literal(x,4) for x in cert['primitive']];Gamma=(3,2,1,0);sgn=(1,-1,1,-1)
    JA=[scale(A[2],-1),scale(A[3],-1),A[0],A[1]]
    def symmetries(pp):
        jt=[pp[2],pp[3],scale(pp[0],-1),scale(pp[1],-1)]
        for i in range(4):
            assert not add(*(mul(diff(pp[i],j),JA[j]) for j in range(4)),jt[i])
            assert not add(transform(pp[i],Gamma,sgn),scale(pp[Gamma[i]],-sgn[i]))
    symmetries(P)
    profile=list(map(lambda n:R(cert['profile_coefficients'][n]),cert['profile_variables']));pb=[]
    for k in range(len(profile)):
        pp=[]
        for component in cert['primitive_basis']:
            poly={}
            for row in component:
                co=sum((R(n,dd) for idx,n,dd in row['weights'] if idx==k),R(0))
                if co:poly[tuple(row['powers'])]=co
            pp.append(poly)
        symmetries(pp);pb.append(pp)
    assert all(P[i]==add(*(scale(pp[i],co) for pp,co in zip(pb,profile))) for i in range(4))
    def omega(pp):
        W=[[{} for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(i+1,4):
                W[i][j]=add(mul(T,add(diff(pp[j],i),scale(diff(pp[i],j),-1))),scale(add(mul(A[i],pp[j]),scale(mul(A[j],pp[i]),-1)),-2));W[j][i]=scale(W[i][j],-1)
        return W
    jet=[[evaluate(omega(pp)[0][j],A0)/2 for pp in pb] for j in (1,2,3)]
    assert rank([[row[j] for j in cert['dependent_indices']] for row in jet])==3
    W=omega(P);C=[[{} for _ in range(6)] for _ in range(6)];p1=(0,1,3,4);p2=(1,2,4,5)
    for mapping in (p1,p2):
        for i in range(4):
            for j in range(4):C[mapping[i]][mapping[j]]=add(C[mapping[i]][mapping[j]],mul(T2,HF[i][j]))
    for i in range(4):
        for j in range(4):
            term=scale(W[i][j],R(1,2));C[p1[i]][p2[j]]=add(C[p1[i]][p2[j]],term);C[p2[j]][p1[i]]=add(C[p2[j]][p1[i]],term)
    assert all(evaluate(C[i][0],A0)==0 for i in range(6))
    C=[[contract(x) for x in row] for row in C];assert C==[[literal(x,2) for x in row] for row in cert['C']]
    perm=cert['permutation'];C=[[C[i][j] for j in perm] for i in perm]
    assert C==[[literal(x,2) for x in row] for row in cert['C_permuted']]
    M=[[literal(x,2) for x in row] for row in cert['M']];kk=[literal(x,2) for x in cert['kernel']];w=literal(cert['w'],2);g=literal(cert['g'],2)
    assert kk[0]=={(0,0):R(1)} and M==[list(row) for row in zip(*M)]
    cp=add(*(mul(mul(kk[i],C[i][j]),kk[j]) for i in range(6) for j in range(6)))
    assert cp==add(mul(mul(w,w),M[0][0]),scale(mul(mul(w,g),M[0][1]),2),mul(mul(g,g),M[1][1]))
    for j in range(1,6):
        assert add(*(mul(kk[i],C[i][j]) for i in range(6)))==add(mul(w,M[0][j+1]),mul(g,M[1][j+1]))
        for i in range(1,6):assert C[i][j]==M[i+1][j+1]
    local=tuple(map(R,cert['cover']['local_box']));count=bernstein_signs(M,local);boxes=[];area=R(0)
    for leaf in cert['cover']['leaves']:
        box=tuple(map(R,leaf['box']));a,b,c,d=box;assert -1<=a<b<=1 and -1<=c<d<=1
        for aa,bb,cc,dd in boxes:assert min(b,bb)<=max(a,aa) or min(d,dd)<=max(c,cc)
        boxes.append(box);area+=(b-a)*(d-c)
        if leaf['proof']=='M':assert a>=local[0] and b<=local[1] and c>=local[2] and d<=local[3]
        else:assert leaf['proof']=='C';count+=bernstein_signs(C,box)
    assert area==4
    base=list(map(R,ray['support_A']));bounds=[]
    for key in ('support_Rplus','support_Rminus'):
        rr=list(map(R,ray[key]));det=rr[0]*rr[3]-rr[1]*rr[2];assert det>0 if key.endswith('Rplus') else det<0
        c0,c1,c2,_,_=line_coefficients(F,rr,base);assert c0>0;bounds.append((c2-c1*c1/(4*c0))/det)
    assert bounds[1]>bounds[0]
    result={'ROC_global_exact':True,'exposed_face_rank':5,'nonaligned':True,'nonpc_exact':True,
      'normal_form_identity':True,'boundary_parameterization_rank':5,'angular_jet_rank':3,
      'primitive_terms':sum(len(x) for x in P),'density_and_Gamma_symmetry_exact':True,'lift_identity_exact':True,
      'cover_rectangles':len(boxes),'positive_Bernstein_matrices':count,'seconds':time.perf_counter()-start,
      'scope':'Internal exact finite certificate. The local six-dimensional ROC/QC equivalence uses the analytic continuation argument in PROOF.txt.'}
    print(json.dumps(result,indent=2));(HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()

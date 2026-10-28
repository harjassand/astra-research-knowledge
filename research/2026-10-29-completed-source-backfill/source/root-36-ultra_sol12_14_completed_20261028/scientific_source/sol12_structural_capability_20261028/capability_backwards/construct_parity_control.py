"""Exact moderate-flip parity control for the frozen five-letter target.

Skew detailed balance is prior machinery. The tested new scoped statement is
full five-letter invariance, with explicit ordinary/10-state controls.
No physical thermodynamic realization or stationary experiment is inferred.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product,permutations
import json,math,time
START=time.monotonic()
import numpy as np
OUT=Path(__file__).resolve().parent
src=json.loads((OUT/'sources/seed_certificate.json').read_text())
QQ=[[F(x) for x in row] for row in src['Q']];P=[[F(i==j)+x/2 for j,x in enumerate(row)] for i,row in enumerate(QQ)]
H=[[F(x) for x in row] for row in src['H']];LL=[[F(x) for x in row] for row in src['L']]
LABEL=[0]*5+list(range(1,6));DELTA=F(1,10)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def mm(a,b):return [[dot(row,col) for col in zip(*b)] for row in a]
def transpose(a):return [list(x) for x in zip(*a)]
def solve(a,b):
    a=[list(row)+[v] for row,v in zip(a,b)];n=len(a)
    for k in range(n):
        j=next(i for i in range(k,n) if a[i][k]);a[k],a[j]=a[j],a[k];div=a[k][k];a[k]=[v/div for v in a[k]]
        for i in range(n):
            if i!=k:
                v=a[i][k];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
    return [row[-1] for row in a]
def rowsum(a):return [sum(row,F(0)) for row in a]
assert rowsum(P)==[1]*10 and rowsum(transpose(P))==[1]*10
assert min(x for row in P for x in row)>=0
PT=transpose(P)
for letter in range(6):
    v=[F(x==letter) for x in LABEL]
    assert [dot(row,v) for row in P]==[dot(row,v) for row in PT]
assert mm(QQ,H)==mm(H,LL)
M=mm(transpose(H),H)
M=[[x/10 for x in row] for row in M]
assert mm(M,LL)==mm(transpose(LL),M)
assert M==[[F(x) for x in row] for row in src['M']]
for letter in range(6):
    diagonal=[int(j<3) if letter==0 else int(j==letter+2) for j in range(8)]
    assert [[F(LABEL[i]==letter)*H[i][j] for j in range(8)] for i in range(10)]==[[H[i][j]*diagonal[j] for j in range(8)] for i in range(10)]
assert all(dot(row,[1,0,0,1,1,1,1,1])==1 for row in H)
def original_parities():
    valid=[];checked=0
    for pp in permutations(range(5)):
        theta=list(pp)+list(range(5,10))
        if any(theta[theta[i]]!=i for i in range(10)):continue
        checked+=1
        if all(P[i][j]==P[theta[j]][theta[i]] for i in range(10) for j in range(10)):valid.append(theta)
    signatures=[tuple(row[5:]) for row in P[:5]]
    assert len(set(signatures))==5
    assert all(P[i][j]==P[j][i] for i in range(5) for j in range(5,10))
    assert P!=PT and not valid
    return {'within_emission_permutations':120,'involutions_checked':checked,'valid_involutions':valid,
            'distinct_marker_signatures':5,'scope':'Frozen10-state representation only; no20-state minimality claim.'}

DEN=2*math.lcm(*(x.denominator for row in P for x in row),10)
IP=np.asarray([[int(x*DEN) for x in row] for row in P],dtype=object)
IA=np.asarray([[(int(P[i][j]*DEN)+int(P[j][i]*DEN))//2 for j in range(10)] for i in range(10)],dtype=object)
IR=np.zeros((20,20),dtype=object);df=int(DELTA*DEN)
for i in range(10):
    for j in range(10):IR[i,j]=IP[i,j];IR[i+10,j+10]=IP[j,i]
    IR[i,i]-=df;IR[i+10,i+10]-=df;IR[i,i+10]=IR[i+10,i]=df
assert min(IR.flat)>=0 and all(sum(row)==DEN for row in IR)
assert all(sum(IR[:,j])==DEN for j in range(20))
theta=list(range(10,20))+list(range(10))
assert all(IR[i,j]==IR[theta[j],theta[i]] for i in range(20) for j in range(20))

def word_table(matrix,labels,length=5):
    current={(a,):np.asarray([int(x==a) for x in labels],dtype=object) for a in range(6)}
    masks=[[i for i,x in enumerate(labels) if x==a] for a in range(6)]
    for step in range(1,length):
        nxt={}
        for word,vec in current.items():
            advanced=vec@matrix
            for a,indices in enumerate(masks):
                vv=np.zeros(len(labels),dtype=object)
                for i in indices:vv[i]=advanced[i]
                if any(vv):nxt[word+(a,)]=vv
        current=nxt
    counts={w:int(sum(v)) for w,v in current.items()}
    assert sum(counts.values())==len(labels)*DEN**(length-1)
    return counts,current

def count_word(matrix,labels,word):
    vec=np.asarray([int(x==word[0]) for x in labels],dtype=object)
    for a in word[1:]:
        vec=vec@matrix
        vec=np.asarray([v if x==a else 0 for v,x in zip(vec,labels)],dtype=object)
    return int(sum(vec))

def feature_data():
    e=F(1,2);eta=F(1,10);facets=[[F(x) for x in row] for row in src['facets']]
    av=[e*eta*r[0] for r in facets];NN=[[e*eta*x for x in row[1:]] for row in facets]
    nt=transpose(NN);gram=mm(nt,NN);inv=[[gram[1][1],-gram[0][1]],[-gram[1][0],gram[0][0]]]
    determinant=gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0];inv=[[x/determinant for x in row] for row in inv]
    CC=mm(inv,nt);assert mm(CC,NN)==[[1,0],[0,1]]
    K=transpose([[F(i==j)+e*x for j,x in enumerate(row)] for i,row in enumerate(LL)])
    data={}
    for a,b in product(range(6),repeat=2):
        i0=int(a==0);psi=[F(i0*(b==k+1)) for k in range(5)];rr=[x-y*i0 for x,y in zip(psi,av)]
        xy=[dot(row,rr) for row in CC];dd=[x-y for x,y in zip(rr,[dot(row,xy) for row in NN])]
        ff=[F(i0)]+xy+[F(a==k+1) for k in range(5)]
        data[a,b]=(ff,dd)
    # Literal shifted monotone-field interpolation, no source coefficient copy.
    zz=[[F(x) for x in row] for row in src['farkas_z']];points=[[F(x) for x in row] for row in src['points']]
    rhs=[]
    for point,field,xi in zip(points,zz,H[:5]):
        ztilde=[field[0]-F(4,5),field[1]];tt=dot(ztilde,point)
        Z=[-5*tt/6]+ztilde+[tt/6]*5
        drift=[x-dot(row,xi) for x,row in zip(xi,K)];rhs.append(dot(Z,drift))
    coeff=solve([[1,x,y,x*x,x*y] for x,y in points],rhs)
    source_check=json.loads((OUT/'sources/source_seed_check.json').read_text())
    assert coeff==[F(x)/2 for x in source_check['shifted_interpolation']['qcoeff_exact']]
    return data,K,coeff

def witness_values(data,K,qq):
    alpha,beta=F(3,2000),F(1,250000);Lambda=F(316808000,3);Mu=F(90000);circle=F(664,75)
    out={}
    for word in product(range(6),repeat=5):
        left2,left,center,right,right2=word
        fp,dp=data[center,right];fm,dm=data[center,left]
        gp=[a-b for a,b in zip(data[right,right2][0],[dot(row,fp) for row in K])]
        gm=[a-b for a,b in zip(data[left,left2][0],[dot(row,fm) for row in K])]
        i0=F(center==0);s2=fm[1]*fp[1]+fm[2]*fp[2]
        sq=qq[0]*i0+qq[1]*(fm[1]+fp[1])/2+qq[2]*(fm[2]+fp[2])/2+qq[3]*fm[1]*fp[1]+qq[4]*(fm[1]*fp[2]+fm[2]*fp[1])/2
        out[word]=sq+circle*(i0-s2)+alpha*(i0+s2)+beta*i0+Lambda*dot(dm,dp)+Mu*dot(gm,gp)
    return out

def main():
    phases={};start=time.monotonic();parities=original_parities();phases['parity_search']=time.monotonic()-start
    # Rank8 and self-adjoint observable restriction are exact input checks.
    solve(M,[F(0)]*8)
    start=time.monotonic();p5,pstates=word_table(IP,LABEL);r5,rstates=word_table(IR,LABEL*2);a5,_=word_table(IA,LABEL)
    words=list(product(range(6),repeat=5))
    assert all(2*p5.get(w,0)==r5.get(w,0) for w in words)
    assert all(p5.get(w,0)==p5.get(w[::-1],0) for w in words)
    assert all(r5.get(w,0)==r5.get(w[::-1],0) for w in words)
    tvA=F(sum(abs(p5.get(w,0)-a5.get(w,0)) for w in words),20*DEN**4)
    phases['three_complete_five_word_tables']=time.monotonic()-start
    print(json.dumps({'stage':'ALL7776_WORDS_EXACTLY_EQUAL','ordinary_reversiblization_TV':float(tvA),'seconds':phases['three_complete_five_word_tables']}),flush=True)
    start=time.monotonic();data,K,qcoef=feature_data()
    for i in range(10):
        expected=[sum((P[i][j]*data[LABEL[i],LABEL[j]][0][k] for j in range(10)),F(0)) for k in range(8)]
        assert expected==H[i]
    ww=witness_values(data,K,qcoef);wd=math.lcm(*(x.denominator for x in ww.values()));wi={w:int(x*wd) for w,x in ww.items()}
    means=[];seconds=[]
    for counts,n in [(p5,10),(r5,20),(a5,10)]:
        mean=F(sum(wi[w]*counts.get(w,0) for w in words),wd*n*DEN**4)
        second=F(sum(wi[w]**2*counts.get(w,0) for w in words),wd*wd*n*DEN**4)
        means.append(mean);seconds.append(second)
    expected=F(src['farkas_drift_pairing'])/4+F(3,2000)+F(1,500000)
    assert means[0]==means[1]==expected<0 and means[2]>=0
    assert seconds[0]==seconds[1]
    assert min(ww.values())>=-29000000 and max(ww.values())<=81000000
    phases['literal_witness_all_word_values_and_means']=time.monotonic()-start
    start=time.monotonic();longer=None;checked=0
    for pref in words:
        pv=pstates.get(pref,np.zeros(10,dtype=object))@IP
        rv=rstates.get(pref,np.zeros(20,dtype=object))@IR
        for letter in range(6):
            checked+=1;cp=sum(v for v,l in zip(pv,LABEL) if l==letter);cr=sum(v for v,l in zip(rv,LABEL*2) if l==letter)
            if 2*cp!=cr:
                longer={'word':pref+(letter,),'target_probability':str(F(int(cp),10*DEN**5)),
                        'lift_probability':str(F(int(cr),20*DEN**5)),
                        'difference_lift_minus_target':str(F(int(cr-2*cp),20*DEN**5))};break
        if longer:break
    assert longer is not None
    phases['first_six_word_difference_search']=time.monotonic()-start
    start=time.monotonic();cube=IR@IR@IR;minimum=min(cube.flat);assert minimum>0
    beta=F(20*int(minimum),DEN**3);k=(5*beta.denominator+beta.numerator-1)//beta.numerator
    mixing={'three_step_Doeblin_beta':str(beta),'display_beta':float(beta),'certified_TV_001_steps':3*k,
            'bound':'TV<= (1-beta)^floor(t/3); 3ceil(5/beta) suffices because exp(5)>100.',
            'orientation_eigenvalue':str(1-2*DELTA),'physical_preparation_acquired':False}
    phases['mixing_minorization']=time.monotonic()-start
    inputs={'denominator':DEN,'target_numerators':IP.tolist(),'parity_lift_numerators':IR.tolist(),
            'ordinary_reversiblization_numerators':IA.tolist(),'target_labels':LABEL,'lift_labels':LABEL*2,
            'parity_involution':theta,'delta':str(DELTA),'target_stationary_denominator':10,'lift_stationary_denominator':20}
    (OUT/'EXACT_MATRICES.json').write_text(json.dumps(inputs,indent=2)+'\n')
    result={'status':'EXACT_MODERATE_FLIP_FIVE_WORD_CONTROL_ACQUIRED','source_pin':'8d51d60762b3ee28c10aaaa56e1b92da119dc1cc',
            'original_parity_search':parities,'delta':str(DELTA),'matrix_sizes':[10,20,10],
            'five_word_entries_compared':len(words),'positive_word_counts':[len(p5),len(r5),len(a5)],
            'maximum_five_word_difference':'0','all_five_word_reversal_checks':'EXACT',
            'emission_indicator_annihilation':'EXACT_(P-P*)g_y_ZERO',
            'observable_restriction_checks':'QH=HL; M=H^T H/10; ML=L^T M; emission invariance; rank8',
            'parity_detailed_balance':'EXACT_ALL400_ENTRIES','parity_path_KL_exact':'0',
            'physical_entropy_production':'NOT_IDENTIFIED_FROM_PARITY_SYMMETRY_ALONE',
            'ordinary_control_five_word_TV':str(tvA),'display_ordinary_control_TV':float(tvA),
            'witness_means':list(map(str,means)),'display_witness_means':list(map(float,means)),
            'witness_second_moments':list(map(str,seconds)),'witness_range':[str(min(ww.values())),str(max(ww.values()))],
            'longer_word_difference':longer,'longer_word_candidates_checked':checked,
            'mixing':mixing,'phases_seconds':phases,'module_seconds':time.monotonic()-START,
            'scope':'Constructive input-model comparator, not a new lifting algorithm or a physical equilibrium realization. '
                    'N541 even-hidden null remains unchanged. All5-letter laws match exactly; full laws differ at6 letters. '
                    'No20-state minimality claim, experimental data, physical parity or preparation acquisition.'}
    (OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','display_witness_means','maximum_five_word_difference','longer_word_candidates_checked','module_seconds']},indent=2),flush=True)

if __name__=='__main__':main()

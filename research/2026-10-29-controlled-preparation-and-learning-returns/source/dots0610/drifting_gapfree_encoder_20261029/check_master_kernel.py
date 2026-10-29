from fractions import Fraction as F
import random,json,math
rng=random.Random(2026102906);T=48;H=3;M=3;p=F(1,2);eta0=F(1,16)
eta=[F(1,8),F(1,16),F(1,32)];share=[F(0),F(1,8),F(1,16)]
bw=[[F(1,M)]*M for _ in range(H)];mw=[F(1,H)]*H
master_loss=F(0);base_loss=[F(0)]*H;base_sq=[F(0)]*H;max_bits=0
for t in range(T):
 # One common signed-record feedback represented after its [0,1] shift.
 obs=[F(rng.randrange(13),12) for _ in range(M)];active=rng.randrange(2)==0
 l=[v/p if active else F(0) for v in obs]
 ml=[sum(bw[b][j]*l[j] for j in range(M)) for b in range(H)]
 master_loss+=sum(mw[b]*ml[b] for b in range(H))
 for b in range(H):base_loss[b]+=ml[b];base_sq[b]+=ml[b]**2
 nm=[mw[b]*(1-eta0*ml[b]) for b in range(H)];normal=sum(nm);mw=[x/normal for x in nm]
 for b in range(H):
  tmp=[bw[b][j]*(1-eta[b]*l[j]) for j in range(M)];ss=sum(tmp)
  bw[b]=[(1-share[b])*x/ss+share[b]/M for x in tmp]
 for x in mw:max_bits=max(max_bits,x.numerator.bit_length(),x.denominator.bit_length())
 assert sum(mw)==1 and all(sum(v)==1 for v in bw)
res=[]
for b in range(H):
 lhs=float(master_loss-base_loss[b]);rhs=math.log(H)/float(eta0)+float(eta0*base_sq[b]);assert lhs<=rhs+1e-12
 res.append(dict(base=b,estimated_master_regret=lhs,pathwise_bound=rhs))
# Exact one-attempt rejection counts expose why prefetch is required.
# Master chooses A/B equally; A has total2 (always accepts), B total3 (accepts3/4).
naive_A=F(1,2)/(F(1,2)+F(1,2)*F(3,4));prefetch_A=F(1,2)*F(3,4)/F(3,4)
assert naive_A==F(4,7) and prefetch_A==F(1,2)
result=dict(T=T,bases=H,master_weight_max_bits=max_bits,exact_normalization_checks=T*(H+1),master_potential_checks=res,naive_post_base_cap_conditional_A=str(naive_A),neutral_prefetch_conditional_A=str(prefetch_A),scope='Exact Fraction master/base arithmetic and cap-bias witness. Synthetic common records; not quantum acquisition or the complete logarithmic controller bank.')
print(json.dumps(result,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(result,indent=2)+'\n')

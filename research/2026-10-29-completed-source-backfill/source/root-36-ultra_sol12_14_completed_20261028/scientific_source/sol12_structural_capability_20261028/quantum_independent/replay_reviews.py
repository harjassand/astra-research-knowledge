"""Independent exact consumers; producer modules are never imported.

The analytic operator/entropy arguments are reviewed separately in Markdown.
This program checks the literal source reduction, every saved scalar cell,
and the actual condition-number-free common-bath fixture.
"""
from pathlib import Path
from fractions import Fraction as Q
from time import perf_counter
import json,sys
import arith as a
import frame as f
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
BASE=HERE.parent

def nchannel(m):
 out=f.zeros(9)
 for i in range(3):
  for j in range(3):
   for b in range(3):
    for d in range(3):
     tr=f.total(m[3*k+b][3*k+d]for k in range(3))if i==j else f.z()
     out[3*i+b][3*j+d]=f.scale(f.sub(tr,m[3*j+b][3*i+d]),Q(1,2))
 return out

def channel():
 for i,s in enumerate(f.SICS):
  assert f.trace(s)==f.z(1)and f.mm(s,s)==s
  for j,t in enumerate(f.SICS):
   assert f.trace(f.mm(s,t))==f.z(1 if i==j else Q(1,4))
 assert f.linear_combination([1]*9,f.SICS)==[[f.z(3*int(i==j))for j in range(3)]for i in range(3)]
 checks=0
 for b,s in zip(f.BELLS,f.SICS):
  nb=nchannel(b)
  def old(u,d):return 3*((u+d)%3)+(u+2*d)%3
  for u in range(3):
   for d in range(3):
    for v in range(3):
     for e in range(3):
      assert nb[old(u,d)][old(v,e)]==(f.scale(s[d][e],Q(1,3))if u==v else f.z())
      checks+=1
 return{'literal_channel_entries':checks,'pair_overlaps':81,'field':'Q[sqrt(-3)]','producer_imports':False}

def sparse():
 raw=json.loads((BASE/'quantum_composition/outputs/SIC_SPARSE_INTERVAL_CERTIFICATE.json').read_text())
 cells=raw['cover'];end=Q(1,5);slacks=[];improvements=[];maxbits=0
 for c in cells:
  lo,hi=Q(c['lo']),Q(c['hi']);assert lo==end and lo<hi;end=hi
  value=2*a.lower_entropy3((1+3*hi)/4)[0]-a.upper_entropy(lo,5)[1]
  threshold=(1-lo)/128
  assert value>=threshold
  # The saved producer lower is checked against an independently tighter bound.
  assert value>=Q(c['lower'])
  slacks.append(value-threshold);improvements.append(value-Q(c['lower']))
  maxbits=max(maxbits,value.numerator.bit_length(),value.denominator.bit_length())
 assert len(cells)==39 and end==Q(63,64)
 c=Q(256,507);tail=Q(11,3)-Q(85,12)*c
 assert tail==Q(137,1521)>Q(1,128)
 return{'cells_independently_recomputed':len(cells),'sqrt_bits':a.BITS,'atanh_terms':a.TERMS,
         'minimum_threshold_slack':a.serial(min(slacks)),
         'minimum_threshold_slack_display':float(min(slacks)),
         'every_saved_lower_is_valid':True,'tail_constant':a.serial(tail),
         'maximum_intermediate_output_bits':maxbits,'producer_imports':False}

def zero(n):return[[Q(0)for _ in range(n)]for _ in range(n)]
def mm(x,y):return[[sum((a*b for a,b in zip(row,col)),Q(0))for col in zip(*y)]for row in x]
def tr(x):return sum((x[i][i]for i in range(len(x))),Q(0))
def kron(x,y):return[[x[i//len(y)][j//len(y)]*y[i%len(y)][j%len(y)]for j in range(len(x)*len(y))]for i in range(len(x)*len(y))]
def ldlt(x,margin=Q(0)):
 n=len(x);assert all(x[i][j]==x[j][i]for i in range(n)for j in range(n))
 l=zero(n);d=[]
 for i in range(n):
  l[i][i]=1
  pivot=x[i][i]-margin-sum((l[i][k]**2*d[k]for k in range(i)),Q(0))
  assert pivot>0;d.append(pivot)
  for j in range(i+1,n):l[j][i]=(x[j][i]-sum((l[j][k]*l[i][k]*d[k]for k in range(i)),Q(0)))/pivot
 return min(d)

def white_bath():
 # Source reconstructed from its literal mathematical formula, not a saved Z.
 h=zero(9);po=zero(9);identity=zero(9)
 for i in range(9):h[i][i]=Q(1,9);identity[i][i]=1
 for b in range(3):h[b][3+b]=h[3+b][b]=[Q(1,36),Q(-1,36),Q(0)][b]
 for i in range(3):
  for j in range(3):po[3*i+i][3*j+j]=1
 u=[[Q(1,2)]*2 for _ in range(2)];v=[[Q(1),Q(0)],[Q(0),Q(0)]]
 ell=1-tr(mm(po,h))/3;assert ell==Q(8,9)and tr(h)==1
 ldlt(h,Q(1,13));assert mm(u,u)==u and mm(v,v)==v and mm(u,v)!=mm(v,u)
 ep=ell**2/2**22;rad=ell**2/2**18
 assert ep==Q(1,5308416)and rad==16*ep
 assert ep+9*rad<=ell**2/2**14
 fraction=Q(140,9*2**22)+Q(35,192);assert fraction<Q(1,2)
 x=[[po[i][j]+ep*h[i][j]for j in range(9)]for i in range(9)]
 xu,iv=kron(x,u),kron(identity,v)
 z=[[xu[i][j]+iv[i][j]for j in range(18)]for i in range(18)]
 ldlt(z);t=tr(z);assert t==12+ep
 marginal=[[sum((z[2*(3*i+b)+d][2*(3*j+b)+d]for b in range(3)for d in range(2)),Q(0))for j in range(3)]for i in range(3)]
 assert marginal==[[t/3 if i==j else Q(0)for j in range(3)]for i in range(3)]
 assert[[z[2*i+1][2*j+1]for j in range(9)]for i in range(9)]==[[e/2 for e in row]for row in x]
 rawlower=ep*ell/4+Q(1,3150)
 parent=json.loads((BASE/'parent/full_white_ray/KAPPA_FREE_RESULT.json').read_text())
 assert Q(parent['raw_Delta_lower'])==rawlower and Q(parent['CMI_excess_lower'])==rawlower/t
 off=[[z[i][6+j]for j in range(6)]for i in range(6)]
 assert any(t for row in mm(off,off)for t in row)
 fid=(3+ep/9)/(3+ep);assert fid>Q(2,3)
 cond=27/ep+1;assert cond>24
 return{'epsilon':a.serial(ep),'a0':a.serial(rad),'large_noise_fraction':a.serial(fraction),
 'raw_Delta_lower':a.serial(rawlower),'normalized_CMI_excess':a.record((rawlower/t,rawlower/t)),
 'trace':a.serial(t),'dimension':18,'reference_dimension':6,'extension_dimension':54,
 'exact_marginal':True,'noncommuting_singular_bath':True,'nonzero_offblock_square':True,
 'source_fidelity':a.serial(fid),'source_condition_lower':a.serial(cond),'producer_imports':False}

def main():
 start=perf_counter();result={'status':'PASS','channel':channel(),'sparse_receiver':sparse(),'kappa_free_fixture':white_bath()}
 result['seconds']=perf_counter()-start
 (HERE/'INDEPENDENT_SOURCE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k!='sparse_receiver'},indent=2))
 print('Sparse cells:',result['sparse_receiver']['cells_independently_recomputed'])
if __name__=='__main__':main()

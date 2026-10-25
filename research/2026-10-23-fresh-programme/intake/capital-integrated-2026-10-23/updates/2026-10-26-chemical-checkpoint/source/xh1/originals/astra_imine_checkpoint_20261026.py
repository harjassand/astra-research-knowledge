"""Working chemical-gate analysis, 26 Oct 2026. All kinetic rates hypothetical.
Primary chemistry: Rosenbaum & Liu 2003, Brudno et al 2010, Joshi et al 2025.
This is a theoretical reversible imine -> stable amine checkpoint, not an experiment.
"""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize_scalar
from math import exp, log

def generator(u_i,a_i,r_bound,r_free,c,u_h):
    # I_B covalent imine hybridized; I_F covalent imine DNA-detached;
    # H_B noncovalent hydrolyzed pair; X irreversibly cleared donor.
    # In H_B the DNA-templated contact can reform imine before donor dissociation.
    return np.array([
        [-(u_i+r_bound),u_i,r_bound],
        [a_i,-(a_i+r_free),0],
        [c,0,-(c+u_h)]],float)

def checkpoint(t_chase,t_reduce,*,u_i,a_i,r_bound,r_free,c,u_h,k_reduce):
    Q=generator(u_i,a_i,r_bound,r_free,c,u_h)
    p=np.array([1.,0.,0.])@expm(Q*t_chase)
    QR=Q-np.diag([k_reduce,k_reduce,0.])
    flux=np.array([k_reduce,k_reduce,0.])
    P_commit = float(p@np.linalg.solve(-QR,(np.eye(3)-expm(QR*t_reduce))@flux))
    # solve -QR int exp(QR t) flux dt ; since QR and exp commute, valid
    # More transparent numerical positivity check
    return P_commit,p, Q

def stg(qc,qw, pc,pw, damage=0.0):
    good=qc*pc; bad=qw*pw
    return good/(good+bad+damage),good,bad,damage

if __name__=='__main__':
  rates=dict(a_i=.02,r_bound=.005,r_free=.05,c=.2,k_reduce=.2)
  for u_c,u_w in ((.003,.3),(.3,3.),(.001,.1)):
    print('\nu matching / mismatching',u_c,u_w,'other rates',rates)
    for t in [0,10,30,60,120,300,600]:
      g, pg,_=checkpoint(t,20, u_i=u_c,u_h=u_c,**rates)
      b, pb,_=checkpoint(t,20, u_i=u_w,u_h=u_w,**rates)
      F,good,bad,_=stg(.5,.05,g,b,1e-5)
      print('t',t,'Pc',round(g,6),'Pw',round(b,6),'selectivity',round(g/b,3),'stage_F',round(F,8),'100_F',round(F**100,6),'protected_reducible',round(pg[0]+pg[1],5))
    obj=lambda t:stg(.5,.05, checkpoint(t,20,u_i=u_c,u_h=u_c,**rates)[0], checkpoint(t,20,u_i=u_w,u_h=u_w,**rates)[0],1e-5)[0]
    opt=minimize_scalar(lambda t:-obj(t), bounds=(0,1000),method='bounded')
    print('opt checkpoint',opt.x,'F100',obj(opt.x)**100)

  # Exact idealized chase result with effective selectivity losses gamma_i.
  def ideal_stage(t,qc,qw,gc,gw,eta,damage):
    p=eta*qc*exp(-gc*t);w=eta*qw*exp(-gw*t)
    return p/(p+w+damage),p,w
  qc,qw,gc,gw,eta,d=.45,.045,.002,.2,.9,1e-5 # gamma per minute
  Δ=gw-gc
  tstar=max(0.,log((Δ*qw*eta)/(gc*d))/gw)
  for tt in [0,tstar,100]:
    f,p,w=ideal_stage(tt,qc,qw,gc,gw,eta,d)
    print('simple effective gamma chase minutes',tt,'p',p,'w',w,'Fstage',f,'F100',f**100)
  numerical=minimize_scalar(lambda t:-ideal_stage(t,qc,qw,gc,gw,eta,d)[0],bounds=(0,200),method='bounded').x
  print('symbolic optimum',tstar,'numerical',numerical)
  assert abs(tstar-numerical)<1e-3
  # No-go: absent protection of imine from irreversible trapping, a pure wait with
  # identical generator leaves no intrinsic discrimination. Identical parameters -> same Pc.
  pc,_,_=checkpoint(100,20,u_i=.01,u_h=.01,**rates)
  pw,_,_=checkpoint(100,20,u_i=.01,u_h=.01,**rates)
  assert abs(pc-pw)<1e-13
  # All probability results bounded
  assert all(0<=checkpoint(t,20,u_i=.003,u_h=.003,**rates)[0]<=1 for t in [0,10,100,1000])
  print('CHECKS PASS')

# Independent analytic checks for the imine-healing toy subsystem:
# Covalent imine I -> hydrolyzed, still DNA-bound donor H at rate r;
# H -> I via imine reformation c, or H -> unjoined-cleared parent X at u.
# The exact slow eigenvalue gives long-time effective loss of imine/checkpoint.
def slow_clearance_rate(r,c,u):
    return 2*r*u/(r+c+u+np.sqrt((r+c+u)**2-4*r*u))

if __name__=='__main__':
  for r in [1e-4, .001, .01]:
    for c in [1e-3, .01, .1,1.]:
      for u in [1e-4,.001,.01,.1,1.]:
        gam_c=slow_clearance_rate(r,c,u)
        for scale in [1.5,3,10,100]:
          gam_w=slow_clearance_rate(r,c,u*scale)
          assert 1<=gam_w/gam_c<=scale*(1+1e-9)
  # independent eigenvalue test for the I/H subgenerator
  r,c,u=.005,.2,.003
  eig=np.linalg.eigvals([[-r,r],[c,-(c+u)]])
  assert abs(slow_clearance_rate(r,c,u)+max(eig.real))<1e-12
  print('EXACT EIGENLOSS/RATIO BOUND PASSED')

  # Composition-only mass measurement cannot determine PNA fourmer order.
  from collections import Counter,defaultdict
  from itertools import product
  group=defaultdict(list)
  for word in product('ACGT',repeat=4):
    group[tuple(word.count(base) for base in 'ACGT')].append(''.join(word))
  hist=Counter(map(len,group.values()))
  assert len(group)==35 and hist=={1:4,4:12,6:6,12:12,24:1}
  assert sum(n*count for n,count in hist.items())==256
  print('FOUR-BASE MASS CLASSES',len(group),'DISTRIBUTION',dict(sorted(hist.items())))

  # Ugi outcome is chemically different from reductive amination: the formerly
  # reactive parent's nitrogen becomes an N-acylated amide. A normal aldehyde
  # donor also generates a new stereocentre at the former carbonyl carbon.
  from rdkit import Chem
  from rdkit.Chem.rdMolDescriptors import CalcMolFormula
  from collections import Counter as AtomCounter
  def count_atoms(smiles):
    mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
    return AtomCounter(atom.GetSymbol() for atom in mol.GetAtoms())
  left=['CN','CC=O','CC(=O)O','C[N+]#[C-]']
  right=['CC(=O)N(C)C(C)C(=O)NC','O']
  countleft=sum((count_atoms(s) for s in left),AtomCounter())
  countright=sum((count_atoms(s) for s in right),AtomCounter())
  assert countleft==countright
  mol=Chem.MolFromSmiles(right[0])
  assert len(Chem.FindMolChiralCenters(mol,includeUnassigned=True))==1
  print('UGI SURROGATE ATOM BALANCE AND STEREOCENTRE PASSED')

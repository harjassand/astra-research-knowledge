"""Ordinary bounded JSON-tree receiving, adapted from retained-clock v4 guard.
Source: continuity_clock_v4_detour_20261101_0132/retained_state_renewal_clock_20261101/receive_clock.py
No diagnostics are ignored here: the entire normalized certificate is proof data.
"""
import multiface as M
from fractions import Fraction as F

def guard_tree(obj,max_depth=64,max_nodes=100000,allow_fraction=False):
 if type(max_depth)is not int or max_depth<0 or type(max_nodes)is not int or max_nodes<1:raise ValueError('exact depth>=0 and node>=1 budgets')
 stack=[(obj,0)];seen=set();nodes=0;keys=0;peak=1
 def push(x,depth):
  if depth>max_depth or nodes+len(stack)>=max_nodes:raise M.BudgetRefusal('certificate pending-node/depth budget')
  stack.append((x,depth))
 while stack:
  x,depth=stack.pop();nodes+=1
  if depth>max_depth or nodes>max_nodes:raise M.BudgetRefusal('certificate depth/node budget')
  if type(x)in(dict,list):
   if id(x)in seen:raise M.BudgetRefusal('certificate must be a finite unshared tree, not a cycle or alias graph')
   seen.add(id(x))
   if type(x)is dict:
    for k,v in x.items():
     keys+=1
     if keys>max_nodes:raise M.BudgetRefusal('certificate key-scan budget')
     if type(k)is not str:raise M.BudgetRefusal('certificate keys must be strings')
     push(v,depth+1)
   else:
    if len(x)>max_nodes-nodes-len(stack):raise M.BudgetRefusal('certificate pending-node budget')
    for v in x:push(v,depth+1)
   peak=max(peak,len(stack))
  elif type(x)not in(type(None),bool,int,float,str) and not(allow_fraction and type(x)is F):raise M.BudgetRefusal('certificate leaves must be JSON scalar types')
 return dict(proof_nodes=nodes,keys_scanned=keys,maximum_pending_nodes=peak)

def same_guarded(a,b):
 """Iterative exact-type equality AFTER both trees pass guard_tree."""
 stack=[(a,b)]
 while stack:
  x,y=stack.pop()
  if type(x)is not type(y):return False
  if type(x)is dict:
   if len(x)!=len(y):return False
   for k,v in x.items():
    if k not in y:return False
    stack.append((v,y[k]))
  elif type(x)is list:
   if len(x)!=len(y):return False
   for v,w in zip(x,y):stack.append((v,w))
  elif x!=y:return False
 return True

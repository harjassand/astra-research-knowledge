"""Same-author canonical certificate receiver and budgeted expression evaluator.
This is NOT an independent mathematical/code receiving implementation.
"""
from fractions import Fraction as F
import multiface as M
from certificate_guard import guard_tree,same_guarded

def certificate(raw,max_masks=1000000):
 return M.encode(M.construct(raw,max_masks=max_masks))

def strict_equal(a,b,max_depth=64,max_nodes=100000):
 guard_tree(a,max_depth,max_nodes);guard_tree(b,max_depth,max_nodes)
 return same_guarded(a,b)

def receive(raw,claimed,max_masks=1000000,max_depth=64,max_nodes=100000):
 if type(claimed)is not dict:return False
 # Guard untrusted structure before any expensive canonical production.
 guard_tree(claimed,max_depth,max_nodes)
 expected=certificate(raw,max_masks=max_masks)
 guard_tree(expected,max_depth,max_nodes)
 return same_guarded(claimed,expected)

def _integer_tag(node):
 if type(node)is int:return node
 if type(node)is dict and len(node)==1 and '__integer_hex__' in node:
  value=node['__integer_hex__']
  if type(value)is not str:raise ValueError('integer hex payload must be a string')
  return int(value,16)
 raise ValueError('exact integer or integer-hex tag required')

def evaluate_expression(node,max_power_bits=1000000,max_depth=64,max_nodes=100000):
 """Guard then iteratively evaluate a finite unshared exact expression tree.
 A caller may raise the depth budget without reaching Python's recursion limit.
 Input nodes and pending guard nodes are budgeted; evaluation stacks are bounded
 by a constant multiple of that finite input tree, not an uncharged recursion.
 """
 if type(max_power_bits)is not int or max_power_bits<0:raise ValueError('exact nonnegative power bit budget')
 guard_tree(node,max_depth,max_nodes,allow_fraction=True)
 stack=[('visit',node)];values=[]
 while stack:
  phase,x=stack.pop()
  if phase=='mul':
   acc=F(1)
   for _ in range(x):acc*=values.pop()
   values.append(acc);continue
  if phase=='pow':
   base=values.pop();k=x
   bound=k*max(abs(base.numerator).bit_length(),base.denominator.bit_length())
   if bound>max_power_bits:raise M.BudgetRefusal('power intermediate bit budget: upper bound '+M.integer_text(bound))
   values.append(base**k);continue
  if type(x)is bool:raise ValueError('Boolean is not an exact rational expression')
  if type(x)in(int,F):values.append(F(x));continue
  if type(x)is str:values.append(F(x));continue
  if type(x)is not dict:raise ValueError('rational or expression dictionary')
  if len(x)==1 and '__integer_hex__' in x:
   values.append(F(_integer_tag(x)));continue
  if len(x)==1 and '__fraction_hex__' in x:
   parts=x['__fraction_hex__']
   if type(parts)is not list or len(parts)!=2 or any(type(v)is not str for v in parts):raise ValueError('two hex strings required')
   values.append(F(int(parts[0],16),int(parts[1],16)));continue
  if x.get('op')=='mul':
   args=x.get('args')
   if type(args)is not list:raise ValueError('multiplication argument list required')
   stack.append(('mul',len(args)))
   for child in reversed(args):stack.append(('visit',child))
   continue
  if x.get('op')=='pow':
   k=_integer_tag(x.get('exponent'))
   if k<0:raise ValueError('nonnegative integer exponent')
   if 'base' not in x:raise ValueError('power base required')
   stack.append(('pow',k));stack.append(('visit',x['base']));continue
  raise ValueError('unknown expression operator')
 if len(values)!=1:raise ValueError('malformed expression evaluation stack')
 return values[0]

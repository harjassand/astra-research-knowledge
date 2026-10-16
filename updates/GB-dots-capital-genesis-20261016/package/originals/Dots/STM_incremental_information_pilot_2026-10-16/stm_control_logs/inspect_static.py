"""Static symbolic pickle inspection. Never imports globals or invokes REDUCE/BUILD.
Untrusted globals/reducers become inert nodes. Numeric bytes decoded with struct.
This is not author code and never uses pickle.load/loads or numpy allow_pickle.
"""
import pickletools, pathlib, struct, json, math
class Node:
 def __init__(self, tag, args=None): self.tag,self.args,self.state=tag,args,None
MARK=object()
def parse(path):
 if path.stat().st_size > 16_000_000: raise ValueError('Diagnostic file size limit')
 b=path.read_bytes(); assert b[:8]==b'\x93NUMPY\x01\x00'
 s=[];memo={}
 def marked():
  i=max(i for i,x in enumerate(s) if x is MARK);v=s[i+1:];del s[i:];return v
 for index,(op,a,pos) in enumerate(pickletools.genops(b[10+int.from_bytes(b[8:10],'little'):])):
  if index>500000 or len(s)>100000 or len(memo)>100000: raise ValueError('Parser resource bound')
  n=op.name
  if n=='PROTO':continue
  elif n=='GLOBAL':
   if a not in {'numpy.core.multiarray _reconstruct','numpy ndarray','numpy dtype','numpy.core.multiarray scalar'}: raise ValueError('Unknown global')
   s.append(Node('global',a))
  elif n=='REDUCE':
   args=s.pop();func=s.pop();s.append(Node('reduce',(func,args)))
  elif n=='BUILD':
   state=s.pop();assert isinstance(s[-1],Node);s[-1].state=state
  elif n=='MARK':s.append(MARK)
  elif n in ('BINPUT','LONG_BINPUT'):memo[a]=s[-1]
  elif n in ('BINGET','LONG_BINGET'):s.append(memo[a])
  elif n in ('BININT','BININT1','BININT2','BINFLOAT','BINUNICODE','SHORT_BINUNICODE','BINBYTES','SHORT_BINBYTES'):s.append(a)
  elif n=='NEWTRUE':s.append(True)
  elif n=='NEWFALSE':s.append(False)
  elif n=='NONE':s.append(None)
  elif n=='EMPTY_TUPLE':s.append(())
  elif n=='EMPTY_LIST':s.append([])
  elif n=='EMPTY_DICT':s.append({})
  elif n=='TUPLE':s.append(tuple(marked()))
  elif n in ('TUPLE1','TUPLE2','TUPLE3'):
   k=int(n[-1]);v=tuple(s[-k:]);del s[-k:];s.append(v)
  elif n=='APPEND':v=s.pop();s[-1].append(v)
  elif n=='APPENDS':v=marked();s[-1].extend(v)
  elif n=='SETITEMS':
   v=marked();s[-1].update(zip(v[::2],v[1::2]))
  elif n=='STOP':assert len(s)==1;return s[0]
  else:raise ValueError('Unsupported opcode '+n)
 raise ValueError('No STOP')
def decode(v):
 if isinstance(v,Node):
  assert v.tag=='reduce'
  func,args=v.args;assert func.tag=='global';name=func.args
  if name=='numpy dtype':return args[0]
  if name=='numpy.core.multiarray scalar':
   dt=decode(args[0]);return numbers(dt,args[1])[0]
  if name=='numpy.core.multiarray _reconstruct':
   ver,shape,dtype,fortran,data=v.state;dt=decode(dtype)
   if dt=='O8':return decode(data[0])
   vals=numbers(dt,data)
   if len(vals)>20:return {'dtype':dt,'shape':shape,'length':len(vals),'first':vals[:3],'last':vals[-3:],'min':min(vals),'max':max(vals)}
   return vals
  raise ValueError('Unrecognized inert node '+name)
 if isinstance(v,dict):return {k:decode(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [decode(x) for x in v]
 return v
def numbers(dt,data):
 fmt={'f8':'d','f4':'f','b1':'?'}.get(dt)
 if fmt is None:raise ValueError('Unsupported numeric dtype '+dt)
 return [x[0] for x in struct.iter_unpack('<'+fmt,data)]
if __name__=='__main__':
 p=pathlib.Path(__file__).parent
 out={f.name:decode(parse(f)) for f in sorted((p/'acquired/training_data_and_model_parameters/training_data').glob('*.npy'))}
 (p/'sample_decoded_summary.json').write_text(json.dumps(out,indent=2,allow_nan=False))
 for k,v in out.items():
  t=v['transitions'];print(k,'nsteps',len(t['action']),'done',t['done'],'reward',t['reward']);print('actions',t['action']);print('distance',[x['dist_destination'] for x in t['info']]);print('current trace lengths',[x['current_series']['length'] for x in t['info']])

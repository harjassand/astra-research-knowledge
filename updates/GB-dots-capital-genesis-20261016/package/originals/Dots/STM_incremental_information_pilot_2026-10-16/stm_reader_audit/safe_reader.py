"""Original, fail-closed symbolic reader for the qualified protocol-3 NPY subset.
No pickle loading, GLOBAL resolution, reducer invocation, NumPy or author imports.
parse preserves memo aliases. decode is presentation-only, never identity evidence.
"""
import ast
import math
import pathlib
import pickletools
import struct

MAX_FILE=16_000_000
MAX_OPS=500_000
MAX_MEMO=100_000
MAX_STACK=100_000
MAX_ITEMS=500_000
MAX_DEPTH=64
MAX_ARRAY=1_000_000
MAX_NDIM=8
GLOBALS=frozenset(('numpy.core.multiarray _reconstruct','numpy ndarray','numpy dtype','numpy.core.multiarray scalar'))
FORMATS={'f8':('d',8),'f4':('f',4),'b1':('?',1)}
class ReaderError(ValueError): pass
class Node:
    __slots__=('tag','args','state')
    def __init__(self,tag,args=None): self.tag,self.args,self.state=tag,args,None

def require(ok,msg):
    if not ok: raise ReaderError(msg)

def parse(path):
    with pathlib.Path(path).open('rb') as f: b=f.read(MAX_FILE+1)
    return parse_bytes(b)

def parse_bytes(b):
    require(type(b) is bytes and len(b)<=MAX_FILE,'File size/type')
    require(b[:8]==b'\x93NUMPY\x01\x00' and len(b)>=10,'NPY v1 only')
    hlen=int.from_bytes(b[8:10],'little'); require(0<hlen<=4096 and 10+hlen<len(b),'Header bounds')
    try: header=ast.literal_eval(b[10:10+hlen].decode('ascii').strip())
    except Exception as e: raise ReaderError('Invalid header') from e
    require(type(header) is dict and set(header)=={'descr','fortran_order','shape'},'Header schema')
    require(header['descr']=='|O' and header['fortran_order'] is False and header['shape']==(),'Scalar object header required')
    root=parse_pickle(b[10+hlen:])
    require(isinstance(root,Node) and root.tag=='reduce' and root.args[0].args=='numpy.core.multiarray _reconstruct','Root array required')
    require(root.state[1]==() and dtype(root.state[2])=='O8','Root scalar object array required')
    return root

def parse_pickle(payload):
    """Parse only inert symbolic protocol-3 data; useful for synthetic tests."""
    require(type(payload) is bytes and len(payload)<=MAX_FILE,'Payload bound')
    s=[]; memo={}; mark=object(); item_count=0; mark_count=0
    def pop():
        require(bool(s) and s[-1] is not mark,'Stack underflow');return s.pop()
    def marked():
        nonlocal mark_count
        require(mark_count>0,'Missing mark');i=len(s)-1
        while s[i] is not mark:i-=1
        v=s[i+1:];del s[i:];mark_count-=1;return v
    try:
        for index,(op,a,pos) in enumerate(pickletools.genops(payload)):
            require(index<MAX_OPS,'Opcode bound');n=op.name
            if index==0: require(n=='PROTO' and a==3,'Protocol 3 required');continue
            if n=='GLOBAL':
                require(a in GLOBALS,'Unknown global');s.append(Node('global',a))
            elif n=='REDUCE':
                args=pop();func=pop();require(type(args) is tuple and isinstance(func,Node) and func.tag=='global' and func.args!='numpy ndarray','Invalid reducer');s.append(Node('reduce',(func,args)))
            elif n=='BUILD':
                state=pop();require(bool(s) and isinstance(s[-1],Node) and s[-1].tag=='reduce' and s[-1].state is None,'Invalid build');s[-1].state=state
            elif n=='MARK':
                mark_count+=1;require(mark_count<=MAX_DEPTH,'Mark nesting bound');s.append(mark)
            elif n in ('BINPUT','LONG_BINPUT'):
                require(type(a) is int and 0<=a<MAX_MEMO and a not in memo and bool(s) and s[-1] is not mark,'Memo index/redefinition');memo[a]=s[-1]
            elif n in ('BINGET','LONG_BINGET'):
                require(a in memo,'Missing memo');s.append(memo[a])
            elif n in ('BININT','BININT1','BININT2','BINFLOAT','BINUNICODE','SHORT_BINUNICODE','BINBYTES','SHORT_BINBYTES'):s.append(a)
            elif n=='NEWTRUE':s.append(True)
            elif n=='NEWFALSE':s.append(False)
            elif n=='NONE':s.append(None)
            elif n=='EMPTY_TUPLE':s.append(())
            elif n=='EMPTY_LIST':s.append([])
            elif n=='EMPTY_DICT':s.append({})
            elif n=='TUPLE':s.append(tuple(marked()))
            elif n in ('TUPLE1','TUPLE2','TUPLE3'):
                k=int(n[-1]);require(len(s)>=k and all(x is not mark for x in s[-k:]),'Tuple underflow');v=tuple(s[-k:]);del s[-k:];s.append(v)
            elif n in ('APPEND','APPENDS'):
                vals=[pop()] if n=='APPEND' else marked();require(bool(s) and type(s[-1]) is list,'List target');item_count+=len(vals);s[-1].extend(vals)
            elif n in ('SETITEM','SETITEMS'):
                if n=='SETITEM':value=pop();key=pop();vals=[key,value]
                else:vals=marked()
                require(bool(s) and type(s[-1]) is dict and len(vals)%2==0,'Dict target/pairs')
                for k,v in zip(vals[::2],vals[1::2]):
                    require(type(k) is str and k not in s[-1],'String unique keys required');s[-1][k]=v
                item_count+=len(vals)
            elif n=='STOP':
                require(len(s)==1 and mark_count==0 and pos+1==len(payload),'Stop stack/trailing data');validate(s[0]);return s[0]
            else:raise ReaderError('Unsupported opcode '+n)
            require(len(s)<=MAX_STACK and len(memo)<=MAX_MEMO and item_count<=MAX_ITEMS,'Resource bound')
    except ReaderError:raise
    except Exception as e:raise ReaderError('Malformed pickle: '+type(e).__name__) from e
    raise ReaderError('No STOP')

def dtype(v):
    require(isinstance(v,Node) and v.tag=='reduce' and v.args[0].args=='numpy dtype','Dtype node')
    a=v.args[1];require(type(a) is tuple and len(a)==3 and type(a[0]) is str and a[1] is False and a[2] is True,'Dtype arguments')
    dt=a[0];require(dt in {*FORMATS,'O8'},'Unknown dtype')
    expected=(3,'|' if dt in ('O8','b1') else '<',None,None,None,-1,-1,63 if dt=='O8' else 0)
    require(type(v.state) is tuple and len(v.state)==len(expected) and all(type(x) is type(y) and x==y for x,y in zip(v.state,expected)),'Dtype state/endian');return dt

def validate(root):
    active=set();done={};visits=0
    def walk(v,depth):
        nonlocal visits
        require(depth<=MAX_DEPTH,'Graph nesting bound');visits+=1;require(visits<=MAX_ITEMS,'Graph work bound')
        if type(v) in (str,bytes,int,bool,type(None)):return 0
        if type(v) is float:require(math.isfinite(v),'Nonfinite float');return 0
        ident=id(v);require(ident not in active,'Cyclic graph')
        if ident in done:require(depth+done[ident]<=MAX_DEPTH,'Aliased nesting bound');return done[ident]
        active.add(ident)
        if isinstance(v,Node):
            require(v.tag in ('global','reduce'),'Node tag')
            children=[v.args,v.state]
        elif type(v) in (list,tuple):children=v
        elif type(v) is dict:children=list(v.values())
        else:raise ReaderError('Unknown value type')
        height=1+max((walk(c,depth+1) for c in children),default=-1)
        if isinstance(v,Node) and v.tag=='reduce':
            f,a=v.args
            if f.args=='numpy dtype':dtype(v)
            elif f.args=='numpy.core.multiarray scalar':
                require(v.state is None and len(a)==2,'Scalar schema');dt=dtype(a[0]);require(dt in FORMATS and type(a[1]) is bytes and len(a[1])==FORMATS[dt][1],'Scalar data');numbers(dt,a[1])
            elif f.args=='numpy.core.multiarray _reconstruct':
                require(len(a)==3 and isinstance(a[0],Node) and a[0].tag=='global' and a[0].args=='numpy ndarray' and type(a[1]) is tuple and len(a[1])==1 and type(a[1][0]) is int and a[1][0]==0 and type(a[2]) is bytes and a[2]==b'b','Reconstruct arguments')
                require(type(v.state) is tuple and len(v.state)==5,'Array state');ver,shape,d,order,data=v.state
                require(type(ver) is int and ver==1 and type(shape) is tuple and len(shape)<=MAX_NDIM and order is False,'Array schema/order')
                require(all(type(x) is int and 0<=x<=MAX_ARRAY for x in shape),'Array shape');count=math.prod(shape);require(count<=MAX_ARRAY,'Array element bound');dt=dtype(d)
                if dt=='O8':require(shape==() and type(data) is list and len(data)==1 and type(data[0]) is dict,'Object wrapper only')
                else:
                    require(type(data) is bytes and len(data)==count*FORMATS[dt][1],'Array byte length');numbers(dt,data)
            else:raise ReaderError('Unknown reducer')
        active.remove(ident);done[ident]=height;return height
    walk(root,0)

def numbers(dt,data):
    require(dt in FORMATS and type(data) is bytes,'Numeric data type');fmt,size=FORMATS[dt]
    require(len(data)%size==0 and len(data)//size<=MAX_ARRAY,'Numeric size')
    if dt=='b1':require(all(x in (0,1) for x in data),'Boolean bytes')
    vals=[x[0] for x in struct.iter_unpack('<'+fmt,data)]
    require(all(not isinstance(x,float) or math.isfinite(x) for x in vals),'Nonfinite numeric data');return vals

def decode(root):
    """Legacy-compatible bounded presentation summary, with alias caching."""
    validate(root);cache={}
    def go(v):
        if id(v) in cache:return cache[id(v)]
        if isinstance(v,Node):
            require(v.tag=='reduce','Bare global not decodable');f,a=v.args
            if f.args=='numpy dtype':out=dtype(v)
            elif f.args.endswith(' scalar'):out=numbers(dtype(a[0]),a[1])[0]
            else:
                _,shape,d,_,data=v.state;dt=dtype(d)
                if dt=='O8':out=go(data[0])
                else:
                    vals=numbers(dt,data)
                    out=({'dtype':dt,'shape':shape,'length':len(vals),'first':vals[:3],'last':vals[-3:],'min':min(vals),'max':max(vals)} if len(vals)>20 else vals)
        elif type(v) is dict:out={k:go(x) for k,x in v.items()}
        elif type(v) in (list,tuple):out=[go(x) for x in v]
        else:return v
        cache[id(v)]=out;return out
    return go(root)

"""Implicit hard-KA frame and two-port swap programs.

Gate checking and planning do not enumerate configuration graphs.  A plan stores
only one chosen quadtree branch and strip vacancy locations.  Its microscopic
execution is intentionally available for testing, not claimed inexpensive at
large side length.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator
import numpy as np

Site=tuple[int,int]  # row, column
Swap=tuple[Site,Site]
Rect=tuple[int,int,int,int] # y0,x0,y1,x1


def strip(rect:Rect, direction:str)->list[Site]:
    y0,x0,y1,x1=rect
    if direction=='R': return [(y,x1) for y in range(y0,y1)]
    if direction=='L': return [(y,x0-1) for y in range(y0,y1)]
    if direction=='U': return [(y1,x) for x in range(x0,x1)]
    if direction=='D': return [(y0-1,x) for x in range(x0,x1)]
    raise ValueError(direction)


def extend(rect:Rect,direction:str)->Rect:
    y0,x0,y1,x1=rect
    return {'R':(y0,x0,y1,x1+1),'L':(y0,x0-1,y1,x1),
            'U':(y0,x0,y1+1,x1),'D':(y0-1,x0,y1,x1)}[direction]


def children(rect:Rect)->list[Rect]:
    y0,x0,y1,x1=rect;n=(y1-y0)//2
    return [(y0+dy*n,x0+dx*n,y0+(dy+1)*n,x0+(dx+1)*n)
            for dy,dx in ((0,0),(0,1),(1,0),(1,1))]


def expansion(child:Rect,parent:Rect, include_sites:bool=True):
    y0,x0,y1,x1=child;Y0,X0,Y1,X1=parent
    dx='R' if x0==X0 else 'L';dy='U' if y0==Y0 else 'D'
    current=child
    for _ in range(y1-y0):
        for direction in (dx,dy):
            yield current,direction,(strip(current,direction) if include_sites else None)
            current=extend(current,direction)
    assert current==parent


class Gate:
    """A deterministic port-independent gate, read on an occupied-port copy."""
    def __init__(self,occupied_port_state:np.ndarray):
        self.a=occupied_port_state
        self.cache:dict[Rect,int]={}
        v=1-self.a.astype(np.int64)
        self.prefix=np.pad(v.cumsum(0).cumsum(1),((1,0),(1,0)))
    def zeros(self,rect:Rect)->int:
        y0,x0,y1,x1=rect;s=self.prefix
        return int(s[y1,x1]-s[y0,x1]-s[y1,x0]+s[y0,x0])
    def good(self,rect:Rect)->bool:
        if rect in self.cache:return self.cache[rect]>=0
        y0,x0,y1,x1=rect;n=y1-y0
        if n!=x1-x0 or n<2 or n&(n-1):raise ValueError('power-of-two square required')
        if n==2:
            self.cache[rect]=0 if self.zeros(rect)>=3 else -1
            return self.cache[rect]>=0
        for i,child in enumerate(children(rect)):
            if not self.good(child):continue
            okay=True
            for old,direction,_ in expansion(child,rect,False):
                Y0,X0,Y1,X1=old
                sr={'R':(Y0,X1,Y1,X1+1),'L':(Y0,X0-1,Y1,X0),
                    'U':(Y1,X0,Y1+1,X1),'D':(Y0-1,X0,Y0,X1)}[direction]
                if self.zeros(sr)==0:
                    okay=False;break
            if okay:
                self.cache[rect]=i;return True
        self.cache[rect]=-1;return False


def line_word(A:list[Site],B:list[Site],r:int=0)->list[Swap]:
    m=len(A)
    assert len(B)==m and 0<=r<m
    out=[]
    for y in range(r,0,-1):out.append((B[y],B[y-1]))
    for y in range(1,m):out.extend(((B[y],B[y-1]),(B[y-1],A[y-1])))
    for y in range(m-1,r,-1):out.append((A[y],A[y-1]))
    assert len(out)==3*(m-1)
    return out


def preparatory_words(rect:Rect,direction:str)->list[list[Swap]]:
    y0,x0,y1,x1=rect
    words=[]
    if direction=='R':
        for x in range(x0,x1-1):
            words.append(line_word([(y,x) for y in range(y0,y1)],[(y,x+1) for y in range(y0,y1)]))
    elif direction=='U':
        for y in range(y0,y1-1):
            words.append(line_word([(y,x) for x in range(x0,x1)],[(y+1,x) for x in range(x0,x1)]))
    return words


@dataclass
class Instruction:
    kind:str
    payload:object
    def word(self)->list[Swap]:
        if self.kind=='base':return list(self.payload)
        rect,direction,r=self.payload
        new=strip(rect,direction)
        shifts=[(new[y],new[y-1]) for y in range(r,0,-1)]
        if direction in ('R','U'):
            pre=[s for w in preparatory_words(rect,direction) for s in w]
            return pre+shifts+pre[::-1]
        y0,x0,y1,x1=rect
        old=([(y,x0) for y in range(y0,y1)] if direction=='L'
             else [(y0,x) for x in range(x0,x1)])
        return shifts+line_word(old,new,0)


def apply(a:np.ndarray,s:Swap,tags:dict[str,Site]|None=None):
    u,v=s;a[u],a[v]=int(a[v]),int(a[u])
    if tags is not None:
        for key,pos in list(tags.items()):
            if pos==u:tags[key]=v
            elif pos==v:tags[key]=u


def plan_frame(a:np.ndarray,rect:Rect,gate:Gate,tags:dict[str,Site])->list[Instruction]:
    if not gate.good(rect):raise ValueError('gate failed')
    y0,x0,y1,x1=rect;n=y1-y0
    instructions=[]
    if n==2:
        occupied=[(y,x) for y in range(y0,y1) for x in range(x0,x1) if a[y,x]]
        moves=[]
        if occupied:
            assert len(occupied)==1
            u=occupied[0];target=(y1-1,x1-1)
            if u[1]!=target[1]:
                v=(u[0],target[1]);moves.append((u,v));u=v
            if u[0]!=target[0]:moves.append((u,target))
        for s in moves:apply(a,s,tags)
        instructions.append(Instruction('base',moves))
    else:
        child=children(rect)[gate.cache[rect]]
        instructions.extend(plan_frame(a,child,gate,tags))
        for current,direction,new in expansion(child,rect):
            r=next(i for i,s in enumerate(new) if a[s]==0)
            instructions.append(Instruction('grow',(current,direction,r)))
            # Execute only the net effect, not the long prepare/unprepare word.
            for i in range(r,0,-1):apply(a,(new[i],new[i-1]),tags)
            if direction in ('L','D'):
                Y0,X0,Y1,X1=current
                old=([(y,X0) for y in range(Y0,Y1)] if direction=='L'
                     else [(Y0,x) for x in range(X0,X1)])
                for u,v in zip(old,new):apply(a,(u,v),tags)
    assert not a[y0:y1,x0].any() and not a[y0,x0:x1].any()
    return instructions


def supported_swap(rect:Rect,u:Site,v:Site)->list[Swap]:
    y0,x0,y1,x1=rect
    pre=[]
    if u[0]==v[0]:
        y=u[0]
        for yy in range(y0,y-1):
            pre.extend(line_word([(yy,x) for x in range(x0,x1)],[(yy+1,x) for x in range(x0,x1)]))
    else:
        x=u[1]
        for xx in range(x0,x-1):
            pre.extend(line_word([(y,xx) for y in range(y0,y1)],[(y,xx+1) for y in range(y0,y1)]))
    return pre+[(u,v)]+pre[::-1]


@dataclass
class PortModule:
    L:int
    ports:tuple[Site,Site]
    shape:tuple[int,int]
    preparation:list[Instruction]
    port_positions:tuple[Site,Site]
    def word(self)->Iterator[Swap]:
        for ins in self.preparation:yield from ins.word()
        u,v=self.port_positions
        path=[u];y,x=u
        while x!=v[1]:x+=(1 if x<v[1] else -1);path.append((y,x))
        while y!=v[0]:y+=(1 if y<v[0] else -1);path.append((y,x))
        edges=list(zip(path,path[1:]));seq=edges+edges[-2::-1]
        for a,b in seq:yield from supported_swap((0,0,*self.shape),a,b)
        for ins in self.preparation[::-1]:yield from ins.word()[::-1]


def make_module(state:np.ndarray,ports:tuple[Site,Site])->PortModule:
    L=min(state.shape)
    if state.shape not in ((L,2*L),(2*L,L)):raise ValueError('rectangle must be (L,2L) or (2L,L)')
    forced=state.copy()
    for s in ports:forced[s]=1
    original=forced.copy();gate=Gate(original)
    tags={'a':ports[0],'b':ports[1]}
    left=(0,0,L,L);right=((0,L,L,2*L) if state.shape[1]==2*L else (L,0,2*L,L))
    if not(gate.good(left) and gate.good(right)):raise ValueError('gate failed')
    prep=plan_frame(forced,left,gate,tags)+plan_frame(forced,right,gate,tags)
    assert all(y>0 and x>0 for y,x in tags.values())
    return PortModule(L,ports,state.shape,prep,(tags['a'],tags['b']))


def legal(a:np.ndarray,s:Swap)->bool:
    u,v=s
    if abs(u[0]-v[0])+abs(u[1]-v[1])!=1:return False
    h,w=a.shape
    for site,other in ((u,v),(v,u)):
        y,x=site
        if not any(0<=yy<h and 0<=xx<w and (yy,xx)!=other and a[yy,xx]==0
                   for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))):return False
    return True

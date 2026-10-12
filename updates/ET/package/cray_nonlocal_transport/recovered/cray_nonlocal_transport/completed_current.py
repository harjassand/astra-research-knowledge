"""Evaluate the actual lifted hard-KA current, or its finite-radius approximation.

Occupations must be supplied as a deterministic callable returning 0 or 1 on
integer lattice sites. Full evaluation may inspect arbitrarily distant sites;
finite cutoff gives the local approximation certified in REPORT.md. The default
cutoff is finite. Set cutoff=None only for a field with finite bad clusters.
"""
from pathlib import Path
from fractions import Fraction
from typing import Callable
import json
import numpy as np
from coarse_flow import current as spatial_current

ROOT=Path(__file__).parent
Site=tuple[int,int]

class CompletedCurrent:
    def __init__(self,root:Path=ROOT):
        self.meta=json.loads((root/'module_metadata.json').read_text())
        data=np.load(root/'module_flow.npz',allow_pickle=False)
        keys=data['u'].astype(np.int64)*(1<<18)+data['v']
        order=np.argsort(keys)
        self.keys=keys[order];self.flow=data['flow'][order]
        self.den=int(self.meta['denominator'])
        self.offsets=tuple(tuple(t)for t in self.meta['gate_offsets'])
        self.allowed=frozenset(self.meta['gate_allowed'])

    def bond(self,x:Site,direction:int,eta:Callable[[Site],int],cutoff:int|None=8)->Fraction:
        if direction not in (0,1):raise ValueError('direction must be 0 or 1')
        step=((1,0),(0,1))[direction];y=(x[0]+step[0],x[1]+step[1])
        bits:dict[Site,int]={}
        def bit(z:Site)->int:
            if z not in bits:
                value=eta(z)
                if value not in (0,1):raise ValueError('Occupation must be 0 or 1')
                bits[z]=int(value)
            return bits[z]
        total=Fraction(0)
        for sx in range(3):
            for sy in range(3):
                bx=((x[0]-sx)//3,(x[1]-sy)//3)
                by=((y[0]-sx)//3,(y[1]-sy)//3)
                if bx==by:
                    modules=((bx,0),((bx[0]-1,bx[1]),0),(bx,1),((bx[0],bx[1]-1),1))
                else:modules=((bx,direction),)
                gates:dict[Site,bool]={}
                def bad(z:Site)->bool:
                    if z not in gates:
                        center=(sx+3*z[0]+1,sy+3*z[1]+1)
                        pattern=sum(bit((center[0]+dx,center[1]+dy))<<j
                                    for j,(dx,dy)in enumerate(self.offsets))
                        gates[z]=pattern not in self.allowed
                    return gates[z]
                for anchor,orientation in modules:
                    ox=sx+3*anchor[0];oy=sy+3*anchor[1]
                    state=0
                    for b in range(3):
                        for a in range(6):
                            site=(ox+a,oy+b)if orientation==0 else(ox+b,oy+a)
                            state|=bit(site)<<(a+6*b)
                    def local_index(z:Site)->int:
                        a,b=z[0]-ox,z[1]-oy
                        return a+6*b if orientation==0 else b+6*a
                    a=local_index(x);b=local_index(y)
                    if ((state>>a)&1)==((state>>b)&1):continue
                    swapped=state^(1<<a)^(1<<b)
                    lo=min(state,swapped);hi=max(state,swapped);key=lo*(1<<18)+hi
                    at=int(np.searchsorted(self.keys,key))
                    if at==len(self.keys) or int(self.keys[at])!=key:continue
                    numerator=int(self.flow[at])*(1 if state==lo else -1)
                    if numerator==0:continue
                    other=(anchor[0]+(orientation==0),anchor[1]+(orientation==1))
                    # Freeze both local reservoirs as good in the coefficient.
                    # This is essential: intermediate module states can be bad.
                    def outside_bad(z:Site)->bool:
                        return False if z==anchor or z==other else bad(z)
                    k=spatial_current(anchor,orientation,outside_bad,cutoff)
                    total+=Fraction(numerator,self.den)*k
        return total/9

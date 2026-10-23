"""Independent exact state-set diagnostic for one-sided terminal extensions."""
from pathlib import Path
import json,time
from check_interface import path,join,adjacency,enumerate_states,Q

def extend(g,side):
    ports=list(g['ports']); old=ports[side]; assert len(adjacency(g)[old])<=3
    ports[side]=g['n']
    return {'n':g['n']+1,'edges':sorted(g['edges']+[(old,g['n'])]),'ports':tuple(ports)}

def state_extend(sig,side,A):
    a,nn,ff=sig[side]
    if A==a or ff[A] or sum(nn)>3:return None
    counts=[0]*Q;flags=[0]*Q;counts[a]=1;flags[a]=int(nn[A]>0)
    rr=(A,tuple(counts),tuple(flags));out=list(sig);out[side]=rr;return tuple(out)

def main():
    start=time.perf_counter();p2=path(2);c4=join('P',p2,p2);k23=join('P',c4,p2)
    u21=join('S',c4,p2)
    cases=[('path2_left_shared_neighbor',p2,0),('cycle4_left_load2',c4,0),
      ('K2_3_left_load3',k23,0),('unequal21_left',u21,0),('unequal21_right',u21,1)]
    records=[]
    for name,g,side in cases:
        t=time.perf_counter();states=enumerate_states(g)[0];h=extend(g,side)
        predicted={w for s in states for A in range(Q) if (w:=state_extend(s,side,A)) is not None}
        actual,proper,star=enumerate_states(h);assert predicted==actual
        records.append({'name':name,'side':side,'parent_n':h['n'],'parent_m':len(h['edges']),
          'old_port_degrees':[len(adjacency(g)[v]) for v in g['ports']],
          'parent_port_degrees':[len(adjacency(h)[v]) for v in h['ports']],
          'old_labeled_states':len(states),'parent_labeled_states':len(actual),
          'parent_proper_colorings':proper,'parent_star_colorings':star,
          'exact_state_set_equality':True,'seconds':time.perf_counter()-t})
    res={'schema':'astra-cycle8-independent-terminal-extension/v1','cases':records,
      'total_body_seconds':time.perf_counter()-start}
    Path(__file__).with_name('EXTENSION_RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps(res,indent=2))
if __name__=='__main__':main()

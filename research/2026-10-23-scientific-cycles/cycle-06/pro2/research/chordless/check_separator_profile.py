"""A targeted receiving check of exact nonadjacent-separator join profiles."""
import argparse
import json
import resource
import time
from pathlib import Path
from separator_profile import profile,join,max_mass,BichromaticCycle


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=Path(__file__).with_name('RESULT.json'))
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('JOIN_RESULT.json'))
    args=parser.parse_args()
    wall,cpu=time.perf_counter(),time.process_time()
    source=json.loads(args.input.read_text())
    obj=next(o for o in source['selected_complete_fixtures'] if o['terminal_colors']==[0,0])
    colors=dict(obj['colors'])
    parts=[]
    for path in obj['paths']:
        parts.append(profile(path,list(zip(path,path[1:])),colors))
    running=parts[0];intermediate=[]
    for p in parts[1:]:
        running=join(running,p);intermediate.append(running)
    direct=profile(obj['vertices'],obj['edges'],colors)
    assert running==direct
    left=join(join(parts[0],parts[1]),parts[2])
    assert all(left[p]['mode']=='connected' for p in ('01','02','03'))
    assert all(parts[3][p]['mode']=='apart' for p in ('01','02','03'))
    assert join(left,parts[3])==direct
    # The forbidden fourth short path duplicates channel01.
    fourth=profile([0,1,100],[(0,100),(100,1)],{0:0,1:0,100:1})
    try:
        join(left,fourth)
    except BichromaticCycle as e:
        obstruction=str(e)
    else:
        raise AssertionError("missing exact C4 obstruction")
    report={'status':'PASS','source_fixture_path_lengths':[len(p)-1 for p in obj['paths']],
            'short_side_profile':left,'long_side_profile':parts[3],
            'sequential_profiles':intermediate,'full_profile':direct,
            'max_component':max_mass(direct),'blocked_join':obstruction,
            'body_wall_seconds':time.perf_counter()-wall,'body_cpu_seconds':time.process_time()-cpu,
            'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'scope':'targeted author receiving check, not independent proof review'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('short_side_profile','long_side_profile','sequential_profiles','full_profile')},indent=2))


if __name__=='__main__':
    main()

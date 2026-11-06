"""Execute the paid write/retention operation; preserve every emitted port record."""
import csv, hashlib, json, struct, time
from fractions import Fraction as Q
from pathlib import Path
from plan import make_plan, save, ROOT
from controller import FixedController
from native_source import PortSource
from exact import require


def main():
    start=time.perf_counter(); plan=make_plan();save(ROOT/'results/PLAN.json',plan)
    planner_seconds=time.perf_counter()-start
    t=time.perf_counter(); source=PortSource(plan);native_prepare_seconds=time.perf_counter()-t
    controller=FixedController(plan);source.write(controller.write_command)
    write_audit=source.audit();steps=plan['executed_schedule_intervals']
    dt=plan['sample_interval'];target=[float(x) for x in plan['target']]
    scale=1<<plan['fixed_point_fraction_bits']; settle_steps=int(plan['settling_time_after_switch']/dt)
    record_path=ROOT/'results/PORT_RECORDS.bin'
    digest=hashlib.sha256(); trace=[]; max_late=0.; read_min=[float('inf')]*6;read_max=[-float('inf')]*6
    t=time.perf_counter()
    with record_path.open('wb') as f:
        for k in range(steps):
            reading=source.read(k)
            command=controller.retention_command(reading)
            packed=struct.pack('<12q',*reading,*command)
            f.write(packed);digest.update(packed)
            y=[v/scale for v in reading]
            relative=max(abs(v/z-1) for v,z in zip(y,target))
            if k>=settle_steps:
                max_late=max(max_late,relative)
                for j,v in enumerate(y):read_min[j]=min(read_min[j],v);read_max[j]=max(read_max[j],v)
            if k%1024==0 or k in (settle_steps,steps-1):
                trace.append([float(k*dt),relative]+y+[v/scale for v in command])
            source.advance(command,k)
    loop_seconds=time.perf_counter()-t
    final=source.audit();cost=source.costs();ledger=controller.ledger()
    require(ledger['observed_integer_bits_max']<=plan['controller_integer_width_bound'])
    require(ledger['calls']==steps and record_path.stat().st_size==steps*96)
    with (ROOT/'results/TRACE.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['time_after_switch','relative_port_error_to_nominal']+
            [f'y{i+1}' for i in range(6)]+[f'command{i+1}' for i in range(6)])
        w.writerows(trace)
    result={'status':'PASS','scope':'executed software source, virtual source time; no physical hardware/real-time claim',
        'planner_seconds':planner_seconds,'native_preparation_seconds':native_prepare_seconds,
        'control_and_native_loop_seconds':loop_seconds,'total_wall_seconds':time.perf_counter()-start,
        'write_end_diagnostic':write_audit,'final_diagnostic':final,
        'maximum_recorded_relative_error_after_settling':max_late,
        'recorded_port_min_after_settling':read_min,'recorded_port_max_after_settling':read_max,
        'theorem_relative_error_bound':plan['port_relative_error_after_settling'],
        'record_format':'little-endian signed int64, six read integers then six command integers per row; divide by 2^40; uniform virtual times k/131072 after the nine-unit write',
        'record_rows':steps,'record_bytes':record_path.stat().st_size,'record_sha256':digest.hexdigest(),
        'controller':ledger,'native_cost':cost,
        'noisy_scope':'deterministic bounded biases; theorem permits all signals within declared bounds',
        'clock_execution':'zero jitter and zero virtual command latency; theorem additionally permits declared jitter/latency'}
    save(ROOT/'results/EXECUTION.json',result)
    print(json.dumps({k:result[k] for k in ['status','planner_seconds','native_preparation_seconds',
        'control_and_native_loop_seconds','maximum_recorded_relative_error_after_settling','record_bytes','record_sha256']},indent=2),flush=True)


if __name__=='__main__':main()

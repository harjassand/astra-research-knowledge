"""Reproduce source-data calculations and the exact energy-phase construction.

Primary measurements are Hartmann et al. Nature Energy (2026), versioned data
https://doi.org/10.5281/zenodo.21997337, source-data Figures 6 and 7.
The fleet experiment below is SYNTHETIC. It is not an observed intervention.
Run with the bundled Python, numpy, scipy, matplotlib, and openpyxl.
"""
from __future__ import annotations
import csv, hashlib, json, math, sys, time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.signal import lfilter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
if not DATA.exists():
    DATA = ROOT.parent / 'grid_observations_data'

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def midpoint_phases(energies, period=F(60)):
    e = [F(x) for x in energies]
    if not e or min(e) <= 0:
        raise ValueError('Positive event-energy weights are required.')
    total, running, out = sum(e), F(0), []
    for value in e:
        out.append(period * (running + value / 2) / total)
        running += value
    return out

def nearest_tick(phase, tick, period=F(60)):
    # Exact nearest rounding; ties go to the greater tick, then wrap modulo T.
    if period / tick != int(period / tick):
        raise ValueError('The period must contain an integer number of ticks.')
    x = phase / tick
    n = (2 * x.numerator + x.denominator) // (2 * x.denominator)
    return (n * tick) % period

def discrepancy_certificate(energies, phases, period=F(60)):
    """Exact span of a primitive of the weighted event train minus its mean.

    Simultaneous events are grouped. Extrema occur immediately before/after
    jumps, so no temporal sampling or optimization tolerance enters this check.
    """
    groups = defaultdict(F)
    for e, phase in zip(energies, phases, strict=True):
        groups[F(phase) % period] += F(e)
    total = sum(groups.values(), F(0))
    running, values = F(0), []
    for phase, e in sorted(groups.items()):
        before = running - total * phase / period
        values.extend((before, before + e))
        running += e
    low, high = min(values), max(values)
    return {'span_J': float(high-low), 'span_exact': str(high-low),
            'minimum_exact': str(low), 'maximum_exact': str(high),
            'total_absolute_energy_J': float(total), 'distinct_slots': len(groups)}

def primary_measurements():
    wb = load_workbook(DATA/'source_data_fig_6.xlsx', read_only=True, data_only=True)
    rows = list(wb['Panel a'].values)
    locations = ['PQ ID 023', 'PQ ID 007', 'PQ ID 051']
    dates = [rows[1][i] for i in range(1,17)]
    profiles = np.array([[[rows[t+2][offset+j] for t in range(20)]
                          for j in range(1,17)] for offset in [0,18,36]],float)
    assert profiles.shape == (3,16,20)
    wb.close()
    profiles -= profiles.mean(axis=2,keepdims=True)
    c = np.fft.rfft(profiles,axis=2)/20
    mag = abs(c[:,:,1])
    lower = np.maximum(2*mag.max(axis=0)-mag.sum(axis=0),0)
    # These are sampled Fourier coefficients; no subsecond reconstruction.
    measured_sum = abs(c[:,:,1].sum(axis=0))
    weekly=[]
    for j,date in enumerate(dates):
        weekly.append({'week': date, 'c1_magnitude_W': dict(zip(locations,map(float,mag[:,j]))),
            'continuous_phase_minimum_abs_c1_W':float(lower[j]),
            'continuous_phase_minimum_sinusoid_peak_W':float(2*lower[j]),
            'recorded_sum_abs_c1_W':float(measured_sum[j]),
            'floor_fraction_of_sum_magnitudes':float(lower[j]/mag[:,j].sum())})
    with (ROOT/'measured_fundamental_bounds.csv').open('w',newline='') as f:
        wr=csv.writer(f);wr.writerow(['week','PQ023_abs_c1_W','PQ007_abs_c1_W','PQ051_abs_c1_W',
                                     'best_possible_abs_c1_W','recorded_sum_abs_c1_W'])
        for j,date in enumerate(dates):wr.writerow([date,*mag[:,j],lower[j],measured_sum[j]])
    w7=load_workbook(DATA/'source_data_fig_7.xlsx',read_only=True,data_only=True)
    r7=list(w7['panel b'].values)
    ireland={}
    for label,j in [('December 2016',5),('December 2021',6)]:
        v=np.array([r7[t+2][j] for t in range(60)],float)
        ireland[label]={'minimum_mHz':float(min(v)),'maximum_mHz':float(max(v)),
            'half_range_mHz':float(np.ptp(v)/2),'fundamental_sinusoid_peak_mHz':float(2*abs(np.fft.rfft(v)[1])/60)}
    rf=list(w7['panel f'].values)
    firmware={}
    for label,timecol,valcol in [('after Current 3',4,5),('after Current 1',4,6)]:
        samples=[(r[timecol],float(r[valcol])) for r in rf[2:]
                 if r[timecol] is not None and isinstance(r[valcol],(int,float))]
        t0=samples[0][0]
        tt=np.array([(t-t0).total_seconds() for t,v in samples])
        vv=np.array([v for t,v in samples])
        threshold=0.5*max(vv)
        above=vv>threshold
        starts=[]
        for j,(t,b) in enumerate(zip(tt,above)):
            if b and (j==0 or not above[j-1] or tt[j]-tt[j-1]>1.5): starts.append(float(t))
        phase=np.array(starts)%60
        firmware[label]={'threshold_A':float(threshold),'event_start_seconds':starts,
            'seconds_modulo_60':phase.tolist(),
            'circular_concentration':float(abs(np.exp(2j*np.pi*phase/60).mean())),
            'sample_count':len(samples), 'scope':'Short descriptive trace; no independent event/population inference.'}
    w7.close()
    return {'primary_data':{'figure6_sha256':sha256(DATA/'source_data_fig_6.xlsx'),
                           'figure7_sha256':sha256(DATA/'source_data_fig_7.xlsx'),
                           'version_doi':'10.5281/zenodo.21997337'},
        'measurement_definitions':{'Fourier':'c_k=(1/L) sum_j p_j exp(-2 pi i k j/L); sinusoid peak=2|c_k|.',
             'phase_floor':'max(2 max_i |c_i|-sum_i |c_i|,0); generous independently shiftable-profile model.',
             'source_profile_resolution_s':3,'number_of_weeks':16,'number_of_profiles':48,
             'uncertainty':'Published profiles do not supply metrological confidence intervals or resolve subsecond power.'},
        'weekly_fundamental_bounds':weekly,
        'ireland':ireland,'firmware':firmware}, profiles

def make_kernel(dt, period=60.0):
    t=np.arange(round(period/dt))*dt
    # Two nonoverlapping finite pulses; signed recharge/draw template, L1=1.
    tri=lambda x: np.maximum(1-abs((x-.15)/.15),0)
    h=.65*tri(t)-.35*tri(t-1.0)
    h/=np.sum(abs(h))*dt
    return h

def physical_replay(energies, phases, h, dt=.001, tau=5.0):
    # Defined model: piecewise-constant kernel with dt-wide bins and exact slots.
    n=len(h);events=np.zeros(n)
    for e,phase in zip(energies,phases):
        index=round(float(phase)/dt)%n
        assert abs(float(phase)-index*dt)<1e-8 or abs(float(phase)-60)<1e-8
        events[index]+=float(e)
    p=np.fft.irfft(np.fft.rfft(events)*np.fft.rfft(h),n=n)
    u=p-p.mean()
    primitive=np.r_[0,np.cumsum(u)*dt]
    # Exact update for z'= -z/tau - u, where z=M*f, on every held-power bin.
    decay=math.exp(-dt/tau)
    gain=-tau*(-math.expm1(-dt/tau))
    z0run=lfilter([gain],[1,-decay],u)
    z_initial=z0run[-1]/(1-decay**n)
    z=lfilter([gain],[1,-decay],u,zi=[decay*z_initial])[0]
    return {'primitive_span_J':float(np.ptp(primitive)),
            'normalized_frequency_peak_J':float(max(abs(z))),
            'power_peak_deviation_W':float(max(abs(u)))},u,z

def synthetic_construction():
    start=time.perf_counter(); rng=np.random.default_rng(20261105)
    period=F(60);tick=F(1,1000);dt=.001
    h=make_kernel(dt)
    results=[];last_traces=None
    for n in [16,64,256,1024,4096]:
        energies=[int(v) for v in rng.integers(5,101,size=n)]
        ideal=midpoint_phases(energies,period)
        exact=discrepancy_certificate(energies,ideal,period)
        assert F(exact['span_exact'])==max(energies)
        rounded=[nearest_tick(p,tick,period) for p in ideal]
        cert=discrepancy_certificate(energies,rounded,period)
        bound=F(max(energies))+sum(energies)*tick/period
        assert F(cert['span_exact'])<=bound
        aligned=[F(0)]*n
        random_phases=[int(k)*tick for k in rng.integers(0,60000,size=n)]
        row={'N':n,'max_event_energy_J':max(energies),'total_absolute_energy_J':sum(energies),
             'ideal_exact_span_J':exact['span_J'],'rounded_exact_certificate':cert,
             'quantization_upper_bound_J':float(bound),'clock_tick_s':float(tick)}
        trace=[]
        for label,phases in [('aligned',aligned),('independent_random_once',random_phases),('weighted_midpoint',rounded)]:
            replay,p,z=physical_replay(energies,phases,h)
            pointcert=discrepancy_certificate(energies,phases,period)
            assert replay['primitive_span_J']<=pointcert['span_J']+1e-6
            assert replay['normalized_frequency_peak_J']<=pointcert['span_J']+1e-6
            row[label]={**replay,'event_discrepancy_span_J':pointcert['span_J']}
            trace.append((label,p,z))
        results.append(row)
        if n==1024:last_traces=trace
    # Timer-resolution sweep on the same fixed illustrative roster.
    energies=[5+(73*i)%96 for i in range(1000)]
    ideal=midpoint_phases(energies)
    sweep=[]
    for tick2 in [F(1,1000),F(1,100),F(1,10),F(1),F(3)]:
        phases=[nearest_tick(p,tick2) for p in ideal]
        cert=discrepancy_certificate(energies,phases)
        sweep.append({'tick_s':float(tick2),'exact_compiled_span_J':cert['span_J'],
            'universal_quantization_bound_J':float(max(energies)+F(sum(energies))*tick2/60),
            'additional_per_event_jitter_2ms_bound_J':float(F(cert['span_exact'])+2*F(sum(energies))*F(2,1000)/60)})
    # Finite IEEE-independent exact certificate / example configuration.
    example_e=[F(10),F(20),F(5),F(15)]
    example_p=midpoint_phases(example_e)
    example={'period_s':60,'energies_J':list(map(str,example_e)),
             'phases_s':list(map(str,example_p)),
             'certificate':discrepancy_certificate(example_e,example_p)}
    (ROOT/'example_schedule.json').write_text(json.dumps(example,indent=2))
    return {'scope':'SYNTHETIC mathematical implementation check, not field measurements or deployed controller.',
        'seed':20261105,'period_s':60,'kernel':'signed finite triangular holds, absolute integral 1',
        'kernel_resolution_s':dt,'grid_model':'z=M*f; dz/dt+z/5 seconds=-u; illustrative, not fitted to a real grid.',
        'population_runs':results,'timer_sweep':sweep,'example':example,
        'local_execution_seconds':time.perf_counter()-start},last_traces

def make_figure(primary, profiles, synthetic, traces):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                        'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(13.4,9),layout='constrained')
    colors=['#0b6e75','#cc5a19','#7566a5']
    ax=axes[0,0]
    t=np.arange(20)*3
    for i,name in enumerate(['PQ 023','PQ 007','PQ 051']):
        ax.plot(t,profiles[i,0],marker='o',markersize=3,label=name,color=colors[i])
    ax.set(title='Measured building profiles: source label 24 March 2024',xlabel='Second within the minute',ylabel='Periodic power component (W)')
    ax.legend(frameon=False)
    ax=axes[0,1]
    weeks=primary['weekly_fundamental_bounds']; x=np.arange(1,17)
    ax.plot(x,[w['recorded_sum_abs_c1_W'] for w in weeks],'-o',label='Recorded sum of three profiles',color=colors[0],markersize=3)
    ax.plot(x,[w['continuous_phase_minimum_abs_c1_W'] for w in weeks],'-s',label='Exact minimum under arbitrary phase shifts',color=colors[1],markersize=3)
    ax.set(title='Measured profiles leave a dominant-source floor',xlabel='Weekly source profile (1–16)',ylabel='Magnitude of complex 1/min coefficient (W)',ylim=(0,140))
    ax.legend(frameon=False,fontsize=9)
    ax=axes[1,0]
    for row, label in enumerate(['after Current 3','after Current 1']):
        times=primary['firmware'][label]['event_start_seconds']
        ax.scatter(times,[row]*len(times),s=45,color=colors[row],label=label)
        for val in times:
            ax.annotate(str(int(val)%60),(val,row),xytext=(0,9),textcoords='offset points',ha='center',fontsize=8)
    ax.set(yticks=[0,1],yticklabels=['Updated trace (source label Current 3)','Other trace (source label Current 1)'],
           xlabel='Seconds from start of published after-update trace',ylim=(-.5,1.5),
           title='Measured irregular gaps retain minute phase\nNumbers show event time modulo 60 s')
    ax=axes[1,1]
    runs=synthetic['population_runs']
    for label,shown,color in [('aligned','Aligned',colors[1]),('independent_random_once','Independent random phases (one draw)',colors[2]),('weighted_midpoint','Weighted midpoint, 1 ms clock',colors[0])]:
        ax.loglog([r['N'] for r in runs],[r[label]['event_discrepancy_span_J'] for r in runs],'-o',label=shown,color=color)
    ax.set(title='Synthetic check: indivisible event-energy imbalance',xlabel='Number of simulated devices',ylabel='Cumulative event-energy span (J)')
    ax.legend(frameon=False,fontsize=8)
    fig.suptitle('Observed minute-locked forcing and a finite scheduling construction',fontsize=16)
    fig.savefig(ROOT/'evidence_and_construction.png',dpi=190)
    fig.savefig(ROOT/'evidence_and_construction.pdf')
    plt.close(fig)

def main():
    primary,profiles=primary_measurements()
    synthetic,traces=synthetic_construction()
    result={'primary_reanalysis':primary,'synthetic_validation':synthetic}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2))
    make_figure(primary,profiles,synthetic,traces)
    floors=[r['continuous_phase_minimum_abs_c1_W'] for r in primary['weekly_fundamental_bounds']]
    print(json.dumps({'measured_phase_only_floor_W':[min(floors),max(floors)],
        'firmware_starts':primary['firmware'],
        'synthetic_population_table':[{'N':r['N'],**{k:r[k]['event_discrepancy_span_J'] for k in ['aligned','independent_random_once','weighted_midpoint']}} for r in synthetic['population_runs']],
        'timer_sweep':synthetic['timer_sweep'],
        'local_execution_seconds':synthetic['local_execution_seconds']},indent=2))

if __name__=='__main__':main()

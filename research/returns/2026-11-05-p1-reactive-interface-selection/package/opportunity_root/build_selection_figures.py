"""Reproduce selection figures from original observations and published model inputs.

No synthetic dataset is used. The local-shell clock is an explicitly conditional
algebraic consequence of a published model, not an empirical conversion time.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output'/'selection'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
    'axes.spines.top':False,'axes.spines.right':False,
    'axes.labelcolor':'#263649','text.color':'#263649',
    'axes.titleweight':'bold','savefig.facecolor':'white'})

def evidence():
    rows=json.loads((ROOT/'table_s2_transcribed.json').read_text())
    categories=['Correct first phase','Different ranked phase',
                'Observed phase outside inventory','Source label ambiguous']
    colors=['#147d92','#d65e41','#d5a544','#9c8eb7']
    counts=[]
    for high in [True,False]:
        cases=[r for r in rows if (r['margin_meV_per_atom']>=60)==high]
        c=[0]*4
        for r in cases:
            i=0 if r['matches_observation'] else (
                3 if r['reactants']=='NaNO3-TiO2' else (
                2 if r['observed_first'] not in r['phases'] else 1))
            c[i]+=1
        counts.append(c)
    fig,axs=plt.subplots(1,2,figsize=(11.2,5.15),gridspec_kw={'width_ratios':[1.1,1]})
    ax=axs[0];left=np.zeros(2)
    for i,(label,color) in enumerate(zip(categories,colors)):
        vals=np.array(counts)[:,i]
        ax.barh([1,0],vals,left=left,color=color,height=.42,label=label)
        for j,v in enumerate(vals):
            if v: ax.text(left[j]+v/2,1-j,str(v),ha='center',va='center',color='white',fontweight='bold')
        left+=vals
    ax.set_yticks([1,0],['Margin ≥60','Margin <60'])
    ax.set_xlim(0,25);ax.set_xticks([0,5,10,15,20,25]);ax.set_xlabel('Number of published reactions')
    ax.set_title('A  First-phase prediction',loc='left',pad=15)
    ax.text(0,1.36,'Energy margin in meV per atom',fontsize=9,color='#5b6979')
    ax.text(0,-.47,'Threshold selected on these data; not external validation.',fontsize=8.8,color='#5b6979')
    ax.set_ylim(-.55,1.55);ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0)
    ax=axs[1]
    d=pd.read_csv(ROOT.parent/'opportunity_materials'/'chen_matched_temperatures.csv')
    d=d[(d.target=='LiMgPO4') & d.temperature_c.isin([800,900])].sort_values('temperature_c')
    for col,label,color,marker in [('predicted','Selected precursors','#147d92','o'),('traditional','Traditional precursors','#d65e41','s')]:
        ax.plot(d.temperature_c,d[col],color=color,lw=2,marker=marker,ms=8,label=label)
        for r in d.itertuples():
            val=getattr(r,col)
            dy=.035 if (col=='predicted' and r.temperature_c==800) or (col=='traditional' and r.temperature_c==900) else -.07
            ax.text(r.temperature_c,val+dy,f'{val:.2f}',color=color,ha='center',fontweight='bold')
    ax.set_title('B  LiMgPO₄ route ranking reverses',loc='left',pad=15)
    ax.set_xticks([800,900]);ax.set_xlim(780,920);ax.set_ylim(.15,.9)
    ax.set_xlabel('Annealing temperature (°C), separate 8 h runs')
    ax.set_ylabel('Target diffraction score')
    ax.legend(loc='upper left',frameon=False,fontsize=9)
    ax.text(0,-.25,'Scores are not mass purity; per-cell error bars are unavailable.',transform=ax.transAxes,fontsize=8.7,color='#5b6979')
    handles,labels=axs[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower left',bbox_to_anchor=(.065,.005),ncol=2,frameon=False,fontsize=9)
    fig.subplots_adjust(left=.12,right=.98,bottom=.26,top=.85,wspace=.43)
    fig.savefig(OUT/'synthesis_evidence.png',dpi=190)
    plt.close(fig)

def clock():
    df=pd.read_excel(ROOT/'41563_2026_2596_MOESM3_ESM.xlsx',sheet_name='Figure_2B')
    df['local_shell_completion_s']=(1e-5)**2/(2*df.y_KD_cm2_s)
    df.to_csv(ROOT/'local_shell_clock_diagnostic.csv',index=False)
    pars=[1e13,2e13,5e13,1e14]
    maxima=[.392,.534,.932,.482]
    diagnostic={
        'model':'h(t)=sqrt(2 K_D t); h=r0; constant coefficient and an already-active homogeneous shell',
        'r0_cm':1e-5,'r0_micrometres':.1,
        'source_units':'Figure 2B axis and source workbook: cm^2/s',
        'at_1000_K':df[df.temperature.eq(1000)][['formula','y_KD_cm2_s','local_shell_completion_s']].to_dict('records'),
        'status':'Conditional mathematical calculation, not observed time or the complete ReactCA prediction',
        'scoring_sensitivity':{'s':pars,'maximum_timewise_BaTiO3_fraction':maxima,
          'source':'Karan et al. 2026 Supplementary Table S3; maxima occur at different times, not final yields'}}
    (ROOT/'clock_diagnostic.json').write_text(json.dumps(diagnostic,indent=2))
    fig,axs=plt.subplots(1,2,figsize=(11.2,4.6))
    ax=axs[0];ax.plot(np.array(pars)/1e13,maxima,'o-',color='#147d92',lw=2)
    for x,y in zip(np.array(pars)/1e13,maxima):ax.annotate(f'{y:.3f}',(x,y),xytext=(0,8),textcoords='offset points',ha='center')
    ax.set_xlabel('Scoring scale s / 10¹³');ax.set_ylabel('Maximum timewise BaTiO₃ mole fraction')
    ax.set_ylim(.25,1.05);ax.set_xticks([1,2,5,10]);ax.set_title('A  Strong model: scale sensitivity',loc='left',pad=15)
    ax.text(0,-.25,'Published model sensitivity, not new experiments or final purity.',transform=ax.transAxes,fontsize=8.7,color='#5b6979')
    ax=axs[1];d=df[df.temperature.eq(1000)].sort_values('local_shell_completion_s')
    ax.scatter(1e6*d.local_shell_completion_s,np.arange(len(d)),color='#147d92',s=44)
    ax.set_yticks(np.arange(len(d)),d.formula)
    ax.set_xscale('log');ax.set_xlabel('Conditional shell traversal time (microseconds)')
    ax.set_title('B  Local transport is not the bulk clock',loc='left',pad=15)
    ax.text(0,-.25,'Derived at 1000 K and assumed r₀ = 0.1 µm; activity is assumed.',transform=ax.transAxes,fontsize=8.7,color='#5b6979')
    fig.subplots_adjust(left=.07,right=.98,bottom=.26,top=.84,wspace=.49)
    fig.savefig(OUT/'synthesis_clock.png',dpi=190);plt.close(fig)

if __name__=='__main__':
    evidence();clock()
    print(OUT/'synthesis_evidence.png')
    print(OUT/'synthesis_clock.png')

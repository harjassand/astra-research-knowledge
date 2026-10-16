"""Own numerical checks of exposure and an explicitly unacquired fixed-rate model."""
import json
from pathlib import Path
import math
import numpy as np
from acquire_and_analyze import read_xlsx

ROOT=Path(__file__).resolve().parent


def analyze_electrical():
    x=read_xlsx(ROOT/"external_excluded_from_publication/final_SIFig7.xlsx")
    data=x["Figure 7 b"]["cells"]
    r=range(2,55001)
    t=np.array([float(data[f"B{i}"]) for i in r])
    v=np.array([float(data[f"C{i}"]) for i in r])
    current=np.array([float(data[f"D{i}"]) for i in r])
    out={"scope":"Terminal trace for 10s/1s waveform only, not independently measured interfacial exposure. Sampled trapezoid integrals omit endpoint intervals; clipping/aliasing and current origin unknown.",
         "header":{k:data[k] for k in ["B1","C1","D1"]},"sample_count":len(t),"t_min":t[0],"t_max":t[-1],
         "voltage_min":float(v.min()),"voltage_max":float(v.max()),"current_min_A":float(current.min()),"current_max_A":float(current.max()),
         "min_voltage_cell":f"Figure 7 b!C{int(v.argmin())+2}","max_voltage_cell":f"Figure 7 b!C{int(v.argmax())+2}",
         "signed_charge_C":float(np.trapezoid(current,t)),"absolute_charge_C":float(np.trapezoid(abs(current),t)),
         "positive_charge_C":float(np.trapezoid(np.maximum(current,0),t)),"negative_charge_C":float(np.trapezoid(np.minimum(current,0),t)),
         "signed_terminal_work_J":float(np.trapezoid(v*current,t)),"absolute_terminal_work_J":float(np.trapezoid(abs(v*current),t)),
         "samples_outside_command_range":int(((v<-.1)|(v>1.5)).sum()),
         "samples_at_stored_extreme_current":int(((current==current.min())|(current==current.max())).sum()),
         "selected_samples":[]}
    for time in [.0002,.001,.003,.005,.01,.02,.05,.1,.25,.5,.9,.9998,1.0002,1.001,1.005,1.01,1.02,1.05,1.1,1.25,1.5,2]:
        j=int(np.argmin(abs(t-time)))
        out["selected_samples"].append({"row":j+2,"t":float(t[j]),"v":float(v[j]),"i_A":float(current[j])})
    cc=x["Figure 7 c"]["cells"]; dd=x["Figure 7 d"]["cells"]
    out["grid_signed_current_and_FR"]=[]
    for row in [7,13,19,25,12,18,24]:
        out["grid_signed_current_and_FR"].append({"row":row,"h_s":cc.get(f"B{row}"),"d_s":cc.get(f"C{row}"),
          "current_stored":cc.get(f"D{row}"),"current_header":cc["D1"],"maximum_FR_percent":dd.get(f"D{row}"),
          "cells":[f"Figure 7 c!B{row}:D{row}",f"Figure 7 d!D{row}"]})
    (ROOT/"electrical_checks.json").write_text(json.dumps(out,indent=2)+"\n")
    return out


def model(h,d,k,r,w,bplus,beta,A):
    """Three chemical configurations W,I,R. All transition coefficients fixed.

    Positive: W -> I at k, I -> R at r. Negative: I,R -> W at w.
    Positive output bplus-A*I; negative output beta. Simplex and nonnegative outputs.
    """
    ek,er,ew=math.exp(-k*h),math.exp(-r*h),math.exp(-w*d)
    if abs(k-r)<1e-9*max(k,r):
        transfer=k*h*er
        jint=(1-er*(1+r*h))/r
    else:
        transfer=k*(er-ek)/(k-r)
        jint=k*((1-er)/r-(1-ek)/k)/(k-r)
    # Before positive hold, W0 = 1-ew+ew*ek*W0.
    W0=(1-ew)/(1-ew*ek)
    # I0 = ew*(er*I0+transfer*W0).
    I0=ew*transfer*W0/(1-ew*er)
    Iintegral=I0*(1-er)/r+W0*jint
    b=(h*bplus-A*Iintegral+d*beta)/(h+d)
    return b, {"W0":W0,"I0":I0,"R0":1-W0-I0,"I_mean_positive":Iintegral/h}


def analyze_model():
    checks=json.loads((ROOT/"workbook_checks.json").read_text())
    bplus=checks["static_dynamic_sheet"][8]["b_per_Ain"]["decimal"]
    rows=[v for v in checks["grid_rows"] if v["duty_h_over_d"] in {"10","100"}]
    beta=1.75 # Illustrative fixed endpoint between neighboring measured static levels.
    def evaluate(logrates,fitrows):
        k,r,w=np.exp(logrates[:3]);A=bplus/(1+math.exp(-logrates[3]))
        return np.array([model(float(v["h_s"] if "/" not in v["h_s"] else eval_fraction(v["h_s"])),float(eval_fraction(v["d_s"])),k,r,w,bplus,beta,A)[0] for v in fitrows])
    observed=np.array([x["ethane_per_Ain"]["decimal"] for x in rows])
    starts=[[-.7,-3,2,2],[0,-2,3,3],[2,-3,4,4],[-1,-5,1,4]]
    # Small deterministic bounded coordinate search avoids undeclared dependencies.
    # Bounds are an illustrative finite-timescale prior, not experimental rate bounds.
    lower=np.array([math.log(.01)]*3+[-12.]);upper=np.array([math.log(1e4)]*3+[12.])
    def objective(p):
        return float(sum((evaluate(p,rows)-observed)**2))
    fits=[]
    for start in starts:
        point=np.clip(np.array(start,dtype=float),lower,upper);score=objective(point)
        for step in [.8,.3,.1,.03,.01,.003,.001]:
            for _ in range(200):
                improved=False
                for j in range(4):
                    for direction in [-1,1]:
                        candidate=point.copy();candidate[j]+=direction*step;candidate=np.clip(candidate,lower,upper)
                        value=objective(candidate)
                        if value<score:
                            point,score=candidate,value;improved=True
                if not improved:break
        fits.append((score,point))
    score,point=min(fits,key=lambda f:f[0])
    rates=np.exp(point[:3]); A=bplus/(1+math.exp(-point[3]))
    k,r,w=map(float,rates)
    parameters={"k_per_s":k,"r_per_s":r,"w_per_s":w,"bplus":bplus,"beta_illustrative":beta,"A":A,
                "status":"DESCRIPTIVE_FIT_NOT_ACQUIRED_PARAMETERS","fixed_across_protocols":True}
    out={"parameters":parameters,"seven_point_fit_RMSE":math.sqrt(score/len(rows)),"fit_rows":[],
         "illustrative_fixed_parameters":{"k_per_s":.5,"r_per_s":.1,"w_per_s":10,"bplus":bplus,"beta":beta,"A":bplus},
         "illustrative_duty10":[],"fit_scope":"Seven b point estimates only. Does not fit X/S separately, electrical traces, full 30-condition grid or state-specific data; no error model or historical originality claim.",
         "full_grid_holdout":[]}
    for item,pred in zip(rows,evaluate(point,rows)):
        out["fit_rows"].append({"row":item["row"],"h_s":item["h_s"],"d_s":item["d_s"],"observed":item["ethane_per_Ain"]["decimal"],"predicted":float(pred),"residual":float(pred-item["ethane_per_Ain"]["decimal"])})
    for h,d in [(.01,.001),(.1,.01),(1,.1),(10,1),(100,10),(1000,100)]:
        b,state=model(h,d,.5,.1,10,bplus,beta,bplus)
        out["illustrative_duty10"].append({"h":h,"d":d,"mean_b":b,"state":state})
    for item in checks["grid_rows"]:
        if item in rows: continue
        b,state=model(float(eval_fraction(item["h_s"])),float(eval_fraction(item["d_s"])),k,r,w,bplus,beta,A)
        out["full_grid_holdout"].append({"row":item["row"],"observed":item["ethane_per_Ain"]["decimal"],"predicted":b,"residual":b-item["ethane_per_Ain"]["decimal"]})
    # Static + held indefinitely: W,I -> 0, hence b -> bplus. Static -: W->1, b->beta.
    # Direct response after ideal pure W reset has I(t)=k*(exp(-rt)-exp(-kt))/(k-r).
    out["predicted_peak_time_after_saturating_write_s"]=math.log(k/r)/(k-r) if abs(k-r)>1e-12 else 1/k
    out["holdout_RMSE"]=float(np.sqrt(np.mean([x["residual"]**2 for x in out["full_grid_holdout"]])))
    (ROOT/"fixed_model_checks.json").write_text(json.dumps(out,indent=2)+"\n")
    return out


def eval_fraction(s):
    from fractions import Fraction
    return Fraction(s)


if __name__=="__main__":
    e=analyze_electrical()
    print(json.dumps({k:v for k,v in e.items() if k!="selected_samples"},indent=2))
    print(json.dumps({"selected_samples":e["selected_samples"]},indent=2))
    m=analyze_model()
    print(json.dumps({k:v for k,v in m.items() if k!="full_grid_holdout"},indent=2))

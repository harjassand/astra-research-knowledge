"""Matched material and collector inventory; explicit unqualified physical scaling hypotheses."""
from fractions import Fraction as F
import math,json,time,resource
from pathlib import Path
start=time.monotonic(); eta=.8052327811687515
n=4; k=1/(1+math.sqrt(2)); H=1/(n*k*k)
# 4 disks fit in original circular envelope, same porous oxide volume.
assert abs(n*k*k*H-1)<1e-14
# pins length scales H, cross-section scales 1/(n H), so inventory and parallel axial R unchanged.
pin_radius=1/math.sqrt(n*H);pin_wetted_area=n*pin_radius*H
rows=[]
for exponent in [1,2]:
 radial_time=k**exponent
 axial_time=H**2
 # alpha = baseline fraction of completion time due to radial front; remainder axial transport.
 # Tnew/Told = alpha*k**p +(1-alpha)*H**2 in declared additive-times hypothesis.
 alpha_speed=(axial_time-1)/(axial_time-radial_time)
 # worst-case parasitics all on pins scales wetted area * completion time.
 alpha_all_pin=(axial_time-1/pin_wetted_area)/(axial_time-radial_time)
 # Illustrative 100% front-control only. No current-cap adjustment hidden.
 for collector_fraction in [0,.5,1]:
  hratio=radial_time*((1-collector_fraction)+collector_fraction*pin_wetted_area)
  charge_ratio=eta+(1-eta)*hratio
  rows.append(dict(p=exponent,collector_fraction=collector_fraction,time_ratio_front_only=radial_time,parasitic_charge_ratio_front_only=hratio,total_charge_ratio_same_metal_front_only=charge_ratio,FE_front_only=eta/charge_ratio,mean_current_ratio_front_only=charge_ratio/radial_time))
 rows.append(dict(p=exponent,minimum_radial_fraction_for_speed_gain=alpha_speed,minimum_radial_fraction_for_no_parasitic_increase_all_pin=alpha_all_pin))
# independent cube/volume accounting for radius 10mm, initial height2mm,pinradius.25mm design choice.
R=10;h=2;a=.25
original=math.pi*R*R*h;new=n*math.pi*(R*k)**2*(h*H)
assert abs(original-new)<1e-10
out=dict(status='DISCRIMINATING_SCALING_PREDICTION_NOT_MEASURED_GAIN',N=n,radius_ratio=k,height_ratio=H,pin_radius_ratio=pin_radius,total_pin_wetted_area_ratio=pin_wetted_area,axial_transport_time_ratio_if_diffusive=H**2,design_mm=dict(original_disk_radius=R,original_thickness=h,new_disk_radius=R*k,new_thickness=h*H,chosen_original_pin_radius=a,new_pin_radius=a*pin_radius),baseline_eta_used_for_conditional_charge_split=eta,rows=rows,seconds=time.monotonic()-start,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
Path(__file__).with_name('subdivision_result.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))

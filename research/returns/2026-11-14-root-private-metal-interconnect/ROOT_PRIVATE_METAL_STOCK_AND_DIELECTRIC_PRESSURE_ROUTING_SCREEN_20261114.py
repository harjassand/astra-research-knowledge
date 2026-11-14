#!/usr/bin/env python3
"""INTRODUCED private-metal switching-cell / passive-network design screen.
No measured wetting, contact, membrane, material or circuit is supplied.
Serial standard-library calculation, no external code/data/network.
"""
import math, json, random, cmath
from pathlib import Path
G=9.80665
P0=101325.
T0=298.15
PAR={
 "rho_metal_kg_m3":6000.,"mu_Pa_s":.002,"metal_sigma_S_m":3e6,
 "gamma_N_m":.5,"contact_cosine_hysteresis":.5,
 "feed_radius_m":100e-6,"feed_length_m":1e-3,
 "bridge_radius_m":250e-6,"bridge_length_m":.5e-3,
 "stroke_m3":.12e-9,"private_metal_m3":.5e-9,
 "gas_m3":20e-9,"diaphragm_area_m2":math.pi*(.5e-3)**2,"diaphragm_k_N_m":5.,
 "temperature_range_K":[288.15,313.15],"vertical_height_m":.02,
 "program_leg_s":.25,"contact_R_each_ohm":.020,
 "open_gap_m":.5e-3,"wall_film_thickness_m":1e-6,
 "aqueous_film_sigma_S_m":5.,"dielectric_film_sigma_S_m":1e-12,
 "dielectric_relative_permittivity":2.5,"stray_C_per_cell_F":10e-15,
 "package_R_per_open_cell_ohm":1e10,
 "terminal_count":16,"source_R_ohm":1000.,"load_R_ohm":10000.
}
EPS0=8.8541878128e-12
def hold_pressure(q,temp,par,compensated=False):
    gas=par["gas_m3"]
    # Compensated means an INTRODUCED freely expanding thermal volume,
    # not a built bag/vent. Its required extra stroke is explicitly paid.
    ratio=temp/T0
    volume=gas*ratio if compensated else gas
    pg=P0*gas*ratio/(volume-q)-P0
    pm=par["diaphragm_k_N_m"]*q/par["diaphragm_area_m2"]**2
    return pg+pm
def pin_pressure(par):
    # Two-meniscus contact-angle-hysteresis threshold law, introduced.
    # No actual surface supplies the simultaneous cosine/gamma/stick law.
    return 2*par["gamma_N_m"]*par["contact_cosine_hysteresis"]/par["feed_radius_m"]
def hydraulic_R(par):
    return 8*par["mu_Pa_s"]*par["feed_length_m"]/(math.pi*par["feed_radius_m"]**4)
def quintic(s):return 10*s**3-15*s**4+6*s**5
def quintic_d(s):return 30*s*s*(1-s)**2
def trajectory(par,compensated=True,intervals=2000):
    pc=pin_pressure(par);rh=hydraulic_R(par);A=par["diaphragm_area_m2"];vs=par["stroke_m3"];duration=par["program_leg_s"]
    # A coupled external head must supply or capture this force. No real
    # membrane-stroke tracking, positive pull coupling, or timing is built.
    phases=[]
    for forward in (True,False):
        records=[];work=0.;diss=0.;max_force=0.;max_pressure=0.
        last=None
        for i in range(intervals+1):
            s=i/intervals
            q=vs*quintic(s) if forward else vs*(1-quintic(s))
            qd=vs*quintic_d(s)/duration*(1 if forward else -1)
            p_internal=hold_pressure(q,T0,par,compensated)
            p_ext=p_internal+(pc if forward else -pc)+rh*qd
            f=A*p_ext
            wdot=p_ext*qd
            ddot=pc*abs(qd)+rh*qd*qd
            if last is not None:
                h=duration/intervals;work+=(last[0]+wdot)*h/2;diss+=(last[1]+ddot)*h/2
            last=(wdot,ddot);max_force=max(max_force,abs(f));max_pressure=max(max_pressure,abs(p_ext))
        phases.append({"forward":forward,"external_work_J":work,"dissipation_J":diss,
                       "max_abs_external_force_N":max_force,"max_abs_pressure_Pa":max_pressure})
    cycle_work=sum(x["external_work_J"] for x in phases)
    dissipated=sum(x["dissipation_J"] for x in phases)
    assert abs(cycle_work-dissipated)<1e-14
    return {"intervals_per_leg":intervals,"phases":phases,"cycle_work_J":cycle_work,
            "dissipation_J":dissipated,"no_mechanical_energy_reset":True}

def solve_complex(a,b):
    a=[list(row)+[z] for row,z in zip(a,b)];n=len(a)
    for k in range(n):
        pivot=max(range(k,n),key=lambda i:abs(a[i][k]))
        if abs(a[pivot][k])<1e-30:raise ArithmeticError("singular terminal model")
        a[k],a[pivot]=a[pivot],a[k];z=a[k][k]
        for j in range(k,n+1):a[k][j]/=z
        for i in range(n):
            if i==k:continue
            z=a[i][k]
            if z:
                for j in range(k,n+1):a[i][j]-=z*a[k][j]
    return [row[n] for row in a]

def normalize(labels):
    table={};return [table.setdefault(v,len(table)) for v in labels]
def programmed_edges(labels):
    # One star per requested electrical net. Distinct nets never share a
    # hub. This is known complete-graph routing, not an algorithmic invention.
    groups={}
    for i,x in enumerate(labels):groups.setdefault(x,[]).append(i)
    return {tuple(sorted((v[0],j))) for v in groups.values() for j in v[1:]}
def conductance_matrix(labels,ron,g_off,c_off,freq):
    n=len(labels);edges=programmed_edges(labels);y=[[0j]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            yy=(1/ron if (i,j) in edges else g_off+2j*math.pi*freq*c_off)
            y[i][i]+=yy;y[j][j]+=yy;y[i][j]-=yy;y[j][i]-=yy
    return y
def terminal_test(labels,ron,g_off,c_off,freq,par):
    n=len(labels);y=conductance_matrix(labels,ron,g_off,c_off,freq)
    a=[row[:] for row in y];src=0
    for i in range(n):a[i][i]+=1/par["load_R_ohm"]
    a[src][src]+=1/par["source_R_ohm"]
    b=[0j]*n;b[src]=1/par["source_R_ohm"]
    v=solve_complex(a,b)
    # Same stimulated net and same parallel loads, ideal zero-ohm wiring.
    size=sum(x==labels[src] for x in labels)
    ideal=(par["load_R_ohm"]/size)/(par["source_R_ohm"]+par["load_R_ohm"]/size)
    intended=[abs(v[i])/ideal for i in range(n) if labels[i]==labels[src]]
    unwanted=[abs(v[i])/ideal for i in range(n) if labels[i]!=labels[src]]
    return {"frequency_Hz":freq,"min_intended_ratio":min(intended),
            "max_unwanted_ratio":max(unwanted,default=0.),
            "max_unwanted_dB":20*math.log10(max(unwanted,default=0.)) if max(unwanted,default=0.) else None}
def dc_disconnected_pair_R(labels,ron,g_off):
    # Inject 1 A into a node in one block, remove it from a node in another.
    n=len(labels)
    pair=next(((i,j) for i in range(n) for j in range(i+1,n) if labels[i]!=labels[j]),None)
    if pair is None:return None
    y=conductance_matrix(labels,ron,g_off,0.)
    a=[row[:-1] for row in y[:-1]];b=[0j]*(n-1)
    i,j=pair
    if i<n-1:b[i]+=1.
    if j<n-1:b[j]-=1.
    v=solve_complex(a,b)+[0j]
    return (v[i]-v[j]).real

def main():
    p=PAR;n=p["terminal_count"];count=n*(n-1)//2
    rn=p["feed_radius_m"];rb=p["bridge_radius_m"]
    r_bridge=p["bridge_length_m"]/(p["metal_sigma_S_m"]*math.pi*rb*rb)
    r_feed=p["feed_length_m"]/(p["metal_sigma_S_m"]*math.pi*rn*rn)
    r_cell=2*p["contact_R_each_ohm"]+r_bridge
    area=math.pi*rb*rb;perimeter=2*math.pi*rb
    gaq=p["aqueous_film_sigma_S_m"]*perimeter*p["wall_film_thickness_m"]/p["open_gap_m"]
    gdie=p["dielectric_film_sigma_S_m"]*perimeter*p["wall_film_thickness_m"]/p["open_gap_m"]
    goff=gdie+1/p["package_R_per_open_cell_ohm"]
    c_intrinsic=EPS0*p["dielectric_relative_permittivity"]*area/p["open_gap_m"]
    coff=c_intrinsic+p["stray_C_per_cell_F"]
    pc=pin_pressure(p);gravity=p["rho_metal_kg_m3"]*G*p["vertical_height_m"]
    corners=[]
    for comp in (False,True):
        for t in p["temperature_range_K"]:
            for q in (0.,p["stroke_m3"]):
                restoring=hold_pressure(q,t,p,comp)
                corners.append({"thermal_compensated":comp,"T_K":t,"metal_displacement_m3":q,
                    "restoring_pressure_Pa":restoring,"adverse_gravity_Pa":gravity,
                    "total_abs_disturbance_Pa":abs(restoring)+gravity,
                    "retained_by_declared_threshold":abs(restoring)+gravity<pc})
    # Private inventory and common dielectric pressure do not insert a metal
    # edge. A common METAL feed connects every selected branch, merging all
    # simultaneous desired nets. No fluidic switching model repairs that.
    matching=[i//2 for i in range(n)]
    requested_net_count=len(set(matching));common_metal_feed_net_count=1
    random.seed(20261114)
    programs=[[0]*n,list(range(n)),matching,[0]*8+[1]*8,
              [i%4 for i in range(n)],list(range(8))*2]
    programs += [normalize([random.randrange(k) for _ in range(n)]) for k in range(2,17) for _ in range(3)]
    rows=[]
    for idx,labels in enumerate(programs):
        edges=programmed_edges(labels)
        # Every requested node block has a star with max path 2, <=15
        # closed cells total, and no inter-block closed edge.
        assert len(edges)==n-len(set(labels))
        assert all(labels[i]==labels[j] for i,j in edges)
        for f in (1e3,1e4,1e5):
            rows.append({"program":idx,"labels":labels,"closed_cells":len(edges),
                         **terminal_test(labels,r_cell,goff,coff,f,p)})
    lowfilm=[]
    for delta in (1e-6,1e-7,1e-8):
        gg=p["aqueous_film_sigma_S_m"]*perimeter*delta/p["open_gap_m"]
        lowfilm.append({"film_m":delta,"single_gap_R_ohm":1/gg,
                        "eight_by_eight_net_R_ohm":1/(64*gg)})
    trajectories=[trajectory(p,True,j) for j in (1000,2000,4000)]
    work_span=max(x["cycle_work_J"] for x in trajectories)-min(x["cycle_work_J"] for x in trajectories)
    # 100 retargetings use the SAME private stocks. q is transferred, not
    # replaced. This is finite bookkeeping, not a reliability campaign.
    use=[0]*count;all_edges=[(i,j) for i in range(n) for j in range(i+1,n)]
    previous=set();changes=0;forward_changes=0;return_changes=0
    for k in range(100):
        target=programmed_edges(programs[k%len(programs)])
        forward_changes+=len(target-previous);return_changes+=len(previous-target)
        for edge in previous.symmetric_difference(target):
            use[all_edges.index(edge)]+=1;changes+=1
        previous=target
    stock0=count*p["private_metal_m3"]
    displaced=len(previous)*p["stroke_m3"]
    reservoir=stock0-displaced
    assert abs(reservoir+displaced-stock0)<1e-22
    # Full partition-class bound for THIS introduced linear circuit model.
    # A0 is the real on-star + positive terminal-load matrix; its inverse
    # is nonnegative with infinity norm <= Rload. The off-edge Laplacian
    # has row absolute sum <=2(n-1)|g+jwC|. Neumann inversion therefore
    # bounds all complex perturbations without sampling every partition.
    # A 1-V source through Rs has <=1/Rs total base current. A max-two-edge
    # star thus has <=2 Ron/Rs voltage spread; global KCL places the ideal
    # zero-wire voltage inside that interval. These are circuit statements,
    # not physical qualification of any Ron/G/C or a simultaneous-source
    # signal-to-noise certification.
    ideal_min=p['load_R_ohm']/(p['load_R_ohm']+n*p['source_R_ohm'])
    base_spread=2*r_cell/p['source_R_ohm']
    base_relative=base_spread/ideal_min
    off_y=abs(complex(goff,2*math.pi*1e5*coff))
    eta=p['load_R_ohm']*2*(n-1)*off_y
    assert eta<1
    relative_perturbation=eta/(1-eta)*(1+base_relative)
    lower_transfer=1-base_relative-relative_perturbation
    assert lower_transfer>0
    work_forward=trajectories[-1]['phases'][0]['external_work_J']
    work_return=trajectories[-1]['phases'][1]['external_work_J']
    output={
      "scope":"INTRODUCED cells, contact-angle pinning, head tracking, pressure compensation, contacts and dielectric; no built array or useful circuit",
      "parameters":p,
      "cell":{"pinning_threshold_Pa":pc,"hydraulic_R_Pa_s_m3":hydraulic_R(p),
              "bridge_bulk_R_ohm":r_bridge,"side_feed_R_if_put_in_current_path_ohm":r_feed,
              "on_cell_R_ohm":r_cell,"max_two_edge_path_R_ohm":2*r_cell,
              "head_full_stroke_m":p["stroke_m3"]/p["diaphragm_area_m2"],
              "bridge_nominal_volume_uL":area*p["bridge_length_m"]*1e9,
              "one_cell_metal_inventory_uL":p["private_metal_m3"]*1e9,
              "compensator_volume_change_uL_over_temperature_range":p["gas_m3"]*(p["temperature_range_K"][1]-p["temperature_range_K"][0])/T0*1e9},
      "retention_corners":corners,"write_and_reset_trajectories":trajectories,
      "electrical":{"aqueous_film_single_gap_R_ohm":1/gaq,
                    "dielectric_film_single_gap_R_ohm":1/gdie,
                    "open_cell_G_S":goff,"intrinsic_gap_C_F":c_intrinsic,"total_open_cell_C_F":coff,
                    "complete_graph_cut_bound_max_parallel_edges":64,
                    "full_class_DC_unconnected_net_R_lower_bound_ohm":1/(64*goff),
                    "full_class_off_network_two_terminal_C_upper_bound_F":64*coff,
                    "max_film_thickness_m_for_100Mohm_network_with_sigma5":p["open_gap_m"]/(64*p["aqueous_film_sigma_S_m"]*perimeter*1e8),
                    "common_metal_feed_requested_nets":requested_net_count,"common_metal_feed_actual_connected_nets":common_metal_feed_net_count,
                    "thin_aqueous_film_cases":lowfilm},
      "finite_program_tests":rows,
      "full_class_introduced_linear_circuit_bound":{
          "scope":"all 16-terminal partitions, one source terminal excited, equal 10kohm terminal loads, <=100kHz; no installed physical parameter claim",
          "ideal_minimum_transfer":ideal_min,"base_relative_spread_bound":base_relative,
          "inverse_perturbation_eta":eta,"relative_complex_perturbation_bound":relative_perturbation,
          "intended_transfer_lower_bound":lower_transfer,
          "intended_transfer_lower_bound_dB":20*math.log10(lower_transfer),
          "unwanted_transfer_upper_bound":relative_perturbation,
          "unwanted_transfer_upper_bound_dB":20*math.log10(relative_perturbation)},
      "finite_same_stock_history":{"retargetings":100,"distinct_test_programs":len(programs),"cell_state_changes":changes,
          "maximum_changes_one_cell":max(use),"switch_cell_count":count,"initial_private_metal_uL":stock0*1e9,
          "final_bridge_metal_uL":displaced*1e9,"final_reservoir_metal_uL":reservoir*1e9,
          "private_metal_mass_g":stock0*p["rho_metal_kg_m3"]*1e3,
          "total_initial_private_gas_mL":count*p["gas_m3"]*1e6,
          "forward_state_changes":forward_changes,"return_state_changes":return_changes,
          "integrated_cell_mechanical_work_J":forward_changes*work_forward+return_changes*work_return,
          "lower_bound_cell_mechanical_work_J":changes*min(work_forward,work_return),
          "scope":"same inventories in an ideal transfer model; no loss map, yield, test/inspection/renewal/head positioning/total machine power"},
      "verification":{"state_cycle_work_refinement_span_J":work_span,
          "minimum_sampled_intended_transfer_ratio":min(x["min_intended_ratio"] for x in rows),
          "maximum_sampled_unwanted_transfer_ratio":max(x["max_unwanted_ratio"] for x in rows)},
      "limitations":["capillary threshold is an introduced simultaneous wetting law, not a qualified oxide/film interface",
         "thermal compensator is a finite-volume requirement, not built hardware or a free pressure reset",
         "private feed layout, fixed pad wetting/contact, membrane, positive pull head and metrology are unconstructed",
         "no leaked metal/dielectric aging/adhesion/retained pressure or 24h/1000-cycle qualification",
         "graph routing is known mathematics; finite sampled AC cases are not the full partition-class AC theorem",
         "10fF stray capacitance and 10Gohm open package isolation are introduced, not installed values",
         "no full layout/electromagnetic/thermomechanical/current-distribution or manufacturing-cost model",
         "tiny cell work excludes programmer motion, observations, pressure supply, stock preparation and full-cycle resources",
         "no new physical device, novelty, platform or ordinary-method advantage established"]
    }
    dest=Path(__file__).with_suffix(".json");dest.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:output[k] for k in ("cell","retention_corners","electrical","finite_same_stock_history","verification")}))
if __name__=="__main__":main()


"""Scientific static figures for the complete acquired-response operation.

The numerical source curves are diagnostics.  The certificate bands are the
independently proved conditional bounds, not confidence bands inferred from
the displayed samples.  The acquired table and compiled path are read only.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator
import numpy as np

from exact_step_prediction import evaluate_path

HERE=Path(__file__).resolve().parent
BLUE="#0072B2"
ORANGE="#D55E00"
GREEN="#009E73"
GREY="#566573"
PALE="#D9EAF4"


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    table_path=HERE/"acquired_step_response.json"
    prediction_path=HERE/"exact_prediction_path.json"
    table=json.loads(table_path.read_text())
    prediction=json.loads(prediction_path.read_text())
    source=json.loads((HERE/"source_trace_diagnostic.json").read_text())
    diagnostic=json.loads((HERE/"retained_source_diagnostics.json").read_text())
    table_sha=file_hash(table_path)
    assert prediction["acquired_table_sha256"]==table_sha
    assert diagnostic["table_sha256"]==table_sha
    node_t=np.array([float(F(t)) for t in table["times_exact"]])
    node_s=np.array([float(F(y)) for y in table["values_exact"]])
    true_s=np.array(diagnostic["source_only_true_step_at_nodes"])
    response_radius=float(F(table["response_error_exact"]))
    sample_t=np.array(source["times"])
    source_x=np.array(source["physical_x"])
    # Use the exact saved polynomial operation at every displayed source time.
    # Conversion to float happens only after the rational evaluation.
    predictor=np.array([
        float(evaluate_path(prediction,F(str(t)))) for t in sample_t
    ])
    prediction_radius=float(F(prediction["uniform_physical_error_bound_exact"]))
    query_error=np.abs(source_x-predictor)
    node_error=np.abs(true_s-node_s)
    r=table["resources"]
    cal_wait=float(F(r["calibration_actual_wait_exact"]))
    dep_wait=float(F(r["deployment_actual_wait_exact"]))
    total_time=float(F(r["actual_protocol_time_exact"]))
    worst_time=float(F(r["worst_total_protocol_time_exact"]))
    horizon=float(F(table["horizon_exact"]))

    plt.rcParams.update({
        "font.family":"DejaVu Sans",
        "font.size":10.5,
        "axes.titlesize":12,
        "axes.labelsize":10.5,
        "legend.fontsize":9,
        "xtick.labelsize":9,
        "ytick.labelsize":9,
        "axes.spines.top":False,
        "axes.spines.right":False,
        "axes.grid":True,
        "grid.color":"#D5D8DC",
        "grid.alpha":.55,
        "grid.linewidth":.6,
        "pdf.fonttype":42,
        "ps.fonttype":42,
        "savefig.facecolor":"white",
        "figure.facecolor":"white",
    })

    def plot_step(ax,letter="A"):
        ax.fill_between(node_t,node_s-response_radius,node_s+response_radius,
                        color=BLUE,alpha=.15,
                        label=f"Conditional certificate ±{response_radius:.7f}",
                        linewidth=0,zorder=1)
        ax.plot(node_t,true_s,color=ORANGE,linestyle="--",linewidth=1.8,
                label="Floating source step (diagnostic)",zorder=3)
        ax.plot(node_t,node_s,color=BLUE,linewidth=1.35,
                label="Acquired piecewise-linear response",zorder=4)
        ax.scatter(node_t[::5],node_s[::5],color=BLUE,s=9,zorder=5)
        ax.set(xlim=(0,horizon),xlabel="Time after input onset",
               ylabel="Position per unit input")
        ax.set_title(f"{letter}  Finite-box acquisition of the response",loc="left",pad=10)
        ax.legend(loc="upper left",frameon=True,framealpha=.94,edgecolor="#E5E7E9")
        ax.text(.98,.035,
                f"Maximum discrepancy at 101 diagnostic nodes: {node_error.max():.6f}",
                ha="right",va="bottom",transform=ax.transAxes,fontsize=9,color=GREY,
                bbox=dict(facecolor="white",edgecolor="none",alpha=.85,pad=3))
        ax.margins(y=.08)

    def plot_query(ax,letter="B"):
        ax.fill_between(sample_t,predictor-prediction_radius,
                        predictor+prediction_radius,color=BLUE,alpha=.15,
                        label=f"Conditional certificate ±{prediction_radius:.8f}",
                        linewidth=0,zorder=1)
        ax.plot(sample_t,source_x,color=ORANGE,linestyle="--",linewidth=1.8,
                label="Retained physical source (floating diagnostic)",zorder=3)
        ax.plot(sample_t,predictor,color=BLUE,linewidth=1.4,
                label="Compiled rational predictor",zorder=4)
        ax.set(xlim=(0,horizon),xlabel="Time after query onset",ylabel="Observed position")
        ax.set_title(f"{letter}  Prediction from the retained state",loc="left",pad=10)
        ax.legend(loc="upper left",frameon=True,framealpha=.94,edgecolor="#E5E7E9")
        ax.text(.98,.035,
                f"Maximum sampled discrepancy: {query_error.max():.6f}  (2,001 times)",
                ha="right",va="bottom",transform=ax.transAxes,fontsize=9,color=GREY,
                bbox=dict(facecolor="white",edgecolor="none",alpha=.85,pad=3))
        ax.margins(y=.08)

    def plot_resources(ax,letter="C"):
        labels=["Forecast horizon","Selected calibration wait",
                "Selected deployment wait","Full realized schedule",
                "Full declared maximum"]
        vals=[horizon,cal_wait,dep_wait,total_time,worst_time]
        colors=[GREEN,"#56B4E9",BLUE,GREY,"#E69F00"]
        pos=np.arange(len(vals))
        ax.barh(pos,vals,color=colors,height=.59,edgecolor="white",linewidth=.6)
        ax.set_xscale("log")
        ax.set_xlim(.7,3e5)
        ax.set_yticks(pos,labels)
        ax.invert_yaxis()
        ax.xaxis.set_major_locator(LogLocator(base=10,numticks=7))
        ax.xaxis.set_major_formatter(FuncFormatter(
            lambda x,p: f"{x:,.0f}" if x>=1 else f"{x:g}"))
        ax.grid(axis="y",visible=False)
        ax.set_axisbelow(True)
        for y,val in zip(pos,vals):
            label=f"{val:,.2f}" if val!=1 else "1"
            ax.text(val*1.09,y,label,ha="left",va="center",fontsize=9.5)
        ax.set_xlabel("Physical time in normalized units (logarithmic axis)")
        ax.set_title(f"{letter}  Full physical time, including idle waits",loc="left",pad=10)

    footer=(
      "Source curves are floating simulation diagnostics. The bands follow from the conditional\n"
      "acquisition and prediction theorem; sampled agreement does not prove them.\n"
      "One initial state · zero source resets · 102 position boxes."
    )
    fig=plt.figure(figsize=(7.6,11.2))
    gs=fig.add_gridspec(3,1,height_ratios=[1.05,1.05,.8],
                       left=.14,right=.965,top=.910,bottom=.130,hspace=.52)
    plot_step(fig.add_subplot(gs[0]))
    plot_query(fig.add_subplot(gs[1]))
    resource_ax=fig.add_subplot(gs[2])
    resource_position=resource_ax.get_position()
    resource_ax.set_position([.31,resource_position.y0,.655,resource_position.height])
    plot_resources(resource_ax)
    fig.suptitle("Acquired prediction of a retained passive device",
                 x=.14,y=.980,ha="left",fontsize=14.5,fontweight="semibold")
    fig.text(.14,.949,
             "Permanent spring · finite measurements · independently compiled numerical output",
             ha="left",fontsize=9.5,color=GREY)
    fig.text(.14,.035,footer,ha="left",va="bottom",fontsize=8.3,color=GREY,
             linespacing=1.45)
    for ext in ("png","pdf"):
        fig.savefig(HERE/f"complete_operation.{ext}",dpi=230)
    plt.close(fig)

    for stem,draw,height in [
        ("acquired_step_response_figure",plot_step,4.5),
        ("retained_query_figure",plot_query,4.5),
        ("physical_time_resource_figure",plot_resources,3.8),
    ]:
        fig,ax=plt.subplots(figsize=(7.6,height))
        fig.subplots_adjust(left=.14 if draw!=plot_resources else .30,
                            right=.965,top=.88,
                            bottom=.20 if draw!=plot_resources else .26)
        draw(ax)
        fig.text(.14 if draw!=plot_resources else .05,.035,
                 ("Source curves are floating diagnostics. Certificate validity follows from the declared\n"
                  "physical theorem and contracts; sample agreement is not a proof."
                  if draw!=plot_resources else
                  "Selected waits are physical time. Simulation and computation wall time\n"
                  "are separate resources."),
                 fontsize=8.2,color=GREY,linespacing=1.35)
        for ext in ("png","pdf"):
            fig.savefig(HERE/f"{stem}.{ext}",dpi=230)
        plt.close(fig)

    metrics={
      "acquired_table_sha256":table_sha,
      "exact_prediction_path_sha256":file_hash(prediction_path),
      "source_diagnostic_sha256":file_hash(HERE/"source_trace_diagnostic.json"),
      "step_response":{
        "diagnostic_node_count":len(node_t),
        "maximum_sampled_absolute_discrepancy":float(node_error.max()),
        "sampled_rms_discrepancy":float(np.sqrt(np.mean(node_error**2))),
        "certificate_exact":table["response_error_exact"],
        "certificate":response_radius,
        "diagnostic_only":True,
      },
      "retained_query":{
        "sample_count":len(sample_t),
        "maximum_sampled_absolute_discrepancy":float(query_error.max()),
        "time_of_maximum_sampled_discrepancy":float(sample_t[int(np.argmax(query_error))]),
        "sampled_rms_discrepancy":float(np.sqrt(np.mean(query_error**2))),
        "certificate_exact":prediction["uniform_physical_error_bound_exact"],
        "certificate":prediction_radius,
        "all_plotted_samples_inside_certificate":bool(np.all(query_error<=prediction_radius)),
        "predictor_evaluation":"Exact rational evaluation of the saved emitted polynomial at each displayed time, converted to float only for drawing.",
        "diagnostic_only":True,
      },
      "resources":{
        "calibration_wait":cal_wait,"deployment_wait":dep_wait,
        "complete_realized_schedule":total_time,"worst_declared_schedule":worst_time,
        "forecast_horizon":horizon,"realized_time_to_horizon_ratio":total_time/horizon,
        "worst_time_to_horizon_ratio":worst_time/horizon,
        "normalized_physical_units":True,
      },
      "figure_files":[
        f"{stem}.{ext}" for stem in [
          "complete_operation","acquired_step_response_figure",
          "retained_query_figure","physical_time_resource_figure"] for ext in ("png","pdf")],
      "scope":"These sampled figures do not prove the uniform theorem or interval-validate the physical ODE. No acquired table or compiled path was modified."
    }
    (HERE/"plot_metrics.json").write_text(json.dumps(metrics,indent=2,sort_keys=True)+"\n")
    assert file_hash(table_path)==table_sha
    print(json.dumps(metrics,indent=2))


if __name__=="__main__":
    main()

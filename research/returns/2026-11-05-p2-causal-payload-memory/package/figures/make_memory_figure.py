"""Publication figure and resource receipt for analytic payload-memory bounds.

No device, quantum-state trajectory, or noisy factory is simulated.
Run with a Python environment containing NumPy and Matplotlib.
"""
from pathlib import Path
from decimal import Decimal, getcontext
import json
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MultipleLocator, StrMethodFormatter

HERE = Path(__file__).resolve().parent
getcontext().prec = 70

N_GAUGE = 1000
S_OUTPUT = N_GAUGE + 1
FIELD_Q = 4096
FIELD_K = 12
HEADER_BITS = 2 * FIELD_K + 1
EPSILON = Decimal("0.01")
KAPPA = Decimal("0.8")
R = Decimal(1) - Decimal(8) * EPSILON * (1-EPSILON) / KAPPA

def decimal_prefix(ell):
    if ell == 0:
        return Decimal(0)
    inverse_dimension = Decimal(2) ** (-ell)
    return max(Decimal(0), Decimal(ell) * (R-inverse_dimension)/(1-inverse_dimension))

exposure = sum((decimal_prefix(ell) for ell in range(1, S_OUTPUT)), Decimal(0))
direct_exposure = Decimal(N_GAUGE * (N_GAUGE+1)//2)
postflag_mean = decimal_prefix(S_OUTPUT)
one_slot_header = exposure + postflag_mean
serial_header = exposure + HEADER_BITS * postflag_mean

receipt = {
    "status": "Analytic theorem bounds and arithmetic only; no simulated or observed device.",
    "distance_convention": "Half diamond: d_diamond(A,B)=||A-B||_diamond/2.",
    "dimension_convention": "Quantum dimension is counted within each classical branch; arbitrary classical records are permitted.",
    "input_for_mean_bound": "Maximally mixed payload, equivalently the input marginal of a Bell-pair experiment.",
    "parameters": {
        "n_gauge": N_GAUGE, "s_quantum_outputs": S_OUTPUT,
        "epsilon_total": float(EPSILON), "kappa": float(KAPPA),
        "emission_model_error_nu": 0,
        "emission_error_scope": "Exact declared emission for these numbers. Under the same fixed timing, an imperfect emission needs r evaluated at epsilon+nu and the additional ell*nu correction to actual expected prefix memory; see ../proofs/emission_error_refinement.txt.",
        "retained_dimension_fraction_r": float(R),
        "finite_field_q": FIELD_Q, "field_degree_k": FIELD_K,
        "seed_bits": 2*FIELD_K, "header_bits": HEADER_BITS,
        "seed_pairs": FIELD_Q**2,
        "selector_labels_including_anchor": FIELD_Q**2+1,
        "certified_character_bias_upper_bound": (2*N_GAUGE-1)/FIELD_Q,
        "field_polynomial": "t^12+t^3+1",
        "field_polynomial_hex": "0x1009"
    },
    "formulas": {
        "dimension_fraction_lower_bound": "max(0,1-8*epsilon*(1-epsilon)/kappa)",
        "prefix_expected_qubits_lower_bound": "f_l=max(0,l*(r-2^(-l))/(1-2^(-l))), l>=1; f_0=0",
        "exposure_before_final_output": "tau*sum_{l=1}^{s-1} f_l",
        "exposure_including_header_latency": "tau*sum_{l=1}^{s-1} f_l + t_hdr*f_s",
        "direct_store_exposure": "tau*s*(s-1)/2 + t_hdr*s"
    },
    "memory_counts": {
        "whole_qubit_capacity_after_gauges": N_GAUGE,
        "whole_qubit_capacity_after_flag": S_OUTPUT,
        "expected_qubits_lower_bound_after_gauges": float(decimal_prefix(N_GAUGE)),
        "expected_qubits_lower_bound_after_flag": float(postflag_mean),
        "capacity_warning": "Whole-qubit capacity is a maximum over classical branches. The expected-memory bound is a separate average and is not asserted branchwise.",
        "early_receiver": "Constant coherent buffering plus O(log n) classical seed/controller state; exact meter and protection overhead are not assigned a number here."
    },
    "retained_qubit_time": {
        "unit": "qubit*arrival_interval; multiply the no-header number by tau in seconds for qubit-seconds",
        "prefix_range": [1, S_OUTPUT-1],
        "expected_lower_bound_without_header_latency": float(exposure),
        "expected_lower_bound_decimal": str(exposure),
        "direct_store_without_header_latency": int(direct_exposure),
        "lower_bound_divided_by_direct_store": float(exposure/direct_exposure),
        "header_latency_coefficient_qubits": float(postflag_mean),
        "header_latency_definition": "t_hdr is time after the flag before ANY selector information is available to the quantum receiver. The unconditioned bound cannot automatically be extended through a progressively revealed header.",
        "direct_store_header_latency_coefficient_qubits": S_OUTPUT,
        "if_header_latency_equals_one_arrival_interval": {
            "expected_lower_bound": float(one_slot_header),
            "direct_store": int(direct_exposure)+S_OUTPUT
        },
        "optional_serial_header_example": {
            "assumption": "A separate classical link buffer assembles 25 metadata bits at one bit per arrival interval and withholds ALL selector information from the quantum receiver until atomic disclosure. This extra interface assumption is not part of the base plotted bound. Progressive disclosure does not justify this number without a conditional bound.",
            "header_latency_in_arrival_intervals": HEADER_BITS,
            "expected_lower_bound": float(serial_header),
            "direct_store": int(direct_exposure)+HEADER_BITS*S_OUTPUT
        },
        "scope": "Expected logical receiver occupancy under the specified input marginal, before physical protection overhead. This lower bound does not assert an achievable fractional-memory strategy."
    },
    "abstract_online_resource_bounds": {
        "fresh_tracial_carriers": S_OUTPUT,
        "source_quantum_gates_at_most": N_GAUGE+2,
        "local_gauge_measurements_at_most": N_GAUGE,
        "flag_correction_gates_at_most": 2,
        "classical_program_work": "O(n*k^2) elementary bit operations with schoolbook field multiplication",
        "classical_working_state": "O(k+log n) bits",
        "excluded_from_abstract_counts": "hardware gate decomposition, meter reset/preparation, calibration, correlated factory errors, routing constants and protection overhead"
    },
    "plotted_dimension_points_at_one_percent": {
        "kappa_4_over_5": float(Decimal(1)-Decimal(8)*EPSILON*(1-EPSILON)/Decimal("0.8")),
        "kappa_4_over_3": float(Decimal(1)-Decimal(6)*EPSILON*(1-EPSILON))
    },
    "figure": {
        "left_epsilon_range": [0,0.08],
        "right_prefix_range": [0,1000],
        "early_buffer_illustration_height": 1,
        "early_buffer_warning": "Line drawn at 1 solely to illustrate O(1) scaling; it is not an exact meter/apparatus count and is not used in the resource calculation.",
        "files": ["causal_memory_bounds.pdf", "causal_memory_bounds.svg", "causal_memory_bounds.png"]
    },
    "governing_local_sources": [
        "../causal_payload_memory.tex, causal-prefix and retained-exposure section",
        "../proofs/late_selector_theorem.txt",
        "../proofs/small_bias_instantiation.txt"
    ]
}
(HERE/"memory_resources.json").write_text(json.dumps(receipt, indent=2)+"\n")

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.labelsize": 11, "axes.titlesize": 12,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
    "legend.fontsize": 9, "axes.linewidth": .8,
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "svg.fonttype": "none", "mathtext.fontset": "dejavusans",
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white"
})

blue = "#1764A2"
purple = "#813C9E"
green = "#16826C"
ink = "#29313A"
gray = "#757C83"

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12.2,5.2), gridspec_kw={"wspace": .29})
fig.subplots_adjust(left=.075,right=.98,bottom=.22,top=.80)
fig.suptitle("Late metadata forces quantum retention", x=.075,y=.968,ha="left",fontsize=17,color=ink,weight="semibold")
fig.text(.075,.907,"Analytic theorem bounds  |  No device simulation",ha="left",fontsize=10.5,color=gray)

eps = np.linspace(0,.08,801)
for kappa,color,label in [(.8,blue,r"Small-bias Pauli: $\kappa=4/5$"),
                          (4/3,purple,r"Full Pauli ensemble: $\kappa=4/3$")]:
    curve = np.maximum(0,1-8*eps*(1-eps)/kappa)
    ax1.plot(eps,curve,color=color,lw=2.3,label=label)
    r1 = 1-8*.01*.99/kappa
    ax1.plot([.01],[r1],"o",color=color,ms=5.5,mec="white",mew=.7,zorder=5)
ax1.axhline(.5,color=gray,lw=1.05,ls=(0,(4,3)),label=r"Half dimension: $m/N=1/2$")
ax1.axvline(.01,color="#B9BFC5",lw=.85,ls=(0,(2,3)),zorder=0)
ax1.annotate("0.9406",xy=(.01,.9406),xytext=(.021,.985),color=purple,fontsize=10,
             arrowprops={"arrowstyle":"-","lw":.8,"color":purple},ha="left",va="center")
ax1.annotate("0.901",xy=(.01,.901),xytext=(.021,.833),color=blue,fontsize=10,
             arrowprops={"arrowstyle":"-","lw":.8,"color":blue},ha="left",va="center")
ax1.set(xlim=(0,.08),ylim=(0,1.035),xlabel=r"Total recovery error $\epsilon$ (half diamond)",ylabel=r"Required dimension fraction $m/N$")
ax1.set_title("A   Dimension required at the selector cut",loc="left",pad=11,color=ink)
ax1.xaxis.set_major_locator(MultipleLocator(.02))
ax1.xaxis.set_major_formatter(PercentFormatter(xmax=1,decimals=0))
ax1.yaxis.set_major_locator(MultipleLocator(.25))
ax1.legend(loc="lower left",frameon=False,borderpad=.2,labelspacing=.65,handlelength=2.7)

ell = np.arange(1,N_GAUGE+1)
inverse = np.exp2(-ell.astype(float))
prefix = np.maximum(0,ell*(float(R)-inverse)/(1-inverse))
ax2.plot(np.r_[0,ell],np.r_[0,ell],color=ink,lw=1.65,ls=(0,(5,3)),label=r"Direct storage: $\ell$")
ax2.plot(np.r_[0,ell],np.r_[0,prefix],color=blue,lw=2.3,label=r"Late-selector mean bound: $f_\ell$")
ax2.plot(ell,np.ones_like(ell),color=green,lw=2.0,label=r"Early $O(1)$ buffer: illustration",zorder=4)
ax2.plot([N_GAUGE],[prefix[-1]],"o",color=blue,ms=5,mec="white",mew=.7,zorder=5)
ax2.annotate("901",xy=(1000,901),xytext=(930,798),fontsize=10,color=blue,
             arrowprops={"arrowstyle":"-","color":blue,"lw":.8},ha="center")
ax2.text(45,965,"$r=0.901$ at 1% total error\n$n=1000$, 25-bit selector",ha="left",va="top",fontsize=10,color=ink)
ax2.set(xlim=(0,1000),ylim=(0,1050),xlabel=r"Emitted prefix length $\ell$",ylabel="Expected retained quantum-memory qubits")
ax2.set_title("B   Retention throughout the stream",loc="left",pad=11,color=ink)
ax2.xaxis.set_major_locator(MultipleLocator(250))
ax2.yaxis.set_major_locator(MultipleLocator(250))
ax2.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax2.legend(loc="upper left",bbox_to_anchor=(.02,.79),frameon=False,borderpad=.2,labelspacing=.65,handlelength=2.7)

for ax in (ax1,ax2):
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["left","bottom"]].set_color("#90979E")
    ax.tick_params(colors=ink)
    ax.grid(axis="y",color="#E5E8EB",lw=.65,zorder=0)
    ax.set_axisbelow(True)

fig.text(.075,.105,
    f"Cumulative bound at 1,000 gauge arrivals: {float(exposure):,.2f} qubit-slots; direct storage uses 500,500.",
    fontsize=10.3,color=ink,ha="left")
fig.text(.075,.058,
    "Mean bounds use the Bell-input marginal and allow variable classical branches. Early-buffer line shows scaling only; its height is not an apparatus count.",
    fontsize=8.5,color=gray,ha="left")
fig.text(.075,.025,
    r"One slot is an arrival interval $\tau$. Delay $t_{\rm hdr}$ before any header information adds at least $901.901\,t_{\rm hdr}$ qubit-time. Protection overhead is additional.",
    fontsize=8.5,color=gray,ha="left")

for ext in ("pdf","svg","png"):
    fig.savefig(HERE/f"causal_memory_bounds.{ext}",dpi=300)
plt.close(fig)

caption = (
    "Analytic quantum-memory bounds for the late-selector payload theorem. "
    "(A) The required dimension fraction 1-8 epsilon(1-epsilon)/kappa for kappa=4/5 and 4/3; "
    "the marked one-percent values are 0.901 and 0.9406. The dashed horizontal line is one-half of the full dimension. "
    "(B) The every-prefix expected-qubit lower bound f_l=max{0,l(r-2^{-l})/(1-2^{-l})} for r=0.901, "
    "compared with direct retention of all l outputs. The early-selector O(1) line is schematic and does not assert an exact meter count. "
    "For n=1000 gauge outputs and one final flag, the expectation of retained quantum exposure before the final output is at least "
    f"{float(exposure):,.8f} tau qubit-time, versus 500,500 tau for direct storage. "
    "Delay t_hdr before any selector information becomes available adds at least 901.901 t_hdr; a progressively disclosed header needs a conditional analysis. The mean bounds use the maximally mixed/Bell-input marginal and remain valid with "
    "branch-dependent memory. Parameters q=4096, k=12 give a 25-bit header. No device or 1000-qubit state was simulated.\n"
)
(HERE/"figure_caption.txt").write_text(caption)
print(json.dumps({"exposure":float(exposure),"direct_store":int(direct_exposure),
                  "postflag_mean":float(postflag_mean),"serial_25_slot_example":float(serial_header),
                  "files":["causal_memory_bounds.pdf","causal_memory_bounds.svg","causal_memory_bounds.png","memory_resources.json","figure_caption.txt"]},indent=2))

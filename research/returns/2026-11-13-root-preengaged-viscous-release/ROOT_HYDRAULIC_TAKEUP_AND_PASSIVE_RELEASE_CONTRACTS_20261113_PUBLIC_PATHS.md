CAPTURED PRELOAD RELEASE WITH A PRE-ENGAGED VISCOUS PATH
13 November 2026 Brisbane / 12 November UTC

Physical operation and scope
A captured, initially compressed spring can relax through a dissipative path while an independent carrier retains both reacting bodies. The useful question is whether an actual damper engages soon enough, at acceptable peak force, within the permitted relative motion. This note constructs one coordinate and a candidate way to pay take-up motion. It does not construct a six-axis joint, a full load-transfer apparatus, a measured hydraulic law or an autonomous service.

Actual primary scope
After dependent local identity/alias/hold checks, the ACE HB-28 main family page was read at its product table, description, Technical Data and Technical Notes:
https://www.acecontrols.com/us/products/motion-control/hydraulic-dampers/hb-12-to-hb-70/hb-28.html
The maker lists 6.74--674.43 lbf, 1.97--19.69 inch strokes, approximately 20% free travel, an 80 N separator-piston extension force, approximate 250,000-cycle life, and customer-provided 1--1.5 mm end-stop margins. It also notes increased break-away force after inactivity and adjustment before installation. These are maker statements, not a measured short-stroke force-speed/temperature map, an installed zero-deadband or static-lock certificate, a life interval for this release, or a quote. No linked product, catalogue, CAD, configurator, image, application, download or contact was followed. No access failure or held-source recovery occurred.

Introduced mechanics
Let x be the opening of a captured internal release coordinate, starting at x=0 with velocity zero. A spring has initial compression a=F/k, and a primary retainer initially carries its force F. After that retainer releases, the spring drives an effective inertia m toward x=a. The carrier and the independent useful-load support are separately required. Their stiffness, guide stability, moments and ownership are not supplied by this scalar model.

All dynamic parameters are INTRODUCED:
F=2500 N; k=5,000,000 N/m; m=100 kg;
a=0.0005 m; omega=sqrt(k/m)=223.60679775 rad/s;
c=2 sqrt(k m)=44721.359550 N s/m;
initial captured elastic energy E0=F^2/(2k)=0.625 J.
The 100 kg effective inertia is not a supplied package mass or free mechanical amplification. The actual moving bodies and any modal/lever inertia need construction.

Assume one initial unengaged travel d. After the first arrival at x=d, an ideal bilateral viscous element remains engaged. Before arrival:
x=a[1-cos(omega t)], v=a omega sin(omega t).
When 0<=d<=2a,
t_d=acos(1-d/a)/omega,
v_d=omega sqrt(2ad-d^2).
If d>2a, the first oscillation never reaches the damper and its peak is 2a=1 mm. This is a specified dead-travel scenario, not a claim that every real HB-28 starts in that state.

For the ideal critically damped law, put tau=t-t_d,
A=d-a, B=v_d+omega A.
Then
x=a+(A+B tau)exp(-omega tau),
v=(v_d-omega B tau)exp(-omega tau).
This gives a constructive take-up budget: monotone approach from below is equivalent, for 0<=d<=a, to
d/a <= 1-1/sqrt(2)=0.2928932188.
Thus this model requires d<=146.4466094 micrometres for monotone relaxation. Critical damping specified only after engagement does not guarantee monotone release when take-up is longer.

Peak force and positive example
At d=0 the ideal peak damping force is 1839.397206 N. At d=25 and 50 micrometres it is 1914.087161 and 2183.653654 N respectively; x approaches 0.5 mm monotonically and all 0.625 J is eventually dissipated. At d=100 micrometres the ideal peak is exactly 3000 N and the motion remains monotone. The first-engagement force c v_d alone requires d<=100 micrometres on the small-root branch if a 3000 N limit is imposed. This is stricter than the monotonicity threshold.

At d=146.4466094 micrometres, the uncapped ideal law asks for 3535.533906 N. At d=200 micrometres it asks for 4000 N and peaks at 0.501831564 mm; at d=0.5 mm it asks for 5000 N and peaks at 0.683939721 mm. An INTRODUCED clipped law f_d=clip(c v,-3000,3000) instead gives sampled peaks 0.504978634 and 0.706539244 mm in those last two cases. The clip is not an ACE characteristic. A family force rating does not provide c, the saturation law, engagement timing, compliance, cavitation response or thermal duty.

The energy balance after take-up is
d/dt [m v^2/2+k(x-a)^2/2] = -f_d(v)v.
The exact pre-take-up event preserves E0. This is internal captured-spring relaxation; useful structural load must remain on an independently constructed support. If a continuing external load acts through x instead, its work must be added and a dissipator alone is not a static support.

Take-up cannot be removed for free by a fixed lever
Using a rounded 50 mm total stroke and a hypothetical initially unengaged 10 mm segment, a fixed motion ratio R gives d_joint=10 mm/R and c_joint=R^2 c_damper; joint force is R times damper force. To reduce take-up to 50 micrometres needs R>=200. To permit the whole 0.5 mm payout within even the entire 50 mm stroke needs R<=100. These conditions are incompatible in this stated fixed-ratio model. End-stop margins would reduce usable travel further. More generally, if free travel is fraction f of usable total stroke, a fixed ratio alone cannot make initial take-up smaller than f times the required joint payout when the whole motion must fit. This is not an obstruction to pre-stroking, staged motion, a different damper or a different mechanism.

At R=20 the listed 80 N separator bias would transform to 1600 N; at R=100 and 200 it would transform to 8000 and 16000 N. These are force transformations, not measured installed loads. An introduced constant signed +/-80 N bias without gearing shifts a from 0.5 mm to 0.484/0.516 mm and the relative-equilibrium energy from 0.625 J to 0.58564/0.66564 J. The actual gas force varies with state and its direction, stiffness and inventory were not supplied. Opposed biases may cancel an external resultant while still loading each local member. At a constant 80 N, a separate 10 mm pre-stroke would require 0.8 J of work; actual reset work and heat require the real force curve.

Candidate construction, still unbuilt
Keep the primary retainer engaged while a damper-end clevis rides in a separately retained adjustment slide. Move the rod through its take-up using that internal slide, rather than moving the useful structure by the full take-up distance. Positively latch the slide to the carrier before releasing the primary retainer. This is a specific additional adjustment operation and load path, not a command that magically eliminates dead travel. A small signed force/displacement check would have to establish actual engagement in the intended payout direction after the relevant hold time, temperature and reversal history. It cannot be inferred from rod position, a catalogue force ceiling or an unmeasured separator option.

The clevis latch, slide, bearings and primary retention must withstand the actual local peak forces; any friction, seal break-away and fluid/gas compression belong in the installed force law. Guide geometry must avoid the previously identified preload-induced lateral instability. A viscous element supplies zero damping force at rest, so an independent positive keeper remains necessary for a continuing payload and a one-hour power loss. The carrier must own all released bodies and stored energy even if one release seizes. Additional stroke, body/rod length, fittings, sensing, setting actuator, heat capacity, maintenance and reset time must be manufactured, routed and paid. No such complete assembly, force map, cost advantage, material qualification, calibration interval or experiment has been acquired or demonstrated here.

Execution and limits
The owned script solves the take-up event and ideal critical trajectory analytically, then integrates the linear and introduced clipped laws by RK4 at 20 and 10 microseconds for 0.2 s after engagement. Across the finite cases, maximum uncapped sampled-peak versus analytic difference is 2.841e-10 m; maximum two-step clipped sampled-peak difference is 3.360e-10 m. Recorded energy residuals are below 6.80e-11 J for the linear law and 4.01e-11 J for the clipped law. These finite diagnostics check this execution; they are not interval enclosures or physical evidence. Repeated reversal deadband, real viscosity/temperature/seal/cavitation behavior, six-axis geometric stiffness, whole workpiece dynamics and service life remain open. The earlier slow-ramp example used different k and m and is not a matched performance comparison.

Owned executable:
ROOT_HYDRAULIC_TAKEUP_AND_CONTROLLED_PRELOAD_RELEASE_20261113.py
9548 bytes; SHA256 6c077e13ed086684bc145fd45789552ed03eea2072a7127c72ab01a9c0bfbe01.
Owned output:
ROOT_HYDRAULIC_TAKEUP_AND_CONTROLLED_PRELOAD_RELEASE_20261113.json
22387 bytes; SHA256 3356ae29bdcf6ffdcbc4969cc81285e9a00cf0b8206fc89b846e7fe916b0ff0c.
Both reside beside this note in work/astra-renewed-pro-programmes-20261103/.

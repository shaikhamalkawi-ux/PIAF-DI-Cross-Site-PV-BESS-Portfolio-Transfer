# R6R8 clean-room scientific definitions

This file is an admission specification, not analysis code. It records the mathematical definitions needed for an independent implementation. R6R8 itself is not modified.

## Time-series construction
For Norway/Boulder session records, with session energy `e_s` (kWh), connected duration `D_s` (h), and overlap `Delta_s,t` (h) with 15-minute interval `t`:

`L_u,t = sum_s e_s * Delta_s,t / D_s`.

The allocation preserves session energy. It is a service envelope, not measured constant charger power.

For Norway/Boulder only, the common archived 1-kW PV trace is scaled on calibration intervals `C_u`:

`K_u = sum_{t in C_u} L_u,t / sum_{t in C_u} p_t^(1kW)`

`PV_u,t(m) = m * K_u * p_t^(1kW)`.

The common PV shape is an experimental control, not site-local solar validation.

## Battery dispatch
Let `[x]_+ = max(x,0)`, `a_t=[PV_t-L_t]_+`, `b_t=[L_t-PV_t]_+`, `eta_c=eta_d=sqrt(0.90)`, battery energy `E`, power `P`, and stored energy `S_t`.

`c_t = min(a_t, P*dt, (E-S_t)/eta_c)`

`d_t = min(b_t, P*dt, eta_d*S_t)`

`S_(t+1) = S_t + eta_c*c_t - d_t/eta_d`, with `0 <= S_t <= E`.

Daily reset is primary: `S_0=0` on every active day. No grid charging. Terminal stored energy receives no benefit credit. `dt=0.25 h` for Norway/Boulder, `dt=0.5 h` for Dingle, and `dt=1 h` for SlimPark.

Let `G_t=b_t-d_t` after battery dispatch and `G_t^PV=b_t` for PV-only. For periods with positive total EV load:

`rho(E,P) = 100 * (1 - sum_t G_t / sum_t L_t)`

`rho_PV = 100 * (1 - sum_t G_t^PV / sum_t L_t)`

`g = rho(E,P) - rho_PV` in percentage points.

## Candidate lattices
`Q3={0.50,0.75,0.90}` and `Q5={0.25,0.50,0.75,0.90,0.95}`.
Energy and power quantiles are estimated separately from calibration duty and combined as a Cartesian label lattice. Physical coordinates are target-specific and rounded to `0.001 kWh` and `0.001 kW` before dispatch.

## Pareto requirements
Only positive-benefit candidates (`g>0`) are eligible as Pareto requirements. Under the study objectives, candidate `x` dominates candidate `y` when `g_x >= g_y`, `E_x <= E_y`, and `P_x <= P_y`, with at least one strict inequality. The Pareto requirement set `P_u` contains nondominated eligible candidates.

For Pareto requirement `q=(E_q,P_q,g_q)` and candidate `y=(E_y,P_y,g_y)`:

`epsilon(q,y) = max([1-g_y/g_q]_+, [E_y/E_q-1]_+, [P_y/P_q-1]_+)`.

Target portfolio loss:

`epsilon_u(A) = max_{q in P_u} min_{y in A} epsilon(q,y)`.

Smaller loss means better absolute target coverage. The 5% and 10% read-offs are descriptive, not engineering acceptance standards.

## Frozen development portfolio
For lattice `L_r`, budget `k`, and 26 raw-supported development units `U_dev`:

`A_dev_(k,r) in argmin_{A subseteq L_r, |A|<=k} max_{u in U_dev} epsilon_u(A)`.

If multiple sets attain the same development objective, the archived pre-external choice is retained; external outcomes are never used to break the tie. Budgets are solved independently and portfolios are not required to be nested.

## Exact same-budget percentile
For exactly-k universe `S_(k,r)={S subseteq L_r: |S|=k}`:

`pi_(u,r)(A) = 100 * #{S in S_(k,r): epsilon_u(S) > epsilon_u(A)} / |S_(k,r)|`.

Ties are NOT counted as beaten. At `k=4`, there are 126 subsets on 3x3 and 12,650 subsets on 5x5.

## Failure decomposition
`epsilon_loc_(u,r)(k) = min_{A subseteq L_r, |A|<=k} epsilon_u(A)`.

`epsilon_dev_(u,r)(k) = epsilon_u(A_dev_(k,r))`.

`Delta_sel_(u,r)(k) = epsilon_dev_(u,r)(k) - epsilon_loc_(u,r)(k) >= 0`.

`epsilon_loc` is an ex-post within-lattice/current-budget benchmark, not a physical feasibility bound or prospective budget predictor.

## Units / display conventions
`epsilon_dev`, `epsilon_loc`, and `pi` are reported as percentages. `Delta_sel` is reported in percentage points (pp). Headline family values are generally displayed to 3 decimals; target percentile tables generally to 2 decimals; target losses/floors generally to 3 decimals. Full-precision machine-readable values, where available, should be used for recomputation rather than rounded display values.

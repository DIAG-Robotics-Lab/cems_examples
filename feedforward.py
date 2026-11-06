import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import solve_ivp

# ======================= Parameters =======================
# --- Real motor:  J dω/dt = τ_e - τ_l - B ω ---
J = 0.05          # Inertia [kg m^2]
B = 0.1           # Viscous friction [N m s/rad]
tau_l = 0.5       # Load torque [N m] (step)
t_load = 4.0      # Time at which the load is applied [s]
w0 = 0.0          # Initial motor speed ω(0) [rad/s]

# --- Model used by the feedforward (estimates, ch. 5) ---
J_hat = 0.05      # Estimated inertia Ĵ
B_hat = 0.1       # Estimated friction B̂
tau_l_hat = 0.5   # Estimated load torque τ̂_l (0 = load not compensated)

# --- Feedback PI controller (ki = 0 -> pure P) ---
kp = 0.5          # Proportional gain
ki = 2.0          # Integral gain

# --- Sinusoidal reference: ω_ref(t) = offset + A sin(2π f t + phase) ---
A = 1.0           # Amplitude [rad/s]
f = 1.0           # Frequency [Hz]
phase = np.pi / 2 # Phase [rad]. π/2 -> ω_ref(0) = offset + A ≠ ω(0) (unmatched IC)
offset = 0.0      # Constant offset [rad/s]

t_end = 6.0       # Simulation time [s]

# Control mode. Options: 'fb', 'ff', 'fb+ff', 'all'
selection = 'all'

# Animation parameters
n_frames = 200    # Animation frames
interval = 30     # ms between frames
# ==========================================================

modes = ['fb', 'ff', 'fb+ff'] if selection == 'all' else [selection]
names = {'fb': 'Feedback only', 'ff': 'Feedforward only', 'fb+ff': 'Feedback + feedforward'}
t = np.linspace(0, t_end, 3000)


def w_ref(t):
    # Sinusoidal speed reference
    return offset + A * np.sin(2 * np.pi * f * t + phase)


def dw_ref(t):
    # Analytic derivative of the reference (needed by the feedforward)
    return A * 2 * np.pi * f * np.cos(2 * np.pi * f * t + phase)


def load(t, value):
    # Step load applied at t_load
    return value * (t >= t_load)


def torques(t, w, e_int, mode):
    # Feedback (PI) and feedforward (5.9) torque components
    e = w_ref(t) - w
    tau_fb = kp * e + ki * e_int if 'fb' in mode else 0.0
    tau_ff = (J_hat * dw_ref(t) + B_hat * w_ref(t) + load(t, tau_l_hat)
              if 'ff' in mode else 0.0)
    return tau_fb, tau_ff


def dynamics(t, x, mode):
    # States: x = [ω, ∫e dt]
    w, e_int = x
    tau_fb, tau_ff = torques(t, w, e_int, mode)
    dw = (tau_fb + tau_ff - load(t, tau_l) - B * w) / J
    return [dw, w_ref(t) - w]


# Simulate every selected mode
results = {}
for mode in modes:
    sol = solve_ivp(dynamics, (0, t_end), [w0, 0.0], t_eval=t, args=(mode,),
                    max_step=t[1] - t[0])
    w, e_int = sol.y
    tau_fb, tau_ff = torques(t, w, e_int, mode)
    results[mode] = (w, w_ref(t) - w, tau_fb + tau_ff)

# Print error indicators
print(f"ω_ref(0) = {w_ref(0):.3f}, ω(0) = {w0:.3f}")
print(f"Model error: Ĵ/J = {J_hat / J:.2f}, B̂/B = {B_hat / B:.2f}, τ̂_l/τ_l = "
      f"{tau_l_hat / tau_l if tau_l else float('nan'):.2f}")
last = t >= t_end - 1 / f   # last reference period
for mode, (w, e, _) in results.items():
    print(f"  {names[mode]:24s} max|e| last period = {np.abs(e[last]).max():.4f}, "
          f"RMS error = {np.sqrt(np.mean(e**2)):.4f}")

# Plot speed, error and applied torque
fig, (ax_w, ax_e, ax_t) = plt.subplots(3, 1, figsize=(10, 9), sharex=True,
                                       gridspec_kw={'height_ratios': [2, 1, 1]})
ax_w.plot(t, w_ref(t), 'k--', lw=1.5, label="Reference")
lines = []   # (speed, error, torque) lines, filled by the animation
for mode in results:
    line, = ax_w.plot([], [], label=names[mode])
    e_line, = ax_e.plot([], [], color=line.get_color())
    t_line, = ax_t.plot([], [], color=line.get_color())
    lines.append((line, e_line, t_line))

for ax in (ax_w, ax_e, ax_t):
    ax.axvline(t_load, color='gray', ls=':', lw=1)
    # Shade the time ranges without / with load
    ax.axvspan(0, t_load, color='tab:green', alpha=0.08, lw=0)
    ax.axvspan(t_load, t_end, color='tab:red', alpha=0.08, lw=0)
    ax.grid(True)

# Label each shaded range with its load torque (x in data, y in axes coords)
for x, val in ((t_load / 2, 0.0), ((t_load + t_end) / 2, tau_l)):
    ax_w.text(x, 0.03, rf"$\tau_l = {val}$ N m", transform=ax_w.get_xaxis_transform(),
              ha='center', va='bottom', fontsize=11,
              bbox=dict(boxstyle='round', fc='white', alpha=0.7, lw=0))
ax_e.axhline(0, color='k', lw=0.8)
ax_w.set_title(f"J_hat/J={J_hat / J:.2f}, B_hat/B={B_hat / B:.2f}, tau_l_hat={tau_l_hat}, "
               f"τ_l={tau_l}, ω(0)={w0}, ω_ref(0)={w_ref(0):.2f}")
ax_w.set_ylabel("Speed [rad/s]")
ax_e.set_ylabel("Error [rad/s]")
ax_t.set_ylabel("Motor torque τ_e [N m]")
ax_t.set_xlabel("Time [s]")
ax_w.legend(loc='upper right')
ax_w.set_xlim(0, t_end)

# Fixed axis limits (lines start empty, so autoscale can't be used)
def limits(ax, arrays):
    lo, hi = min(a.min() for a in arrays), max(a.max() for a in arrays)
    pad = 0.1 * (hi - lo + 1e-9)
    ax.set_ylim(lo - pad, hi + pad)

limits(ax_w, [w for w, _, _ in results.values()] + [w_ref(t)])
limits(ax_e, [e for _, e, _ in results.values()])
limits(ax_t, [tau for _, _, tau in results.values()])
time_text = ax_w.text(0.01, 0.92, '', transform=ax_w.transAxes)

# Frames map onto the fine simulation grid
idx = np.linspace(1, len(t), n_frames).astype(int)


def update(frame):
    k = idx[frame]
    for (line, e_line, t_line), (w, e, tau) in zip(lines, results.values()):
        line.set_data(t[:k], w[:k])
        e_line.set_data(t[:k], e[:k])
        t_line.set_data(t[:k], tau[:k])
    time_text.set_text(f"t = {t[k - 1]:.2f} s")
    return [l for trio in lines for l in trio] + [time_text]


ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=interval, blit=True)

plt.tight_layout()
plt.show()
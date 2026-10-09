import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import control as ct

# ======================= Parameters =======================
J = 0.05        # Inertia [kg m^2]
B = 0.1         # Viscous friction [N m s/rad]
kp = 2.0        # Proportional gain
ki = 5.0        # Integral gain
tau_l = 0.5     # Load torque [N m]
t_load = 1.0    # Time at which the load torque is applied [s]
t_end = 4.0     # Simulation time [s]

# Input type. Options: 'step', 'ramp'
input_type = 'step'
input_gain = 1.0  # step: amplitude [rad/s] | ramp: slope [rad/s^2]

# Set display mode. Options: 'p', 'pi', 'all'
selection = 'all'

n_points = 2000   # Simulation resolution (fine enough for fast poles)
n_frames = 200    # Animation frames
interval = 30     # ms between frames
# ==========================================================

s = ct.TransferFunction.s

# Plant and controllers
P_ideal = 1 / (J * s)
P_fric = 1 / (J * s + B)
C_p = kp
C_pi = kp + ki / s

# Time vector, reference and load torque
t = np.linspace(0, t_end, n_points)
u = input_gain * (np.ones_like(t) if input_type == 'step' else t)
d = (t >= t_load).astype(float)


def response(C, P, with_load):
    """Speed = W_ref * reference - W_dist * tau_l * load step."""
    _, w = ct.forced_response(ct.feedback(C * P, 1), T=t, U=u)
    if with_load:
        _, w_d = ct.forced_response(ct.feedback(P, C), T=t, U=d)
        w = w - tau_l * w_d
    return w


curves = []   # (label, speed)
if selection in ['p', 'all']:
    curves.append(("P-Control (ideal, no load)", response(C_p, P_ideal, False)))
    curves.append(("P-Control with friction and load", response(C_p, P_fric, True)))
if selection in ['pi', 'all']:
    curves.append(("PI-Control with friction and load", response(C_pi, P_fric, True)))

# Final tracking errors
print(f"Input: {input_type}, gain {input_gain}")
for label, w in curves:
    print(f"  {label:35s} error at t_end = {u[-1] - w[-1]:+.4f}")

# Figure: speed (top) and tracking error (bottom)
fig, (ax, ax_e) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                               gridspec_kw={'height_ratios': [2, 1]})
all_w = np.concatenate([w for _, w in curves] + [u])
all_e = np.concatenate([u - w for _, w in curves])
pad = 0.1 * (all_w.max() - all_w.min() + 1e-9)
ax.set_xlim(0, t_end)
ax.set_ylim(min(0, all_w.min()) - pad, all_w.max() + pad)
pad_e = 0.1 * (all_e.max() - all_e.min() + 1e-9)
ax_e.set_ylim(all_e.min() - pad_e, all_e.max() + pad_e)

ax.plot(t, u, 'k--', lw=1.5, zorder=5, label=f"Reference ({input_type})")
for a in (ax, ax_e):
    a.axvline(t_load, color='gray', ls=':', lw=1)
ax.text(t_load, ax.get_ylim()[0], ' load applied', color='gray', va='bottom')
ax_e.axhline(0, color='k', lw=0.8)

ax.set_ylabel("Speed [rad/s]")
ax_e.set_ylabel("Error [rad/s]")
ax_e.set_xlabel("Time [s]")
ax.grid(True)
ax_e.grid(True)

lines, err_lines = [], []
for label, _ in curves:
    line, = ax.plot([], [], label=label)
    e_line, = ax_e.plot([], [], color=line.get_color())
    lines.append(line)
    err_lines.append(e_line)
ax.legend(loc='best')
time_text = ax.text(0.01, 0.95, '', transform=ax.transAxes)

# Frames map onto the fine simulation grid
idx = np.linspace(1, n_points, n_frames).astype(int)


def update(frame):
    k = idx[frame]
    for line, e_line, (_, w) in zip(lines, err_lines, curves):
        line.set_data(t[:k], w[:k])
        e_line.set_data(t[:k], u[:k] - w[:k])
    time_text.set_text(f"t = {t[k - 1]:.2f} s")
    return lines + err_lines + [time_text]


ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=interval, blit=True)
plt.tight_layout()
plt.show()
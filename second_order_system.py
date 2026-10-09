import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import control as ct

# ======================= Parameters =======================
J = 0.05        # Inertia [kg m^2]
B = 0.1         # Viscous friction [N m s/rad]
kp = 0.3        # Proportional gain
ki = 2.0        # Integral gain

# Input type. Options: 'step', 'ramp'
input_type = 'step'
input_gain = 1.0  # step: amplitude [rad/s] | ramp: slope [rad/s^2]

# Scheme to show. Options: 'standard', 'relocated', 'all'
selection = 'all'

# Damping comparison (Fig. 3.1 / 3.2): if True, kp is recomputed
# for every xi in xi_list (ki fixed) -> kp = 2*xi*J*wn - B
compare_damping = False
xi_list = [0.3, 1.0, 2.0]

# Animation parameters
t_end = 5.0     # Simulation time [s]
n_frames = 200  # Animation frames
interval = 30   # ms between frames
# ==========================================================

# Create the atomic transfer function element
s = ct.TransferFunction.s
P = 1 / (J * s + B)


def closed_loops(kp, ki):
    W_std = ct.feedback((kp + ki / s) * P, 1)              # has a zero
    W_rel = ct.feedback(ki / s * ct.feedback(P, kp), 1)    # no zeros
    return ct.minreal(W_std, verbose=False), ct.minreal(W_rel, verbose=False)


def kind_of(xi):
    if np.isclose(xi, 1.0):
        return 'critically damped'
    return 'underdamped' if xi < 1 else 'overdamped'


wn0 = np.sqrt(ki / J)
cases = [(2 * x * J * wn0 - B, ki) for x in xi_list] if compare_damping else [(kp, ki)]
schemes = ['standard', 'relocated'] if selection == 'all' else [selection]
T = np.linspace(0, t_end, n_frames)

# Input signal
u = input_gain * (np.ones_like(T) if input_type == 'step' else T)

# Pre-compute all responses
data = []   # (scheme index, label, y)
for kp_i, ki_i in cases:
    wn = np.sqrt(ki_i / J)
    xi = (kp_i + B) / (2 * J * wn)
    W_std, W_rel = closed_loops(kp_i, ki_i)
    for k, name in enumerate(schemes):
        W = W_std if name == 'standard' else W_rel
        _, y = ct.forced_response(W, T=T, U=u)
        data.append((k, f"ξ={xi:.2f} ({kind_of(xi)})", y))

y_max = max(max(y.max() for _, _, y in data), u.max()) * 1.1

fig, axes = plt.subplots(1, len(schemes), figsize=(6 * len(schemes), 5), squeeze=False)
axes = axes[0]
for ax, name in zip(axes, schemes):
    ax.set_xlim(0, t_end)
    ax.set_ylim(0, y_max)
    ax.plot(T, u, 'k--', lw=1, label=f"Reference ({input_type})")
    ax.set_title(f"{name.capitalize()} PI scheme - {input_type} input")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Speed [rad/s]")
    ax.grid(True)

lines, dots = [], []
for k, label, _ in data:
    line, = axes[k].plot([], [], label=label)
    dot, = axes[k].plot([], [], 'o', color=line.get_color())
    lines.append(line)
    dots.append(dot)

for ax in axes:
    ax.legend(fontsize=8)
time_text = axes[0].text(0.02, 0.95, '', transform=axes[0].transAxes)


def update(frame):
    for line, dot, (_, _, y) in zip(lines, dots, data):
        line.set_data(T[:frame + 1], y[:frame + 1])
        dot.set_data([T[frame]], [y[frame]])
    time_text.set_text(f"t = {T[frame]:.2f} s")
    return lines + dots + [time_text]


ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=interval, blit=True)
plt.tight_layout()
plt.show()
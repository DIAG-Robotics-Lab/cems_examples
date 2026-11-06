import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.animation as animation
from scipy import signal

# ======================= Parameters =======================
# --- Continuous signal: x(t) = Σ A_i sin(2π f_i t + φ_i) ---
freqs = [1.0, 7.0]      # Component frequencies [Hz]
amps = [1.0, 0.4]       # Component amplitudes
phases = [0.0, 0.0]     # Component phases [rad]
t_end = 2.0             # Displayed time window [s]

# --- Sampling ---
fs = 20.0               # Sampling frequency [Hz] (static figures)

# --- Display mode ---
animate = True         # False -> 4 separate static figures | True -> 1 animated window
fs_max = 30.0           # Animation: fs sweeps from fs_max ...
fs_min = 3.0            # ... down to fs_min [Hz]
n_frames = 150          # Animation frames
interval = 80           # ms between frames

# Reconstruction from samples. Options: 'sinc' (ideal, Shannon), 'zoh' (hold), 'both'
reconstruction = 'sinc'

# --- Anti-aliasing filter (analog Butterworth before the sampler) ---
anti_alias = False
filter_order = 4        # Filter order (higher = sharper)
cutoff_ratio = 0.5      # Cut-off = cutoff_ratio * fs (0.5 -> Nyquist frequency)

# --- Quantization ---
n_bits = 3              # Bit depth -> 2^n_bits levels
full_scale = None       # Quantizer range ±full_scale; None -> sum of amplitudes

# --- Output figures ---
save_figs = not animate # True -> save figures (static) or a GIF (animation) to save_dir
save_dir = 'figures'    # Output folder
save_format = 'pdf'     # Static figures: 'pdf', 'png', 'svg', ...
# ==========================================================

freqs, amps, phases = map(np.asarray, (freqs, amps, phases))
V = full_scale if full_scale else amps.sum()   # quantizer full scale
levels = 2 ** n_bits
delta = 2 * V / levels                         # quantization step Δ
t = np.linspace(0, t_end, 2000)                # "continuous" time


def components(fs):
    # Amplitude and phase of each component after the (optional) anti-aliasing filter
    if not anti_alias:
        return amps, phases
    b, a = signal.butter(filter_order, 2 * np.pi * cutoff_ratio * fs, analog=True)
    _, H = signal.freqs(b, a, worN=2 * np.pi * freqs)
    return amps * np.abs(H), phases + np.angle(H)


def x_of(t, A, ph):
    # Sum of sinusoids evaluated at times t
    return np.sum(A[:, None] * np.sin(2 * np.pi * freqs[:, None] * t + ph[:, None]), axis=0)


def alias(f, fs):
    # Apparent frequency after sampling: folded into [0, fs/2]
    return np.abs(f - fs * np.round(f / fs))


def quantize(x):
    # Uniform mid-rise quantizer on [-V, V] with 2^n_bits levels (clips outside)
    q = delta * (np.floor(x / delta) + 0.5)
    return np.clip(q, -V + delta / 2, V - delta / 2)


# Summary in the terminal
print(f"Highest frequency {freqs.max()} Hz -> Shannon-Nyquist requires fs >= {2 * freqs.max()} Hz")
for f_i in freqs:
    print(f"  {f_i:6.2f} Hz is seen as {alias(f_i, fs):6.2f} Hz when fs = {fs} Hz")
print(f"Quantizer: {n_bits} bit, {levels} levels, step Δ = {delta:.4g}, "
      f"ideal SNR (full-scale sine) = {6.02 * n_bits + 1.76:.1f} dB")

if animate:
    # One window with the 4 plots, redrawn at every frame
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    ax_t, ax_f, ax_q, ax_e = axes.flat
else:
    # One separate figure per plot (name -> (fig, ax))
    figs = {name: plt.subplots(figsize=(8, 4.5))
            for name in ('time', 'spectrum', 'quantization', 'quantization_error')}
    ax_t, ax_f, ax_q, ax_e = (ax for _, ax in figs.values())
y_lim = 1.25 * max(V, amps.sum())
f_top = 1.1 * max(freqs.max(), fs_max if animate else fs)


def draw(fs):
    for ax in (ax_t, ax_f, ax_q, ax_e):
        ax.cla()   # clear the previous frame (no effect on static figures)
    A, ph = components(fs)
    Ts = 1 / fs
    # Samples also outside the window, so the sinc reconstruction has no edge effects
    n = np.arange(np.floor(-t_end / Ts), np.ceil(2 * t_end / Ts) + 1)
    tn = n * Ts
    xn = x_of(tn, A, ph)
    inside = (tn >= 0) & (tn <= t_end)
    aliasing = np.any((freqs > fs / 2) & (A > 0.01 * amps.max()))

    # --- Time domain: signal, samples, reconstruction ---
    ax_t.plot(t, x_of(t, amps, phases), color='gray', lw=1, label="Original x(t)")
    if anti_alias:
        ax_t.plot(t, x_of(t, A, ph), color='tab:blue', lw=1.5, label="After anti-alias filter")
    if reconstruction in ('sinc', 'both'):
        x_rec = np.sinc(fs * (t[:, None] - tn[None, :])) @ xn   # Whittaker-Shannon
        ax_t.plot(t, x_rec, 'r--', lw=1.5, label="Reconstruction (sinc)")
    if reconstruction in ('zoh', 'both'):
        ax_t.step(tn[inside], xn[inside], where='post', color='tab:orange', label="Zero-order hold")
    ax_t.plot(tn[inside], xn[inside], 'ko', ms=4, label="Samples")
    # Status: aliasing, residual aliasing (attenuated by the filter) or OK
    if not aliasing:
        status, color = "OK", 'green'
    elif anti_alias:
        a_max = A[freqs > fs / 2].max()
        status, color = f"RESIDUAL ALIASING (max alias amplitude {a_max:.2f})", 'darkorange'
    else:
        status, color = "ALIASING", 'red'
    ax_t.set_title(f"fs = {fs:.2f} Hz  (Nyquist fs/2 = {fs / 2:.2f} Hz)  →  {status}",
                   color=color, fontweight='bold')
    ax_t.set_xlim(0, t_end)
    ax_t.set_ylim(-y_lim, y_lim)
    ax_t.set_xlabel("Time [s]")
    ax_t.set_ylabel("x(t)")

    # --- Frequency domain: components and their aliases ---
    ax_f.axvspan(0, fs / 2, color='tab:green', alpha=0.12, label="0 … fs/2 (representable)")
    for k in range(1, int(f_top / (fs / 2)) + 1):
        ax_f.axvline(k * fs / 2, color='gray', ls=':', lw=0.8)   # folding lines
    ax_f.axvline(fs, color='k', ls='--', lw=1, label="fs")
    ax_f.stem(freqs, amps, linefmt='C7-', markerfmt='C7o', basefmt=' ', label="Original")
    if anti_alias:
        ax_f.stem(freqs, A, linefmt='C0-', markerfmt='C0o', basefmt=' ', label="Filtered")
    above = freqs > fs / 2
    if above.any():
        fa = alias(freqs[above], fs)
        ax_f.stem(fa, A[above], linefmt='r-', markerfmt='r^', basefmt=' ', label="Aliases")
        for f_i, f_a, a_i in zip(freqs[above], fa, A[above]):
            ax_f.annotate('', xy=(f_a, a_i), xytext=(f_i, a_i),
                          arrowprops=dict(arrowstyle='->', color='r', connectionstyle='arc3,rad=0.3'))
    ax_f.set_xlim(0, f_top)
    ax_f.set_ylim(0, 1.3 * amps.max())
    ax_f.set_title("Spectrum: components above fs/2 fold back")
    ax_f.set_xlabel("Frequency [Hz]")
    ax_f.set_ylabel("Amplitude")

    # --- Quantization of the samples ---
    xs = xn[inside]
    xq = quantize(xs)
    ax_q.plot(t, x_of(t, A, ph), color='gray', lw=1, label="Signal")
    ax_q.step(tn[inside], xq, where='post', color='tab:purple', label=f"Quantized ({n_bits} bit)")
    ax_q.plot(tn[inside], xs, 'ko', ms=3, label="Samples")
    if levels <= 32:   # draw the levels only when they are readable
        for lvl in np.arange(-V + delta / 2, V, delta):
            ax_q.axhline(lvl, color='tab:purple', lw=0.5, alpha=0.3)
    ax_q.set_xlim(0, t_end)
    ax_q.set_ylim(-y_lim, y_lim)
    ax_q.set_title(f"Quantization: {levels} levels, Δ = {delta:.3g}")
    ax_q.set_xlabel("Time [s]")
    ax_q.set_ylabel("x")

    # --- Quantization error (noise) ---
    e = xq - xs
    snr = 10 * np.log10(np.mean(xs ** 2) / np.mean(e ** 2))
    ax_e.stem(tn[inside], e, linefmt='C4-', markerfmt='C4o', basefmt='k-')
    ax_e.axhline(delta / 2, color='k', ls='--', lw=0.8, label="±Δ/2")
    ax_e.axhline(-delta / 2, color='k', ls='--', lw=0.8)
    ax_e.set_xlim(0, t_end)
    ax_e.set_title(f"Quantization error: SNR = {snr:.1f} dB")
    ax_e.set_xlabel("Time [s]")
    ax_e.set_ylabel("x_q − x")

    for ax in (ax_t, ax_f, ax_q, ax_e):
        ax.grid(True)
        ax.legend(fontsize=8, loc='upper right')


if save_figs:
    os.makedirs(save_dir, exist_ok=True)

if animate:
    # fs sweeps from fs_max down to fs_min
    fs_values = np.linspace(fs_max, fs_min, n_frames)
    draw(fs_values[0])
    fig.tight_layout()
    ani = animation.FuncAnimation(fig, lambda i: draw(fs_values[i]), frames=n_frames,
                                  interval=interval)
    if save_figs:
        path = os.path.join(save_dir, f"sampling_sweep_fs{fs_max:g}-{fs_min:g}.gif")
        print(f"Saving {path} (may take a while)...")
        ani.save(path, writer='pillow', fps=1000 / interval)
else:
    draw(fs)
    # Layout and (optional) saving: e.g. figures/sampling_time_fs10.pdf
    for name, (fig, _) in figs.items():
        fig.tight_layout()
        if save_figs:
            path = os.path.join(save_dir, f"sampling_{name}_fs{fs:g}.{save_format}")
            fig.savefig(path, bbox_inches='tight')
            print(f"Saved {path}")

plt.show()

# CEMS – Control Examples in Python

A collection of small Python scripts that simulate and plot the behaviour of
controlled electric motors and second-order systems, following the CEMS course
notes. Every script has its **parameters at the top of the file**, so you can
change a value, run the script again and immediately see how the response changes.
Most scripts show their result as an **animation**: the curves are drawn
progressively over time. `sampling.py` can do both: static figures ready
to be saved and used in documents, or an animation.

New scripts will be added to this folder over time.

---

## Contents

1. [What you need](#1-what-you-need)
2. [Installing Python](#2-installing-python)
3. [Using the terminal](#3-using-the-terminal)
4. [Getting the scripts](#4-getting-the-scripts)
5. [Installing the required libraries](#5-installing-the-required-libraries)
6. [Running a script](#6-running-a-script)
7. [Changing the parameters](#7-changing-the-parameters)
8. [The scripts](#8-the-scripts)
9. [Troubleshooting](#9-troubleshooting)
10. [Adding new scripts](#10-adding-new-scripts)

---

## 1. What you need

- A computer running Windows, macOS or Linux
- **Python 3.9 or newer**
- A **text editor** to open and change the scripts. Any of these is fine:
  - [Visual Studio Code](https://code.visualstudio.com/) (recommended, free)
  - IDLE (installed together with Python)
  - Notepad / TextEdit (they work, but have no colours or help)
- An internet connection, the first time only, to install the libraries

You do **not** need to know how to program. You only need to change numbers at
the top of a file and run it.

---

## 2. Installing Python

A Python script is a plain text file ending in `.py`. To run it, you need the
**Python interpreter**, the program that reads the file and executes it line by line.

### Windows

1. Go to <https://www.python.org/downloads/> and download the latest Python 3.
2. Run the installer.
   **Important:** on the first screen tick **"Add python.exe to PATH"**, then
   click **Install Now**.
3. When it finishes, check it works (see [Section 3](#3-using-the-terminal)):
   ```
   python --version
   ```
   You should see something like `Python 3.12.4`. If `python` is not found, try `py --version`.

### macOS

1. Download the macOS installer from <https://www.python.org/downloads/> and run it.
2. Check it works:
   ```
   python3 --version
   ```
   On macOS, always type `python3` and `pip3` instead of `python` and `pip`.

### Linux

Python 3 is usually already installed. Check with `python3 --version`.
If it is missing (Ubuntu/Debian):
```
sudo apt install python3 python3-pip python3-venv
```

---

## 3. Using the terminal

The **terminal** (also called *command line*, *command prompt* or *shell*) is a
window where you type commands instead of clicking.

**Opening it**

| System  | How to open the terminal |
|---------|--------------------------|
| Windows | Press `Win`, type **cmd** or **PowerShell**, press Enter |
| macOS   | Press `Cmd + Space`, type **Terminal**, press Enter |
| Linux   | `Ctrl + Alt + T` |
| VS Code | Menu **Terminal → New Terminal** (opens already in the project folder) |

**The few commands you need**

The terminal always "is" inside a folder, called the *current directory*.
Python looks for your script in that folder.

| What it does                  | Windows      | macOS / Linux |
|-------------------------------|--------------|---------------|
| Show the current folder       | `cd`         | `pwd`         |
| List the files in the folder  | `dir`        | `ls`          |
| Enter a folder                | `cd foldername` | `cd foldername` |
| Go up one folder              | `cd ..`      | `cd ..`       |

Tips:

- You can drag a folder from the file explorer into the terminal window to paste its full path, e.g. `cd ` + drag + Enter.
- If a folder name contains spaces, put it in quotes: `cd "My Documents"`.
- Press the up arrow (↑) to recall the previous command.

---

## 4. Getting the scripts

Download or copy this folder somewhere easy to find, e.g. your Desktop.
This is its whole content:

```
pkg/
├── README.md                ← this file
├── requirements.txt         ← list of the libraries the scripts need
├── notes.pdf                ← course lecture notes
├── motor_p_pi.py            ← motor speed control, P vs PI (Chapter 2)
├── second_order_system.py   ← second-order step/ramp response (Chapter 3)
├── feedforward.py           ← feedback vs feedforward (Chapter 5)
└── sampling.py              ← sampling, aliasing and quantization (Chapter 6.1)
```

Then open a terminal and move into the folder, for example:

```
cd Desktop/pkg
```

Type `dir` (Windows) or `ls` (macOS/Linux): you should see the `.py` files listed.

---

## 5. Installing the required libraries

Python on its own can't do control simulations or plots. The scripts use four
external **libraries** (packages of ready-made code):

| Library      | Used for |
|--------------|----------|
| `numpy`      | Numerical arrays and maths |
| `matplotlib` | Plots and animations |
| `scipy`      | Scientific routines (used by `control`) |
| `control`    | Transfer functions, feedback, step responses |

Libraries are installed with **pip**, Python's package installer.

### Step 5.1 (recommended): create a virtual environment

A *virtual environment* is a private folder holding the libraries for this
project, so they don't interfere with anything else on your computer. You
create it **once**. From inside the project folder:

| Windows | macOS / Linux |
|---------|---------------|
| `python -m venv .venv` | `python3 -m venv .venv` |

Then **activate** it. You must do this **every time you open a new terminal**:

| Windows (cmd) | Windows (PowerShell) | macOS / Linux |
|---------------|----------------------|---------------|
| `.venv\Scripts\activate` | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |

When it is active, the terminal line starts with `(.venv)`.

> On PowerShell, if you get an error about "running scripts is disabled", run
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, answer `Y`, then try again.

You can skip this step and install the libraries globally. It works too, but
it is less tidy.

### Step 5.2: install the libraries

With the environment active, install all the libraries listed in `requirements.txt`:

```
pip install -r requirements.txt
```

(on macOS/Linux without a virtual environment: `pip3 install -r requirements.txt`)

Check that it worked:

```
python -c "import numpy, matplotlib, control; print('All good')"
```

You only do this once. The libraries stay installed.

---

## 6. Running a script

From the terminal, inside the project folder (with `(.venv)` active if you created it):

| Windows | macOS / Linux |
|---------|---------------|
| `python second_order_system.py` | `python3 second_order_system.py` |

What happens:

1. Python reads the file from top to bottom.
2. Some scripts print numbers (errors, RMS values…) in the terminal.
3. A **plot window** opens and the **animation** starts: the curves are drawn
   progressively. When it reaches the end it starts again from the beginning.
   You can zoom, pan and save the figure with the toolbar buttons.
4. The script ends when you **close the plot window**. Until then, the terminal stays busy.

To stop a script that is running, press `Ctrl + C` in the terminal.

### Running from VS Code

1. **File → Open Folder…** and choose the project folder.
2. Install the **Python** extension when VS Code suggests it.
3. Bottom-right (or `Ctrl+Shift+P` → *Python: Select Interpreter*), select the `.venv` interpreter.
4. Open a script and press the ▶ **Run** button in the top-right corner.

### Running from IDLE

Open the `.py` file with IDLE (right click → *Edit with IDLE*) and press **F5**.

---

## 7. Changing the parameters

Every script starts with a block like this:

```python
# ======================= Parameters =======================
J = 0.05        # Inertia [kg m^2]
B = 0.1         # Viscous friction [N m s/rad]
kp = 0.3        # Proportional gain
ki = 2.0        # Integral gain
...
input_type = 'step'   # Options: 'step', 'ramp'
# ==========================================================
```

This is the **only part you need to edit**.

1. Open the script in your editor.
2. Change a value, e.g. `kp = 0.3` → `kp = 1.0`.
3. **Save** the file (`Ctrl + S` / `Cmd + S`).
4. Run it again (Section 6) and compare the plot.

Some syntax rules:

- Everything after `#` is a **comment**: Python ignores it. It explains the parameter and its unit.
- Decimal numbers use a **dot**, not a comma: `0.05`, not `0,05`.
- Text options go between **quotes**: `input_type = 'ramp'`. Use exactly one of the listed options.
- `True` / `False` must start with a capital letter.
- Lists use square brackets: `xi_list = [0.3, 1.0, 2.0]`.
- Do not change the indentation (spaces at the start of lines) of the code below the parameter block.

If you break something, Python stops and prints an error that tells you the line number.
Undo your change (`Ctrl + Z`) and try again.

---

## 8. The scripts

All scripts model a motor with inertia **J** and viscous friction **B**, whose
speed ω is controlled by a P or PI controller:

```
            1
P(s) = ─────────          C_P(s) = kp          C_PI(s) = kp + ki / s
        J s + B
```

All animated scripts share two animation parameters: `n_frames` (number of frames) and
`interval` (milliseconds between frames: larger means slower).

### `motor_p_pi.py` – motor speed control, P vs PI (Chapter 2)

Compares three cases, drawn as an animation:

- **P control without friction** (ideal plant 1/(Js)), no load
- **P control with friction and a load torque** τ_l: it shows a steady-state error
- **PI control with friction and load**: the integral action removes the error

The upper plot shows the speed, the lower one the **tracking error**
(reference − speed). The load is **applied at a chosen time** (`t_load`), so you
can watch the speed drop and the PI controller recover it. The final error of
each case is printed in the terminal.

| Parameter | Meaning |
|-----------|---------|
| `J`, `B`, `kp`, `ki` | System and controller values |
| `tau_l`, `t_load` | Load torque and the time it is applied |
| `t_end` | Simulation time [s] |
| `input_type` | `'step'` or `'ramp'` |
| `input_gain` | Step amplitude or ramp slope |
| `selection` | `'p'`, `'pi'` or `'all'` |
| `n_points` | Simulation resolution (keep it high for fast systems) |

Expected final errors (eqs. 2.21, 2.29, 2.34, 2.55):

| Case | Step | Ramp |
|---|---|---|
| P, ideal | 0 | J·A/kp |
| P, friction + load | (B·A + τ_l)/(B + kp) | keeps growing |
| PI, friction + load | 0 | B·A/ki |

Things to try: set `input_type = 'ramp'` and see that P control with friction
loses the ramp, while PI follows it with a small constant error.

### `second_order_system.py` – second-order response (Chapter 3)

Reproduces the transient analysis of the notes. With a PI controller
the closed loop is a second-order system:

```
              N(s)                         ki                 kp + B
W(s) = ─────────────────────      ωn = √ ───── ,      ξ = ──────────
        s² + 2ξωn s + ωn²                  J                 2 J ωn
```

Two schemes are compared side by side, drawn as an animation:

- **Standard PI**: N(s) = (kp s + ki)/J. It has a **zero**, which adds overshoot.
- **PI with relocated proportional action**: N(s) = ωn². It has no zeros.

| Parameter | Meaning |
|-----------|---------|
| `J`, `B`, `kp`, `ki` | System and controller values |
| `input_type` | `'step'` or `'ramp'` |
| `input_gain` | Step amplitude or ramp slope |
| `t_end` | Simulation time [s] |
| `selection` | `'standard'`, `'relocated'` or `'all'` |
| `compare_damping` | `True` → ignore `kp` and plot one curve per damping value in `xi_list` (like Fig. 3.2 and 3.3) |
| `xi_list` | Damping values to compare, e.g. `[0.3, 1.0, 2.0]` |

The type of response depends on the damping ξ:

| ξ | Poles | Response |
|---|-------|----------|
| 0 < ξ < 1 | complex conjugate, −ξωn ± jωn√(1−ξ²) | **underdamped**: oscillates |
| ξ = 1 | two coincident real, −ωn | **critically damped**: fastest without oscillations |
| ξ > 1 | two distinct real | **overdamped**: no oscillations, slower |

Things to try:

- Set `compare_damping = True` and compare the two schemes: the standard one
  overshoots even when ξ = 1, because of its zero.
- Increase `ki` and watch ωn grow (faster response, poles further from the origin).
- Switch to `'ramp'`: the error is B·A/ki for the standard scheme and
  (B+kp)·A/ki for the relocated one.

### `feedforward.py` – feedback vs feedforward (Chapter 5)

Tracks a **sinusoidal speed reference** with three strategies:

- **Feedback only**: PI controller on the error. It always lags behind a moving reference.
- **Feedforward only**: the torque is computed from a *model* of the motor,
  τ_ff = Ĵ·dω_ref/dt + B̂·ω_ref + τ̂_l (eq. 5.9). There is no correction, so any
  model error remains.
- **Feedback + feedforward**: the feedforward does most of the work and the
  feedback corrects what the model gets wrong.

The animation shows speed, tracking error and motor torque. The terminal prints
the error over the last period and the RMS error of each strategy.

| Parameter | Meaning |
|-----------|---------|
| `J`, `B`, `tau_l`, `t_load`, `w0` | **Real** motor: inertia, friction, load torque, load time, initial speed |
| `J_hat`, `B_hat`, `tau_l_hat` | **Estimates** used by the feedforward (set equal to the real ones for a perfect model) |
| `kp`, `ki` | Feedback PI gains (`ki = 0` → P only) |
| `A`, `f`, `phase`, `offset` | Reference ω_ref(t) = offset + A·sin(2πft + phase) |
| `t_end` | Simulation time [s] |
| `selection` | `'fb'`, `'ff'`, `'fb+ff'` or `'all'` |

Things to try:

- **Default** (perfect model, ω_ref(0) = 1 ≠ ω(0) = 0): feedforward alone tracks
  perfectly once the initial error decays slowly with τ = J/B (eq. 5.23 without
  feedback). Adding feedback makes it decay much faster, with τ = J/(B+kp).
- **Wrong model**, e.g. `J_hat = 0.03`, `B_hat = 0.05`: feedforward alone keeps a
  permanent error. Feedback + feedforward still works well.
- **Unknown load**, `tau_l_hat = 0`: after `t_load` the feedforward-only speed
  drifts away by τ_l/B, while any scheme with integral feedback recovers.
- Increase `f`: feedback-only gets worse and worse, while the feedforward doesn't care.

### `sampling.py` – sampling, aliasing and quantization (Chapter 6.1)

Shows what goes wrong when a continuous signal is turned into numbers. The
signal is a sum of sinusoids. With `animate = False` (default) it opens four
separate static figures, one per plot, and can save each of them to a file.
With `animate = True` the four plots are shown in one window and fs sweeps
from `fs_max` down to `fs_min`, so you can watch aliasing appear.

- **Time domain** (`time`): the signal, its samples and the signal
  *reconstructed* from the samples (ideal sinc interpolation and/or zero-order hold).
  The title turns red when fs < 2·f_max (Shannon-Nyquist, eq. 6.1).
- **Spectrum** (`spectrum`): each component, the green band 0 … fs/2 that can be
  represented, and the red **aliases**. Every component above fs/2 folds back to
  f_alias = |f − fs·round(f/fs)|.
- **Quantization** (`quantization`): the samples rounded to the 2^n_bits levels
  of the converter.
- **Quantization error** (`quantization_error`): always within ±Δ/2
  (Δ = range / 2^n_bits), with the measured SNR. The ideal value for a
  full-scale sine is about 6.02·n_bits + 1.76 dB.

With `save_figs = True` the figures are written to `save_dir` as
`sampling_<plot>_fs<fs>.<format>`, e.g. `figures/sampling_time_fs10.pdf`.
Since the file name contains fs, running the script with different `fs` values
does not overwrite the previous figures. Other parameter changes do, so rename
or move the files you want to keep. In animation mode a GIF is saved instead
(`sampling_sweep_fs30-3.gif`), which can take a minute: set `save_figs = False`
if you only want to watch it.

| Parameter | Meaning |
|-----------|---------|
| `freqs`, `amps`, `phases` | Components of the signal (lists of the same length) |
| `t_end` | Displayed time window [s] |
| `fs` | Sampling frequency [Hz] (static figures) |
| `animate` | `False` → 4 static figures, `True` → animated sweep of fs |
| `fs_max`, `fs_min`, `n_frames`, `interval` | Animation: fs range, number of frames, ms between frames |
| `reconstruction` | `'sinc'`, `'zoh'` or `'both'` |
| `anti_alias`, `filter_order`, `cutoff_ratio` | Butterworth low-pass before sampling, cut-off = `cutoff_ratio`·fs |
| `n_bits`, `full_scale` | Bit depth and converter range ±`full_scale` (`None` = automatic) |
| `save_figs`, `save_dir`, `save_format` | Save the figures (or the GIF), output folder, file format of static figures (`'pdf'`, `'png'`, `'svg'`…) |

Things to try:

- **Aliasing**: compare `fs = 30` (OK) with `fs = 10`. The 7 Hz component looks like a
  3 Hz one, and the reconstruction is a completely different signal that
  still passes through every sample.
- **Exactly at Nyquist**: `freqs = [5.0]`, `amps = [1.0]`, `phases = [0.0]`,
  `fs = 10`. The title says OK (fs = 2·f), yet every sample falls on a zero
  crossing and the signal disappears. In practice fs must be clearly **above** 2·f_max.
- **Anti-aliasing filter**: `anti_alias = True`. The 7 Hz component is attenuated
  before sampling, so the alias shrinks. Lower `cutoff_ratio` or raise
  `filter_order` to remove it further: a real filter is not a perfect cut at fs/2.
- **Bit depth**: change `n_bits` from 2 to 8 and watch the staircase and the SNR.
  Each extra bit halves Δ and adds about 6 dB.
- **Saturation**: `full_scale = 0.8` (smaller than the signal) makes the
  converter clip, and the error grows beyond ±Δ/2.

---

## 9. Troubleshooting

| Problem | Solution |
|---------|----------|
| `'python' is not recognized…` (Windows) | Use `py` instead of `python`, or reinstall Python with **"Add to PATH"** ticked |
| `command not found: python` (macOS/Linux) | Use `python3` |
| `ModuleNotFoundError: No module named 'control'` | The libraries are not installed in the Python you are using. Activate `.venv` and run `pip install -r requirements.txt` again |
| `can't open file 'motor_p_pi.py': No such file or directory` | You are in the wrong folder. Use `cd` to go into the project folder and check with `dir` / `ls` |
| `SyntaxError` after editing | Check the line shown: a missing quote, a comma instead of a dot, or a changed indentation |
| No window appears | It may be hidden behind other windows. Check the taskbar/dock |
| The animation does not move (Spyder / Jupyter) | These show static images by default. Run the script from the terminal, or type `%matplotlib qt` in the console first |
| The terminal seems stuck | The script is waiting for you to close the plot window |

---

## 10. Adding new scripts

To keep the collection consistent, each new script should:

- Be a single `.py` file in this folder, with a clear name (e.g. `position_control.py`)
- Start with a **parameter block** between `# ===` lines, with units and options in the comments
- Show its result as an animation, with the `n_frames` and `interval` parameters
  (and, like `sampling.py`, optionally as static figures meant for documents)
- Add any new library to `requirements.txt`
- Get a short section in [Section 8](#8-the-scripts) of this README

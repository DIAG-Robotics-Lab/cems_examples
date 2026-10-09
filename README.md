# CEMS – Control Examples in Python

A collection of small Python scripts that simulate and plot the behaviour of
controlled electric motors and second-order systems, following the CEMS course
notes. Every script has its **parameters at the top of the file**, so you can
change a value, run the script again and immediately see how the response changes.

New scripts will be added to this folder over time.

---

## Contents

- [CEMS – Control Examples in Python](#cems--control-examples-in-python)
  - [Contents](#contents)
  - [1. What you need](#1-what-you-need)
  - [2. Installing Python](#2-installing-python)
    - [Windows](#windows)
    - [macOS](#macos)
    - [Linux](#linux)
  - [3. Using the terminal](#3-using-the-terminal)
  - [4. Getting the scripts](#4-getting-the-scripts)
  - [5. Installing the required libraries](#5-installing-the-required-libraries)
    - [Step 5.1 (recommended): create a virtual environment](#step-51-recommended-create-a-virtual-environment)
    - [Step 5.2: install the libraries](#step-52-install-the-libraries)
  - [6. Running a script](#6-running-a-script)
    - [Running from VS Code](#running-from-vs-code)
    - [Running from IDLE](#running-from-idle)
  - [7. Changing the parameters](#7-changing-the-parameters)
  - [8. Troubleshooting](#8-troubleshooting)

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

Download or copy this folder somewhere easy to find, e.g. your Desktop. It looks like this:

```
CEMS-control-examples/
├── README.md                  ← this file
├── requirements.txt           ← list of the libraries the scripts need
├── motor_p_pi.py              ← motor speed control with proportional/integral action, animated
└── second_order_system.py     ← second-order step/ramp response, animated
```

Then open a terminal and move into the folder, for example:

```
cd Desktop/cems_examples
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
| `python second_order.py` | `python3 second_order.py` |

What happens:

1. Python reads the file from top to bottom.
2. Some numbers (poles, damping, errors…) are printed in the terminal.
3. A **plot window** opens. You can zoom, pan and save the figure with the toolbar buttons.
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


## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `'python' is not recognized…` (Windows) | Use `py` instead of `python`, or reinstall Python with **"Add to PATH"** ticked |
| `command not found: python` (macOS/Linux) | Use `python3` |
| `ModuleNotFoundError: No module named 'control'` | The libraries are not installed in the Python you are using. Activate `.venv` and run `pip install -r requirements.txt` again |
| `can't open file 'motor.py': No such file or directory` | You are in the wrong folder. Use `cd` to go into the project folder and check with `dir` / `ls` |
| `SyntaxError` after editing | Check the line shown: a missing quote, a comma instead of a dot, or a changed indentation |
| No window appears | It may be hidden behind other windows. Check the taskbar/dock |
| The animation does not move (Spyder / Jupyter) | These show static images by default. Run the script from the terminal, or type `%matplotlib qt` in the console first |
| The terminal seems stuck | The script is waiting for you to close the plot window |

---
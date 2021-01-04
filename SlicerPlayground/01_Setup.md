# Initial setup

This wlakthrough is done on macOS 11.1. Everything that's done inside Slicer is OS-agnostic.
Basic system setup on linux should be very similar to what's written here.

In order to simplify the workflow - local Slicer environment will be used. The Jupyter lab server will be started and setup from inside Slicer.

## Setup actions

The goal is to setup a jupyter lab environment with some plugins.

Steps:

1. Install latest version of Slicer
2. Ensure that node.js is in the same PATH as Slicer
3. Install Jupyter lab
4. Install Jupyter lab extensions
5. Launch Jupyter lab in Slicer

All commands will be called from mac terminal.

### 1. Install latest version of Slicer


In order to simplify command input add an environment variable with slicer executable path

```bash
export SLICER_PATH="/Applications/MedicalImaging/Slicer.app/Contents/MacOS/Slicer"
```

To update pip in the Slicer python environment call:

```bash
$SLICER_PATH -c "pip_install('--upgrade pip')"
```

### 2. Ensure that node.js is in the same PATH as Slicer

To add Slicer binaries location to system path, add the following lines to the `.bash_profile` or `.bashrc` file:

```bash
# 3D Slicer paths
# export PATH="/Applications/MedicalImaging/Slicer.app/Contents/lib/Python/bin:${PATH}"
```

### 3. Install Jupyter lab

Install dependencies:

```bash
$SLICER_PATH -c "pip_install('jupyter ipywidgets ipyevents ipycanvas --no-warn-script-location')"
$SLICER_PATH -c "pip_install('emoji')"  # this very important :)
$SLICER_PATH -c "pip_install('pandas matplotlib')"  # regular stuff everyone's used to having in their notebooks
$SLICER_PATH -c "pip_install('jupyterlab')"
$SLICER_PATH -c "slicer.util._executePythonModule('jupyter', ['labextension', 'install',
                                             '@jupyter-widgets/jupyterlab-manager',
                                             'ipycanvas',
                                             'ipyevents'])"
```

### 4. Install additional extensions

The jupyterlab_sublime extension provides some useful key bindings in the notebook editor (like like duplication and multi-cursor editing).

```bash
$SLICER_PATH -c "slicer.util._executePythonModule('jupyter', ['labextension', 'install', '@ryantam626/jupyterlab_sublime'])"
```

### 5. Launch Jupyter lab in Slicer

```bash
$SLICER_PATH --no-main-window -c "slicer.util._executePythonModule('jupyter', ['lab'])"
```

---

### Links, hints and extra tools

For more notebook examples check out:
[https://github.com/lassoan/SlicerNotebookDemos](https://github.com/lassoan/SlicerNotebookDemos)


Elyra jupyter lab extension provides some nice features for building workflows. Including a visual workflow editor and an interface to launching custom dockerized environments in k8s.

```python
pip_install('--upgrade elyra --no-cache-dir')
```

Very good explanation of an approach to hacking into slicer:
[https://discourse.slicer.org/t/fov-spacing-match-volumes/11905/4](https://discourse.slicer.org/t/fov-spacing-match-volumes/11905/4)


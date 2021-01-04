# Slicer Playground

A set of jupyter notebooks for playing around with the Slicer python API.

The notebooks illustrate usage of various tools bundled with slicer to achieve image processing tasks. The tools and API vary in each notebook. If external data is used in a notebook (like a picture or a NRRD image), the files are bundled with the playground in the `img/` folder.

## Playground

```
.
├── 01_Setup.md                     - Instructions to setup Jupyter Lab in Slicer
├── 02_Hello_Slicer.ipynb           - Basic verification that the environment is working
├── 03_Volumes&Orientations.ipynb   - Volume orientation notebook
├── 04_Data_sampling.ipynb          - Data sampling notebook
├── img                             - Playground image assets
└── playground_utils.py             - Helper functions
```
## Links, references and examples

The linked materials contain a big number of useful snippets, ready-to-use functions and logic that can be coppied.

Main:

- [Slicer python script repository](https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository)
- [Slicer documentation](https://slicer.readthedocs.io/en/latest/index.html)

Extra:

- [QIICR Slicer Development Toolbox.](https://github.com/QIICR/SlicerDevelopmentToolbox/blob/master/SlicerDevelopmentToolboxUtils/mixins.py)

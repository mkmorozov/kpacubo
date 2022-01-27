# KPACUBO
KPACUBO is a set Jupyter notebooks focused on the best practices in both software development and data science, namely,
- code reuse,
- explicit data gathering procedures,
- efficient data management,
- clear analysis validation criteria.

# SETUP
1) Create kpacubo environment:

conda env create -f environment.yml

2) Add kpacubo environment to Jupyter:

python -m ipykernel install --user --name=kpacubo

## ENVIRONMENT EXPORT

Windows: conda env export --no-builds | findstr -v "prefix" > environment.yml

Linux: conda env export --no-builds | grep -v "prefix" > environment.yml

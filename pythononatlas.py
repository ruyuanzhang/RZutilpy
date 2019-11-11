'''
Here are some instructions for setup python environment on CMRR servers (4/10)
'''

# Add anaconda path to your .bash_profile
PATH = /opt/local/anaconda3
export PATH

# Create an conda environment in your folder, you can specify environment name (envname) and python version (X.X). In your terminal, type:
cd yourfolder
conda create --prefix=envname python=X.X

# To activate the environment, please use obsolute path of environment. Conda will remove the original path of anaconda and add the new environment path. In your terminal, type:
source activate ..../yourfolder/envname

# deactivate the environment can use. In your teminal, type:
source deactivate


# But be careful, all packages will be installed under this folder. So might take a lot of space
# Note that the conda command used in windows and mac/linux are slightly different


## specific for Ruyuan Zhang on atlas4, atlas10 and stone



# rz created a python enviroment called 'atlaspythonenv' under the user home directory
# procedures to activate the environment

# 20181113, RZ change the name to 'rzpyenv'
cd ~
source activate ~/rzpyenv

# MUST USE OBSOLUTE PATH HERE !!!
#  deactivate ipython
source deactivate
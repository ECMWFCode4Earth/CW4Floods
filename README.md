# CW4Floods
Main repository for challenge 31/2022: Flood forecasting: the power of citizen science


### How to contribute 

- Clone the repositories
- Create the conda environment from the requirements.txt file using `conda create --name CW4F --file requirements.txt`
- Activate the conda environment using `conda activate CW4F`
- To make changes
  - Added it in the task for github
  - Link it to an issue
  - Create a branch for the same 
  - Make changes to your branch
  - Push your code
- Happy coding!

### Cheat sheet 
- To generate the requirements.txt `conda list -e > requirements.txt`

### BUGS

If you have issue with cfgrib
# install library
RUN pip uninstall cfgrib
RUN pip install ecmwflibs
RUN pip install eccodes==1.3.1
RUN pip install cfgrib
RUN pip install -e .

### To-DO 
- Improve the readme file.
- Discuss about the environment file
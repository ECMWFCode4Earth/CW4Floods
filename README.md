# CW4Floods
Main repository for challenge 31/2022: Flood forecasting: the power of citizen science

### How to contribute 

- Clone the repositories
- Create the conda environment from the requirements.txt file using `conda create --name CW4F --file requirements.txt`
- Activate the conda environment using `conda activate CW4F`
- Set the data folder structure 
```
  📦CW4F_data
  ┣ 📂efas
  ┃ ┣ 📜efas_2020.grib
  ┣ 📂glofas
  ┃ ┣ 📜glofas_2021.grib
  ┗ 📜export.csv
```
- To make changes
  - Added it in the task for github
  - Link it to an issue
  - Create a branch for the same 
  - Make changes to your branch
  - Push your code
- Happy coding!

### Cheat sheet 
- To generate the requirements.txt `conda env export > environment.yaml`

### BUGS

If you have issue with cfgrib

This might not be required.
- pip uninstall cfgrib
- conda install ecmwflibs
- conda install eccodes==1.3.1
- conda install cfgrib
- conda install -e .

and only this might be required
- conda install -c conda-forge cfgrib

### To-DO 
- Improve the readme file.

# Guidance On Cloning An Conda Environment To An Offline Linux PC

Inspired by these discussion:

* [How can I install a conda environment when offline?](https://stackoverflow.com/questions/31729731/how-can-i-install-a-conda-environment-when-offline)

* [conda install --offline does not work #2035](https://github.com/conda/conda/issues/2035)

## Part I: Prepare the package cache
* Find a linux machine with Internet connected. (Don't expect the packages on Windows machine to run properly on Linux.)
* Create a new environment 'truck' or whatever other name you want.
```sh
conda create -n truck
```
* Activate the environment.
```sh
source activate truck
```
* Install packages in the environment 'truck'.
```sh
conda install python=3.6 numpy scipy matplotlib h5py pandas
```
* Find the directory of "package cache".
```sh
conda info
```
* Know exactly what packages are used in the environment 'truck'.
```sh
conda list
```

## Part II: Move the data
* Create a folder `conda_moving` under your home directory.
```sh
mkdir -p $HOME/conda_moving
```
* Download two python scripts into the folder `conda_moving`.

    * `backup_pkgs.py`

    * `extract_pkgs.py`

* Save list of packages to file `list.txt`.
```sh
cd $HOME/conda_moving
# source activate truck
conda list --explict > list.txt
# Open `list.txt` and have a visual check.
```
* Backup the selected subset of package cache to the subfolder `pkg_bak`.
    * You may recheck the path to the package cache
```sh
conda info
```
    * Modify the variable `pkg_source_dir` in around 41th line of file `backup_pkgs.py`.
    * Create the subfolder `pkg_bak/linux-64` to store the package caches.
```sh
mkdir -p $HOME/conda_moving/pkg_bak/linux-64
```
    * Run the script.
```sh
python backup_pkgs.py
```
* Until now, you have caches folder (filled with .tar.bz2), list (.txt), and python scripts (.py) in folder `conda_moving`.
* Find your way to copy the folder to the offline machine.

## Part III: Install packages in offline mode
* Assume that you have the folder `conda_moving` ready under home directory of the offline machine.
```sh
cd $HOME/conda_moving
```
* Assume that you have conda (Anaconda, Miniconda, ...) installed and loaded on the offline machine.
```sh
# The way I use to load conda. It might not work on your machine.
module load anaconda3
``` 
* Extract the package caches from zipped file `*.tar.bz2` to their corresponding folders.
```sh
python extract_pkgs.py
```
* Let conda know about these package caches.
```sh
conda index $HOME/conda_moving/pkg_bak/linux-64
```
* Create the environment `yard` or whatever other name you want.
```sh
conda create -n yard --offline
```
* Activate the environment.
```sh
source activate yard
```
* Install the packages from caches.
```sh
conda install --offline -c file:/$HOME/conda_moving/pkg_bak python=3.6 numpy scipy matplotlib h5py pandas
```
* If lucky, the installation may end here.
* If not lucky enough, some errors of dependencies might prompt out. I suggest you remove those problematic packages from the list of installation. Let it go as far as you can. And refer to next section to add other accepted versions of missed packages.

## Part III: Add other packages to existed environment.
* Log onto the online machine. Install some packages.
* Copy those new caches `*.tar.bz2` to the folder `/$HOME/conda_moving/pkg_bak/linux-64` on the offline machine.
* Extract the zipped file `example.tar.bz2`.
```sh
mkdir example
tar -xjf example.tar.bz2 -C example/ 
```
* Index.
```sh
conda index $HOME/conda_moving/pkg_bak/linux-64
```
* Activate the environment and install the package.
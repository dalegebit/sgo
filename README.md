# sgo
Easy tool for those who want to submit slurm jobs

## Download

```
$ git clone https://github.com/dalegebit/sgo.git
```

## Install

Running:
```
$ cd sgo
$ bash ./install.sh
```
sgo.py will be copied to ~/.local/bin and ~/.local/bin will be added to PATH.


## Usage

```
$ sgo -h
usage: sgo [-h] [--ntasks NTASKS] [--nodes NODES] [--time TIME]
              [--output OUTPUT] [--user USER] [-o OUTPUT_SL]
              file

positional arguments:
  file                  name of the execution file

optional arguments:
  -h, --help            show this help message and exit
  --ntasks NTASKS       number of cores per node, default is 2
  --nodes NODES         number of nodes, default is 1
  --time TIME           expected running time in seconds, default is 10
  --output OUTPUT       name of the *.out file, default is
                        `execution_file_name`.out
  --user USER           user name, default is the current user
  -o OUTPUT_SL, --output_sl OUTPUT_SL
                        name of the *.sl file to build
```
To run the example in http://cacs.usc.edu/education/cs596/src/mpi/mpi\_simple.c, just type this after compilation:
```
$ sgo mpi_simple
```
Then mpi\_simple.sl will be automatically generated under the current directory and submitted to slurm.


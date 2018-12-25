#!/usr/bin/python

import argparse
import getpass
import sys
import os.path
from subprocess import call

# Configure argument parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--ntasks", type=int, default=1, help="number of cores per node, default is 1"
)
parser.add_argument(
    "-n", "--nodes", type=int, default=1, help="number of nodes, default is 1"
)
parser.add_argument(
    "-c", "--cpus", type=int, default=1, help="number of cpus per task, default is 1"
)
parser.add_argument(
    "-t",
    "--time",
    type=int,
    default=10,
    help="expected running time in seconds, default is 10",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="",
    help="the *.out file, default is `execution_file_name`.out",
)
parser.add_argument(
    "-u", "--user", type=str, default="", help="user name, default is the current user"
)
parser.add_argument(
    "-i",
    "--input_file",
    type=str,
    default="",
    help="the input file like *.in, default is none",
)
parser.add_argument(
    "-s", "--output_sl", type=str, default="", help="the *.sl file to build"
)
parser.add_argument(
    "-g", "--gpus", type=int, default=0, help="number of gpus, default is 0"
)
parser.add_argument(
    "--command", type=str, default="srun", help="run command, default is srun"
)
parser.add_argument(
    "--args", type=str, default="", help="other argument for the program"
)
parser.add_argument("file", type=str, help="the execution file")

# Parse and initialize arguments`
args = parser.parse_args()
if args.output == "":
    args.output = args.file + ".out"
if args.user == "":
    args.user = getpass.getuser()
if args.output_sl == "":
    args.output_sl = args.file + ".sl"
if args.command == "srun" or args.command == "mpirun":
    args.command += " -n $SLURM_NTASKS"

# Exit if the file provided does not exist
if not os.path.exists(args.file):
    sys.exit("{} does not exist!".format(args.file))
if args.input_file != "" and not os.path.exists(args.input_file):
    sys.exit("{} does not exist!".format(args.input_file))

# Build *.sl file
with open(args.output_sl, "w") as f:
    f.write("#!/bin/bash\n")
    f.write("#SBATCH --ntasks-per-node={}\n".format(args.ntasks))
    f.write("#SBATCH --nodes={}\n".format(args.nodes))
    f.write("#SBATCH --cpus-per-task={}\n".format(args.cpus))
    if args.gpus != 0:
        f.write("#SBATCH --gres=gpu:{}\n".format(args.gpus))
    f.write(
        "#SBATCH --time={}:{}:{}\n".format(
            str(args.time // 3600).zfill(2),
            str(args.time // 60 % 60).zfill(2),
            str(args.time % 60).zfill(2),
        )
    )
    f.write("#SBATCH --output={}\n".format(args.output))
    f.write("#SBATCH -A lc_an2\n")
    f.write("WORK_HOME=/home/rcf-proj/an2/{}\n".format(args.user))
    #  f.write("cd $WORK_HOME\n")
    srun_command = "{} {} {}".format(args.command, args.file, args.args)
    if args.input_file != "":
        srun_command += " < {}".format(args.input_file)
    f.write(srun_command)

# Submit the job
call(["sbatch", args.output_sl])

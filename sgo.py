#!/usr/bin/python

import argparse
import getpass
import sys
import os.path
from subprocess import call

# Configure argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--ntasks', type=int, default=1)
parser.add_argument('--nodes', type=int, default=1)
parser.add_argument('--time', type=int, default=10)
parser.add_argument('--output', type=str, default='')
parser.add_argument('--user', type=str, default='')
parser.add_argument('-o', '--output_sl', type=str, default='')
parser.add_argument('file', type=str)

# Parse and initialize arguments
args = parser.parse_args()
if args.output == '':
    args.output = args.file + '.out'
if args.user == '':
    args.user = getpass.getuser()
if args.output_sl == '':
    args.output_sl = args.file + '.sl'

# Exit if the file provided does not exist
if not os.path.exists(args.file):
    sys.exit("{} does not exist!".format(file))

# Build *.sl file
with open(args.output_sl, 'w') as f:
    f.write("#!/bin/bash\n")
    f.write("#SBATCH --ntasks-per-node={}\n".format(args.ntasks))
    f.write("#SBATCH --nodes={}\n".format(args.nodes))
    f.write("#SBATCH --time={}:{}:{}\n".format(
        str(args.time // 3600).zfill(2),
        str(args.time // 60 % 60).zfill(2),
        str(args.time % 60).zfill(2)
    ))
    f.write("#SBATCH --output={}\n".format(args.output))
    f.write("#SBATCH -A lc_an2\n")
    f.write("WORK_HOME=/home/rcf-proj/an2/{}\n".format(args.user))
    #  f.write("cd $WORK_HOME\n")
    f.write("srun -n $SLURM_NTASKS --mpi=pmi2 {}".format(args.file))

# Submit the job
call(['sbatch', args.output_sl])



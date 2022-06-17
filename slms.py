# SLMS: Seamless Loops Made Simple
# This is just a simple wrapper for the PyDub to generate simple loops.
# It is meant to be a command line utility with the following syntax:

# SINGLE FILE MODE:
# slms.py <file> -m <margin length> -o <output file>
# If -m is not provided, assume 0.5 seconds, or if the audio is less than 1.5 seconds, use 15% of the audio length.
# If -o is not provided, use the input file name with _seamless appended to the end of the file name.

# FOLDER MODE:
# slms.py <folder> -m <margin length> -o <output folder>
# Same rules for -m
# If -o is not provided, use the input folder name with _seamless appended to the end of the folder name.

# The only function we will use is slmsify(input, output, margin).
# This file is only for the CLI.

# Imports
import os # For file and folder operations
import sys # For getting command line arguments
import argparse # For parsing command line arguments
import scripts # For slmsify

# CLI
# Check if we have valid arguments supplied, if not, print usage and exit.

parser = argparse.ArgumentParser(description='SLMS: Seamless Loops Made Simple')
parser.add_argument('input', help='Input file or folder')
parser.add_argument('-m', '--margin', help='Margin length in seconds', default=0.5)
parser.add_argument('-o', '--output', help='Output file or folder')

def print_usage():
    parser.print_help()

args = parser.parse_args()

# Check if we valid arguments, if not, print usage and exit.
if not args.input:
    print_usage()
    sys.exit(1)

# Check if we have a valid input file or folder.
if not os.path.exists(args.input):
    print('Invalid input file or folder.')
    sys.exit(1)

# If path is a file, we can just use slmsify.
if os.path.isfile(args.input):
    scripts.slmsify(args.input, args.output, args.margin)
    sys.exit(0)

# If path is a folder, we need to iterate through all files in the folder and slmsify them.
if os.path.isdir(args.input):
    for file in os.listdir(args.input):
        if os.path.isfile(os.path.join(args.input, file)):
            scripts.slmsify(os.path.join(args.input, file), args.output, args.margin)
    sys.exit(0)

# If we get here, we have an invalid input path.
print_usage()
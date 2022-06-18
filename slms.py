# SLMS: Seamless Loops Made Simple
# This is just a simple wrapper for the PyDub to generate simple loops.
# It is meant to be a command line utility with the following syntax:

# SINGLE FILE MODE:
# slms.py <file> -m <margin length> -o <output file> -f <output format>
# If -m is not provided, assume 0.5 seconds, or if the audio is less than 1.5 seconds, use 15% of the audio length.
# If -o is not provided, use the input file name with _seamless appended to the end of the file name.
# If -f is not provided, use the format of the input file.

# FOLDER MODE:
# slms.py <folder> -d -m <margin length> -o <output folder> -f <output format>
# -d is a flag to indicate that the input is a folder.
# Same rules for -m
# If -o is not provided, use the input folder name with _seamless appended to the end of the folder name.
# Same rules for -f

# The only function we will use is slmsify(input, output, margin).
# Input and output must be paths to audio files, not directories.
# Margin will be an optional argument, the others must be provided, meaning we will need to generate default paths if output is not provided.

# For CLI behaviour, there are only a finite number of possibilities for the parameters.

# This file is only for the CLI.

# Imports
import os # For file and folder operations
import sys # For getting command line arguments
import argparse # For parsing command line arguments
import scripts # For slmsify

# CLI
# Check if we have valid arguments supplied, if not, print usage and exit.
parser = argparse.ArgumentParser(description='SLMS: Seamless Loops Made Simple')
parser.add_argument('input', help='Path to input file or folder')
# -d flag
parser.add_argument('-d', '--directory', action='store_true', help='Input is a folder', dest='directory')
# -m flag
parser.add_argument('-m', '--margin', type=float, help='Margin length in seconds', dest='margin')
# -o flag
parser.add_argument('-o', '--output', help='Path to output file or folder', dest='output')
# -f flag
parser.add_argument('-f', '--format', help='Format of output file. If not provided, use the same format as the input file.', dest='format')
args = parser.parse_args()

# First we determine which of the 12 cases we are in by finding input_type, input_path_validity, and ouput_path_supplied
input_type = "file" if not args.directory else "folder"
input_path_validity = "valid" if os.path.exists(args.input) else "invalid"
output_path_supplied = "yes" if args.output else "no"
output_path_exists = "yes" if args.output and os.path.exists(args.output) else "no"

def case(target_input_type, target_input_path_validity, target_output_path_supplied, target_output_path_exists):
    return (
        ((input_type == target_input_type) or (input_type == "*")) and 
        ((input_path_validity == target_input_path_validity) or (input_path_validity == "*")) and 
        ((output_path_supplied == target_output_path_supplied) or (output_path_supplied == "*")) and 
        ((output_path_exists == target_output_path_exists) or (output_path_exists == "*"))
        )

def ask_overwrite(path):
    print("Output file or folder already exists. Overwrite? (y/n)")
    while True:
        answer = input().lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Invalid answer. Try again.")

def generate_output_file(input_file):
    # We assume input_file is a complete path to an audio file.
    # We start with the default name of the input with _seamless appended to the end.
    # If it already exists, we further add another suffix _<number> to the end of the file name.
    input_file_name = input_file.split(".")[0]
    extensions = ".".join(input_file.split(".")[1:])
    print("debug", input_file_name, extensions)
    number = 0
    while os.path.exists(input_file_name + "_seamless" + ("_" + str(number) if number > 0 else "") + "." + extensions):
        number += 1
    return input_file_name + "_seamless" + ("_" + str(number) if number > 0 else "") + "." + extensions

def generate_output_folder(input_folder):
    # We assume input_folder is a complete path to a folder.
    # We start with the default name of the input with _seamless appended to the end.
    # If it already exists, we further add another suffix _<number> to the end of the folder name.
    input_folder_name = input_folder.split("/")[-1]
    number = 0
    while os.path.exists(input_folder_name + "_seamless" + ("_" + str(number) if number > 0 else "")):
        number += 1
    return input_folder_name + "_seamless" + ("_" + str(number) if number > 0 else "")

# Now, we write the code to handle each of the 16 cases.

# Case 1 -> file, valid, yes, yes: Ask the user if they want to overwrite the output file. If they do, do it. If not, exit.
def case_1():
    if ask_overwrite(args.output):
        scripts.slmsify(args.input, args.output, args.margin, args.format)
    else:
        print("Exiting.")
        sys.exit(0)
if case("file", "valid", "yes", "yes"):
    case_1()
# Case 2 -> file, valid, yes, no: Directly call slmsify with the input and output paths.
def case_2():
    scripts.slmsify(args.input, generate_output_file(args.input), args.margin, args.format)
if case("file", "valid", "yes", "no"):
    case_2()
# Case 3 -> file, valid, no, yes: Impossible.
# Case 4 -> file, valid, no, no: Generate a default output path and call slmsify with the input and output paths.
def case_4():
    scripts.slmsify(args.input, generate_output_file(args.input), args.margin, args.format)
if case("file", "valid", "no", "no"):
    case_4()
# Case 5-8 -> file, invalid, *, *: The input file is invalid. Print an error message and exit.
def case_5_8():
    print("Input file or folder is invalid.")
    sys.exit(1)
if case("file", "invalid", "*", "*"):
    case_5_8()
# Case 9 -> folder, valid, yes, yes: Call slmsify on every file in the input folder, and save the output (with the same file name) in the output folder. If the file exists, ask the user if they want to overwrite. If they do, do it. If not, exit.
def case_9():
    for file in os.listdir(args.input):
        # We assume file is a complete path to an audio file, remember to use basename to get the file name.
        output_file = os.path.join(args.output, os.path.basename(file))
        if os.path.exists(output_file):
            if not ask_overwrite(output_file):
                continue
        scripts.slmsify(os.path.join(args.input, file), output_file, args.margin, args.format)
if case("folder", "valid", "yes", "yes"):
    case_9()
# Case 10 -> folder, valid, yes, no: Same as case 9, just create the path before calling slmsify.
def case_10():
    # Recursively make the non-existing directories in the output path.
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    case_9()
if case("folder", "valid", "yes", "no"):
    case_10()
# Case 11 -> folder, valid, no, yes: Impossible.
# Case 12 -> folder, valid, no, no: Generate a default output path, and call case 9.
def case_12():
    output_folder = generate_output_folder(args.input)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    case_9()
if case("folder", "valid", "no", "no"):
    case_12()
# Case 13-16 -> folder, invalid, *, *: The input folder is invalid. Print an error message and exit.
def case_13_16():
    print("Input file or folder is invalid.")
    sys.exit(1)
if case("folder", "invalid", "*", "*"):
    case_13_16()
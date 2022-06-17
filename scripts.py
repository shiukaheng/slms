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


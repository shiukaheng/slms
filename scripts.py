# SLMS: Seamless Loops Made Simple
# This is just a simple wrapper for the PyDub to generate simple loops.
# It is meant to be a command line utility with the following syntax:

# This file contains the functional code for the SLMS program

import pydub # For audio manipulation

# Dict of supported audio file extensions to its format, this is not actually exhaustive, but it is a good start.
supported_extensions = {
    ".mp3": "mp3",
    ".wav": "wav",
    ".flac": "flac",
    ".aac": "aac",
    ".m4a": "m4a",
    ".ogg": "ogg",
    ".wma": "wma",
}

def check_if_output_format_is_supported(format):
    if format not in supported_extensions.values():
        raise Exception("Unsupported output format: "+format)

def get_audio_format_from_extension(path):
    print(path)
    file_extension = "."+".".join(path.split(".")[1:])
    # Check if the extension is actually supported (whatever is supported by FFMPEG), otherwise raise error.
    if not file_extension in supported_extensions:
        raise Exception("Unsupported file extension: "+file_extension)
    return supported_extensions[file_extension]

def open_audio_file(path):
    # Open the audio file and return it.
    return pydub.AudioSegment.from_file(path, get_audio_format_from_extension(path))

def slmsify(input, output, margin, output_format):
    # Do output format check if not none
    if output_format:
        check_if_output_format_is_supported(output_format)

    file = open_audio_file(input)

    # If margin == None
    if margin == None:
        # If input file is of length < 1.5 seconds, use 15% of the audio length.
        if len(file) < 1500:
            margin = len(file) * 0.15
        # Else, use 0.5 seconds.
        else:
            margin = 500

    margin = int(margin)

    print(f"Processing input file {input} with margin {margin}, output file {output}")
    
    # Split into start, middle, and end.
    start = file[:margin]
    middle = file[margin:len(file)-margin]
    end = file[len(file)-margin:]

    # Create new_start and new_end for a seamless loop.
    # Method: new_start will be crossfade of end to start
    new_start = end.append(start, crossfade=margin)

    # Combine new_start and new_end into new_middle.
    new_file = new_start + middle

    print(f"Outputting to {output}")
    computed_output_format = output_format or get_audio_format_from_extension(output)
    new_file.export(output, format=computed_output_format)
    print("Done!")
    return 0

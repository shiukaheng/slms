# SLMS - Seamless loops made simple
This minimalist python script that allows you to convert audio samples into seamless loops.

It uses PyDub and FFMPEG behind the scenes.
## CLI usage
```
slms.py [-h] [-d] [-m MARGIN] [-o OUTPUT] [-f FORMAT] input

positional arguments:
  input                 Path to input file or folder

options:
  -h, --help            show this help message and exit
  -d, --directory       Input is a folder
  -m MARGIN, --margin MARGIN
                        Margin length in seconds
  -o OUTPUT, --output OUTPUT
                        Path to output file or folder
  -f FORMAT, --format FORMAT
                        Format of output file. If not provided, use the same format as the input file.
````
## Dependencies
### MacOS
```
brew install libav
- OR -
brew install ffmpeg
```
### Linux
```
apt-get install libav-tools libavcodec-extra
- OR -
apt-get install ffmpeg libavcodec-extra
```
### Windows
- Download and extract libav from Windows binaries provided [here](http://builds.libav.org/windows/).
- Add the libav /bin folder to your PATH envvar
- pip install pydub

## Issues
- As of now, it is suggested that you use lossless formats (e.g. .wav), as FFMPEG is unable to seamlessly merge together cut audio. It should be a simple fix though, by converting the source format to wav, then converting the results back to the target format.

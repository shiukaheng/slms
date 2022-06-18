# SLMS - Seamless loops made simple
This minimalist python script that allows you to convert audio samples into seamless loops. The idea is really simple, we use the audio's ending to crossfade with the beginning, so when it loops around, it fades seamlessly from the end to the start again. The audio will be shorter though.

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
### PDM
This repo uses PDM for dependency management. See how you can get it [here](https://github.com/shiukaheng/slms/edit/main/README.mdhttps://pdm.fming.dev/latest/#installation). Once you have it, run ```pdm install```, and once you have the other dependencies installed, you can run the script using ```pdm run python slms.py [args]```
### FFMPEG / LibAV
#### MacOS
```
brew install libav
- OR -
brew install ffmpeg
```
#### Linux
```
apt-get install libav-tools libavcodec-extra
- OR -
apt-get install ffmpeg libavcodec-extra
```
#### Windows
- Download and extract libav from Windows binaries provided [here](http://builds.libav.org/windows/).
- Add the libav /bin folder to your PATH envvar
- pip install pydub

## Issues
- As of now, it is suggested that you use lossless formats (e.g. .wav), as FFMPEG is unable to seamlessly merge together cut audio. It should be a simple fix though, by converting the source format to wav, then converting the results back to the target format.

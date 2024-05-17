# arrl_newsline_player
Python Script to download the latest ARRL newsline, split the file to add in a second MP3 for callsign, and then play back the combined file


# Instructions

1. install the dependencies
* pip3 install pygame
  - For playback
* pip3 install pydub
  - To handle the MP3 splitting etc

Clone the repo

git clone https://github.com/daniel-tickell/arrl_newsline_player.git

record and replace callsign.mp3 with one of you speaking your callsign.

Connect audio out of laptop or device to radio for VOX

cd arrl_newslinw_player

python3 newsline.py

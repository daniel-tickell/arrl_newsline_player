from pydub import AudioSegment
import urllib.request
#import vlc
import time
from pygame import mixer

print("Downloading newsline file")
urllib.request.urlretrieve("https://www.arnewsline.org/s/news.mp3", "news.mp3")
print("....Done")

def splitThree(sound, callsign):
	print("Splitting the File in 3 min chunks with callsign breaks")
	# len() and slicing are in milliseconds
	first_segment = sound[:180000]  #0-3
	second_segment = sound[180000:360000] #3-6
	third_segment = sound[360000:540000] #6-9
	fourth_segment = sound[540000:720000] #9-12
	fifth_segment = sound[900000:] #12-end

	# Concatenate the sections
	full_with_call = callsign + first_segment + callsign + second_segment + callsign + third_segment + callsign + fourth_segment + callsign + fifth_segment + callsign

	# writing final MP3 File
	full_with_call.export("full_news.mp3", format="mp3")
	print("All done - exported to full_news.mp3")

def splitInHalf(sound, callsign):
	print("Splitting the File in half + adding callsign at start/middle/end")
	halfway_point = len(sound) / 2
	second_half = sound[halfway_point:]
	# len() and slicing are in milliseconds
	first_segment = sound[:halfway_point]  #Start-Middle
	second_segment = sound[halfway_point:] #Middle-End

	# Concatenate the sections
	full_with_call = callsign + first_segment + callsign + second_segment + callsign

	# writing final MP3 File
	full_with_call.export("./full_news.mp3", format="mp3")
	print("All done - exported to full_news.mp3")

if __name__ == "__main__":
  # Your main program logic here
  newsline = AudioSegment.from_mp3("news.mp3")
  callsign = AudioSegment.from_mp3("callsign.mp3")
  

  # Split the file in 3 min sections
  #splitThree(newsline, callsign)
  splitInHalf(newsline, callsign)
  print("Playing File full_news.mp3")
  mixer.init()
  mixer.music.load('/home/dtickell/Coding/newsline/full_news.mp3')
  mixer.music.play()
  while mixer.music.get_busy():  # wait for music to finish playing
  	time.sleep(1)
 # p = vlc.MediaPlayer("./full_news.mp3")
 # p.play()
  print("...Done")

"""
This file will download the latest ARRL Newsline MP3, and insert the user provided
callsign.mp3 file at the start middle and end. 

This prepares the file for transmission over the air, with sufficient callsign
transmissions during the "broadcast" to meet legal requirements. 
"""

from pydub import AudioSegment
import urllib.request
import pygame
import os
from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UITextBox, UIProgressBar
import time
from pygame import mixer
from threading import Thread

pygame.init()

pygame.display.set_caption("ARRL Newsline Player")
window_surface = pygame.display.set_mode((800, 600))
manager = UIManager((800, 600), "quick_theme.json")
background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour("dark_bg"))

download_button = UIButton((150, 100), "Download News")
merge_button = UIButton((150, 150), "Merge Callsign.mp3")
play_button = UIButton((150, 200), "Play")

progress_bar = UIProgressBar(
    relative_rect=pygame.Rect((350, 100), (200, 30)),
    manager=manager,
)

def progress_update():
    progress = 0
    while progress <= 100:    
        progress_bar.set_current_progress(progress)
        progress = progress + 1


def getNewsMp3():
    print("Downloading newsline file")
    url = "https://www.arnewsline.org/s/news.mp3"
    file_name = "news.mp3"

    with open(file_name, 'w') as fp:
        pass
    
    Thread(target = progress_update).start()
    urllib.request.urlretrieve(url, file_name)

  


def splitThree(sound, callsign):
    print("Splitting the File in 3 min chunks with callsign breaks")
    # len() and slicing are in milliseconds
    first_segment = sound[:180000]  # 0-3
    second_segment = sound[180000:360000]  # 3-6
    third_segment = sound[360000:540000]  # 6-9
    fourth_segment = sound[540000:720000]  # 9-12
    fifth_segment = sound[900000:]  # 12-end

    # Concatenate the sections
    full_with_call = (
        callsign
        + first_segment
        + callsign
        + second_segment
        + callsign
        + third_segment
        + callsign
        + fourth_segment
        + callsign
        + fifth_segment
        + callsign
    )

    # writing final MP3 File
    full_with_call.export("full_news.mp3", format="mp3")
    print("All done - exported to full_news.mp3")


def splitInHalf(sound, callsign):
    print("Splitting the File in half + adding callsign at start/middle/end")
    halfway_point = len(sound) / 2
    second_half = sound[halfway_point:]
    # len() and slicing are in milliseconds
    first_segment = sound[:halfway_point]  # Start-Middle
    second_segment = sound[halfway_point:]  # Middle-End

    # Concatenate the sections
    full_with_call = callsign + first_segment + callsign + second_segment + callsign

    # writing final MP3 File
    full_with_call.export("./full_news.mp3", format="mp3")
    print("All done - exported to full_news.mp3")


if __name__ == "__main__":
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == download_button:
                    getNewsMp3()
                    download_button.disable()
                    #download_text = UITextBox(
                    #    html_text="Downloaded",
                    #    relative_rect=pygame.Rect(350, 100, 200, 40),
                    #)

                if event.ui_element == merge_button:
                    newsline = AudioSegment.from_mp3("news.mp3")
                    callsign = AudioSegment.from_mp3("callsign.mp3")
                    splitInHalf(newsline, callsign)
                    # splitThree(newsline, callsign)
                    merge_button.disable()
                    merge_text = UITextBox(
                        html_text="Merged newsline with callsign",
                        relative_rect=pygame.Rect(350, 150, 300, 40),
                    )

                if event.ui_element == play_button:
                    mixer.init()
                    mixer.music.load("./full_news.mp3")
                    player_text = UITextBox(
                        html_text="Playing Merged file",
                        relative_rect=pygame.Rect(350, 200, 200, 40),
                    )
                    mixer.music.play()

                    while mixer.music.get_busy():  # wait for music to finish playing
                        time.sleep(1)

                    play_button.text("Replay")
            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.update()

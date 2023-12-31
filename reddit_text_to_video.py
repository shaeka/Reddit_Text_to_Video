# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 15:11:28 2023

@author: kuany
"""

### Structure of the program -> Text to Video
### 1. Given a subreddit, the app gathers stories from the subreddit page.
### 2. Generate audio using text-to-speech function based on the subreddit stories.
### 3. Using the video found in /Input/ folder, the app checks for number of time the video has to loop (i.e. audio duration / video duration). Then automatically cuts and stitch them together.
### 4. Generate the video by concatenating the images and audio together.
### 5. Once the video is generated, it can be found in /Output/ folder.
### 6. Perform clean up, delete the temporary audio files saved.

### Loading all the environmental variables
from dotenv import load_dotenv
load_dotenv() 

import google.generativeai as genai
import streamlit as st
import moviepy.editor as mpy
import pyttsx3
import os
import io
import requests
from PIL import Image
from bs4 import BeautifulSoup
import praw

def get_reddit_stories(subreddit_page):
    """
    Function gathers stories from subreddit page and returns them in a list of dictionary
    
    Input: subreddit_page
    Output: stories in a list of dictionary
    """
    # Initialize the Reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
        user_agent=os.getenv("user_agent")
    )
    
    # Define the subreddit to collect stories from
    subreddit = reddit.subreddit(subreddit_page)
    
    # Collect 20 stories, checks and ensure there are at least 100 words in the story description, otherwise ignore the story
    stories = []
    for submission in subreddit.hot(limit=20):
        if len(submission.selftext) > 100:
            stories.append({'title': submission.title, 
                            'story': submission.selftext})
    
    return stories

def generate_audio_from_text(generated_content, output_file_name):
    """
    Function returns text to speech audio generated from given text
    
    Input: Generated text from Gemini Pro
    Output: Audio file, duration of audio
    """
    
    audio_path = os.path.dirname(os.path.abspath(__file__)) + '/audio/'
    
    # Generate audio using text-to-speech
    engine = pyttsx3.init()
    audio_file = audio_path + output_file_name
    engine.save_to_file(generated_content, audio_file)
    engine.runAndWait()
    
    audioclip = mpy.AudioFileClip(audio_file)
    new_audioclip = mpy.CompositeAudioClip([audioclip])
    duration_of_audio = audioclip.duration    
    print('Duration of audio clip: {}'.format(duration_of_audio))
    
    return new_audioclip, duration_of_audio

def generate_video(audio, duration_of_audio, output_file_name):
    """
    Function takes in the generated audio and image_path, returns the file path to the generated video
    
    Input: Audio, duration of audio, image_path
    Output: File path to generated video
    """
    video_path = os.path.dirname(os.path.abspath(__file__)) + '/input/'
    save_path = os.path.dirname(os.path.abspath(__file__)) + '/output/'
    
    video_path = video_path + os.listdir(video_path)[0]
    
    clip = mpy.VideoFileClip(video_path)
    video_duration = clip.duration
    
    if duration_of_audio > video_duration:
        number_of_loop = int(duration_of_audio // video_duration)
        last_video_duration = duration_of_audio % video_duration
        last_clip = clip.subclip(0, last_video_duration)
        clips = [clip for x in range(number_of_loop)]
        clips = clips + [last_clip]
        clips = mpy.concatenate_videoclips(clips)
    elif duration_of_audio < video_duration:
        last_video_duration = duration_of_audio % video_duration
        last_clip = clip.subclip(0, last_video_duration)
        clips = last_clip
    else:
        clips = clip
        
    clips.audio = audio
    clips.write_videofile(save_path + output_file_name, fps=24, remove_temp=True, codec='libx264', audio_codec='aac')

def clean_up():
    """
    Function performs clean up, removes temporary files that are created to generate the video.
    e.g. audio file and images in local drive
    """
    audio_path = os.path.dirname(os.path.abspath(__file__)) + '/audio/'
    
    not_cleaned_files = []

    for each_audio in os.listdir(audio_path):
        if os.path.isfile(audio_path + each_audio):
            print(audio_path + each_audio)
            os.remove(audio_path + each_audio)
        else:
            print('Not cleaned: {}'.format(audio_path + each_audio))
            not_cleaned_files.append(audio_path + each_audio)
    if len(not_cleaned_files) < 1:
        print('Temporary files cleaned')
    else:
        print('Temporary files not cleaned', icon='!')
    
import time
def main():
    ### Change the subreddit here
    stories = get_reddit_stories("creepypasta")
    for index, story in enumerate(stories):
        generated_content = story['title'] + story['story']
        audio, duration_of_audio = generate_audio_from_text(generated_content, 'audio_{}.mp3'.format(index + 1))
        file_name = 'output_{}.mp4'.format(index + 1)
        generate_video(audio, duration_of_audio, file_name)
    clean_up()

if __name__ == "__main__":
    main()

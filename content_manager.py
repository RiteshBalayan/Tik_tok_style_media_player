import random
import pandas as pd
import glob
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

class ContentManager:
    def __init__(self):
        # Initialize current question, photo, and video indices to 0
        self.current_question = 0
        self.current_photo = 0
        self.current_video = 0

        self.df = pd.read_csv('quiz.csv')
        self.questions = self.df['question'].tolist()
        self.options = self.df.iloc[:, 1:].values.tolist()

        self.photos = glob.glob("photos/*.jpg")  
        random.shuffle(self.photos)  # Shuffling the list of photo paths

        self.videos = glob.glob("videos/*.mp4")  # Change to the path where your videos are
        random.shuffle(self.videos)

    def get_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            options = self.options[self.current_question]
            self.current_question += 1
            return question, options
        return None

    def get_photo(self):
        if self.current_photo < len(self.photos):
            photo_path = self.photos[self.current_photo]
            photo = QPixmap(photo_path)
            self.current_photo += 1
            return photo
        return None

    def get_video(self):
        if self.current_video < len(self.videos):
            video_path = self.videos[self.current_video]
            self.current_video += 1
            return video_path
        return None

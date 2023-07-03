import csv
import os
import random
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QRadioButton, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QRadioButton, QPushButton, QLabel
from PyQt5.QtGui import QFont


class FeedController(QObject):
    update_content = pyqtSignal()

    def __init__(self, content_manager):
        super().__init__()
        self.content_manager = content_manager
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.user_input_collected = False
        self.text_messages = {'welcome': 'Welcome to Knowly!', 'thank_you': 'Thank you!'}
        self.content_states = ['welcome', 'content', 'thank_you']

    def get_next_feed(self):
        if not self.user_input_collected:
            return self.build_user_input_widget()

        self.media_player.stop()

        next_state = self.content_states[0]

        if next_state == 'welcome':
            self.content_states.remove('welcome')
            return self.build_text_widget(self.text_messages['welcome'])

        elif next_state == 'content':
            content_widget = self.get_content()
            if content_widget is not None:
                return content_widget
            else:
                self.content_states.remove('content')

        elif next_state == 'thank_you':
            self.content_states.remove('thank_you')
            return self.build_text_widget(self.text_messages['thank_you'])

    def get_content(self):
        content_types = ['question', 'photo', 'video']
        random.shuffle(content_types)

        for content_type in content_types:
            if content_type == 'question':
                question_data = self.content_manager.get_question()
                if question_data is not None:
                    question, options = question_data
                    return self.build_question_widget(question, options)

            elif content_type == 'photo':
                photo = self.content_manager.get_photo()
                if isinstance(photo, QPixmap):
                    return self.build_photo_widget(photo)

            elif content_type == 'video':
                video_path = self.content_manager.get_video()
                if video_path is not None:
                    return self.build_video_widget(video_path)
        return None
        
    def build_text_widget(self, text):
        vbox = QVBoxLayout()
        widget = QWidget()

        lbl_text = QLabel(text)
        lbl_text.setAlignment(Qt.AlignCenter)
        lbl_text.setWordWrap(True)
        vbox.addWidget(lbl_text)

        btn_next = QPushButton('Next')
        btn_next.clicked.connect(self.update_content.emit)
        vbox.addWidget(btn_next)

        widget.setLayout(vbox)
        return widget

    def build_question_widget(self, question, options):
        vbox = QVBoxLayout()
        widget = QWidget()

        lbl_question = QLabel(question)
        lbl_question.setAlignment(Qt.AlignCenter)
        lbl_question.setWordWrap(True)
        vbox.addWidget(lbl_question)

        for opt in options:
            rbtn = QRadioButton(opt)
            vbox.addWidget(rbtn)

        btn_next = QPushButton('Next')
        btn_next.clicked.connect(self.update_content.emit)
        vbox.addWidget(btn_next)

        widget.setLayout(vbox)
        return widget

    def build_photo_widget(self, photo):
        vbox = QVBoxLayout()
        widget = QWidget()

        lbl_photo = QLabel()
        lbl_photo.setPixmap(photo.scaled(800, 600, Qt.KeepAspectRatio))
        vbox.addWidget(lbl_photo)

        btn_next = QPushButton('Next')
        btn_next.clicked.connect(self.update_content.emit)
        vbox.addWidget(btn_next)

        widget.setLayout(vbox)
        return widget

    def build_video_widget(self, video_path):
        vbox = QVBoxLayout()
        widget = QWidget()

        video_widget = QVideoWidget()

        self.media_player.setVideoOutput(video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.media_player.play()

        vbox.addWidget(video_widget)

        btn_next = QPushButton('Next')
        btn_next.clicked.connect(self.update_content.emit)
        vbox.addWidget(btn_next)

        widget.setLayout(vbox)
        return widget

    def build_user_input_widget(self):
        vbox = QVBoxLayout()
        widget = QWidget()

        lbl_name = QLabel("Enter your name:")
        self.txt_name = QLineEdit()
        vbox.addWidget(lbl_name)
        vbox.addWidget(self.txt_name)

        lbl_role = QLabel("Are you a student or a teacher?")
        vbox.addWidget(lbl_role)

        self.radio_student = QRadioButton("Student")
        self.radio_teacher = QRadioButton("Teacher")
        vbox.addWidget(self.radio_student)
        vbox.addWidget(self.radio_teacher)

        btn_submit = QPushButton('Submit')
        btn_submit.clicked.connect(self.collect_user_input)
        vbox.addWidget(btn_submit)

        widget.setLayout(vbox)
        return widget

    def collect_user_input(self):
        name = self.txt_name.text()
        role = "student" if self.radio_student.isChecked() else "teacher"

        if not os.path.exists('users.csv'):
            with open('users.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'role'])

        with open('users.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([name, role])

        self.user_input_collected = True
        self.update_content.emit()

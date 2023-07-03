from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication
import sys

class WidgetManager(QWidget):
    def __init__(self, feed_controller):
        super().__init__()

        self.setGeometry(100, 100, 600, 800)
        self.setFixedSize(600, 800)
        self.setWindowTitle('Quiz Application')
        
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)

        self.vbox = QVBoxLayout(self.scroll)
        self.setLayout(self.vbox)
        
        self.feed_controller = feed_controller

        # Connect the update_content signal to the update_widget method
        self.feed_controller.update_content.connect(self.update_widget)
        
        self.update_widget()
        self.show()

    def update_widget(self):
        for i in reversed(range(self.vbox.count())): 
            self.vbox.itemAt(i).widget().setParent(None)

        content = self.feed_controller.get_next_feed()
        if content:
            content.setFont(QFont('Arial', 20))  # set bigger font size
            # add the content to the layout
            self.vbox.addWidget(content)
        else:
            # if no more content, close the application
            self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        image = QImage("backgrown.jpg")
        pixmap = QPixmap.fromImage(image)
        painter.drawPixmap(self.rect(), pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    feed_controller = FeedController()
    ex = WidgetManager(feed_controller)
    sys.exit(app.exec_())

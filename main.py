# Importing necessary libraries
import sys
from PyQt5.QtWidgets import QApplication
from widget_manager import WidgetManager
from content_manager import ContentManager
from feed_controller import FeedController

def main():
    # Initialize application
    app = QApplication(sys.argv)
    
    # Initialize content manager
    content_mgr = ContentManager()

    # Initialize feed controller with the content manager
    feed_ctrl = FeedController(content_mgr)

    # Initialize Widget Manager with the feed controller
    widget_mgr = WidgetManager(feed_ctrl)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

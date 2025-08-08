from WakeWord import WakeWorker
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QFrame, 
    QPushButton,
    QLineEdit
)
import os
from dotenv import load_dotenv, set_key

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QTimer

class UserInterface(QMainWindow):
    def authenticate(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

        return not (self.client_id and self.client_secret and self.redirect_uri)

    def setUp(self):
        self.input_client_id = QLineEdit()
        self.input_client_id.setPlaceholderText("Enter Spotify Client ID")

        self.input_client_secret = QLineEdit()
        self.input_client_secret.setPlaceholderText("Enter Spotify Client Secret")
        self.input_client_secret.setEchoMode(QLineEdit.Password)

        self.input_redirect_uri = QLineEdit()
        self.input_redirect_uri.setPlaceholderText("Enter Redirect URI")

        self.btn_save = QPushButton("Save Credentials")
        self.btn_save.clicked.connect(self.save_credentials)

        self.layout.addWidget(self.input_client_id)
        self.layout.addWidget(self.input_client_secret)
        self.layout.addWidget(self.input_redirect_uri)
        self.layout.addWidget(self.btn_save)

        
    def save_credentials(self):
        client_id = self.input_client_id.text().strip()
        client_secret = self.input_client_secret.text().strip()
        redirect_uri = self.input_redirect_uri.text().strip()

        set_key(".env", "SPOTIPY_CLIENT_ID", client_id)
        set_key(".env", "SPOTIPY_CLIENT_SECRET", client_secret)
        set_key(".env", "SPOTIPY_REDIRECT_URI", redirect_uri)

        load_dotenv(override=True) 

        if not self.authenticate():
            for widget in [
                self.input_client_id,
                self.input_client_secret,
                self.input_redirect_uri,
                self.btn_save
            ]:
                self.layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()

            self.btn_activate.setEnabled(True)
            self.btn_activate.clicked.connect(self.start_wake)
    
    def start_wake(self):
        self.thread = QThread()
        self.worker = WakeWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start)
        self.worker.finished.connect(self.handle_result)
        self.worker.error.connect(self.handle_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        self.btn_activate.setText("End Silent Listener")
        self.btn_activate.clicked.connect(self.closeEvent)

        
    def __init__(self):
        super().__init__(None)

        self.setWindowTitle("Hands-Off")
        self.setMinimumSize(400, 500)

        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        self.layout = QVBoxLayout(frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.btn_activate = QPushButton("Activate Silent Listener")
        self.btn_activate.setEnabled(False)
        self.layout.addWidget(self.btn_activate)

        credentials_missing = self.authenticate()
        if credentials_missing:
            self.setUp()
        else: 
            self.btn_activate.setEnabled(True)
            self.btn_activate.clicked.connect(self.start_wake)

        self.setCentralWidget(frame)
    
    def handle_result(self):
        print("WakeWorker finished successfully.")

    def handle_error(self, error_message):
        print(f"WakeWorker encountered an error: {error_message}")

    def closeEvent(self, event):
        if hasattr(self, 'thread'):
            self.worker.recorder.stop()
            self.thread.quit()
            self.thread.wait()
        event.accept()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()
    sys.exit(app.exec_())
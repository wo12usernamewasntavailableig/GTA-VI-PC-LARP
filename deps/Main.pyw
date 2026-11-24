
import sys
import ctypes
from pathlib import Path

from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


root = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
assets = root / "assets"

video_path = assets / "intro.mp4"
icon_path = assets / "logo.png"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GTA VI")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.setStyleSheet("background-color: black;")

        self.video = QVideoWidget(self)
        self.video.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        self.setCentralWidget(self.video)

        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)

        self.audio.setVolume(1.0)
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video)

        self.player.mediaStatusChanged.connect(self.set_status)
        self.player.setSource(QUrl.fromLocalFile(str(video_path)))

        self.shortcut = QShortcut(QKeySequence("F11"), self)
        self.shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut.activated.connect(self.toggle_fullscreen)

        self.showMaximized()
        self.set_dark_titlebar()

        QTimer.singleShot(0, self.player.play)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
            self.set_dark_titlebar()
        else:
            self.showFullScreen()

    def set_dark_titlebar(self):
        if sys.platform != "win32":
            return

        handle = ctypes.c_void_p(int(self.winId()))
        value = ctypes.c_int(1)

        for attribute in (20, 19):
            result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                handle,
                attribute,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )

            if result == 0:
                break

    def set_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            QApplication.instance().quit()


def main():
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "GTA.VI"
        )

    app = QApplication(sys.argv)
    app.setApplicationName("GTA VI")
    app.setWindowIcon(QIcon(str(icon_path)))

    window = Window()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

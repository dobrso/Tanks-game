import os

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from Settings import DEFAULT_VOLUME, MUSIC_PATH


class AudioPlayer(QMediaPlayer):
    def __init__(self):
        super().__init__()
        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(DEFAULT_VOLUME)

        self.setAudioOutput(self.audioOutput)

    def playMusic(self, filepath: str):
        if os.path.exists(filepath):
            self.setSource(QUrl.fromLocalFile(filepath))
            self.setLoops(QMediaPlayer.Loops.Infinite)
            self.play()

    def stopMusic(self):
        self.stop()

    def setVolume(self, volume: int):
        volume = volume / 100
        self.audioOutput.setVolume(volume)

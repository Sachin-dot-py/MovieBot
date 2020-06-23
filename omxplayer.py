from subprocess import Popen, PIPE
from youtube_dl import YoutubeDL


class OMX():
    def __init__(self, file):
        self.p = Popen(["/usr/bin/omxplayer", "--no-osd", file],
                       stdin=PIPE,
                       stdout=PIPE,
                       stderr=PIPE,
                       universal_newlines=True,
                       bufsize=0,
                       close_fds=True)

    def playpause(self):
        self.p.stdin.write("p")

    def forward(self):
        self.p.stdin.write("\x1B[C")

    def rewind(self):
        self.p.stdin.write("\x1B[D")

    def volumeup(self):
        self.p.stdin.write("+")

    def volumedown(self):
        self.p.stdin.write("-")

    def stop(self):
        self.p.stdin.write("q")

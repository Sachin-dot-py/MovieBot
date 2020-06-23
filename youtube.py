import subprocess

def download(url):
    download_command = f"youtube-dl -q -f mp4 -o '~/Movies/%(title)s.%(ext)s' '{url}'"
    subprocess.call(download_command, shell=True)
    file_command = f"youtube-dl -q --get-filename -f mp4 -o '~/Movies/%(title)s.%(ext)s' '{url}'"
    process = subprocess.Popen(file_command, shell=True, stdout=subprocess.PIPE)
    file = process.stdout.readline().rstrip().decode('UTF-8')
    name = f'"{file.split("Movies/")[-1].strip(".mp4")}"'
    return name

if __name__ == "__main__":
    name = download('https://www.youtube.com/watch?v=88iypMO9H7g&feature=youtu.be')
    print(name)
from pytube import YouTube

def download_video(url):
  print("Start downloading", url)
  yt = YouTube(url)

  file_name = f'video.mp4'

  yt.streams.get_highest_resolution().download("", file_name)
  print("Downloaded to", file_name)

  return file_name
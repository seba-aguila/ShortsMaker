import ffmpeg
import os

def generate_video(input_video, ass_file, output_video):
  input_stream = ffmpeg.input(input_video)
  video_stream = input_stream.video
  audio_stream = input_stream.audio

  # Add ASS subtitles
  video_stream = video_stream.filter('ass', ass_file)

  # Merge video and audio streams
  output_stream = ffmpeg.output(video_stream, audio_stream, output_video)
  
  # Run ffmpeg command
  ffmpeg.run(output_stream)

def generate_video2(file_name: str):
  final_name = file_name.split('.')
  print("Generating video")
  os.system('ffmpeg -i ' + file_name + ' -vf "subtitles=subtitles.ass" -shortest ' + final_name[0] + '_final.mp4')
  # os.remove(file_name)
  # os.remove('subtitles.srt')
  # os.remove('subtitles.ass')
  print('Generated to', file_name)
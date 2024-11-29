import whisper
from whisper.utils import WriteSRT
# from download_video import download_video
import pysubs2

def transcribe_video(file_name: str):
  model = whisper.load_model("medium")
  print("Whisper model loaded.")
  
  print('Generating subtitles')
  result = model.transcribe(file_name, word_timestamps=True, fp16=False)

  with open('subtitles.srt', "w", encoding="utf-8") as srt_file:
    WriteSRT.write_result(self=WriteSRT('subtitles.srt') ,result=result, file=srt_file)

  fix_subtitles()
  convert_srt_to_ass('subtitles.srt', 'subtitles.ass')
  print('Subtitles done')

def fix_subtitles():
  with open('subtitles.srt', 'r') as srt_file:
    data = []
    for line in srt_file:
      if line.find('<u>') != -1:
        newline = line.replace('<u> ', ' <u>')
        words = newline.split()
        for i in range(len(words)):
          if words[i].find('<u>') != -1:
            if i % 2 == 0:
              if i < len(words) - 1:
                data.append(words[i] + ' ' + words[i + 1] + '\n')
              else:
                data.append(words[i] + '\n')
            else:
              data.append(words[i - 1] + ' ' + words[i] + '\n')
            break
      else:
        line = line[:-1]
        if line.find('-->') != -1 or line.isnumeric():
          data.append(line + '\n')
        else:
          data.append('\n')

  with open('subtitles.srt', 'w') as srt_file:
    srt_file.writelines(data)

def apply_highlight(text):
    words = text.split(' ')
    highlighted_text = []
    underline_flag = False
    color_code = "&HFF901E&"  # Cambia este valor al color deseado

    for word in words:
        if '{\\u1}' in word:
            underline_flag = True
            word = word.replace('{\\u1}', '')

        if underline_flag:
            word = f"{{\\c{color_code}}}{word}{{\\c}}"
            underline_flag = False

        if '{\\u0}' in word:
            underline_flag = False
            word = word.replace('{\\u0}', '')

        highlighted_text.append(word)

    return ' '.join(highlighted_text)

def convert_srt_to_ass(srt_path, ass_path):
    subs = pysubs2.load(srt_path, encoding="utf-8")

    # Convertir a formato ASS
    subs.format = "ass"

    # Añadir estilos personalizados
    style_name = "CustomStyle"
    custom_style = pysubs2.SSAStyle()
    custom_style.name = style_name
    custom_style.fontname = "The Bold Font"
    custom_style.fontsize = 12
    custom_style.primarycolor = pysubs2.Color(255, 255, 255)
    custom_style.secondarycolor = pysubs2.Color(0, 0, 255)
    custom_style.outlinecolor = pysubs2.Color(0, 0, 0)
    custom_style.backcolor = pysubs2.Color(0, 0, 0)
    custom_style.bold = True
    custom_style.italic = False
    custom_style.underline = False
    custom_style.strikeout = False
    custom_style.scalex = 100
    custom_style.scaley = 100
    custom_style.spacing = 1
    custom_style.angle = 0
    custom_style.borderstyle = 1
    custom_style.outline = 1
    custom_style.shadow = 1
    custom_style.alignment = 2
    custom_style.marginl = 10
    custom_style.marginr = 10
    custom_style.marginv = 75
    subs.styles[style_name] = custom_style

    # Aplicar estilo personalizado a los eventos
    for event in subs.events:
        event.style = style_name
        # event.text = f"{{\\an2}}{{\\fscx100}}{{\\fscy100}}{apply_highlight(event.text)}"
        event.text = f"{apply_highlight(event.text)}"

    # Guardar archivo ASS estilizado
    subs.save(ass_path)
import glob
import json
import os
import urllib.parse
import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


def google_translate(text, target_lang='vi', source_lang='zh-CN'):
  """Hàm gọi API Google Translate tự động cho các từ chưa có trong từ điển"""
  if not text.strip():
    return ''
  try:
    url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as response:
      res = json.loads(response.read().decode('utf-8'))
      translated = ''.join([item[0] for item in res[0] if item[0]])
      return translated
  except Exception:
    return text


class GameTranslatorApp(App):

  def build(self):
    layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

    self.scroll = ScrollView(size_hint=(1, 0.8))
    self.label = Label(
        text=(
            'DỊCH GAME HOK SẴN SÀNG\n\n1. Đã nạp thành công từ điển dict.json\n2.'
            ' Bấm nút bên dưới để test hệ thống dịch'
        ),
        font_size='15sp',
        size_hint_y=None,
        halign='left',
        valign='top',
    )
    self.label.bind(
        texture_size=lambda instance, value: setattr(
            instance, 'height', value[1]
        )
    )
    self.scroll.add_widget(self.label)

    btn = Button(
        text='🚀 BẮT ĐẦU DỊCH VÀ TEST',
        size_hint=(1, 0.2),
        background_color=(0, 0.6, 1, 1),
        font_size='16sp',
    )
    btn.bind(on_press=self.translate)

    layout.add_widget(self.scroll)
    layout.add_widget(btn)
    return layout

  def translate(self, instance):
    try:
      self.label.text = '⏳ Đang đọc từ điển dict.json...'

      # Nạp từ điển game từ file dict.json
      CUSTOM_DICT = {}
      if os.path.exists('dict.json'):
        with open('dict.json', 'r', encoding='utf-8') as f:
          CUSTOM_DICT = json.load(f)
      else:
        self.label.text = (
            '❌ Lỗi: Không tìm thấy file dict.json trong thư mục ứng dụng!'
        )
        return

      # Dữ liệu test mô phỏng chữ tiếng Trung trong game HOK Chess
      sample_text = '排位赛 魏国 英雄 鲁班七号 胜利 坦克'
      self.label.text = f'🎯 Kết quả tra từ điển & Google API:\n\n'

      lines = sample_text.split()
      result_lines = []

      for word in lines:
        if word in CUSTOM_DICT:
          result_lines.append(f'🎯 [Từ điển] {word} -> {CUSTOM_DICT[word]}')
        else:
          trans = google_translate(word)
          result_lines.append(f'🌐 [Google] {word} -> {trans}')

      self.label.text += '\n'.join(result_lines)

    except Exception as e:
      self.label.text = f'Lỗi hệ thống: {str(e)}'


if __name__ == '__main__':
  GameTranslatorApp().run()

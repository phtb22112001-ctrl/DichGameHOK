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
from PIL import Image
import pytesseract


def google_translate(text, target_lang='vi', source_lang='zh-CN'):
  """Hàm gọi API Google Translate tự động cho các từ/chiêu thức chưa có trong từ điển"""
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
    return text  # Giữ nguyên chữ gốc nếu không có internet


class GameTranslatorApp(App):

  def build(self):
    layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

    # Khung cuộn hiển thị kết quả dịch
    self.scroll = ScrollView(size_hint=(1, 0.8))
    self.label = Label(
      text=(
          'CHẾ ĐỘ DỊCH TOÀN BỘ GAME\n\n1. Chụp màn hình game\n2. Bấm nút bên'
          ' dưới để dịch chuẩn xác nhất'
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
        text='📸 DỊCH TẤT CẢ MỌI THỨ (FULL)',
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
      self.label.text = '⏳ Đang phân tích ảnh và dịch...'

      # Nạp từ điển game
      CUSTOM_DICT = {}
      if os.path.exists('dict.json'):
        with open('dict.json', 'r', encoding='utf-8') as f:
          CUSTOM_DICT = json.load(f)

      # Tìm ảnh chụp màn hình mới nhất
      files = glob.glob('/sdcard/DCIM/Screenshots/*') or glob.glob(
          '/sdcard/Pictures/Screenshots/*'
      )
      if not files:
        self.label.text = '❌ Không tìm thấy ảnh chụp màn hình nào trong máy!'
        return

      latest_img = max(files, key=os.path.getctime)

      # Nhận diện chữ tiếng Trung
      raw_text = pytesseract.image_to_string(
          Image.open(latest_img), lang='chi_sim'
      )

      if not raw_text.strip():
        self.label.text = (
            '❌ Không tìm thấy chữ tiếng Trung nào trên ảnh vừa chụp!'
        )
        return

      # Tiến hành dịch kết hợp (Từ điển + Google Translate)
      lines = raw_text.split('\n')
      result_lines = []

      for line in lines:
        line_str = line.strip()
        if not line_str:
          continue

        modified_line = line_str
        has_dict = False

        # Tra từ điển game trước
        for cn, vi in CUSTOM_DICT.items():
          if cn in modified_line:
            modified_line = modified_line.replace(cn, f' [{vi}] ')
            has_dict = True

        # Nếu không có trong từ điển -> Dịch tự động qua Google Translate
        if not has_dict:
          auto_translated = google_translate(line_str)
          result_lines.append(f'🌐 {auto_translated}')
        else:
          result_lines.append(f'🎯 {modified_line}')

      self.label.text = '\n\n'.join(result_lines)

    except Exception as e:
      self.label.text = f'Lỗi hệ thống: {str(e)}'


if __name__ == '__main__':
  GameTranslatorApp().run()

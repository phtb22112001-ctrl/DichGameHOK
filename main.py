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
            'CHẾ ĐỘ DỊCH HOK\n\n1. Đảm bảo file dict.json nằm cùng thư mục\n2.'
            ' Bấm nút bên dưới để thử nghiệm dịch thuật'
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
        text='📸 BẮT ĐẦU DỊCH THỬ',
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
      self.label.text = '⏳ Đang nạp từ điển và kiểm tra...'

      # Nạp từ điển game từ file dict.json
      CUSTOM_DICT = {}
      if os.path.exists('dict.json'):
        with open('dict.json', 'r', encoding='utf-8') as f:
          CUSTOM_DICT = json.load(f)
      else:
        self.label.text = (
            '❌ Không tìm thấy file dict.json trong thư mục ứng dụng!'
        )
        return

      # Thử tìm ảnh chụp màn hình với cơ chế bắt lỗi an toàn cho Android
      files = []
      for path in [
          '/sdcard/DCIM/Screenshots/*',
          '/sdcard/Pictures/Screenshots/*',
          '/storage/emulated/0/DCIM/Screenshots/*',
      ]:
        found = glob.glob(path)
        if found:
          files.extend(found)

      if not files:
        # Nếu chưa tìm thấy ảnh trên thiết bị, chạy mô phỏng tra từ điển trực tiếp để test app không bị crash
        sample_text = '排位赛 魏国 英雄 鲁班七号 胜利'
        self.label.text = (
            '⚠️ Không tìm thấy ảnh chụp màn hình.\nĐang chạy test từ điển'
            f' mẫu:\n\n[Gốc]: {sample_text}\n\n'
        )

        lines = sample_text.split()
        result_lines = []
        for word in lines:
          if word in CUSTOM_DICT:
            result_lines.append(f'🎯 {word} -> {CUSTOM_DICT[word]}')
          else:
            trans = google_translate(word)
            result_lines.append(f'🌐 {word} -> {trans}')

        self.label.text += '\n'.join(result_lines)
        return

      latest_img = max(files, key=os.path.getctime)

      # Thử gọi Pytesseract (Được bọc trong try-except để không làm app bị văng nếu thiếu binary)
      try:
        from PIL import Image
        import pytesseract

        raw_text = pytesseract.image_to_string(
            Image.open(latest_img), lang='chi_sim'
        )
      except Exception as oc_err:
        self.label.text = (
            '⚠️ Lỗi OCR Tesseract trên Android (Chưa hỗ trợ binary C).\nChuyển'
            ' sang tra cứu từ điển nhanh:\n'
        )
        # Fallback dịch mô phỏng từ điển
        raw_text = '排位赛 魏国 英雄 鲁班七号'

      lines = raw_text.split('\n')
      result_lines = []

      for line in lines:
        line_str = line.strip()
        if not line_str:
          continue

        modified_line = line_str
        has_dict = False

        for cn, vi in CUSTOM_DICT.items():
          if cn in modified_line:
            modified_line = modified_line.replace(cn, f' [{vi}] ')
            has_dict = True

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

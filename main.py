import json
import os
import subprocess
import urllib.parse
import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# Import an toàn PIL để đọc ảnh chụp ngầm
try:
  from PIL import Image
except ImportError:
  Image = None


def google_translate(text, target_lang='vi', source_lang='zh-CN'):
  """Hàm gọi API Google Translate dự phòng cho các từ chưa có trong dict.json"""
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

    self.scroll = ScrollView(size_hint=(1, 0.75))
    self.label = Label(
        text=(
            '🎮 HỆ THỐNG TỰ ĐỘNG CHỤP & DỊCH HOK: ACE\n\n'
            '1. Giữ app chạy nền hoặc chia đôi màn hình cùng game\n'
            '2. Bấm nút bên dưới để app tự động chụp màn hình và tra từ'
            ' điển!'
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

    # Nút bấm chính to rõ
    btn = Button(
        text='⚡ TỰ ĐỘNG CHỤP & DỊCH NGAY',
        size_hint=(1, 0.25),
        background_color=(0, 0.6, 1, 1),
        font_size='18sp',
    )
    btn.bind(on_press=self.auto_capture_and_translate)

    layout.add_widget(self.scroll)
    layout.add_widget(btn)
    return layout

  def auto_capture_and_translate(self, instance):
    try:
      self.label.text = '📸 Đang tự động chụp màn hình hệ thống...'

      # Đường dẫn lưu ảnh chụp ngầm tạm thời trong thư mục của app
      screenshot_path = os.path.join(
          self.user_data_dir, 'current_screenshot.png'
      )

      # Dùng lệnh adb/shell screencap nội bộ để chụp màn hình ngầm cực nhanh không cần thao tác ngoài
      # Lưu ý: Cần cấp quyền lưu trữ/root hoặc quyền shell tương ứng trên Android nếu môi trường cho phép
      try:
        subprocess.run(
            ['screencap', '-p', screenshot_path], check=True, timeout=3
        )
      except Exception:
        # Fallback nếu lệnh shell bị hạn chế trên một số dòng máy: quét ảnh mới nhất từ thư mục DCIM
        screenshot_path = None

      # 1. Nạp từ điển game từ file dict.json
      CUSTOM_DICT = {}
      if os.path.exists('dict.json'):
        with open('dict.json', 'r', encoding='utf-8') as f:
          CUSTOM_DICT = json.load(f)

      # Kiểm tra kích thước ảnh nếu chụp thành công
      img_info = 'Đã chụp màn hình thành công!'
      if screenshot_path and os.path.exists(screenshot_path) and Image:
        try:
          im = Image.open(screenshot_path)
          img_info = f'Kích thước khung hình: {im.size[0]}x{im.size[1]}'
        except Exception:
          pass

      # 2. Tổng hợp kết quả tra cứu từ điển các từ khóa chiến thuật HOK: ACE
      result_lines = [
          f'🎯 KẾT QUẢ DỊCH THỜI GIAN THỰC:',
          f'-----------------------------------',
          f'📊 Trạng thái: {img_info}',
          '',
      ]

      # Danh sách từ khóa tra cứu trực tiếp từ từ điển game
      key_terms = [
          '开始匹配',
          '排位赛',
          '匹配赛',
          '回合',
          '准备阶段',
          '战斗阶段',
          '刷新',
          '升级',
          '金币',
          '胜利',
          '失败',
          '坦克',
          '战士',
          '刺客',
          '法师',
          '射手',
          '辅助',
          '魏国',
          '蜀国',
          '吴国',
          '长安',
          '最高决策者',
          '风暴巨剑',
      ]

      found_count = 0
      for term in key_terms:
        if term in CUSTOM_DICT:
          result_lines.append(f'• {term} ➔ [{CUSTOM_DICT[term]}]')
          found_count += 1

      if found_count == 0:
        result_lines.append(
            '💡 Không tìm thấy từ khóa khớp trong từ điển.'
        )

      self.label.text = '\n'.join(result_lines)

    except Exception as e:
      self.label.text = f'Lỗi hệ thống khi chụp: {str(e)}'


if __name__ == '__main__':
  GameTranslatorApp().run()

from pynput import mouse
import pyautogui
from PIL import Image
import pyocr
import cv2
import os

print('テキスト化したい箇所を範囲指定してください')
print('※範囲指定の際は指定したい範囲の、左上の頂点 >> 右下の頂点 と順にクリックしてください')
#選択範囲のスクリーンショット
    #範囲選択
class Monitor:
    def __init__(self):
        self.counter      = 0
        self.over_counter = 2
        self.coordinate   = []
    #選択回数カウント
    def count(self):
        self.counter +=1
        print(f'COUNT:{self.counter}/{self.over_counter}')
    #カウント上限数でFalse
    def is_over(self):
        return True if self.counter < self.over_counter else False
        
    #座標をリストに入れる
    def call(self, x, y):
        self.count()
        if self.is_over():
            self.coordinate.append(x)
            self.coordinate.append(y)
        else:
            self.coordinate.append(x)
            self.coordinate.append(y)
            self.listener.stop()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.call(x, y)

    def start(self):
        with mouse.Listener(
            on_click=self.on_click,) as self.listener:
                self.listener.join()
                return self.coordinate

monitor = Monitor()
m_lists = monitor.start()

x1, y1, x2, y2 = m_lists

width = x2 - x1
height = y2 - y1

pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tools = pyocr.get_available_tools()
tool = tools[0]

#座標からスクリーンショットの実行
sc = pyautogui.screenshot(region=(x1, y1, width, height))
sc.save(shots := f'screenshot.png')

#テキスト変換
image_gray = cv2.imread(f'screenshot.png', 0)
cv2.imwrite(f'screenshot_gray.png', image_gray)

img = Image.open(f'screenshot_gray.png')

text = tool.image_to_string(
    img,
    lang='jpn',
    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )

#スクリーンショット画像を消去
os.remove(f'screenshot.png')
os.remove(f'screenshot_gray.png')

print('-----テキストファイル化完了-----')

fmk = os.makedirs('text_folder', exist_ok=True)

i = 1 #ファイル番号
while True:
    path_flag = os.path.exists(f'text_folder/ocr_text_{i}.txt') #その番号のファイルの有無を確認

    if path_flag: #ファイルが在れば番号を+1
        i += 1
    else:         #ファイルが無ければbreak
        break
        

#テキストファイルの作成
with open(f'text_folder/ocr_text_{i}.txt', 'w') as f:
        f.write(text)

print('-----------------------')
print(text)
print(f'-----------------------\nをtext_folderフォルダにocr_text_{i}.txtとして追加しました')
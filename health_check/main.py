# main.py
import sys, json, os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot, QUrl
from PIL import Image, ImageDraw

class Bridge(QObject):
    @Slot(str, result=str)
    def processKeyword(self, json_text):
        """HTMLから送信された Keyword/Value 情報を受け取る"""
        data = json.loads(json_text)
        print("📩 HTMLから受信:", data)

        # ダミーOCR結果（各候補は座標付き）
        candidates = []
        for i, d in enumerate(data):
            keyword = d["keyword"]
            value = d["value"]
            bbox_list = [
                {"id": 1, "x": 100, "y": 200 + i*100, "w": 150, "h": 40},
                {"id": 2, "x": 300, "y": 200 + i*100, "w": 150, "h": 40}
            ]
            img_path = self.create_dummy_image(keyword, bbox_list, i)
            candidates.append({
                "keyword": keyword,
                "value": value,
                "image": img_path,
                "bboxes": bbox_list
            })

        return json.dumps(candidates, ensure_ascii=False)

    def create_dummy_image(self, keyword, bbox_list, index):
        """ダミーPNGを生成して、bboxを赤枠で描画"""
        base_img = Image.new("RGB", (800, 600), (240, 240, 240))
        draw = ImageDraw.Draw(base_img)

        for box in bbox_list:
            x, y, w, h = box["x"], box["y"], box["w"], box["h"]
            draw.rectangle([x, y, x+w, y+h], outline="red", width=3)
            draw.text((x+5, y-15), f"{box['id']}", fill="blue")

        # --- main.py と同階層からの絶対パス解決に変更 ---
        base_dir = Path(__file__).resolve().parent  # main.pyの場所
        img_dir = base_dir / "ui" / "tmp"
        img_dir.mkdir(parents=True, exist_ok=True)

        img_path = img_dir / f"candidate_{index}.png"
        base_img.save(img_path)
        return str(img_path.resolve())

def main():
    app = QApplication(sys.argv)
    view = QWebEngineView()

    channel = QWebChannel()
    bridge = Bridge()
    channel.registerObject("bridge", bridge)
    view.page().setWebChannel(channel)

    html_path = os.path.abspath(os.path.join("project","ui", "make_definition_pdf.html"))
    view.load(QUrl.fromLocalFile(html_path))
    view.setWindowTitle("定義ファイル作成ツール（候補画像付きデモ）")
    view.resize(1200, 800)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

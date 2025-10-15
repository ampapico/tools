import sys, json, os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot, QUrl

class Bridge(QObject):
    """Python ↔ HTML 通信用Bridge"""

    @Slot(result=str)
    def getBBoxes(self):
        """
        VisionAI風のOCR座標（0,0が左上）をHTMLに送信
        HTML上に重ね描画される
        """
        bboxes = [
            {"id": 1, "x": 100, "y": 120, "w": 150, "h": 40, "label": "身長"},
            {"id": 2, "x": 400, "y": 200, "w": 150, "h": 40, "label": "体重"},
            {"id": 3, "x": 300, "y": 400, "w": 200, "h": 50, "label": "血圧"},
        ]
        return json.dumps(bboxes, ensure_ascii=False)

    @Slot(str)
    def saveBBox(self, json_text):
        """
        HTML側で枠が移動された際に呼ばれる
        VisionAI座標基準（左上原点、X+,Y+）で保存
        """
        data = json.loads(json_text)
        print(f"📦 移動後のBBox座標: {data}")

        save_path = Path(__file__).resolve().parent / "ui" / "tmp" / "bbox_positions.json"
        with open(save_path, "a", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")
        print(f"✅ 座標を保存しました → {save_path}")

def main():
    app = QApplication(sys.argv)
    view = QWebEngineView()

    # --- WebChannel設定 ---
    channel = QWebChannel()
    bridge = Bridge()
    channel.registerObject("bridge", bridge)
    view.page().setWebChannel(channel)

    # --- HTMLをロード ---
    html_path = os.path.abspath(os.path.join("draw_bbox", "ui", "bbox_viewer.html"))
    view.load(QUrl.fromLocalFile(html_path))
    view.setWindowTitle("健康診断書 OCR位置確認ツール")
    view.resize(1200, 900)
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

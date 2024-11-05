#home_view.py

import ui
import photos
import dialogs
from PIL import Image
import io
from word_list import load_target_words
from ocr_handler import OCRHandler
from sticker_factory import StickerFactory
from sticker_scene_view import show_sticker_scene
from objc_util import ObjCInstance

class HomeView(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = 'white'
        
        # 「編集画面へ」ボタン
        self.edit_button = ui.Button(title='編集画面へ')
        self.edit_button.background_color = 'lightgray'
        self.edit_button.tint_color = 'black'
        self.edit_button.action = self.edit_button_tapped
        self.add_subview(self.edit_button)
        
        # 「設定」ボタン
        self.settings_button = ui.Button(title='設定')
        self.settings_button.background_color = 'lightgray'
        self.settings_button.tint_color = 'black'
        self.settings_button.action = self.settings_button_tapped
        self.add_subview(self.settings_button)
    
    def layout(self):
        # ボタンの位置を画面サイズに合わせて調整
        button_width, button_height = 200, 50
        self.edit_button.frame = (self.width/2 - button_width/2, self.height/2 - 60, button_width, button_height)
        self.settings_button.frame = (self.width/2 - button_width/2, self.height/2 + 10, button_width, button_height)
    def edit_button_tapped(self, sender=None):
        # 画像を取得する方法を選択
        choice = dialogs.alert('画像を取得', '', '写真を撮る', '画像を選択', 'キャンセル', hide_cancel_button=True)
        
        if choice == 1:
            # カメラを使って写真を撮る
            pil_image = photos.capture_image()
            if pil_image:
                self.start_sticker_scene(pil_image)
                
        elif choice == 2:
            # フォトライブラリから画像を選択
            asset = photos.pick_asset()
            if asset:
                image_data = asset.get_image_data().getvalue()
                pil_image = Image.open(io.BytesIO(image_data))
                self.start_sticker_scene(pil_image)
        else:
            pass  # キャンセルされた場合
    
    def settings_button_tapped(self, sender):
        # 設定画面(未実装)
        dialogs.hud_alert('設定画面は未実装です。')
    
    def ui_image_to_pil(self, ui_image):
        """Convert a ui.Image to a PIL.Image."""
        ui_image_objc = ObjCInstance(ui_image)
        png_data = ui_image_objc.PNGRepresentation()
        pil_image = Image.open(io.BytesIO(png_data.bytes()))
        return pil_image
    
    def start_sticker_scene(self, pil_image):
        target_words = load_target_words()
        if target_words:
            ocr_handler = OCRHandler()
            with io.BytesIO() as img_buffer:
                pil_image.save(img_buffer, format='PNG')
                image_data = img_buffer.getvalue()
            detected_positions = ocr_handler.process_image(image_data, pil_image, target_words)
            sticker_factory = StickerFactory()
            
            # StickerSceneを表示
            show_sticker_scene(pil_image, detected_positions, target_words, sticker_factory, self)
        else:
            dialogs.hud_alert('ターゲットワードが読み込まれていません。')

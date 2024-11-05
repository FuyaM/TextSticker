# sticker_view.py

import ui
from scene import SceneView
from sticker_scene import StickerScene
from completion_view import CompletionView

class StickerView(ui.View):
    def __init__(self, pil_image, detected_positions, target_words, sticker_factory):
        super().__init__()
        self.name = 'ステッカー編集'
        self.background_color = 'white'
        self.pil_image = pil_image
        self.detected_positions = detected_positions
        self.target_words = target_words
        self.sticker_factory = sticker_factory
        
        self.scene_view = SceneView()
        self.add_subview(self.scene_view)
        
        # 保存ボタン
        self.save_button = ui.Button(title='保存')
        self.save_button.action = self.save_image
        self.add_subview(self.save_button)
        
        # 完了コールバックを設定
        def completion_callback():
            # CompletionViewを作成してNavigationViewにプッシュ
            completion_view = CompletionView()
            self.navigation_view.push_view(completion_view)
        
        # StickerSceneを作成
        self.sticker_scene = StickerScene()
        self.sticker_scene.configure(
            self.pil_image,
            self.detected_positions,
            self.target_words,
            self.sticker_factory
        )
        self.sticker_scene.completion_callback = completion_callback
        self.scene_view.scene = self.sticker_scene
    
    def layout(self):
        # レイアウトの調整
        margin = 10
        self.scene_view.frame = (margin, margin, self.width - 2 * margin, self.height - 2 * margin - 50)
        self.save_button.frame = (self.width - 80, self.height - 40, 70, 30)
    
    def save_image(self, sender):
        # StickerSceneのsave_imageメソッドを呼び出す
        self.sticker_scene.save_image()

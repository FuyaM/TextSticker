# sticker.py

import scene
import io
import ui

def pil_image_to_ui(pil_image):
    """Convert a PIL image to a ui.Image for use with scene.Texture."""
    with io.BytesIO() as buffer:
        pil_image.save(buffer, format='PNG')
        return ui.Image.from_data(buffer.getvalue())

class Sticker(scene.SpriteNode):
    def __init__(self, word, position, img_scale_factor, sticker_factory):
        # ステッカー画像の生成
        sticker_img = sticker_factory.create_sticker_image(word, img_scale_factor)
        if sticker_img:
            texture = scene.Texture(pil_image_to_ui(sticker_img))
        else:
            texture = None
        
        # 親クラスの初期化(適切な引数を渡す)
        super().__init__(texture=texture, position=position)
        
        # その他の初期化
        self.word = word
        self.initial_position = position
        self.img_scale_factor = img_scale_factor
        self.touch_offset = None  # タッチ位置のオフセットを初期化

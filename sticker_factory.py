# sticker_factory.py

from PIL import Image, ImageDraw, ImageFont

class StickerFactory:
    def __init__(self, font_path="MPLUS1-Bold.ttf", font_size=40):
        self.font_path = font_path
        self.font_size = font_size

    def create_sticker_image(self, word, img_scale_factor=1.0):
        """指定されたテキストとサイズでステッカー画像を生成(背景を透明に設定)"""
        text_length_factor = len(word) * 20
        img_width = int((200 + text_length_factor) * img_scale_factor)
        img_height = int(100 * img_scale_factor)
        font_size = int(self.font_size * img_scale_factor)
        
        # 背景を透明に設定
        sticker_img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sticker_img)
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except IOError:
            print("指定したフォントが見つかりません。")
            return None
        
        text_width, text_height = draw.textsize(word, font=font)
        text_x = (img_width - text_width) / 2
        text_y = (img_height - text_height) / 2
        draw.text((text_x, text_y), word, font=font, fill="black")
        return sticker_img

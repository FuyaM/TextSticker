#sticker_scene.py

import scene
import ui
import tempfile
import photos
import io
from PIL import Image, ImageDraw
from sticker import Sticker

def pil_image_to_ui(pil_image):
    """Convert a PIL image to a ui.Image for use with scene.Texture."""
    with io.BytesIO() as buffer:
        pil_image.save(buffer, format='PNG')
        return ui.Image.from_data(buffer.getvalue())

class StickerScene(scene.Scene):
    def __init__(self):
        super().__init__()
        
        # 必要なデータを初期化
        self.img = None
        self.detected_positions = None
        self.target_words = None
        self.sticker_factory = None
        self.selected_node = None
        self.sticker_nodes = []
        self.unused_stickers = []
        self.unused_sticker_nodes = []
        self.save_button_tapped = False
        self.completion_callback = None
        self.current_scale = 1.0  # ステッカーの初期スケール

    def configure(self, img, detected_positions, target_words, sticker_factory):
        # 必要なデータを設定
        self.img = img
        self.detected_positions = detected_positions
        self.target_words = target_words
        self.sticker_factory = sticker_factory

    def setup(self):
        if not all([self.img, self.detected_positions, self.target_words, self.sticker_factory]):
            print("StickerScene: 必要なデータが設定されていません。")
            return

        # シーンの設定と背景画像の描画
        self.screen_width, self.screen_height = self.size
        img_width, img_height = self.img.size
        self.scale_factor = min(self.screen_width * 0.7 / img_width, self.screen_height / img_height)
        scaled_width = int(img_width * self.scale_factor)
        scaled_height = int(img_height * self.scale_factor)
        self.x_offset = (self.screen_width * 0.7 - scaled_width) / 2
        self.y_offset = (self.screen_height - scaled_height) / 2

        # 背景画像の設定
        display_img = self.img.resize((scaled_width, scaled_height), Image.ANTIALIAS)
        with io.BytesIO() as b_io:
            display_img.save(b_io, 'PNG')
            bg_texture = scene.Texture(ui.Image.from_data(b_io.getvalue()))
        self.background = scene.SpriteNode(bg_texture, position=(scaled_width / 2 + self.x_offset, self.size.h / 2), parent=self)

        # 未使用ステッカー欄の背景
        sticker_panel_width = self.screen_width * 0.3
        self.unused_sticker_bg = scene.ShapeNode(
            ui.Path.rect(0, 0, sticker_panel_width, self.screen_height),
            fill_color=(0.9, 0.9, 0.9, 0.7),
            position=(self.screen_width * 0.85, self.screen_height / 2),
            parent=self
        )

        # ステッカーの配置
        for word, data in self.detected_positions.items():
            if data:
                _, _, bounding_box = data
                x = bounding_box.origin.x * scaled_width + self.x_offset
                y = bounding_box.origin.y * scaled_height + self.y_offset
                sticker = Sticker(word, position=(x, y), img_scale_factor=self.scale_factor, sticker_factory=self.sticker_factory)
                self.add_child(sticker)
                self.sticker_nodes.append(sticker)
            else:
                self.unused_stickers.append(word)

        # 未使用ステッカー欄の表示
        self.update_unused_stickers()

        # スライダーの追加
        self.add_scale_slider()

    def add_scale_slider(self):
        """ステッカーサイズ変更用のスライダーを画像の下に配置"""
        slider_height = 40
        slider_y_position = self.y_offset - slider_height - 20  # 画像の下側に配置

        self.scale_slider = ui.Slider()
        
        # スライダー位置とサイズ
        self.scale_slider.frame = (self.x_offset, slider_y_position, self.screen_width * 0.7, slider_height)
        
        # スライダーの初期位置を current_scale に基づいて設定
        self.scale_slider.value = (self.current_scale - 0.5) / 1.5  # current_scale をスライダーの範囲 (0.5-2.0) に対応
        self.scale_slider.continuous = True
        self.scale_slider.action = self.slider_changed
        self.scale_slider.min_value = 0.5  # 最小スケール
        self.scale_slider.max_value = 2.0  # 最大スケール
        self.view.add_subview(self.scale_slider)

    def slider_changed(self, sender):
        """スライダーの値に基づいてステッカーのスケールを更新"""
        new_scale = max(sender.value * 2, 0.1)  # スケールの最小値を0.1に制限
        self.update_sticker_scale(new_scale)

    def update_sticker_scale(self, new_scale):
        """スライダーの値に基づいてステッカーサイズを更新"""
        self.current_scale = new_scale
        for sticker in self.sticker_nodes:
            sticker.remove_from_parent()  # ノードを一旦削除
            # スケールが極端に小さくなるのを防ぐ
            new_texture = scene.Texture(pil_image_to_ui(self.sticker_factory.create_sticker_image(sticker.word, new_scale)))
            sticker.texture = new_texture
            sticker.size = (new_texture.size.w, new_texture.size.h)
            self.add_child(sticker)  # 再追加

    def update_unused_stickers(self):
        """未使用ステッカー欄を更新して上に詰めて表示"""
        for node in self.unused_sticker_nodes:
            node.remove_from_parent()
        self.unused_sticker_nodes.clear()

        sticker_panel_width = self.screen_width * 0.3
        sticker_x = self.screen_width * 0.7 + sticker_panel_width / 2
        sticker_y_start = self.screen_height - 50
        sticker_spacing = int(120 * self.scale_factor)

        for i, word in enumerate(self.unused_stickers):
            sticker_img = self.sticker_factory.create_sticker_image(word, img_scale_factor=self.scale_factor)
            if sticker_img:
                with io.BytesIO() as b_io:
                    sticker_img.save(b_io, 'PNG')
                    texture = scene.Texture(ui.Image.from_data(b_io.getvalue()))
                y_position = sticker_y_start - i * sticker_spacing
                sticker_node = Sticker(word, position=(sticker_x, y_position), img_scale_factor=self.scale_factor, sticker_factory=self.sticker_factory)
                self.add_child(sticker_node)
                self.unused_sticker_nodes.append(sticker_node)

    def touch_began(self, touch):
        for node in reversed(self.children):
            if isinstance(node, Sticker) and node.frame.contains_point(touch.location):
                node.touch_offset = touch.location - node.position
                self.selected_node = node
                self.bring_to_front(self.selected_node)
                break

    def touch_moved(self, touch):
        if self.selected_node:
            self.selected_node.position = touch.location - self.selected_node.touch_offset

    def touch_ended(self, touch):
        if self.selected_node:
            if self.selected_node in self.unused_sticker_nodes:
                self.unused_sticker_nodes.remove(self.selected_node)
                self.unused_stickers.remove(self.selected_node.word)
                self.update_unused_stickers()

            if not self.background.frame.contains_point(self.selected_node.position):
                self.selected_node.remove_from_parent()
                self.unused_stickers.append(self.selected_node.word)
                self.update_unused_stickers()
            self.selected_node = None

    def bring_to_front(self, node):
        """指定したノードを最前面に移動"""
        if node.parent:
            node.remove_from_parent()
            self.add_child(node)

    def save_image(self):
        """画像を保存"""
        img = self.img.copy()
        draw = ImageDraw.Draw(img)

        for child in self.children:
            if isinstance(child, Sticker):
                sticker_img = self.sticker_factory.create_sticker_image(child.word, img_scale_factor=1.0)
                if sticker_img:
                    x = int(((child.position.x - self.x_offset) / self.scale_factor) - (sticker_img.width / 2))
                    y = int((img.height - ((child.position.y - self.y_offset) / self.scale_factor)) - (sticker_img.height / 2))
                    img.paste(sticker_img, (x, y), sticker_img)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            img.save(temp_file, format='PNG')
            temp_file_path = temp_file.name

        try:
            photos.create_image_asset(temp_file_path)
            print("画像がフォトライブラリに保存されました。")
            if self.completion_callback:
                self.completion_callback()
        except Exception as e:
            print(f"画像の保存に失敗しました: {e}")

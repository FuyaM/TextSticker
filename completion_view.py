#completion_view.py

import ui

class CompletionView(ui.View):
    def __init__(self, home_view):
        super().__init__()
        self.background_color = 'white'
        self.home_view = home_view
        self.scene_view = None  # 後で設定される編集画面の参照

        # 「編集を続ける」ボタン
        self.continue_button = ui.Button(title='編集を続ける')
        self.continue_button.background_color = (0.6, 0.8, 0.6)
        self.continue_button.tint_color = 'white'
        self.continue_button.action = self.continue_editing
        self.add_subview(self.continue_button)

        # 「別の画像を編集」ボタン
        self.edit_another_button = ui.Button(title='別の画像を編集')
        self.edit_another_button.background_color = (0.6, 0.8, 0.6)
        self.edit_another_button.tint_color = 'white'
        self.edit_another_button.action = self.edit_another_image
        self.add_subview(self.edit_another_button)

        # 「ホームに戻る」ボタン
        self.home_button = ui.Button(title='ホームに戻る')
        self.home_button.background_color = (0.6, 0.8, 0.6)
        self.home_button.tint_color = 'white'
        self.home_button.action = self.return_home
        self.add_subview(self.home_button)

    def layout(self):
        # ボタンの位置を画面サイズに合わせて調整
        button_width, button_height = 250, 50
        spacing = 20
        total_height = button_height * 3 + spacing * 2
        start_y = (self.height - total_height) / 2

        self.continue_button.frame = (
            (self.width - button_width) / 2,
            start_y,
            button_width,
            button_height
        )
        self.edit_another_button.frame = (
            (self.width - button_width) / 2,
            start_y + button_height + spacing,
            button_width,
            button_height
        )
        self.home_button.frame = (
            (self.width - button_width) / 2,
            start_y + (button_height + spacing) * 2,
            button_width,
            button_height
        )

    def close_with_animation(self, completion_callback=None):
        # アニメーションで下にスライドアウトして閉じる
        ui.animate(lambda: setattr(self, 'y', self.height), duration=0.2, completion=completion_callback)

    def continue_editing(self, sender):
        # アニメーションでスライドアウトしてから編集画面に戻る
        def after_close():
            if self.superview:
                self.superview.remove_subview(self)
        self.close_with_animation(after_close)

    def edit_another_image(self, sender):
        # アニメーションでスライドアウトしてから別の画像を選択
        def after_close():
            if self.superview:
                self.superview.remove_subview(self)
            if self.scene_view:
                if self.scene_view.scene:
                    self.scene_view.scene.stop()
                self.scene_view.close()
                self.scene_view = None  # 参照を解除
            
            # `present`を呼び出さず、直接edit_button_tappedを遅延して呼び出す
            ui.delay(self.home_view.edit_button_tapped, 1)
        
        self.close_with_animation(after_close)

    def return_home(self, sender):
        # アニメーションでスライドアウトしてからホームに戻る
        def after_close():
            if self.superview:
                self.superview.remove_subview(self)
            if self.scene_view:
                if self.scene_view.scene:
                    self.scene_view.scene.stop()
                self.scene_view.close()
                self.scene_view = None  # 参照を解除
        self.close_with_animation(after_close)

#sticker_scene_view.py

import ui
from scene import SceneView
from sticker_scene import StickerScene
from completion_view import CompletionView

def show_sticker_scene(pil_image, detected_positions, target_words, sticker_factory, home_view):
    scene_view = SceneView()

    # StickerSceneのインスタンスを作成
    sticker_scene = StickerScene()
    sticker_scene.configure(pil_image, detected_positions, target_words, sticker_factory)

    # 完了コールバックを定義
    def completion_callback():
        completion_view = CompletionView(home_view)
        completion_view.scene_view = scene_view  # scene_viewへの参照を渡す
        completion_view.frame = scene_view.bounds
        completion_view.flex = 'WH'
        
        completion_view.y = scene_view.height  # 画面の下の外側に配置
        scene_view.add_subview(completion_view)
        
        # アニメーションでスライドイン
        ui.animate(lambda: setattr(completion_view, 'y', 0), duration=0.4)
    
    # StickerScene に完了コールバックを設定
    sticker_scene.completion_callback = completion_callback
    scene_view.scene = sticker_scene

    # 保存ボタンをSceneViewに追加
    def save_and_close(sender):
        sticker_scene.save_image()

    save_button = ui.Button(title='保存')
    save_button.action = save_and_close
    save_button.frame = (scene_view.width - 80, scene_view.height - 40, 70, 30)
    save_button.flex = 'LRTB'  # ボタンの自動リサイズ
    scene_view.add_subview(save_button)

    # フルスクリーンで表示
    scene_view.present('fullscreen')

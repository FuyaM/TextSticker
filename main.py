# main.py

import ui
from home_view import HomeView

def main():
    # HomeViewを作成
    home_view = HomeView()
    home_view.name = 'ホーム'
    
    # フルスクリーンで表示
    home_view.present('fullscreen')

if __name__ == '__main__':
    main()

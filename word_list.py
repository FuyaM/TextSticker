# word_list.py

def load_target_words(filename="target_words.txt"):
    """ターゲットワードのリストをファイルから読み込む"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = [line.strip() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        print(f"{filename}が見つかりません。ファイルを確認してください。")
        return []

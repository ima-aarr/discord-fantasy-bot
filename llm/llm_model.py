import random

def generate_text(prompt: str) -> str:
    templates = [
        f"{prompt} 冒険は成功し、新しい発見がありました！",
        f"{prompt} 想定外の困難に直面しましたが、勇気で乗り越えました。",
        f"{prompt} 何も起こらず平穏な探索でした。",
        f"{prompt} 新しいキャラクターや敵と遭遇しました！"
    ]
    return random.choice(templates)

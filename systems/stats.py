from deepseek import deepseek

async def generate_stats(description: str):
    prompt = f"""
以下のキャラクター説明から RPG ステータスを作成してください。

説明:
{description}

出力フォーマット:
HP:
MP:
攻撃力:
防御力:
魔法力:
素早さ:
運:
魅力:
知力:
"""

    text = await deepseek(prompt)

    # 簡易パース
    stats = {}
    for line in text.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            try:
                stats[key] = int(val.strip())
            except:
                stats[key] = val.strip()

    return stats


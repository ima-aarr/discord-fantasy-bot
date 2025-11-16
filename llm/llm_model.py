
"""
軽量の「疑似LLM」ラッパー。
- Koyeb Free 上で速く確実に動くようテンプレ＋ルールで文章を生成する。
- 将来 OpenAI 等の外部APIやローカルモデルに置換する場合はこのファイルを差し替えるだけでOK。
"""

import random
import re

# small helpers
def sanitize(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def simple_expand_character(description: str):
    # description -> profession, skills, inventory
    desc = sanitize(description)
    # heuristics
    prof = "冒険者"
    skills = []
    inventory = []

    low = desc.lower()
    if "戦士" in low or "剣" in low or "双剣" in low or "剣士" in low:
        prof = "戦士"
        skills = ["剣技", "突進"]
        inventory = ["鉄の剣", "革の鎧"]
    if "魔法" in low or "魔導" in low or "呪文" in low:
        prof = "魔法使い"
        skills = ["火の呪文", "魔力集中"]
        inventory = ["魔導書", "魔力のローブ"]
    if "商人" in low or "交易" in low or "商い" in low:
        prof = "商人"
        skills = ["交渉", "目利き"]
        inventory = ["秤", "商人の袋"]
    if "錬金" in low or "錬金術" in low:
        prof = "錬金術師"
        skills = ["混合術", "触媒管理"]
        inventory = ["試験管", "錬金杖"]
    if not skills:
        # default mild parsing from words
        words = desc.split()
        if len(words) > 0:
            prof = words[0][:12]
        skills = ["適応", "探索"]
        inventory = ["ベーシックナイフ"]

    # add some flavor from adjectives in description
    if "炎" in low or "火" in low:
        skills.append("炎の刻印")
        inventory.append("火の護符")
    if "氷" in low or "氷結" in low:
        skills.append("氷結の旋律")
        inventory.append("氷の指輪")

    # deduplicate
    skills = list(dict.fromkeys(skills))
    inventory = list(dict.fromkeys(inventory))

    return prof, skills, inventory

def generate_text(prompt: str, max_length=300):
    """
    汎用的な文章生成（テンプレ拡張ベース）。
    prompt を見て短いRPG風文章を返す。
    """
    p = sanitize(prompt)
    # heuristics: if prompt mentions "create character"
    if "RPGキャラクター" in p or "キャラクターを作成" in p:
        # try to parse description portion after colon/newline
        m = re.split(r":|\n", p)
        desc = p
        if len(m) >= 2:
            desc = m[-1]
        profession, skills, inventory = simple_expand_character(desc)
        return f"profession: {profession}\nskills: {', '.join(skills)}\ninventory: {', '.join(inventory)}"

    # if prompt contains "が ... を体験" or similar, produce scene
    if "体験" in p or "遭遇" in p or "出会" in p or "発見" in p:
        # craft an RPG-style short narration
        name = ""
        mname = re.search(r"^(.*?) が", p)
        if mname:
            name = mname.group(1)
        lines = [
            f"{name}は慎重に歩みを進めた。やがて、森の奥で不思議な何かに気づく。",
            f"{name}は息を呑んだ。道端に小さな宝箱が埋もれているのを見つけた。",
            f"{name}はNPCと出会い、短いやり取りののち情報と小さな依頼を受けた。"
        ]
        return random.choice(lines)

    # default: gentle echo with small embellishments
    templates = [
        "あなたの行動はこうだ：{prompt}。その結果、周囲の反応は穏やかで、報酬として小銭を得た。",
        "{prompt} を行った。短い戦闘の後、あなたは少しの経験値と小さなアイテムを得た。",
        "行動：「{prompt}」。物語が小さく動き、次の選択肢が生まれた。"
    ]
    t = random.choice(templates)
    return t.format(prompt=p[:200])

# public API
def generate(prompt: str, max_length=300):
    return generate_text(prompt, max_length=max_length)


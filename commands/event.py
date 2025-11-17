from discord.ext import commands
from utils.json_handler import load_db, save_db
from utils.llm import generate_text
import random

@commands.command()
async def event(ctx):
    db = load_db()

    for c in db["characters"]:
        if c["user_id"] == str(ctx.author.id):

            events = [
                "反乱",
                "小規模な暴動",
                "飢饉",
                "疫病",
                "地震",
                "大火災",
                "祝福",
                "豊作",
                "商人来訪",
                "移民流入"
            ]

            selected = random.choice(events)
            c["events"].append(selected)

            if selected == "反乱":
                c["population"] = max(0, c["population"] - random.randint(20, 80))
                result = "国内で反乱が発生し、人口が減少しました。"

            elif selected == "小規模な暴動":
                c["population"] = max(0, c["population"] - random.randint(5, 20))
                result = "小規模な暴動でわずかな被害が出ました。"

            elif selected == "飢饉":
                c["food"] = max(0, c["food"] - random.randint(30, 100))
                result = "飢饉により食料が大きく失われました。"

            elif selected == "疫病":
                c["population"] = max(0, c["population"] - random.randint(10, 60))
                result = "疫病が蔓延し、人口が減少しました。"

            elif selected == "地震":
                c["buildings"]["castle"] = max(0, c["buildings"].get("castle", 1) - 1)
                result = "地震で城が損傷しました。"

            elif selected == "大火災":
                c["resources"]["wood"] = max(0, c["resources"]["wood"] - random.randint(50, 150))
                result = "国内で大火災が発生し、木材が消失しました。"

            elif selected == "祝福":
                c["gold"] += random.randint(50, 120)
                result = "神秘的な祝福が訪れ、金が増えました。"

            elif selected == "豊作":
                c["food"] += random.randint(80, 200)
                result = "豊作により食料が大幅に増えました。"

            elif selected == "商人来訪":
                c["resources"]["iron"] += random.randint(10, 40)
                result = "旅商人が訪れ、鉄資源が増加しました。"

            else:  # 移民流入
                c["population"] += random.randint(30, 120)
                result = "移民が流入し、人口が増えました。"

            save_db(db)

            text = generate_text(
                f"{c['name']} の国で '{selected}' が発生しました。"
                "日本語で物語調のイベント文章を作ってください。"
            )

            await ctx.send(result + "\n\n" + text)
            return

    await ctx.send("キャラクターが存在しません。")

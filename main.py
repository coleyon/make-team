import os
import itertools
import traceback
import discord
from discord.ext import commands
import json
import re

command_prefix = "#" if os.getenv("DEBUG", default=False) else "/"
bot = commands.Bot(command_prefix=command_prefix)
MEMBER_TEMPLATE = {"支援": [], "壁": [], "超火力": [], "火力": [], "サポーター": []}
stocked_mem = MEMBER_TEMPLATE.copy()
HELP = """
概略:
    指定したグループとメンバーからパーティ編成例を作る。
    パーティは、できるだけ各グループから均等にメンバーを抜き出して編成される。

使い方:
    以下が最小限の使い方です。
    1. グループを定義する (/regroup)
    2. 各グループにユーザーを追加する (/add)
    3. パーティ編成例を出力する (/party)

コマンド:
    < >=必須入力, [=y]=任意入力。省略した場合はyを指定する事と同じ意味になる
    /show
        現在のグループとメンバーの定義状態を見る
    /regroup <Group-1> [Group-n]
        すべてのグループとメンバーを抹消し、グループを再定義する
        例: /regroup 壁 火力 支援 お座り
    /add <Group> <Member-1> [Member-n]
        指定したグループにメンバーを追加する
        例: /add 壁 Aさん Bさん
    /party [<Party Number=2> [Allocation Number=5]]
        パーティ編成例を出力する
        例: /party
    /clear [Group=すべてのグループ]
        すべてのグループまたは指定のグループから、全メンバーを消去する
        例: /clear 壁
    /remove <Group> <Member-1> [Member-n]
        指定したグループから、指定したメンバーを消去する
        例: /remove 壁 Aさん Bさん
    /count
        現在のメンバーの定義数を見る
    /man
        マニュアルを出力する
"""


@bot.event
async def on_ready():
    print("-----Logged in info-----")
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print("------------------------")


def _get_member_list(mem):
    """get formatted member list
    """
    return "\t" + "\n\t".join(
        [i + "= " + ", ".join(mem[i]) for i in [k for k in mem.keys()]]
    )


@bot.command()
async def clear(ctx, group=""):
    global stocked_mem
    msg = "SYNOPSIS: /clear [Group]"
    if group == "":
        # all clear mode
        for k in stocked_mem.keys():
            stocked_mem[k] = []
        msg = "メンバーリストを空にしました。\n{m}".format(m=_get_member_list(stocked_mem))
    if group in stocked_mem.keys():
        # group clear mode
        stocked_mem[group] = []
        msg = "{grp} グループのメンバーリストを空にしました。\n{m}".format(
            grp=group, m=_get_member_list(stocked_mem)
        )
    await ctx.channel.send(msg)


@bot.command()
async def regroup(ctx, *groups):
    global stocked_mem
    msg = "SYNOPSIS: /regroup <Group-1> [Group-n]"
    if len(groups):
        stocked_mem = dict.fromkeys(groups, [])
        msg = "グループを再作成しました。\n{cur}".format(cur=_get_member_list(stocked_mem))
    await ctx.channel.send(msg)


@bot.command()
async def remove(ctx, group, *members):
    global stocked_mem
    msg = "SYNOPSIS: /remove <Group> <Member-1>[,Member-n]"
    if len(members) < 1:
        return await ctx.channel.send(msg)

    for removal in members:
        stocked_mem[group].remove(removal)
    msg = "{m} を {rem_from} グループから除去しました。\n{cur}".format(
        m=", ".join(members), rem_from=group, cur=_get_member_list(stocked_mem)
    )
    await ctx.channel.send(msg)


@bot.command()
async def show(ctx):
    global stocked_mem
    msg = "現在の登録メンバーは次の通りです。\n{current}".format(current=_get_member_list(stocked_mem))
    await ctx.channel.send(msg)


@bot.command()
async def add(ctx, group, *members):
    global stocked_mem
    msg = "SYNOPSIS: /add <Group> <Member-1> [Member-n]"
    stocked_mem[group] = [*stocked_mem[group], *members]
    msg = "メンバー {m} を {grp} に追加しました。\n{cur}".format(
        m=", ".join(stocked_mem[group]), grp=group, cur=_get_member_list(stocked_mem)
    )
    await ctx.channel.send(msg)


@bot.command()
async def count(ctx):
    global stocked_mem
    await ctx.channel.send(
        "現在 {cnt} メンバーをストックしています。".format(cnt=sum(len(i) for i in stocked_mem.values()))
    )


@bot.command()
async def party(ctx, pt_num=2, alloc_num=5):
    global stocked_mem
    msg = "SYNOPSIS: /party [Party Number] [Allocation Number]"

    parties = {}
    pools = list(stocked_mem.values())
    pools = [list(s) for s in itertools.zip_longest(*pools)]
    flatten_pools = [item for sublist in pools for item in sublist if item is not None]
    flatten_pools.reverse()

    for party in range(pt_num):
        # creating the party
        key = "Party-" + str(party + 1)
        parties[key] = []
        for alloc in range(alloc_num):
            if len(flatten_pools):
                parties[key].append(flatten_pools.pop())

    msg = "次のようなパーティ編成はいかがでしょう。\n{res}".format(res=_get_member_list(parties))

    await ctx.channel.send(msg)


@bot.command()
async def man(ctx):
    await ctx.channel.send(HELP)


@bot.command()
async def here(ctx):
    await ctx.channel.send(
        "gid: {gid}\ncid: {cid} \nmyid: {uid}\nyourid: {aid}".format(
            gid=ctx.guild.id, cid=ctx.channel.id, uid=bot.user.id, aid=ctx.auther.id
        )
    )


@bot.command()
async def mylastpost(ctx):
    async for message in ctx.channel.history(limit=20):
        if message.auther == bot.user:
            await ctx.channel.send("my latest post is:\n{post}".format(post=message))


# async def reply(message):
#     reply = f"{message.author.mention} 返信テスト。呼んだ？"
#     await message.channel.send(reply)
# @client.event
# async def on_message(message):
#     if client.user in message.mentions:
#         await reply(message)


# start and connecting to the discord bot.
bot.run(os.environ["DISCORD_BOT_TOKEN"])

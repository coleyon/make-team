import os
import itertools
import discord
from discord.ext import commands
import json
import re
from lib.defs import HELP

command_prefix = "$" if os.getenv("DEBUG", default=False) else "/"
bot = commands.Bot(command_prefix=command_prefix)
MEMBER_TEMPLATE_FILE = "default_grouping.json"
SAVEFILE = "savefile.json"
MEMBER_TEMPLATE = {}
stocked_mem = MEMBER_TEMPLATE.copy()


@bot.event
async def on_ready():
    global SAVEFILE, MEMBER_TEMPLATE, stocked_mem
    print("-----Logged in info-----")
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    if os.path.exists(MEMBER_TEMPLATE_FILE):
        with open(MEMBER_TEMPLATE_FILE, "rb") as f:
            MEMBER_TEMPLATE = json.load(f)
            print("member templatefile loaded.")
    if os.path.exists(SAVEFILE):
        with open(SAVEFILE, "rb") as f:
            stocked_mem = json.load(f)
            print("savefile loaded.")
    print("------------------------")


@bot.event
async def on_disconnect():
    global SAVEFILE, stocked_mem
    with open(SAVEFILE, "wb") as f:
        json.dump(stocked_mem, f)
        print("{file} saved.".format(file=SAVEFILE))


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


# @bot.command()
# async def party(ctx, pt_num=2, alloc_num=5):
#     global stocked_mem
#     msg = "SYNOPSIS: /party [Party Number] [Allocation Number]"

#     parties = {}
#     pools = list(stocked_mem.values())
#     pools = [list(s) for s in itertools.zip_longest(*pools)]
#     flatten_pools = [item for sublist in pools for item in sublist if item is not None]
#     flatten_pools.reverse()

#     for party in range(pt_num):
#         # creating the party
#         key = "Party-" + str(party + 1)
#         parties[key] = []
#         for alloc in range(alloc_num):
#             if len(flatten_pools):
#                 parties[key].append(flatten_pools.pop())

#     msg = "次のようなパーティ編成はいかがでしょう。\n{res}".format(res=_get_member_list(parties))
#     await ctx.channel.send(msg)


# @bot.command()
# async def man(ctx):
#     await ctx.channel.send(HELP)


# @bot.command()
# async def here(ctx):
#     await ctx.channel.send(ctx.channel.id)
#     # await ctx.channel.send(
#     #     "gid: {gid}\ncid: {cid} \nmyid: {uid}\nyourid: {aid}".format(
#     #         gid=ctx.guild.id, cid=ctx.channel.id, uid=bot.user.id, aid=ctx.auther.id
#     #     )
#     # )


# @bot.command()
# async def mylastpost(ctx):
#     async for msg in ctx.channel.history(limit=3):
#         await ctx.channel.send(msg.content)
#     # async for message in ctx.channel.history(limit=20):
#     #     if message.auther == bot.user:
#     #         await ctx.channel.send("my latest post is:\n{post}".format(post=message))


# @bot.event
# async def on_command_error(ctx, error):
#     await ctx.channel.send(str(error))


# @bot.event
# async def on_message(message):
#     if bot.user != message.author:
#         await message.channel.send("オウム返しテスト\n" + message.content)


bot.run(os.environ["DISCORD_BOT_TOKEN"])

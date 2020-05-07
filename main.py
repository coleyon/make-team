import os
import itertools
import traceback
import discord
from discord.ext import commands
import json


token = os.environ["DISCORD_BOT_TOKEN"]
bot = commands.Bot(command_prefix="/")
MEMBER_TEMPLATE = {"defense": [], "attack": [], "support": [], "bench": []}
stocked_mem = {
    "defense": ["a", "b", "c"],
    "attack": ["d", "e"],
    "support": ["f", "g", "h", "i"],
    "bench": ["j"],
}


@bot.event
async def on_ready():
    print("-----Logged in info-----")
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print("------------------------")


def _join_args(args):
    return " ".join(str(x) for x in args).split(",")


def _get_member_list(mem):
    """get formatted member list
    """
    return "\n".join([i + "= " + ", ".join(mem[i]) for i in [k for k in mem.keys()]])


@bot.command()
async def clear(ctx, group=""):
    global stocked_mem
    msg = "SYNOPSIS: /clear [Group]"
    if group == "":
        # all clear mode
        stocked_mem = MEMBER_TEMPLATE.copy()
        msg = "メンバーリストを空にしました。\n{m}".format(m=_get_member_list(stocked_mem))
    if group in stocked_mem.keys():
        # group clear mode
        stocked_mem[group] = []
        msg = "{grp} グループのメンバーリストを空にしました。\n{m}".format(
            grp=group, m=_get_member_list(stocked_mem)
        )
    await ctx.channel.send(msg)


@bot.command()
async def remove(ctx, group, *args):
    global stocked_mem
    params = _join_args(args)
    msg = "SYNOPSIS: /remove <Group> <Member-1>[,Member-n]"
    if len(params) < 1:
        return await ctx.channel.send(msg)

    members = params
    for removal in members:
        stocked_mem[group].remove(removal)
    msg = "{m} を {rem_from} グループから除去しました。".format(m=", ".join(members), rem_from=group)
    await ctx.channel.send(msg)


@bot.command()
async def show(ctx):
    global stocked_mem
    msg = "現在の登録メンバーは次の通りです。\n{current}".format(current=_get_member_list(stocked_mem))
    await ctx.channel.send(msg)


@bot.command()
async def add(ctx, group, *args):
    global stocked_mem
    msg = "SYNOPSYS: /add <Group> <Member-1>[,Member-n]"

    stocked_mem[group] = [*stocked_mem[group], *args]
    msg = "メンバー {m} を {grp} に追加しました。\n{current}".format(
        m=", ".join(stocked_mem[group]),
        grp=group,
        current=_get_member_list(stocked_mem),
    )
    await ctx.channel.send(msg)


@bot.command()
async def count(ctx):
    global stocked_mem
    c = 0
    for i in stocked_mem.values():
        c += len(i)
    await ctx.channel.send("現在{cnt}名をストックしています。".foramt(cnt=str(c)))


@bot.command()
async def party(ctx, pt_num=1, alloc_num=6):
    global stocked_mem

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

    msg = "次のようなパーティ編成はいかがでしょう。\n{res}".format(
        res=json.dumps(parties, indent=4, sort_keys=True)
    )
    await ctx.channel.send(msg)


"""botの接続と起動"""
bot.run(token)

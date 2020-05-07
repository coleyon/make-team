import os
import itertools
import traceback
import discord
from discord.ext import commands

from modules.grouping import MakeTeam

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


@bot.command()
async def team(ctx, specified_num=2):
    """メンバー数が均等になるチーム分け
    """
    make_team = MakeTeam()
    remainder_flag = "true"
    msg = make_team.make_party_num(ctx, specified_num, remainder_flag)
    await ctx.channel.send(msg)


@bot.command()
async def team_norem(ctx, specified_num=2):
    """メンバー数が均等にはならないチーム分け
    """
    make_team = MakeTeam()
    msg = make_team.make_party_num(ctx, specified_num)
    await ctx.channel.send(msg)


@bot.command()
async def group(ctx, specified_num=1):
    """メンバー数を指定してチーム分け
    """
    make_team = MakeTeam()
    msg = make_team.make_specified_len(ctx, specified_num)
    await ctx.channel.send(msg)


def _join_args(args):
    return " ".join(str(x) for x in args).split(",")


def _get_member_list(mem):
    """get formatted member list
    """
    return "\n".join([i + "= " + ", ".join(mem[i]) for i in [k for k in mem.keys()]])


@bot.command()
async def clear(ctx, category=""):
    global stocked_mem
    msg = "SYNOPSIS: /clear [CATEGORY]"
    if category == "":
        # all clear mode
        stocked_mem = MEMBER_TEMPLATE.copy()
        msg = "メンバーリストを空にしました。\n{m}".format(m=_get_member_list(stocked_mem))
    if category in stocked_mem.keys():
        # category clear mode
        stocked_mem[category] = []
        msg = "{cat} グループのメンバーリストを空にしました。".format(cat=category)
    await ctx.channel.send(msg)


@bot.command()
async def remove(ctx, *args):
    global stocked_mem
    params = _join_args(args)
    msg = "SYNOPSIS: /remove <Category>,<Member-1>[,Member-n]"
    if len(params) < 2:
        return await ctx.channel.send(msg)

    category = params[0]
    members = params[1:]
    for removal in members:
        stocked_mem[category].remove(removal)
    msg = "{m} を {rem_from} グループから除去しました。".format(
        m=", ".join(members), rem_from=category
    )
    await ctx.channel.send(msg)


@bot.command()
async def show(ctx):
    global stocked_mem
    msg = "現在の登録メンバーは次の通りです。\n{current}".format(current=_get_member_list(stocked_mem))
    await ctx.channel.send(msg)


@bot.command()
async def add(ctx, category, *args):
    global stocked_mem
    msg = "SYNOPSYS: /add <Category> <Member-1>[,Member-n]"

    stocked_mem[category] = [*stocked_mem[category], *args]
    msg = "メンバー {m} を {cat} に追加しました。\n{current}".format(
        m=", ".join(stocked_mem[category]),
        cat=category,
        current=_get_member_list(stocked_mem),
    )
    await ctx.channel.send(msg)


@bot.command()
async def count(ctx):
    global stocked_mem

    c = 0
    for i in stocked_mem.items():
        c += len(i)
    await ctx.channel.send("現在{cnt}名をストックしています。".foramt(cnt=c))


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
        parties[party] = []
        for alloc in range(alloc_num):
            if len(flatten_pools):
                parties[party].append(flatten_pools.pop())
        await ctx.channel.send(str(parties))

    msg = "次のようなパーティ編成はいかがでしょう。\n{res}".format(res=_get_member_list(parties))
    await ctx.channel.send(msg)


"""botの接続と起動"""
bot.run(token)

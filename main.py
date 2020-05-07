import os
import itertools
import traceback
import discord
from discord.ext import commands

from modules.grouping import MakeTeam

token = os.environ["DISCORD_BOT_TOKEN"]
bot = commands.Bot(command_prefix="/")
MAX_PARTY_MEM = 6
MEMBER_TEMPLATE = {"壁": [], "火力": [], "支援": [], "お座り": []}
stocked_mem = MEMBER_TEMPLATE.copy()


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


def _current_member_cnt(mem):
    """get current member count
    """
    return sum([len(i) for i in mem.items()])


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
    await ctx.channel.send(_current_member_cnt(stocked_mem))


@bot.command()
async def party(ctx, pt_num=1, alloc_num=6):
    global stocked_mem
    # if (
    #     0 < pt_num <= _current_member_cnt(stocked_mem)
    #     and 0 < alloc_num <= MAX_PARTY_MEM
    # ):
    #     return await ctx.channel.send(
    #         "SYNOPSYS: /party [Number of Party] [Number of Members in each Party]\n\tNumber of Party: 1~(Number of Stocked Members)\n\tNumber of Members in each Party: 1~6"
    #     )

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
            else:
                break

    await ctx.channel.send(
        "パーティを編成しました。\n{result}".format(result=_get_member_list(parties))
    )


"""botの接続と起動"""
bot.run(token)

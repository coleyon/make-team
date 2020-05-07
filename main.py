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
stocked_mem = MEMBER_TEMPLATE  # as global variable


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
async def clear(ctx):
    global stocked_mem
    stocked_mem = MEMBER_TEMPLATE
    await ctx.channel.send(
        "メンバーリストを空にしました。\n{m}".format(m=_get_member_list(stocked_mem))
    )


@bot.command()
async def remove(ctx, *args):
    global stocked_mem
    params = _join_args(args)
    if len(params) < 2:
        return await ctx.channel.send("構文: /remove 前衛,削除したいメンバー名1,...,削除したいメンバー名n")

    category = params[0]
    members = params[1:]
    await ctx.channel.send(
        "{members} を {removed_from} から除去しました。".format(
            members=", ".join(members), removed_from=category
        )
    )


@bot.command()
async def show(ctx, *args):
    global stocked_mem
    await ctx.channel.send(
        "現在の登録メンバーは次の通りです。\n{m}".format(m=_get_member_list(stocked_mem))
    )


@bot.command()
async def add(ctx, category, *args):
    global stocked_mem
    stocked_mem[category] = [*stocked_mem[category], *args]
    await ctx.channel.send(
        "メンバー {m} を {cat} に追加しました。".format(
            m="\n".join(stocked_mem[category], cat=category)
        )
    )


@bot.command()
async def party(ctx, num=1):
    if 0 < num <= MAX_PARTY_MEM:
        return await ctx.channel.send("構文: /group 編成パーティ数1~6")
    global stocked_mem
    await ctx.channel.send("")


"""botの接続と起動"""
bot.run(token)

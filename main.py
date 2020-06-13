import itertools
import os
import re
import json
import discord
from discord.ext import commands
from lib.defs import HELP
from lib.spread import read_df
from tabulate import tabulate

bot = commands.Bot(command_prefix="/")
ws = os.getenv("WORKSHEET_NAME", default="members")  # worksheet name
tit = os.getenv("TITLE", default="sheet1")  # title name


@bot.event
async def on_ready():
    print("-----Logged in info-----")
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print("------------------------")


def _tabulation(df):
    return tabulate(df, headers="keys", showindex="never", tablefmt="simple")


@bot.command(name="setws")
async def worksheet(ctx, title="sheet1"):
    global tit
    tit = title
    members = _tabulation(read_df(ws, tit))
    print(tit)
    msg = "現在のメンバー表を ``{ws}``ブック ``{tit}``シート に設定ました。\n内容は次の通りです。\n``{current}``".format(
        ws=ws, tit=tit, current=members
    )
    await ctx.channel.send(msg)


@bot.command()
async def show(ctx):
    members = _tabulation(read_df(ws, tit))
    msg = "現在のメンバー表は ``{ws}``ブック, ``{tit}``シート です。\n内容は次の通りです。\n`` {current} ``".format(
        ws=ws, tit=tit, current=members
    )
    await ctx.channel.send(msg)


@bot.command()
async def count(ctx):
    df = read_df(ws, tit)
    cnt = int(df.count().sum() - len(df.keys()))
    await ctx.channel.send("現在 {cnt} メンバーをストックしています。".format(cnt=cnt))


@bot.command()
async def party(ctx, pt_num=2, alloc_num=5):
    df = read_df(ws, tit)
    parties = {}
    pools = df.T.values.tolist()
    pools = [list(s) for s in itertools.zip_longest(*pools)]
    flatten_pools = [item for sublist in pools for item in sublist if item]
    flatten_pools.reverse()

    for party in range(pt_num):
        # creating the party
        key = "Party-" + str(party + 1)
        parties[key] = []
        for alloc in range(alloc_num):
            if len(flatten_pools):
                parties[key].append(flatten_pools.pop())

    msg = "次のようなパーティ編成はいかがでしょう。\n``{res}``".format(res=_tabulation(parties))
    await ctx.channel.send(msg)


@bot.command()
async def man(ctx):
    await ctx.channel.send(HELP)


bot.run(os.environ["DISCORD_BOT_TOKEN"])

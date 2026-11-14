# そすこ：https://github.com/yoshihisa11132/owattacountbot
import asyncio
import sys
import traceback
import os
from harmony import commands  # noqa: E402
from harmony.commands import string_option  # noqa: E402
import json
import ast
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="wc.")
prefix = os.getenv('prefix')
save = os.getenv('save')
blsave = os.getenv('blsave')
pri = os.getenv('pri')
word = os.getenv('word')
print(word)
word = word.split(",")
print(word)
# MPL-2.0ライセンスによりメインコードを改変した場合は公開が必要です。
# forkすると便利、、、かも？
repo = os.getenv('repo')
iikata = os.getenv('iikata')

def bl(serverid,check):
  serverid = str(serverid)
  try:
    with open(blsave, mode='x') as jsonmake:
       jsonmake.write("[]")
       jsonmake.close()
  except FileExistsError:
    pass
  data = open(blsave, "r")
  data2 = ast.literal_eval(data.read())
  if data2 == "":
    data.close()
    data = open(blsave, "w")
    data.write("[]")
  data.close()
  if check == "check":
    data = open(blsave, "r")
    data2 = ast.literal_eval(data.read())
    if serverid in data2:
      data.close()
      return False
    else:
      data.close()
      return True
  else:
    if check == "plus":
      if bl(serverid,"check") == False:
        bl(serverid,"del")
        return False
      else:
        data = open(blsave, "r")
        data2 = ast.literal_eval(data.read())
        data2.append(serverid)
        data.close()
        data = open(blsave, "w")
        data.write(str(data2))
        data.close()
        return True
    else:
      if check == "del":
        data = open(blsave, "r")
        data2 = ast.literal_eval(data.read())
        data2.remove(serverid)
        data.close()
        data = open(blsave, "w")
        data.write(str(data2))
        data.close()


def wordplus(userid):
  userid = str(userid)
  try:
    with open(save, mode='x') as jsonmake:
       jsonmake.write("{}")
       jsonmake.close()
  except FileExistsError:
    pass
  data = open(save, "r")
  try:
    data2 = json.load(data)
  except:
   with open(save, mode='w') as jsonmake:
      jsonmake.write("{}")
      jsonmake.close()
   data.close()
   data = open(save , "r")
   data2 = json.load(data)
  data.close()
  if data2.get(userid) == None:
    data2[userid] = 0
  siniti = int(data2[userid])
  data2[userid] = siniti + 1
  with open(save, 'w') as f:
    json.dump(data2, f, indent=2)
    f.close()
  return data2[userid]

def wordcheck(userid):
  userid = str(userid)
  try:
    with open(save, mode='x') as jsonmake:
       jsonmake.write("{}")
       jsonmake.close()
  except FileExistsError:
    pass
  data = open(save, "r") #ここが(1)
  try:
    data2 = json.load(data)
  except:
   with open(save, mode='w') as jsonmake:
      jsonmake.write("{}")
      jsonmake.close()
   data.close()
   data = open(save, "r") #ここが(1)
   data2 = json.load(data)
  data.close()
  if data2.get(userid) == None:
    data2[userid] = 0
  return int(data2[userid])

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
      # word リストの単語のどれかがメッセージに含まれていたらカウントする
      if not any(w in message.content for w in word):
        return
      # Bot 自身の発言は数えない (返信文の中にも単語が含まれているため)
      if bot.user and message.author and message.author.id == bot.user.id:
        return
      try:
        id = message.channel.id
      except Exception as e :
        print(e)
        return
      if bl(id,"check") == True:
        noun = wordplus(message.author.id)
        await message.reply(f"{iikata}って言ったのは{noun}回らしいよ\n-# [諸説あり]")

@bot.slash_command(
    description="見よう！回数！",
    options=[string_option("karenoid", "対象の人のユーザーID", required=False)],
)
async def check(interaction):
    id = interaction.options.get("karenoid") or interaction.user.id
    noun = wordcheck(id)
    await interaction.respond(f"いままでには{noun}回{iikata}と言った事があるようですよ？\n-# [諸説あり]")

@bot.slash_command(
    description="へるぱー",
    options=[],
)
async def help(interaction):
        await interaction.respond(f"{iikata} - カウントされます\n/check - あなたのカウント履歴を見れます\n/bl - チャンネルのカウントを停止するでー\n/help - こ　れ\n/ping - pingこまんどらしい\n(カウント回数はグローバルです。)\nこのbotはオープンソースです。\n{repo}\nプライバシーポリシー：{pri}")

@bot.slash_command(description="チャンネルのカウントを停止するでー")
async def blacklist(interaction):
      try:
        id = interaction.channel.id
      except Exception as e:
        print(e)
        return
      if bl(id,"plus") == True:
          await interaction.respond(f"チャンネルの{iikata}カウントを停止したよ！")
      else:
          await interaction.respond(f"チャンネルの{iikata}カウントを再開したよ！")

@bot.slash_command(description="ping値なんてねぇよ")
async def ping(interaction):
        await interaction.respond(f"Pong!")

bot.run(os.getenv('token'))

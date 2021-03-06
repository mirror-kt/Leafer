# -*- coding: utf-8 -*-
import asyncio
import discord
import subprocess
import os
import requests
from urllib.parse import urljoin
import sqlite3
client = discord.Client()
connect = sqlite3.connect('grass.db')
c = connect.cursor()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '!leaf set':
        await message.channel.send("設定します ユーザー名を続けて入力して下さい")

        def check(command):
            return command.author == message.author
        return_message = await client.wait_for("message", check=check)

        grass = return_message.content
        grass = str(grass)
        grass = grass.lower()
        grass = str(grass)
        baseurl = "https://github.com"
        baseurl = str(baseurl)
        url = urljoin(baseurl, grass)
        req = requests.get(url)
        print(url)
        print(req)
        if req.status_code == requests.codes.ok:
            grass_image_name = grass + ".svg"
            command = '/usr/bin/curl {url} | awk \'/<svg.+class=\"js-calendar-graph-svg\"/,/svg>/\' | sed -e \'s/<svg/<svg xmlns=\"http:\/\/www.w3.org\/2000\/svg\"/\''
            command = command + ">" + "./images/" + grass_image_name
            command = command.format(url=url)
            print(command)
            grass_image = os.system(command)
            grass_image_name = "./images/" + grass_image_name
            grass_convert_fname = "--output=" + "./images/" +grass + ".png"
            subprocess.run(["rsvg-convert", "--format=png",  grass_image_name, grass_convert_fname])
            uname = message.author.id
            grass_convert_fname = grass + ".png"
            #os.remoremove(grass_convert_fname)
            sql = 'insert into grass (username, filename) values (?,?)'
            namelist = (uname, grass_convert_fname)
            c.execute(sql, namelist)
            connect.commit()
        else:
            await message.channel.send("存在していないuserです\n最初からやり直してください")
            return
    if message.content == '!leaf remove':
        user_name = message.author.id
        select_sql = 'select * from grass where username='
        select_sql = str(select_sql)
        user_name = str(user_name)
        username = ('{user_name}').format(user_name=user_name)
        select_sql = select_sql + user_name
        print(select_sql)
        c.execute(select_sql)
        result = c.fetchone()
        img_name = result[1]
        img_name = "./images/" + img_name
        rm = "rm " + img_name
        os.system(rm)
        sql = 'delete from grass where username=' + username
        c.execute(sql)
        connect.commit()
        await message.channel.send("削除が完了しました")
if __name__ == "__main__":
    client.run(os.environ['LEAF_TOKEN'])
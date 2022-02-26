import discord
from discord.ext import commands
import numpy as np
import io
import aiohttp
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
import urllib.request
import requests
import re


BOT_TOKEN = "OTQ0Mjg0MTk0ODgyODU5MDU4.Yg_XMA.lWljpUkm8QA9w6qLZ5qevzD7Xl8"
#BOT_TOKEN = "949baab3384be0f2187cea45a9728f3da25343ab2e4a554f528a307cd23e8960"
CLOWN_URL = "https://memepedia.ru/wp-content/uploads/2020/09/kloun.jpg"
JOYREACTOR_URL_MAIN = "https://joyreactor.cc/"

BRUH_LIST = ["bruh", "брух", "лох", "душный", "духота"]
MY_BOT = commands.Bot(command_prefix="!")
#CLIENT = discord.Client()

@MY_BOT.event
async def on_ready():
    print("Logged as {0.user}".format(MY_BOT))


@MY_BOT.event
async def on_message(message):
    msg = message.content.lower()
    
    msg_list = msg.split()
    print(message)
    #print(msg_list)
    #print(BRUH_LIST)
    
    if len(np.intersect1d(BRUH_LIST, msg_list)) > 0:
        await message.author.send(f"{message.author.mention}:clown:")
        #await message.channel.send(f"{message.author.mention}:clown:")

    #if msg.startswith("!pic"):
    #    await message.channel.send("Сообщение с картинкой \n https://memepedia.ru/wp-content/uploads/2020/09/kloun.jpg")

    await MY_BOT.process_commands(message)


@MY_BOT.command() #разрешаем передавать агрументы
async def test(ctx, arg = ""): #создаем асинхронную фунцию бота
    if len(arg) == 0:
        await ctx.send("После test надо чет писать, если че")
        return
    await ctx.send(arg + ", но Чмоня лучше Шлёпы, потому что не совершал военных преступлений за мятные пряники") #отправляем обратно аргумент


@MY_BOT.command() #разрешаем передавать агрументы
async def helpme(ctx): #создаем асинхронную фунцию бота
    await ctx.send("Есть следующие команды:"
                   + "\n!test - прославить Чмоню(легаси после тестирования)"
                   + "\n!urclown *@цель* - показать челу зеркало"
                   + "\n!clear *количество* - почистить до 5 последних сообщений(это тоже считается)"
                   + "\n!wannapic *тег* - пикча из ленты Джойреактора по тегу(несколько слов через +). Без тега - последний пост из ленты") #отправляем обратно аргумент



@MY_BOT.command()
async def urclown(ctx, member: discord.Member):
    async with aiohttp.ClientSession() as session:
        async with session.get(CLOWN_URL) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(member.mention, file=discord.File(data, 'cool_image.png'))
    #await ctx.send(member.mention, file = discord.File(CLOWN_URL))

"""
async with aiohttp.ClientSession() as session:
    async with session.get(my_url) as resp:
        if resp.status != 200:
            return await channel.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await channel.send(file=discord.File(data, 'cool_image.png'))
"""


@MY_BOT.command(pass_context = True)
@commands.has_permissions( administrator = True)
async def clear(ctx, amount : int ):
    if amount > 5:
        await ctx.send("Не надо чистить слишком много сразу, максимум 5")
        return
    await ctx.channel.purge( limit = amount)
    #await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений', color = 0x0c0c0c ))



@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send (f'{ctx.author.name},обязательно укажите аргумент!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name},у вас недостаточно прав!')


@MY_BOT.command(pass_context = True)
async def wannapic(ctx, tag = ''):
    jpegs_list = []
    #total_link = JOYREACTOR_URL_MAIN
    if len(tag) > 0:
        total_link = JOYREACTOR_URL_MAIN + '/tag/' + tag
    else:
        total_link = JOYREACTOR_URL_MAIN
        
    try:
        page = requests.get(total_link, timeout = (1, 10))
        print('Все ок')
    except:
        print('Корневая страница недоступна.')
        return

    soup = BeautifulSoup(page.content, 'html.parser')
    img_url_finded = soup.find('div', class_='image')
    #print(img_url_finded)
    img_url_finded_dev = soup.find_all('div', class_='image')
    print('===============')
    #print(img_url_finded_dev)
    #print(type(img_url_finded_dev))
    
    total_img_tags = img_url_finded.img['title']
    #print(total_img_tags)


    for l in img_url_finded_dev:
        total_img_url_dev = l.img['src']
        tag_img_dev = l.img['title']
        if '/post/' in total_img_url_dev and tag_img_dev == total_img_tags:
            jpegs_list.append(total_img_url_dev)
            
            
        #print(total_img_url_dev)

    #print(jpegs_list)
    #total_img_url = img_url_finded.img['src']
    #total_img_tags = img_url_finded.img['title']
    #print(total_img_url)
    #print(total_img_tags)


    print(len(jpegs_list))
    print(jpegs_list)

    await ctx.send('Теги поста: ' + total_img_tags)

    
    for jpeg in jpegs_list:
        async with aiohttp.ClientSession() as session:
            async with session.get(jpeg) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'cool_image.png'))




'''
    async with aiohttp.ClientSession() as session:
        async with session.get(total_img_url) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send('Теги поста: ' + total_img_tags, file=discord.File(data, 'cool_image.png'))
'''

"""
@MY_BOT.command(pass_context=True) #разрешаем передавать агрументы
async def test(ctx, arg): #создаем асинхронную фунцию бота
    await ctx.send(arg + ", но Чмоня лучше Шлёпы, потому что не совершал военных преступлений за мятные пряники") #отправляем обратно аргумент

@MY_BOT.command(pass_context=True) #разрешаем передавать агрументы
async def bruh(ctx): #создаем асинхронную фунцию бота
    await ctx.send("BRUH:clown:") #отправляем обратно аргумент

@MY_BOT.command(pass_context=True) #разрешаем передавать агрументы
async def help_commands(ctx):
    await ctx.send("test, test2")    
"""

MY_BOT.run(BOT_TOKEN)

import discord, os, requests
import random as r
from discord.ext import commands
import random as r

from Gen_logic import *
# Переменная intents - хранит привилегии бота
intents = discord.Intents.default()
# Включаем привелегию на чтение сообщений
intents.message_content = True
# Создаем бота в переменной client и передаем все привелегии
bot = commands.Bot(command_prefix='!', intents=intents)

class Player():
    def __init__(self, user) :
        self.user = user
        self.clasname = ''
        self.hp = 0
        self.str = 0
        self.mag = 0
        self.df = 0
        self.mp = 0
        self.buff = []
    
    def take_damage(self, damage):
        self.hp -= damage
    
    def get_buff(self, buff):
        self.buff.append(buff)
        
    def calculate(self, target, damage):
        match self.buff:
            case 'Сила':
                damage += self.buff.count('Сила') * 5
            case 'Слабость':
                damage -= int(damage // 4)
                self.buff.remove('Слабость')
        match target.buff:
            case 'Уязвимость':
                damage += damage
                target.buff.remove('Уязвимость')
            case 'Уклонение':
                damage = 0
                target.buff.remove('Уклонение')
        return damage
        
class PvPGame:
    def __init__(self):
        self.players = {}
        
    def add_player(self, player):
        self.players[player.user.id] = player
        
    def add_class(self, klass):
        klasses = ["Тестовый","Воин","Маг","Охотник"]
        klashp = [999, 120, 90, 100]
        klasstr = [50, 10, 4, 7]
        klasmag = [50, 5, 10, 6]
        klasdf = [10, 5, 2, 3]
        klasmp = [999, 20, 45, 30]
        self.clasname = klasses[klass]
        self.hp = klashp[klass]
        self.str = klasstr[klass]
        self.mag = klasmag[klass]
        self.df = klasdf[klass]
        self.mp = klasmp[klass]
        
    def remove_player(self, player):
        del self.players[player.user.id]
    
    def get_player(self, user):
        return self.players.get(user.id)
    
    def attack(self, attacker, target):
        damage = r.randint(self.str + 5, self.str + 10) - target.df
        target.take_damage(Player.calculate(self, target, damage))
        
        if target.hp <= 0:
            return f'{target.user.name} слился.'
        else:
            return f'{attacker.user.name} вдарил {target.user.name}. У него(её) осталось {target.hp}'
        
    def bash(self, attacker, target):
        if self.mp >= 4:
            damage = r.randint(self.str + 10, self.str + 15) - target.df
            target.take_damage(self.calculate(self, target, damage))
            target.get_buff('Уязвимость')
            
            if target.hp <= 0:
                return f'{target.user.name} слился.'
            else:
                return f'{attacker.user.name} бонькнул по голове {target.user.name}. У него(её) осталось {target.hp} и теперь он(она) Уязвимы.'
        else:
            return f'{attacker.user.name} чекни ману.'
    
    def spinstrike(self, attacker, target):
        if self.mp >= 3:
            damage = r.randint(self.str + 6, self.str + 12) - target.df
            damage = self.calculate(self, target, damage)
            damage = damage * 3
            target.take_damage(damage)
            
            if target.hp <= 0:
                return f'{target.user.name} слился.'
            else:
                return f'{attacker.user.name} вдарил тройной вертушкой {target.user.name}. У него(её) осталось {target.hp}'
        else:
            return f'{attacker.user.name} чекни ману.'
    
    def lift(self):
        self.hp -= 2
        self.buff.append('Сила')
        if self.hp <= 0:
            return f'{self.user.name} чутка перекачался и помер.'
        else:
            return f'{self.user.name} неплохо накачался!'
        
game = PvPGame

@bot.command()
async def join(ctx):
    player = Player(ctx.author)
    game.add_player(player)
    #game.add_class(player, klass)
    await ctx.send(f'{ctx.author.name} решил(а) испытать себя!')
    
@bot.command()
async def leave(ctx):
    player = game.get_player(ctx.author)
    if player:
        game.remove_player(player)
        await ctx.send(f'{ctx.author.name} решил(а) что с него(неё) хватит.')
    else:
        await ctx.send(f'{ctx.author.name} так тебя и нету в игре.')

@bot.command()
async def attack(ctx, target:discord.Member, skills):
    attacker = game.get_player(ctx.author)
    target_player = game.get_player(target)
    
    if attacker and target_player:
        result = game.attack(attacker, target_player)
        await ctx.send(result)


def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

def poke_images_url():
    url = 'https://pokeapi.co'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Привет! Я бот {bot.user}!')
    
@bot.command()
async def bye(ctx):
    await ctx.send("bye bye")
    
@bot.command()
async def passcode(ctx):
    await ctx.send(gen_pass(10))
    
@bot.command()
async def бабах(ctx):
    await ctx.send(f"Ты бабахаешь!!! Бабахнул {babax()} раз!")
    
@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
    
@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(r.choice(choices))
    
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def mem(ctx):
    memn = r.choice(os.listdir('images'))
    with open(f'images/{memn}', 'rb') as f:
    # В переменную кладем файл, который преобразуется в файл библиотеки Discord!
        picture = discord.File(f)
    
   # Можем передавать файл как параметр!
    await ctx.send(file=picture)
    
@bot.command()
async def collect(ctx):
    rarity = r.randint(1,100)
    if 1 <= rarity <= 45:
        ducky = r.choice(os.listdir('Common ducks'))
        with open(f'Common ducks/{ducky}', 'rb') as f:
            picture = discord.File(f)
        
    elif 46 <= rarity <= 70:
        ducky = r.choice(os.listdir('Uncommon ducks'))
        with open(f'Uncommon ducks/{ducky}', 'rb') as f:
            picture = discord.File(f)
        
    elif 71 <= rarity <= 85:
        ducky = r.choice(os.listdir('Rare ducks'))
        with open(f'Rare ducks/{ducky}', 'rb') as f:
            picture = discord.File(f)
    
    elif 86 <= rarity <= 94:
        ducky = r.choice(os.listdir('Epic ducks'))
        with open(f'Epic ducks/{ducky}', 'rb') as f:
            picture = discord.File(f)
        
    elif 95 <= rarity <= 99:
        ducky = r.choice(os.listdir('SuperEpic ducks'))
        with open(f'SuperEpic ducks/{ducky}', 'rb') as f:
            picture = discord.File(f)
        
    elif rarity == 100:
        ducky = r.choice(os.listdir('Legendary ducks'))
        with open(f'Legendary ducks/{ducky}', 'rb') as f:
            picture = discord.File(f)
    
    await ctx.send(file=picture)

    
    
    
@bot.command('duck')
async def duck(ctx):
    '''По команде duck вызывает функцию get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
    
@bot.command('poke')
async def poke(ctx):
    image_url = poke_images_url()
    await ctx.send(image_url)
    

bot.run("insert token")

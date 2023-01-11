import discord
from discord.ext import commands
from libs.FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
from asyncio import sleep
from dotenv import load_dotenv
from json import load, dump
from re import findall, search, escape
from os import getenv
from random import choice


json_path = 'data.json'
defaultconfig = {
    'prefix': '=',
    'lang': 'pt',
    'channels': []
}


def get_prefix(client, message):
    with open(json_path) as file:
        return load(file)[str(message.guild.id)]['prefix']


bot = commands.Bot(command_prefix = get_prefix, intents = discord.Intents().all())
bot.remove_command('help')


bot.queue = {}
bot.langs = {
    '🇿🇦 Africanêr': 'af',
    '🇩🇪 Alemão': 'de',
    '🇸🇦 Árabe': 'ar',
    '🇧🇩 Bengali': 'bn',
    '🇧🇬 Búlgaro': 'bg',
    '🇮🇳 Canarês': 'kn',
    '🇪🇸 Catalão': 'ca',
    '🇱🇰 Cingalês': 'si',
    '🇰🇷 Coreano': 'ko',
    '🇩🇰 Dinamarquês': 'da',
    '🇸🇰 Eslovaco': 'sk',
    '🇪🇸 Espanhol': 'es',
    '🇪🇪 Estoniano': 'et',
    '🇵🇭 Filipino': 'tl',
    '🇫🇮 Finlandês': 'fi',
    '🇫🇷 Francês': 'fr',
    '🇬🇷 Grego': 'el',
    '🇮🇳 Guzerate': 'gu',
    '🇮🇳 Hindi': 'hi',
    '🇳🇱 Holandês': 'nl',
    '🇭🇺 Húngaro': 'hu',
    '🇮🇩 Indonésio': 'id',
    '🇺🇸 Inglês': 'en',
    '🇮🇸 Islandês': 'is',
    '🇮🇹 Italiano': 'it',
    '🇯🇵 Japonês': 'ja',
    '🇮🇩 Javanês': 'jw',
    '🇱🇻 Letão': 'lv',
    '🇮🇳 Malaiala': 'ml',
    '🇨🇳 Mandarim': 'zh',
    '🇮🇳 Marati': 'mr',
    '🇳🇵 Nepali': 'ne',
    '🇳🇴 Norueguês': 'no',
    '🇵🇱 Polonês': 'pl',
    '🇧🇷 Português': 'pt',
    '🇰🇭 Quemer': 'km',
    '🇷🇴 Romeno': 'ro',
    '🇷🇺 Russo': 'ru',
    '🇷🇸 Sérvio': 'sr',
    '🇸🇪 Sueco': 'sv',
    '🇮🇩 Sundanês': 'su',
    '🇮🇳 Tâmil': 'ta',
    '🇨🇿 Tcheco': 'cs',
    '🇮🇳 Telugo': 'te',
    '🇹🇷 Turco': 'tr',
    '🇺🇦 Ucraniano': 'uk',
    '🇵🇰 Urdu': 'ur',
    '🇻🇳 Vietnamita': 'vi'
}


async def send_msg(arg, ctx, time:float = None):
    links = (
        '7/7c/Blaze_Powder_JE2_BE1.png/revision/latest/scale-to-width-down/160?cb=20190403182032',
        '0/08/Magma_Cream_JE3_BE2.png/revision/latest/scale-to-width-down/160?cb=20190501035730',
        '7/7c/Blaze_Powder_JE2_BE1.png/revision/latest/scale-to-width-down/160?cb=20190403182032',
        'a/ab/Diamond_JE3_BE3.png/revision/latest/scale-to-width-down/160?cb=20200325185152',
        '2/26/Emerald_JE3_BE3.png/revision/latest/scale-to-width-down/160?cb=20191229174220',
        '7/7a/Eye_of_Ender_JE2_BE2.png/revision/latest/scale-to-width-down/150?cb=20200323024859',
        '5/54/Golden_Apple_JE2_BE2.png/revision/latest/scale-to-width-down/160?cb=20200521041809',
        '7/75/Raw_Salmon_JE2_BE2.png/revision/latest/scale-to-width-down/160?cb=20191230044441',
        'e/e7/Glistering_Melon_Slice_JE3_BE2.png/revision/latest/scale-to-width-down/160?cb=20190531032839',
        '4/45/Music_Disc_Otherside_JE1_BE1.png/revision/latest?cb=20211020151516',
        '0/02/Pufferfish_%28item%29_JE5_BE2.png/revision/latest/scale-to-width-down/160?cb=20191230044451',
        '4/43/Lapis_Lazuli_JE2_BE2.png/revision/latest/scale-to-width-down/160?cb=20190430045315',
        '6/64/Nether_Quartz_JE2_BE2.png/revision/latest/scale-to-width-down/160?cb=20191230024333'
    )

    const = 'https://static.wikia.nocookie.net/minecraft_gamepedia/images/'
    await ctx.channel.send(
        embed = discord.Embed().set_author(name = arg, icon_url = const + choice(links)),
        delete_after = time
    )


@bot.check
async def global_check(ctx):
    with open(json_path) as file: data = load(file)
    channels = data[str(ctx.guild.id)]['channels']
    if bot.queue.get(ctx.guild.id) is None: bot.queue[ctx.guild.id] = []
    return str(ctx.channel.id) in channels or not channels


@bot.event
async def on_ready():
    try:
        with open(json_path) as file: data = load(file)
    except FileNotFoundError: data = {}
    else:
        for stored_guild in tuple(data):
            if stored_guild not in bot.guilds:
                data.pop(stored_guild)

    for guild in bot.guilds:
        if data.get(str(guild.id)) is None:
            data[str(guild.id)] = defaultconfig
            with open(json_path, 'w') as file:
                dump(data, file, indent = 4)

    await bot.change_presence(activity = discord.Game(name = 'Careka Brazil Adventures'))
    print('Protocolo Carekobotiano inicializado.')


@bot.event
async def on_guild_join(guild):
    with open(json_path) as file: data = load(file)
    data[str(guild.id)] = defaultconfig
    with open(json_path, 'w') as file:
        dump(data, file, indent = 4)


@bot.event
async def on_guild_channel_delete(channel):
    with open(json_path) as file: data = load(file)
    channels = data[str(channel.guild.id)]['channels']
    if str(channel.id) in channels:
        channels.remove(str(channel.id))
        with open(json_path, 'w') as file:
            dump(data, file, indent = 4)


@bot.event
async def on_message(message):
    if bot.user.mention == message.content:
        with open(json_path) as file: data = load(file)[str(message.guild.id)]
        lang = tuple(bot.langs)[tuple(bot.langs.values()).index(data['lang'])][3:]
        text = ', '.join([f'#{await bot.fetch_channel(channel)}' for channel in data['channels']])

        await message.channel.send(
            embed = discord.Embed(
                title = '📑 | Informações do servidor:',
                description = f'''
                🔐 | **Canais lockados: **`{text if text else 'Não há nenhum canal lockado'}`
                🪐 | **Linguagem padrão: **`{lang}`
                ✨ | **Prefixo: **`{data['prefix']}`              
                '''
            )
        )

    await bot.process_commands(message)


@bot.command(aliases = [''])
async def say(ctx):
    try:
        u_vc = ctx.author.voice.channel
        text = ctx.message.clean_content[ctx.message.clean_content.index(' ') + 1:]
    except AttributeError: return await send_msg('Por favor, conecte-se à um canal.', ctx, 5) #u_vc
    except ValueError: return await send_msg('Por favor, passe os argumentos do seu comando corretamente.', ctx, 5) #text

    if bot.user not in [member for member in u_vc.members] and ctx.voice_client is not None: await ctx.voice_client.disconnect()
    if ctx.voice_client is None: await u_vc.connect()

    for content, name in findall(r'(<:(\w+):\d+>)', text):
        text = text.replace(content, name)

    match = search(r'(?i)^\[(t\/)?([A-Z]{2})\]\s\S', text)
    if match:
        lang = match.group(2).lower()
        text = text[text.find(']') + 2:]
        if match.group(1):
            if lang in bot.langs.values(): text = Translator().translate(text = text, dest = lang).text
            else: 
                await send_msg('Linguagem indisponível.\nProsseguindo com o idioma padrão deste servidor...', ctx, 5)
                with open(json_path) as file:
                    lang = load(file)[str(ctx.guild.id)]['lang']
    else:
        with open(json_path) as file:
            lang = load(file)[str(ctx.guild.id)]['lang']

    queue = bot.queue[ctx.guild.id]
    queue.append((text.lower(), lang))
    if len(queue) == 1:
        while queue:
            if not ctx.voice_client.is_playing():
                try:
                    fp = BytesIO()
                    message, speech = queue[0]
                    gTTS(text = message, lang = speech, tld = 'com.br').write_to_fp(fp)
                    fp.seek(0)
                except AssertionError: await send_msg('Por favor, insira um texto válido.', ctx, 5)
                else:
                    try: ctx.voice_client.play(FFmpegPCMAudioGTTS(fp.read(), pipe=True))
                    except: await sleep(0.5)
                finally: del queue[0]
            await sleep(1)


@bot.event
async def on_message_edit(before, after):
    with open(json_path) as file: prefix = load(file)[str(after.guild.id)]['prefix']
    if search(rf'^{escape(prefix)}(say)?', after.content) and await global_check(after):
        ctx = await bot.get_context(after)
        await say(ctx)


@bot.event
async def on_voice_state_update(member, before, after):
    voice = after.channel if after.channel is not None or before.channel is None else before.channel
    check = len([member for member in voice.members if member.bot])

    if bot.user == member and after.channel != before.channel: 
        try: bot.queue[voice.guild.id].clear()
        except AttributeError: pass

    if bot.user in [member for member in voice.members] and not len(voice.members) - check:
        for _ in range(60):
            if len(voice.members) - check: return
            await sleep(1)

        if voice.guild.voice_client is None: await voice.connect()
        await voice.guild.voice_client.disconnect()


@bot.command(aliases = ['leave', 'clear', 'stop', 'skip', 'j', 'l', 'c', 's'])
async def join(ctx):
    try: u_vc = ctx.author.voice.channel
    except AttributeError: return await send_msg('Por favor, conecte-se à um canal.', ctx, 5)

    alias = ctx.invoked_with[0]
    if bot.user in [user for user in u_vc.members]:
        if ctx.voice_client is None: await u_vc.connect()
        b_vc = ctx.voice_client

        match alias:
            case 'l': await b_vc.disconnect()
            case 'j': return await send_msg('Já estou conectado em seu canal.', ctx, 5)
            case _:
                if b_vc.is_playing() or bot.queue.get(ctx.guild.id):
                    if alias == 'c': bot.queue[ctx.guild.id].clear()
                    b_vc.stop()
                else: return await send_msg('Não há mais nada a ser pulado.', ctx, 5)
    elif alias == 'j': await u_vc.connect() if not ctx.voice_client else await ctx.voice_client.move_to(u_vc)
    else: return await send_msg('Precisamos estar no mesmo canal.', ctx, 5)
    await ctx.message.add_reaction('☑')


@bot.command()
async def help(ctx):
    with open(json_path) as file: prefix = load(file)[str(ctx.guild.id)]['prefix']
    await ctx.send(
        embed = discord.Embed(
            title = f'{"⠀"*5}  🤖⠀|⠀Comandos do CarekoBot',
            description = f'''
            ```{'★ PRINCIPAIS ★':^43}```
            **「 🎧 」{prefix}say `texto`:**
            ➠ Reproduz uma mensagem TTS no canal de voz do usuário.
            **「 🗒️ 」{prefix}default `linguagem`:**
            ➠ Altera a linguagem padrão do bot em seu servidor.
            **「 🪐 」{prefix}langs:**
            ➠ Providencia uma lista de todas as linguagens suportadas.
            **「 🔇 」{prefix}stop:**
            ➠ Interrompe a mensagem TTS que está tocando.
            **「 🔕 」{prefix}clear:**
            ➠ Remove todas as mensagens TTS da lista de espera.
            **「 👀 」{prefix}join:**
            ➠ Força a entrada do bot para o canal do usuário.
            **「 👻 」{prefix}leave:**
            ➠ Força o bot a sair do canal de voz que ele está.
            
            ```{'★ CONFIGURAÇÕES (ADM ONLY) ★':^43}```
            **「 ✨ 」{prefix}prefix `prefixo`:**
            ➠ Muda o prefixo dos comandos em seu servidor.
            **「 🔒 」{prefix}lock `canal`:**
            ➠ Trava os comandos em um determinado canal de texto.
            **「 🔐 」{prefix}unlock `canal`:**
            ➠ Destrava os comandos de um determinado canal de texto.
            ⠀
            '''
        )
    )


@bot.command()
async def langs(ctx):
    with open(json_path) as file: prefix = load(file)[str(ctx.guild.id)]['prefix']
    await ctx.send(
        embed = discord.Embed(
            title = '🌎⠀|⠀Linguagens Suportadas',
            description = '\n'.join(f'{name[:3]}`【 {prefix + "lang "}{value} 】` ➠ ***{name[3:]}***' for name, value in bot.langs.items())
        )
    )


@bot.command(aliases = ['default', 'd'])
@commands.max_concurrency(number = 1, per = commands.BucketType.default, wait = True)
async def lang(ctx, arg):
    with open(json_path) as file: data = load(file)
    lang = [key for key, value in bot.langs.items() if value == arg]
    if not lang: await send_msg(f'Por favor, insira uma linguagem válida.\nDigite "{data[str(ctx.guild.id)]["prefix"]}langs" para ver as opções disponíveis.', ctx)
    elif arg == data[str(ctx.guild.id)]['lang']: await send_msg('Essa linguagem já está definida como padrão deste servidor.', ctx)
    else:
        data[str(ctx.guild.id)]['lang'] = arg
        with open(json_path, 'w') as file: dump(data, file, indent = 4)    
        await send_msg(f'Linguagem padrão redefinida para: {lang[0][3:]}', ctx)


@bot.command()
@commands.has_permissions(administrator = True)
@commands.max_concurrency(number = 1, per = commands.BucketType.default, wait = True)
async def prefix(ctx, arg):
    if len(arg) <= 3:
        with open(json_path) as file: data = load(file)
        prefix = data[str(ctx.guild.id)]['prefix']
        data[str(ctx.guild.id)]['prefix'] = arg
        if arg == prefix: await send_msg('Esse prefixo já é o padrão deste servidor.', ctx)
        else:
            with open(json_path, 'w') as file: dump(data, file, indent = 4)
            await send_msg(f'Prefixo padrão redefinido para: {arg}', ctx)
    else: await send_msg('O prefixos não pode exceder 3 caracteres.', ctx)


@bot.command()
@commands.has_permissions(administrator=True)
@commands.max_concurrency(number = 1, per=commands.BucketType.default, wait = True)
async def lock(ctx, *, arg):
    if search(r'^<#[\d]+>$', arg):
        with open(json_path) as file: data = load(file)
        channels = data[str(ctx.guild.id)]['channels']
        if arg[2:-1] in channels: await send_msg('O canal requisitado já está lockado', ctx)
        elif len(channels) >= 3: await send_msg('Não é possível lockar mais de 3 canais em um servidor só.', ctx)
        else:
            try: await bot.fetch_channel(arg[2:-1])
            except discord.NotFound: return await send_msg('O canal requisitado não existe.', ctx)
            channels.append(arg[2:-1])
            with open(json_path, 'w') as file: dump(data, file, indent = 4)
            await send_msg(f'O canal requisitado foi lockado com sucesso.', ctx)
    elif len(findall(r'<#[\d]+>', arg)) > 1: await send_msg('Por favor, insira um canal por vez.', ctx)
    else: await send_msg('Por favor, insira um canal de texto válido.', ctx)


@bot.command()
@commands.has_permissions(administrator = True)
@commands.max_concurrency(number = 1, per =  commands.BucketType.default, wait = True)
async def unlock(ctx, *, arg):
    with open(json_path) as file: data = load(file)
    channels = data[str(ctx.guild.id)]['channels']
    if not channels: await send_msg('Não há nenhum canal lockado neste servidor.', ctx)
    elif search(r'^<#[\d]+>$', arg):
        try: await bot.fetch_channel(arg[2:-1])
        except discord.NotFound: return await send_msg('O canal requisitado não existe.', ctx)
        if arg[2:-1] not in channels: await send_msg('O canal requisitado não está lockado.\nPor favor, marque o bot para ver quais estão.', ctx)
        else:
            channels.remove(arg[2:-1])
            with open(json_path, 'w') as file: dump(data, file, indent = 4)
            await send_msg(f'O canal requisitado foi desbloqueado com sucesso.', ctx)
    elif len(findall(r'<#[\d]+>', arg)) > 1: await send_msg('Por favor, insira um canal por vez.', ctx)
    else: await send_msg('Por favor, insira um canal de texto válido.', ctx)


@bot.event
async def on_command_error(ctx, error):
    errors = {
        commands.CommandNotFound: 'Comando não encontrado.',
        commands.MissingRequiredArgument: 'Por favor, passe os argumentos do seu comando corretamente.',
        commands.MissingPermissions: 'Você não tem permissão para usar este comando.'
        }

    if isinstance(error, tuple(errors)) and await global_check(ctx):
        await send_msg(errors.get(type(error)), ctx, 5)
    else: print(error)


load_dotenv()
token = getenv('token')
bot.run(token)

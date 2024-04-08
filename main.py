import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
queues = {}
playback_history = {}

def check_queue(ctx, guild_id):
    if queues.get(guild_id):
        voice_client = ctx.guild.voice_client
        source = queues[guild_id].pop(0)
        voice_client.play(source, after=lambda x=None: check_queue(ctx, guild_id))

@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='música'), status=discord.Status.do_not_disturb)
    print(f"{client.user.name} is logged in.")

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'default_search': 'ytsearch',
            'noplaylist': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if not url.startswith('http'):
                url = f"ytsearch:{url}"
            data = ydl.extract_info(url, download=not stream)
            data = data['entries'][0] if 'entries' in data else data
            filename = data['url'] if stream else ydl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}), data=data)

@client.command()
async def play(ctx, *, search: str):
    """Reproduce una canción basada en el término de búsqueda dado o la añade a la cola si ya hay música reproduciéndose."""
    async with ctx.typing():
        player = await YTDLSource.from_url(search, loop=client.loop, stream=True)
        guild_id = ctx.guild.id

        if guild_id in playback_history:
            playback_history[guild_id].append(player.title)
        else:
            playback_history[guild_id] = [player.title]

        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            if guild_id in queues:
                queues[guild_id].append(player)
            else:
                queues[guild_id] = [player]
            await ctx.send(f'**{player.title}** ha sido añadido a la cola.')
        else:
            ctx.voice_client.play(player, after=lambda x=None: check_queue(ctx, guild_id))
            await ctx.send(f'**Ahora reproduciendo:** {player.title}')

@client.command()
async def next(ctx):
    """Pasa a la siguiente canción en la cola."""
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Pasando a la siguiente canción...")
    else:
        await ctx.send("No hay música reproduciéndose actualmente.")

@client.command()
async def join(ctx):
    """Une al bot al canal de voz del usuario."""
    if not ctx.message.author.voice:
        await ctx.send("No estás conectado a un canal de voz.")
        return

    channel = ctx.message.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    await channel.connect()

@client.command()
async def stop(ctx):
    """Detiene la reproducción de música y desconecta al bot del canal de voz."""
    await ctx.voice_client.disconnect()

@client.command()
async def pause(ctx):
    """Pausa la reproducción de música actual."""
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Música pausada.")
    else:
        await ctx.send("Actualmente no hay música reproduciéndose.")

@client.command()
async def resume(ctx):
    """Reanuda la reproducción de música pausada."""
    voice_client = ctx.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Música reanudada.")
    else:
        await ctx.send("La música no está pausada.")

@client.command()
async def queue(ctx):
    """Muestra las canciones en la cola."""
    guild_id = ctx.guild.id
    
    if guild_id in queues and queues[guild_id]:
        message = "**Cola de Reproducción:**\n"
        for i, source in enumerate(queues[guild_id], start=1):
            message += f"{i}. {source.title}\n"
        await ctx.send(message)
    else:
        await ctx.send("La cola está vacía.")
        
@client.command()
async def history(ctx):
    """Muestra el historial de canciones reproducidas."""
    guild_id = ctx.guild.id

    if guild_id in playback_history and playback_history[guild_id]:
        message = "**Historial de Busqueda/Reproducción:**\n"
        for i, title in enumerate(playback_history[guild_id], start=1):
            message += f"{i}. {title}\n"
        await ctx.send(message)
    else:
        await ctx.send("El historial está vacío.")


client.run(os.getenv('DISCORD_TOKEN'))

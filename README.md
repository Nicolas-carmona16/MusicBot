# Bot de Música para Discord

Este bot de Discord es una herramienta diseñada para reproducir música en canales de voz, permitiendo a los usuarios disfrutar de sus canciones favoritas directamente en Discord. Utiliza `yt_dlp` para buscar y reproducir música de YouTube y gestiona las interacciones del usuario a través de `discord.py`.

## Funcionalidades

- Reproducción de música de YouTube en canales de voz.
- Comandos para controlar la reproducción (play, pause, resume, stop, next).
- Gestión de colas de reproducción.
- Historial de reproducción para ver canciones anteriores.
- Uso de variables de entorno para la seguridad del token del bot.

## Requisitos

- Python 3.6+
- FFmpeg
- Bibliotecas de Python: `discord.py[voice]`, `yt-dlp`, `python-dotenv`

## Instalación y Configuración

### Paso 1: Instalar Dependencias

Instala las dependencias necesarias ejecutando:

```bash
pip install -U discord.py[voice] yt-dlp python-dotenv
```

### Paso 2: FFmpeg

Asegúrate de tener FFmpeg instalado y agregado al PATH de tu sistema para que discord.py pueda utilizarlo para el procesamiento de audio.

### Paso 3: Configurar Variables de Entorno

Crea un archivo .env en el directorio raíz de tu proyecto y añade la siguiente línea:

```bash
DISCORD_TOKEN=tu_token_de_discord_aquí
```

Reemplaza tu_token_de_discord_aquí con el token real de tu bot de Discord. Esto ayudará a mantener tu token seguro y fuera del código fuente.

### Paso 4: Invitar el Bot a tu Servidor de Discord

Asegúrate de haber creado un bot en el Portal de Desarrolladores de Discord y de haberlo invitado a tu servidor de Discord.

## Ejecución

Para iniciar el bot, ejecuta el siguiente comando en la terminal:

```bash
python main.py
```

Asegúrate de estar en el directorio correcto que contiene tu script.

##  Comandos del Bot

- !join: Une al bot al canal de voz del usuario.
- !play <nombre de la canción o URL>: Busca la canción en YouTube y la reproduce. Si ya hay una canción reproduciéndose, la añade a la cola.
- !pause: Pausa la reproducción actual.
- !resume: Reanuda la reproducción pausada.
- !stop: Detiene la reproducción y desconecta al bot del canal de voz.
- !next: Salta a la siguiente canción en la cola.
- !queue: Muestra las canciones actuales en la cola.
- !history: Muestra un historial de las canciones reproducidas.

Recuerda que debes estar en un chat de voz para que el bot pueda unirse y reproducir musica.
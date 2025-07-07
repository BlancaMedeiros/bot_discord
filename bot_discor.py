import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o .env

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Prefixo de comando
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='atribuir_cargo')
@commands.has_permissions(manage_roles=True)
async def atribuir_cargo(ctx, cargo_id: int, *user_ids: int):
    guild = ctx.guild
    cargo = guild.get_role(cargo_id)

    if not cargo:
        await ctx.send(f"❌ Cargo com ID `{cargo_id}` não encontrado.")
        return

    adicionados = []
    nao_encontrados = []

    for user_id in user_ids:
        membro = guild.get_member(user_id)
        if membro:
            try:
                await membro.add_roles(cargo)
                adicionados.append(membro.name)
            except discord.Forbidden:
                await ctx.send(f"⚠️ Permissão insuficiente para dar cargo a {membro.name}")
        else:
            nao_encontrados.append(user_id)

    msg = f"✅ Cargo `{cargo.name}` atribuído a: {', '.join(adicionados) if adicionados else 'ninguém'}."
    if nao_encontrados:
        msg += f"\n⚠️ Usuários não encontrados no servidor: {', '.join(map(str, nao_encontrados))}"

    await ctx.send(msg)

# Inicie o bot
bot.run(TOKEN)

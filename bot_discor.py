import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

@bot.command(name='atribuir_cargo')
@commands.has_permissions(manage_roles=True)
async def atribuir_cargo(ctx, cargo_id: int):
    if not ctx.message.attachments:
        await ctx.send("❌ Você precisa anexar um arquivo `.txt` com os IDs dos usuários (um por linha).")
        return

    arquivo = ctx.message.attachments[0]

    if not arquivo.filename.endswith(".txt"):
        await ctx.send("❌ O arquivo precisa ser `.txt`.")
        return

    conteudo = await arquivo.read()
    linhas = conteudo.decode().splitlines()

    try:
        user_ids = [int(linha.strip()) for linha in linhas if linha.strip().isdigit()]
    except ValueError:
        await ctx.send("⚠️ O arquivo contém linhas que não são números válidos de ID.")
        return

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
            nao_encontrados.append(str(user_id))

    msg = f"✅ Cargo `{cargo.name}` atribuído a: {', '.join(adicionados) if adicionados else 'ninguém'}."
    if nao_encontrados:
        msg += f"\n⚠️ IDs não encontrados no servidor: {', '.join(nao_encontrados)}"

    await ctx.send(msg)

bot.run(TOKEN)

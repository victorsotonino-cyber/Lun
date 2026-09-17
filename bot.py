import os
import discord
from discord.ext import commands

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Tus emojis personalizados para el panel
EMOJI_SOPORTE = "<:emoji_11:1550144504990801930>"
EMOJI_TIENDA = "<:emoji_20:1550146329915949077>"
EMOJI_REPORTE = "<:emoji_10:1550144465765793792>"
EMOJI_REGALO = "<:emoji_14:1550144666618302525>"
EMOJI_MANTENIMIENTO = "<:emoji_9:1550144328540618882>"
EMOJI_VIPERFINDER = "<:emoji_12:1550144549412802631>"

# Vista con los botones de control dentro del ticket (Reclamar y Cerrar)
class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Reclamar", style=discord.ButtonStyle.green, emoji="🙋‍♂️", custom_id="ticket_reclamar")
    async def reclamar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"🔒 Ticket reclamado por {interaction.user.mention}")
        button.disabled = True
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Cerrar", style=discord.ButtonStyle.red, emoji="🔒", custom_id="ticket_cerrar")
    async def cerrar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⚠️ El canal se cerrará en 5 segundos...")
        import asyncio
        await asyncio.sleep(5)
        await interaction.channel.delete()

# Vista principal del panel de tickets
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Soporte", style=discord.ButtonStyle.secondary, emoji=EMOJI_SOPORTE, custom_id="ticket_soporte", row=0)
    async def soporte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.crear_ticket(interaction, "soporte")

    @discord.ui.button(label="Tienda", style=discord.ButtonStyle.secondary, emoji=EMOJI_TIENDA, custom_id="ticket_tienda", row=0)
    async def tienda_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.crear_ticket(interaction, "tienda")

    @discord.ui.button(label="Reporte", style=discord.ButtonStyle.secondary, emoji=EMOJI_REPORTE, custom_id="ticket_reporte", row=0)
    async def reporte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.crear_ticket(interaction, "reporte")

    @discord.ui.button(label="Mantenimiento", style=discord.ButtonStyle.secondary, emoji=EMOJI_MANTENIMIENTO, custom_id="ticket_mantenimiento", row=1)
    async def mantenimiento_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.crear_ticket(interaction, "mantenimiento")

    @discord.ui.button(label="Regalo", style=discord.ButtonStyle.secondary, emoji=EMOJI_REGALO, custom_id="ticket_regalo", row=2)
    async def regalo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.crear_ticket(interaction, "regalo")

    @discord.ui.button(label="Viperfinder", style=discord.ButtonStyle.secondary, emoji=EMOJI_VIPERFINDER, custom_id="ticket_viperfinder", row=2)
    async def viperfinder_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.crear_ticket(interaction, "viperfinder")

    async def crear_ticket(self, interaction: discord.Interaction, tipo: str):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        canal = await guild.create_text_channel(name=f"ticket-{tipo}-{interaction.user.name}", overwrites=overwrites)
        
        # Enviar mensaje dentro del nuevo ticket con los botones de Reclamar y Cerrar
        embed_ticket = discord.Embed(
            title=f"Ticket de {tipo.capitalize()}",
            description=f"Hola {interaction.user.mention}, un miembro del staff te atenderá pronto.\nUsa los botones de abajo para gestionar el ticket.",
            color=discord.Color.blue()
        )
        await canal.send(embed=embed_ticket, view=TicketControlView())
        
        await interaction.response.send_message(f"¡Canal de ticket creado con éxito! Ve a {canal.mention}", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot conectado correctamente como {bot.user}')

@bot.command(name="panel")
@commands.has_permissions(administrator=True)
async def panel(ctx):
    embed = discord.Embed(
        title="Lunar Market — Crear un Ticket",
        description=(
            f"{EMOJI_SOPORTE} **soporte** — Ayuda general con compras, problemas técnicos o preguntas sobre la tienda.\n"
            f"{EMOJI_TIENDA} **tienda** — Consultas relacionadas con productos, pagos, envíos o inventario.\n"
            f"{EMOJI_REPORTE} **reporte** — Reportes de usuarios, fraudes o comportamientos inapropiados.\n"
            f"{EMOJI_REGALO} **regalo** — Consultas sobre cajas/regalos.\n"
            f"{EMOJI_MANTENIMIENTO} **mantenimiento** — Avisos o dudas sobre mantenimientos.\n"
            f"{EMOJI_VIPERFINDER} **viperfinder** — Soporte para ViperFinder / herramientas relacionadas.\n\n"
            "Pulsa el botón correspondiente para crear un ticket."
        ),
        color=discord.Color.from_rgb(114, 137, 218)
    )
    await ctx.send(embed=embed, view=TicketView())

@bot.command(name="ayuda")
async def ayuda(ctx):
    embed_ayuda = discord.Embed(
        title="📖 Guía de Comandos del Bot",
        description="Aquí tienes la lista de comandos disponibles:",
        color=discord.Color.green()
    )
    embed_ayuda.add_field(name="!panel", value="Envía el panel de tickets con botones interactivos. (Admin)", inline=False)
    embed_ayuda.add_field(name="!ayuda", value="Muestra esta guía de comandos.", inline=False)
    await ctx.send(embed=embed_ayuda)

# Arranca usando la variable de entorno TOKEN de Railway
bot.run(os.getenv('TOKEN'))

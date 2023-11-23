import json
import discord
from discord import app_commands
import mecha

with open("config.json", 'r') as f:
    config = json.loads(f.read())

guild = discord.Object(id=config["guild"])

def valid_command(com):
    command = com
    if command[0] == "/":
        command = command[1:]
    try:
        mc = mecha.Mecha()
        mc.parse(command)
        return True, ""
    except Exception as e:
        return False, e

class MyClient(discord.Client):

    def __init__(self, intents):
        super().__init__(intents=intents)
        self.synced = False


    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.wait_until_ready();
        if not self.synced:
            await tree.sync(guild=guild)

#    async def on_message(self, message):
#        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
client = MyClient(intents=intents)


tree = app_commands.CommandTree(client)

@tree.command(name="help", description="Prints Help context", guild=guild)
async def help(interaction: discord.Interaction):
    """Help""" #Description when viewing / commands
    await interaction.response.send_message("hello")

@tree.command(name="parse", description="parses a minecraft command", guild=guild)
async def parse(interaction: discord.Interaction, command: str):

    valid, e = valid_command(command)
    if valid:
        await interaction.response.send_message("Command: \"" + command + "\" is valid")
    else:
        await interaction.response.send_message("Command: \"" + command + "\" is invalid, Error: " + str(e))





client.run(config["token"])

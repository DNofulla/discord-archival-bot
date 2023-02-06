import discord
from dotenv import load_dotenv
import os
import time

load_dotenv()
DISCORD_API_TOKEN = os.getenv('DISCORD_API_TOKEN')

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.archive_deleted_channel = discord.utils.get(self.get_all_channels(), name='archived-deleted')
        self.archive_edited_channel = discord.utils.get(self.get_all_channels(), name='archived-edits')
        self.channels_to_ignore = ['1067167101086863500', '1067254426831687731']

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


    async def on_message_delete(self, message):

        if self.user.id != message.author.id:
            embed = discord.Embed(title="Deleted Message", color=0xff0000)
            embed.add_field(name="Author", value=f"{message.author.mention}")
            embed.add_field(name="Channel", value=f"<#{message.channel.id}>")
            embed.add_field(name="Message", value=message.content, inline=False)
            await self.archive_deleted_channel.send(embed=embed)
            if message.attachments:
                for attachment in message.attachments:
                    attachment_embed = discord.Embed(title="Deleted Message", color=0xff0000)
                    attachment_embed.add_field(name="Author", value=f"{message.author.mention}")
                    attachment_embed.add_field(name="Channel", value=f"<#{message.channel.id}>")
                    attachment_embed.set_image(url=attachment.url)
                    await self.archive_deleted_channel.send(embed=attachment_embed)
                    time.sleep(0.5)

    async def on_message_edit(self, before, after):
        embed = discord.Embed(title="Edited Message", color=0xff0000)
        embed.add_field(name="Author", value=f"{before.author.mention}")
        embed.add_field(name="Channel", value=f"<#{before.channel.id}>")
        embed.add_field(name="Message ID", value=f"<https://discordapp.com/channels/{before.guild.id}/{before.channel.id}/{before.id}>", inline=False)
        embed.add_field(name="Original Message", value=before.content, inline=False)
        embed.add_field(name="Edited Message", value=after.content, inline=False)
        await self.archive_deleted_channel.send(embed=embed)
        

            

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(f'{DISCORD_API_TOKEN}')
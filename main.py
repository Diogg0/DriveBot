import discord
from discord.ext import commands
from discord import app_commands
from backend import *


# DISCORD DriveBot CODE
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="%", intents=intents,
                   activity=discord.Game(name="Driving Google!", type=3))

slash = bot.tree


@bot.event
async def on_ready():
    print("Bot is Online!")
    await slash.sync(guild=discord.Object(id=GUILD_ID))  # comment it out after first reboot
    print("Slash commands synced to guild, please comment above line out now!")


# I decided to have a dynamic search helper instead of a direct dropdown list
# This is because the dropdown list would hold maximum 100 folders, files even if its not a possibility in the earlier stages it can lead to the code breaking

@slash.command(guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    folder="The name of the folder",
    file="The name of the file"
)
async def access(itx: discord.Interaction, folder: str, file: str):
    """
    Get direct access to the google drive file you want
    """
    # Maybe you raise an error on returning file
    if folder not in get_all_folders():
        return await itx.response.send_message(f"Could not find folder named: `{folder}`", ephemeral=True)
    if file not in get_all_files(folder):
        return await itx.response.send_message(f"Could not find file named: `{file}` in folder named: `{folder}`", ephemeral=True)

    await itx.response.defer(ephemeral=True)
    link = get_file(folder, file)

    try:
        await itx.user.send(link)
    # DM failure exceptions can be weird so I'll just use an all seeing exception block
    except:
        await itx.followup.send(link, ephemeral=True)
    else:
        await itx.followup.send('🏎️ DM SENT!')


@access.autocomplete('folder')
async def autocomplete_callback(interaction, current: str):
    current = current.lower().replace(' ', '').replace('-', '')
    return [
        app_commands.Choice(name=name, value=name) for name in get_all_folders() if current.lower() in name.lower()
    ][:25]


@access.autocomplete('file')
async def autocomplete_callback(interaction, current: str):
    current = current.lower().replace(' ', '').replace('-', '')
    return [
        app_commands.Choice(name=name, value=name) for name in get_all_files(interaction.namespace['folder']) if current.lower() in name.lower()
    ][:25]


@slash.command(guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    file="The file you wish to upload",
    folder="The folder in which the file should be uploaded",
)
async def upload(itx: discord.Interaction, file: discord.Attachment, folder: str):
    """
    Uploads the file to specified folder
    """
    if folder not in get_all_folders():
        return await itx.response.send_message(f"Could not find folder named: `{folder}`", ephemeral=True)
    file_name = file.filename[file.filename.rfind('/') + 1:]
    if file_name in get_all_files(folder):
        return await itx.response.send_message(
            f"Please rename your file, existing file named: `{file}` found in folder: `{folder}`", ephemeral=True)

    await itx.response.defer(ephemeral=True)

    path = await download_file(file)

    uploaded = upload_file(file_name, path, folder)
    if uploaded:
        await itx.followup.send(f"File: `{file_name}` uploaded successfully! Location Folder: `{folder}`",
                                ephemeral=True)
    else:
        await itx.followup.send('File was not uploaded... please retry later', ephemeral=True)


@upload.autocomplete('folder')
async def autocomplete_callback(interaction, current: str):
    current = current.lower().replace(' ', '').replace('-', '')
    return [
               app_commands.Choice(name=name, value=name) for name in get_all_folders() if
               current.lower() in name.lower()
           ][:25]


@slash.command(guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    folder="The name of the new folder"
)
async def create_folder(itx: discord.Interaction, folder: str):
    if folder in get_all_folders():
        return await itx.response.send_message('Folder already exists', epehemeral=True)

    created = create_drive_folder(folder)
    if created:
        await itx.response.send_message(f"Successfully created folder named: {folder}", ephemeral=True)
    else:
        await itx.response.send_message(f"Folder was not created... ", ephemeral=True)

bot.run(TOKEN)

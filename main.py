import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import aiohttp

TOKEN = "TOKEN"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="w", intents=intents)

async def create_welcome_card(member: discord.Member):
    background_url = "https://raw.githubusercontent.com/Bytex86/WFSC/refs/heads/main/image.png"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(background_url) as resp:
            background = Image.open(BytesIO(await resp.read()))
        
        async with session.get(str(member.display_avatar.with_size(256).with_format("png"))) as resp:
            avatar = Image.open(BytesIO(await resp.read())).resize((200, 200))
    
    mask = Image.new("L", (200, 200), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=255)
    
    avatar_with_border = Image.new("RGBA", (210, 210), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(avatar_with_border)
    draw_border.ellipse((0, 0, 210, 210), fill=(255, 255, 255, 255))
    avatar_with_border.paste(avatar, (5, 5), mask)
    
    background = background.convert("RGBA")
    avatar_x = 412  # change 
    avatar_y = 270   # change
    background.paste(avatar_with_border, (avatar_x, avatar_y), avatar_with_border)
    
    draw = ImageDraw.Draw(background)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    text = member.name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (1024 - text_width) // 2  # centered
    text_y = 500  # change
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    buffer = BytesIO()
    background.save(buffer, "PNG")
    buffer.seek(0)
    return buffer

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Watching over the AISC server"))
    print(f'> WFSC Bot logged in as {bot.user}')

@bot.command()
async def test(ctx):
    if ctx.author.id != 123: # owner or tester id
        await ctx.send('Error 404: Server replied with "no"') 
        return
    card = await create_welcome_card(ctx.author)
    await ctx.send(file=discord.File(card, "welcome.png"))

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(123) # welcome channel id
    if not channel:
        return
    
    card = await create_welcome_card(member)
    await channel.send(file=discord.File(card, "welcome.png"))
    
    message = (
        f"Welcome to the **official AISC server** {member.mention}! 🎉\n\n"
        "Please verify to access all channels.\n"
        "Please introduce yourself in <#> (access will be granted after verification) and check out ⁠<id:customize> to get more roles.\n"
        "Feel free to DM <@> for any queries.\n"
        "Please remember this is a SFW community. Make sure to review our ⁠rules.\n\n"
        "Enjoy your stay here, and Keep AISC-ing! 🚀"
    )
    
    await channel.send(message)

if __name__ == "__main__":
    bot.run(TOKEN)

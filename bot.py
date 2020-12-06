from discord.ext import commands
import keyring

TOKEN = keyring.get_password("NSBOT", "password")

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='hello', help='Responds with greeting!')
async def greeting(context):
    response = f"Hello {context.author.display_name}"
    await context.send(response)


@bot.command(name='run', help='Runs the natural selection simulation!')
async def run(context, n_agents: int = 10, n_food: int = None, days: int = None):
    response = f"The model will run with {n_agents} agents and {n_food} food over {days} days."
    await context.send(response)


# To keep the test server clean
@bot.command(name='clear', help='Clears all the messages in a channel.')
@commands.has_role("admin")
async def clear(context):
    await context.channel.purge()


# Turn off the bot from Discord.
@bot.command(name='stop', help='Stops the bot from running')
@commands.has_role("admin")
async def stop(context):
    await context.bot.logout()


bot.run(TOKEN)

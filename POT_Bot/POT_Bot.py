import discord
import recommender
import sharpness
import urllib.request
import techiness

client = discord.Client()
#recommender.initialmapfile()

@client.event
async def on_ready():
    print('Log in as {0.user} successful.'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!!h'):
        msg = 'Recommend a random loved or unranked map within a specified star range. **Usage:**\n!!rl LB UB *prints a map with SR in the range [LB,UB]*. \n!!ru LB UB *prints an unranked map with 50+ favourites with SR in the range [LB,RB].\n!!sh **mapID** or !!tech **mapLink** *prints the Techiness value of the specified map.'
        await message.channel.send(msg)
    if message.content.startswith('!!rl'):
        getmap = recommender.recommendloved(message.content[4:]) #Strip the !!r at the front to get star range
        await message.channel.send(getmap)
    if message.content.startswith('!!ru'):
        getmap = recommender.recommendunranked(message.content[4:])
        await message.channel.send(getmap)
    if message.content.startswith('!!tech'): #Invoking the sharpness calculator
        maplink = message.content[6:]
        mapID = maplink.split('/')[-1]
        urllib.request.urlretrieve('https://osu.ppy.sh/osu/'+ mapID, 'test/'+mapID+'.osu')
        techinessMap = techiness.techiness('test/'+mapID+'.osu')
        await message.channel.send('Techiness value: ' + '%.3f' % techinessMap)

client.run('NTg0Njg1NDI1MDQyNjUzMjA4.XPOmZQ.OVYr-DO_OLkirvj16WUUkjT5FCk')
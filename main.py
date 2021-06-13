import discord
import os
import json
import re
from dotenv import load_dotenv

path = [os.path.dirname(os.path.abspath(__file__))]

#https://www.geeksforgeeks.org/python-convert-string-dictionary-to-dictionary/

client = discord.Client()
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

classes = ["Hellion","Vocaloid","Shifter","Fighter","Outcast","Scout","Warlock","Hacker"]
gang_symbols = {"Mafia":"<:mafia_symbol:849395018019766332>", "Biker":"<:tigerbiker:849297017046171728>","Sukeban":"<:sukeflower:849396667333345292>"}

in_use = [False]

f = open(path[0] + '\\sona.json',"r")
sona = json.load(f)
f.close()

f = open(path[0] + '\\gallery.json',"r")
gallery_json = json.load(f)
f.close()

f = open(path[0] + '\\captions.json',"r")
captions = json.load(f)
f.close()

@client.event
async def on_ready():
    print(f'{client.user.name} is online nerd')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #if message.content == '*test':
    #    embedVar = discord.Embed(title=f'{message.author}', color=0xccccff)
    #    embedVar.add_field(name='Sona', value='Stats:', inline=False)
    #    embedVar.set_image(url='https://media.discordapp.net/attachments/846226652942041148/846227132174303252/unknown.png?width=1008&height=1132')
    #    await message.channel.send(embed=embedVar)

    if message.content == '*quit' and message.author.id == 542033277163274260:
        await message.channel.send('killing bot')
        quit()

    if message.content == '*help':
        desc = '''
                `*help` - Shows a list of all commands
                `*addsona -name <name>` - Creates a sona profile
                `*add -image <url>` - Adds an image to the profile, only excepts urls for images
                `*add -name <name>` - Edits name of profile
                `*sona` - Displays profile
                `*delsona` - Deletes sona
                `*gallery` - Displays gallery of images, use reactions to scroll through the gallery, only the person that issued the command can use the gallery
                `*addgallery -image <url>`- Adds an image to the gallery
                `*caption <page> <caption>` - Adds a caption to a specified image
                `*delentry <page>` - Deletes a given page
                `*delgallery` - Clears gallery
                '''
        embedVar = discord.Embed(title='Command List',description=desc,color=0xccccff)
        await message.channel.send(embed=embedVar)

    if message.content == '*backup' and message.author.id == 542033277163274260:
        f = open(path[0] + '\\sona.json',"r")
        await message.channel.send(file=discord.File(f, 'sona.json'))
        f.close()

        f = open(path[0] + '\\gallery.json',"r")
        await message.channel.send(file=discord.File(f, 'gallery.json'))
        f.close()

        f = open(path[0] + '\\captions.json',"r")
        await message.channel.send(file=discord.File(f, 'captions.json'))
        f.close()
        

    if message.content[:14] == '*addsona -name':
        if str(message.author) in sona:
            await message.channel.send(f'<@{message.author.id}> sorry you can\'t have more than one sona')
        else:
            #name_index = message.content.index(' -url')
            name = message.content[15:]
            #image_url = message.content[name_index+1:]

            sona[str(message.author)] = [name,'', 'stats']

            mafia = [str(i) for i in message.author.roles if str(i) == "Mafia"]
            biker = [str(i) for i in message.author.roles if str(i) == "Biker"]
            sukeban = [str(i) for i in message.author.roles if str(i) == "Sukeban"]
            gang = [i for i in mafia + biker + sukeban]

            chosen_classes = [str(i) for i in message.author.roles if str(i) in classes]

            embedVar = discord.Embed(title=f'{name}', color=0xccccff)
            embedVar.add_field(name="Gang:",value=str(gang[0]) + f' {gang_symbols[str(gang[0])]}')
            if len(chosen_classes) > 1:
                embedVar.add_field(name="Classes:",value=', '.join(chosen_classes))
            elif len(chosen_classes) == 1:
                embedVar.add_field(name="Class:",value=chosen_classes[0])
            #embedVar.set_image(url=image_url)
            await message.channel.send(embed=embedVar)
    
    if message.content[:11] == '*add -image':
        if str(message.author) not in sona:
            await message.channel.send(f'<@{message.author.id}> you don\'t have a sona yet nerd')
        else:
            mafia = [str(i) for i in message.author.roles if str(i) == "Mafia"]
            biker = [str(i) for i in message.author.roles if str(i) == "Biker"]
            sukeban = [str(i) for i in message.author.roles if str(i) == "Sukeban"]
            gang = [i for i in mafia + biker + sukeban]

            image_url = message.content[12:]
            sona[str(message.author)][1] = image_url

            chosen_classes = [str(i) for i in message.author.roles if str(i) in classes]

            embedVar = discord.Embed(title=f'{sona[str(message.author)][0]}', color=0xccccff)
            embedVar.add_field(name="Gang:",value=str(gang[0]) + f' {gang_symbols[str(gang[0])]}')

            if len(chosen_classes) > 1:
                embedVar.add_field(name="Classes:",value=', '.join(chosen_classes))
            elif len(chosen_classes) == 1:
                embedVar.add_field(name="Class:",value=chosen_classes[0])
            embedVar.set_image(url=sona[str(message.author)][1])

            embedVar.set_image(url=image_url)

            await message.channel.send(embed=embedVar)
    
    if message.content[:10] == '*add -name':
        if str(message.author) not in sona:
            await message.channel.send(f'<@{message.author.id}> you don\'t have a sona yet nerd')
        else:
            mafia = [str(i) for i in message.author.roles if str(i) == "Mafia"]
            biker = [str(i) for i in message.author.roles if str(i) == "Biker"]
            sukeban = [str(i) for i in message.author.roles if str(i) == "Sukeban"]
            gang = [i for i in mafia + biker + sukeban]

            new_name = message.content[11:]
            sona[str(message.author)][0] = new_name

            chosen_classes = [str(i) for i in message.author.roles if str(i) in classes]

            embedVar = discord.Embed(title=f'{sona[str(message.author)][0]}', color=0xccccff)
            embedVar.add_field(name="Gang:",value=str(gang[0]) + f' {gang_symbols[str(gang[0])]}')

            if len(chosen_classes) > 1:
                embedVar.add_field(name="Classes:",value=', '.join(chosen_classes))
            elif len(chosen_classes) == 1:
                embedVar.add_field(name="Class:",value=chosen_classes[0])

            embedVar.set_image(url=sona[str(message.author)][1])

            await message.channel.send(embed=embedVar)

    if message.content == '*sona':
        if str(message.author) not in sona:
            await message.channel.send(f'<@{message.author.id}> you don\'t have a sona yet nerd')
        else:
            mafia = [str(i) for i in message.author.roles if str(i) == "Mafia"]
            biker = [str(i) for i in message.author.roles if str(i) == "Biker"]
            sukeban = [str(i) for i in message.author.roles if str(i) == "Sukeban"]
            gang = [i for i in mafia + biker + sukeban]

            chosen_classes = [str(i) for i in message.author.roles if str(i) in classes]

            embedVar = discord.Embed(title=f'{sona[str(message.author)][0]}',color=0xccccff)
            embedVar.add_field(name="Gang:",value=str(gang[0]) + f' {gang_symbols[str(gang[0])]}')

            if len(chosen_classes) > 1:
                embedVar.add_field(name="Classes:",value=', '.join(chosen_classes))
            elif len(chosen_classes) == 1:
                embedVar.add_field(name="Class:",value=chosen_classes[0])

            embedVar.set_image(url=sona[str(message.author)][1])

            await message.channel.send(embed=embedVar)
    
    if message.content[:8] == '*delsona':
        if str(message.author) not in sona:
            await message.channel.send(f'<@{message.author.id}> you don\'t have a sona yet nerd')
        else:
            del sona[str(message.author)]
            await message.channel.send('Sona deleted')

    if message.content[:8] == '*gallery' and not in_use[0]:
        
        if str(message.author) in gallery_json:
        
            in_use[0] = True

            pages = [discord.Embed(title=(f'Page: {i+1}'),description=(f'{captions[str(message.author)][i]}'),color=0xccccff) for i in range(len(gallery_json[str(message.author)]))]
            for i in range(len(pages)):
                pages[i].set_image(url=gallery_json[str(message.author)][i])

            gallery = await message.channel.send(embed=pages[0])

            await gallery.add_reaction('◀')
            await gallery.add_reaction('▶')

            page_number = 0
            reaction = None

            def check(reaction, user):
                return user == message.author

            while True:
                if str(reaction) == '◀':
                    if page_number > 0:
                        page_number -= 1
                        await gallery.edit(embed = pages[page_number])
                elif str(reaction) == '▶':
                    if page_number < len(pages)-1:
                        page_number += 1
                        await gallery.edit(embed = pages[page_number])

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout = 30.0,check=check)
                    await gallery.remove_reaction(reaction, user)
                except:
                    break
            
            in_use[0] = False
            await gallery.clear_reactions()

        else:
            await message.channel.send('You don\'t have a gallery nerd')

    elif message.content[:12] == '*gallery' and  in_use[0]:
        await message.channel.send('Another gallery is already in use, please wait')
    
    if message.content[:18] == '*addgallery -image' and len(message.content) > 18:
        if str(message.author) in gallery_json:
            gallery_json[str(message.author)].append(message.content[19:])
            captions[str(message.author)].append('')

            embedVar = discord.Embed(title=(f'Page: {len(gallery_json[str(message.author)])}'),description='',color=0xccccff)
            embedVar.set_image(url=gallery_json[str(message.author)][len(gallery_json[str(message.author)])-1])

            await message.channel.send(embed=embedVar)
        else:
            gallery_json[str(message.author)] = []
            captions[str(message.author)] = ['']

            gallery_json[str(message.author)].append(message.content[19:])

            embedVar = discord.Embed(title=('Page: 1'),description='',color=0xccccff)
            embedVar.set_image(url=gallery_json[str(message.author)][0])

            await message.channel.send(embed=embedVar)

        json_to_save = json.dumps(gallery_json)
        f = open(path[0] + '\\gallery.json',"w")
        f.write(json_to_save)
        f.close()

    if message.content == '*delgallery':
        del gallery_json[str(message.author)]
        await message.channel.send('Gallery deleted')

        json_to_save = json.dumps(gallery_json)
        f = open(path[0] + '\\gallery.json',"w")
        f.write(json_to_save)
        f.close()

    if message.content[:9] == '*delentry':
        try:
            entry = int(message.content[10:])
            if entry > len(gallery_json[str(message.author)]) or entry < 1:
                await message.channel.send('Not a valid entry')
            else:
                print(gallery_json[str(message.author)])
                del gallery_json[str(message.author)][entry-1]
                del captions[str(message.author)][entry-1]
                if len(gallery_json[str(message.author)]) == 0:
                    del gallery_json[str(message.author)]
                    del captions[str(message.author)]
                await message.channel.send((f'Entry {entry} deleted'))

                json_to_save = json.dumps(gallery_json)
                f = open(path[0] + '\\gallery.json',"w")
                f.write(json_to_save)
                f.close()
        except:
            await message.channel.send('Not a valid entry')

    if message.content[:8] == '*caption':
        if len(message.content) < 10:
            await message.channel.send('You need to provide an argument nerd')
        else:
            entry = re.search('^\*caption \d+',message.content)
            if entry == None:
                await message.channel.send('Invalid argument nerd')
            else:
                if int(message.content[len('*caption '):entry.end()]) > len(captions[str(message.author)]) or int(message.content[len('*caption '):entry.end()]) < 1:
                    await message.channel.send('Not a valid entry')
                else:
                    captions[str(message.author)][int(message.content[len('*caption '):entry.end()])-1] = message.content[entry.end()+1:]
                    await message.channel.send((f'Entry {int(message.content[9:entry.end()])} updated'))

                    json_to_save = json.dumps(captions)
                    f = open(path[0] + '\\captions.json',"w")
                    f.write(json_to_save)
                    f.close()
        
    json_to_save = json.dumps(sona)
    f = open(path[0] + '\\sona.json', "w")
    f.write(json_to_save)
    f.close()
        

client.run(token)
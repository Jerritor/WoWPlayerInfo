import random
import requests
import requests_oauthlib
import json
from requests.auth import HTTPBasicAuth

#STEPS:
#1) import wowprogress guild list
#2) use guild list to find list of players
#3) use list of players to get raiderio info


### 1) import list of guilds in Sargeras realm
with open('us_sargeras_tier27.json') as f:
    sargeras = json.load(f)

guildRanks = [68]

#get random number of guilds in the realm
#while x < 200: #number of guilds
#    hasNum = True
#    while hasNum:
#        newnum = random.randint(0, len(sargeras) - 1)
#        if (newnum not in guildRanks):
#            hasNum = False
#    guildRanks.append(newnum)
#    x += 1

#get all of the guilds in the realm
x = 0
while x < len(sargeras) - 1:
    if x != 68: #68 is my friends' guild
        guildRanks.append(x)
    x += 1

print(guildRanks)



### 2) import blizzard guild info

#prints all guilds and realm rank
guildURLs = []
for i in sargeras:
    #print(i['realm_rank'], i['name'])
    if (i['realm_rank'] in guildRanks):
        guildname = i['name']
        guildname = guildname.replace(' ','-')
        guildname = guildname.lower()
        guildGetURL = 'https://us.api.blizzard.com/data/wow/guild/sargeras/' + guildname + '/roster'
        guildURLs.append(guildGetURL)

for i in guildURLs:
    print(i)

#read access token
f = open('token.txt', 'r')
#print(f.read())
token = f.read()
f.close()

#get parameters
reqdata = {'namespace': 'profile-us',
          'locale': 'en-US',
          'access_token': token}

#open chars.txt and save onto list
chars = [] #only chars
charIlvls = { 'people': []} #chars and item levels
#f = open('chars.txt', 'r')
#f1 = open('charLevels.txt', 'r')
#for line in f1:
#    charName= line.rstrip('\n')
#    charIlvl = charName.split(",") #[0] name, [1] ilvl

#    chars.append(charIlvl[0])

#    charIlvls["name"].append(charIlvl[0])
#    charIlvls["ilvl"].append(charilvl[1])

#f.close()
#f1.close()

#gets all characters from all selected guilds
for url in guildURLs:
    r = requests.get(url, params = reqdata)
    guildJson = r.json()
    try:
        for member in guildJson['members']:
            name = member['character']['name']
            ilvl = member['character']['level']
            print(name, ilvl)
            if name not in chars:
                chars.append(name)

                charIlvls['people'].append({"name":name, "ilvl":ilvl})

                #charIlvls["name"] =(name)
                #charIlvls["ilvl"].append(ilvl)
    except:
        print("ERROR:", guildJson)

#write new charlist to file
f = open('chars.txt', 'w')
for i in chars:
    f.write(i + "\n")
f.close()

print(chars)


#write new charItems to file
with open('charLevels.txt', 'w') as convert_file:
    convert_file.write(json.dumps(charIlvls, indent = 4))

print(charIlvls)









####EXTRA stuff
#r = requests.get("https://us.api.blizzard.com/data/wow/guild/sargeras/Airstrike/roster", params = r1data)


#with requests.Session() as session:
#   r = session.get("https://us.battle.net/oauth/token", allow_redirects = False)




#r1 = requests.get("https://us.api.blizzard.com/data/wow/guild/sargeras/Airstrike/roster", params = r1data)

#print(r1.json())



#r = requests.get('https://us.api.blizzard.com/data/wow/guild/sargeras/airstrike/roster', params = reqdata)
#guildsJson = r.json()
#print(r.text)

#charlist = []
#for i in guildsJson['members']:
#    charlist.append(i['character']['name'])
#print(charlist)
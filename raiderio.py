import requests
import json
import atexit
import time
import sys
import random

#VARIABLES and their get request fields:
#Level: chars

#default-
#Name: name
#Race: race
#Class: class
#Faction: faction
#Achievement Points: achievement_points


#gear
#Item Level: item_level_equipped


#raid_progression
#Number of raid bosses killed in Normal difficulty: castle-nathria/normal_bosses_killed
#Number of raid bosses killed in Heroic difficulty: castle-nathria/heroic_bosses_killed
#Number of raid bosses killed in Mythic difficulty: castle-nathria/mythic_bosses_killed


#mythic_plus_scores_by_season:current
#Raider IO Score: scores/all


#mythic_plus_ranks (world rank)
#Mythic Plus Overall Rank: overall/world
#Mythic Plus Class Rank: class/world
#Mythic Plus Faction Rank: faction_overall/world
#Mythic Plus Faction Class Rank: faction_class/world


#NOTES:
#removed Number of raid bosses killed in LFR difficulty because it was unavailable

t = time.localtime()
currentTime = time.strftime("%H:%M:%S", t)
currentTime = str(currentTime)
currentTime = currentTime.replace(':','-')
currentTime = "C:/Users/jetorres/PycharmProjects/weather/json files/" + currentTime + ".json"
print(currentTime)


writeToFile = currentTime #'raiderio.json'


charNames = []
getInfo = { 'people':[]} #info to json

def writeToJSON():
    with open(writeToFile, 'w') as convert_file:
        convert_file.write(json.dumps(getInfo, indent=4))

def run_on_exit():
    print("Writing to raiderio.json...")
    writeToJSON()
    print('Last logged texts:')
    print(rGear.text)
    print(rRaid.text)
    print(rMScore.text)
    print(rMRank.text)

atexit.register(run_on_exit)

#open list of characters
f = open('charsNotLogged.txt', 'r')
lines = 0
for line in f:
    lineFixed = line.rstrip('\n')
    charNames.append(lineFixed)
    if lines > 36000:
        break
f.close()
updatedCharNames = charNames.copy()
random.shuffle(updatedCharNames) #shuffle names to be queried


#requests are limited to 300 per min. 4 requests per character so 75 max per minute.
reqs = 0 #number of requests
for name in charNames:
    if reqs > 240: #60 chars to be safe. 60*4 = 240
        print("Sleeping for 20 secs...")
        time.sleep(20)
        reqs = 0
    #else:
    #    time.sleep(1) #1 sec delay per character


    gearFields = {'region': 'us',
                  'realm': 'Sargeras',
                  'name': name,
                  'fields': 'gear'}

    raidFields = {'region': 'us',
                  'realm': 'Sargeras',
                  'name': name,
                  'fields': 'raid_progression'}

    mythicScoreFields = {'region': 'us',
                         'realm': 'Sargeras',
                         'name': name,
                         'fields': 'mythic_plus_scores_by_season:current'}

    mythicRankFields = {'region': 'us',
                        'realm': 'Sargeras',
                        'name': name,
                        'fields': 'mythic_plus_ranks'}
    try:
        print("Querying", name, "gear...")
        rGear = requests.get("https://raider.io/api/v1/characters/profile", params=gearFields, timeout=5)
        # time.sleep(1)  # 0.3 sec delay per get
        print("Querying", name, "raid...")
        rRaid = requests.get("https://raider.io/api/v1/characters/profile", params=raidFields, timeout=5)
        # time.sleep(1)  # 0.3 sec delay per get
        print("Querying", name, "mythic score...")
        rMScore = requests.get("https://raider.io/api/v1/characters/profile", params=mythicScoreFields, timeout=5)
        # time.sleep(1)  # 0.3 sec delay per get
        print("Querying", name, "mythic ranks...")
        rMRank = requests.get("https://raider.io/api/v1/characters/profile", params=mythicRankFields, timeout=5)
        print("Querying", name, "done.")
    except requests.exceptions.Timeout:
        print("Timeout. Exiting...")
        sys.exit(-1)
    except requests.exceptions.HTTPError:
        print("HTTP Error. Exiting...")
        sys.exit(-1)
    except requests.exceptions.ConnectionError:
        print("Connection Error. Exiting...")
        sys.exit(-1)
    except:
        print("Other Error. Exiting...")
        sys.exit(-1)

    reqs += 4
    print("Reqs:", reqs)

    # remove name
    updatedCharNames.remove(name)

    # update charsNotLogged
    f = open('charsNotLogged.txt', 'w')
    for i in updatedCharNames:
        f.write(i + "\n")
    f.close()

    charGear = rGear.json()
    charRaid = rRaid.json()
    charMScore = rMScore.json()
    charMRank = rMRank.json()

    # print(charMScore)

    try:
        name = charGear['name']
        race = charGear['race']
        charClass = charGear['class']
        faction = charGear['faction']
        achPts = charGear['achievement_points']
        ilvl = charGear['gear']['item_level_equipped']

        normalBosses = charRaid['raid_progression']['castle-nathria']['normal_bosses_killed']
        heroicBosses = charRaid['raid_progression']['castle-nathria']['heroic_bosses_killed']
        mythicBosses = charRaid['raid_progression']['castle-nathria']['mythic_bosses_killed']

        ioScore = charMScore['mythic_plus_scores_by_season'][0]['scores']['all']

        overallRank = charMRank['mythic_plus_ranks']['overall']['world']
        classRank = charMRank['mythic_plus_ranks']['class']['world']
        factionRank = charMRank['mythic_plus_ranks']['faction_overall']['world']
        factionClassRank = charMRank['mythic_plus_ranks']['faction_class']['world']

        getInfo['people'].append({'name': name,
                                  'race': race,
                                  'class': charClass,
                                  'faction': faction,
                                  'achievment_pts': achPts,
                                  'ilvl': ilvl,
                                  'normal_bosses_killed': normalBosses,
                                  'heroic_bosses_killed': heroicBosses,
                                  'mythic_bosses_killed': mythicBosses,
                                  'io_score': ioScore,
                                  'overall_ank': overallRank,
                                  'class_rank': classRank,
                                  'faction_rank': factionRank,
                                  'faction_class_rank': factionClassRank})

        # update raiderio.json
        writeToJSON()

        print(name, "appended.")
    except:
        print("ERROR:")
        print(rGear.text)
        print(rRaid.text)
        print(rMScore.text)
        print(rMRank.text)

#write get info to file
writeToJSON()


#######


#mythic_plus_ranks (world rank) -
#Mythic Plus Overall Rank: overall/world
#Mythic Plus Class Rank: class/world
#Mythic Plus Faction Rank: faction_overall/world
#Mythic Plus Faction Class Rank: faction_class/world
import xml.etree.ElementTree as ET
import random
import uuid
import fetcher
import json
import os
import datetime
import pytz

#generate static list of static channel names
#get schedule JSON
#parse wanted tags
    #build channel list
    #build guide

NUM_CHANNELS        = 400
DADDY_JSON_FILE     = "daddyliveSchedule.json"
M3U8_OUTPUT_FILE    = "daily.m3u8"
EPG_OUTPUT_FILE     = "daily.xml"

def generate_unique_ids(count, seed=42):
    random.seed(seed)
    ids = []
    for _ in range(count):
        id_str = str(uuid.UUID(int=random.getrandbits(128)))  # Generate a unique UUID
        ids.append(id_str)
    return ids

def loadJSON(filepath):
    # Open and read the JSON file
    with open(filepath, 'r', encoding='utf-8') as file:
        json_object = json.load(file)

    # Print the Python dictionary
    # print(json_object)

    return json_object
def addChannelByTerm(term, section):
    for day, value in dadjson.items():
        try:
            sport = dadjson[f"{day}"][section]
            for game in sport:
                if term in game["event"]:
                    print(game["event"])
                
                    for channel in game["channels"]:
                        #Creating Time Data
                        date_time = day.replace("th ", " ").replace("rd ", " ").replace("st ", " ").replace("nd ", " ")
                        date_time = date_time.replace("-", game["time"] + " -")
                        # Parse the cleaned date string into a datetime object
                        date_format = "%A %d %b %Y %H:%M - Schedule Time UK GMT"
                        start_date = datetime.datetime.strptime(date_time, date_format)
                        start_date = start_date + datetime.timedelta(hours=17)
                        
                        # Convert the datetime object into the two requested formats
                        # format_24_hour = parsed_date.strftime("%Y%m%d%H%M00")
                        startTime = start_date.strftime("%Y%m%d000000")
                        format_12_hour = start_date.strftime("%m/%d/%y - %I:%M %p") + " (MST)"

                        stop_date = start_date + datetime.timedelta(days=2)
                        stopTime = stop_date.strftime("%Y%m%d000000")
                        # Print the results
                        # print(f"24-hour format: {format_24_hour}")
                        # print(f"12-hour format: {format_12_hour}")

                        UniqueID    = unique_ids.pop()
                        channelName = game["event"] + " " + format_12_hour + " " + channel["channel_name"]
                        channelID   = f"{channel['channel_id']}"
                        logo        = "https://raw.githubusercontent.com/JHarding86/daddylive-m3u/refs/heads/main/hardingtv.png"

                        with open(M3U8_OUTPUT_FILE, 'a', encoding='utf-8') as file:  # Use 'a' mode for appending
                            file.write(f'#EXTINF:-1 tvg-id="{UniqueID}" tvg-name="{channelName}" tvg-logo="{logo}" group-title="USA (DADDY LIVE)", {game["event"]}\n')
                            file.write(f"https://xyzdddd.mizhls.ru/lb/premium{channelID}/index.m3u8\n")
                            file.write('\n')

                        #Creating M3U8 Data
                        xmlChannel      = ET.Element('channel')
                        xmlDisplayName  = ET.Element('display-name')
                        xmlIcon         = ET.Element('icon')

                        xmlChannel.set('id', UniqueID)
                        xmlDisplayName.text = channelName
                        xmlIcon.text = logo

                        xmlChannel.append(xmlDisplayName)
                        xmlChannel.append(xmlIcon)

                        root.append(xmlChannel)

                        #Creating EPG Data
                        programme   = ET.Element('programme')
                        title       = ET.Element('title')
                        desc        = ET.Element('desc')

                        programme.set('start', startTime + " +0000")
                        programme.set('stop', stopTime + " +0000")
                        programme.set('channel', UniqueID)

                        title.text = channelName
                        desc.text = ""

                        programme.append(title)
                        programme.append(desc)

                        root.append(programme)
        except KeyError as e:
            print(f"KeyError: {e} - One of the keys {day} or {section} does not exist.")

unique_ids = generate_unique_ids(NUM_CHANNELS)

fetcher.fetchHTML(DADDY_JSON_FILE, "https://thedaddy.to/schedule/schedule-generated.json")

dadjson = loadJSON(DADDY_JSON_FILE)

if os.path.isfile(M3U8_OUTPUT_FILE):
    os.remove(M3U8_OUTPUT_FILE)

root = ET.Element('tv')

addChannelByTerm("NHL", "Ice Hockey")
addChannelByTerm("NFL", "Am. Football")

tree = ET.ElementTree(root)
tree.write(EPG_OUTPUT_FILE, encoding='utf-8', xml_declaration=True)
import json
import datetime
import requests
import time
from elasticsearch import Elasticsearch
from ssl import create_default_context
import os
import random

PAYLOAD_INPUT = #PLEASE ENTER!!!
ENTRYPOSTHEADER_INPUT = #PLEASE ENTER!!!
NEXTPOSTHEADER_INPUT = #PLEASE ENTER!!!

def elasticsearchConnect():
    """
    Connect to ElasticSearch with environment credentials
    """
    ### Connect to Elasticsearch ###
    try:
        esClient = Elasticsearch(hosts=["0.0.0.0"])
    except Exception as e:
        print('[ERROR][elasticsearchConnector]: Environ "get" error')
        print(e)
        return False
    ### Connection Check Up ###
    if esClient.ping() != True:
        print('[ERROR][elasticsearchConnector]: ElasticSearch "connect" error')
        return False
    return esClient


def format_time_string_to_date(dateNow, timeValue, timeKind):
    if timeKind == "Minute" or timeKind == "Minuten":
        return dateNow
    elif timeKind == "Stunde" or timeKind == "Stunden":
        return dateNow
    elif timeKind == "Tag" or timeKind == "Tagen":
        days = datetime.timedelta(timeValue)
        return dateNow - days
    elif timeKind == "Woche" or timeKind == "Wochen":
        days = datetime.timedelta(timeValue * 7)
        return dateNow - days
    elif timeKind == "Monat" or timeKind == "Monaten":
        days = datetime.timedelta(timeValue * 30.41)
        return dateNow - days
    elif timeKind == "Jahr" or timeKind == "Jahren":
        days = datetime.timedelta(timeValue * 365)
        return dateNow - days


def get_poll(pollIds, polls, postsResponse, esClient):
    dateNow = datetime.date.today()
    for post in postsResponse:
        try:
            pollAnswersText = {}
            pollAnswersVotesInPercent = {}
            post = post["backstagePostThreadRenderer"]["post"]
            post = post[list(post.keys())[0]]
            ### TIME ###
            date = post["publishedTimeText"]["runs"][0]["text"].split()
            if date[0] == "Geteilt:":
                post = post["originalPost"]["backstagePostRenderer"]
                date = post["publishedTimeText"]["runs"][0]["text"].split()
            timeKind = date[2]
            timeValue = int(date[1])
            date = format_time_string_to_date(dateNow, timeValue, timeKind)
            ### --- ###
            channelId = post["authorText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"].replace(
                "/channel/", "")
            pollId = post["postId"]
            if pollId in pollIds:
                continue
            pollQuestion = post["contentText"]["runs"][0]["text"].split("\n")
            pollQuestionCache = ""
            for index, word in enumerate(pollQuestion):
                try:
                    if pollQuestion[index+1] != " ":
                        pollQuestionCache += word+" "
                    else:
                        pollQuestionCache += word
                except:
                    pollQuestionCache += word
            pollQuestion = pollQuestionCache
            ### --- ###
            for count, answer in enumerate(post["backstageAttachment"]["pollRenderer"]["choices"]):
                answerText = answer["text"]["runs"][0]["text"]
                answerVotePercent = answer["voteRatioIfNotSelected"]
                pollAnswersText["answerText_"+str(count+1)] = str(answerText)
                pollAnswersVotesInPercent["answerPercent_"+str(count+1)] = answerVotePercent
            ### --- ###
            likes = int(post["voteCount"]["simpleText"].replace(".", ""))
            totalVotes = int(post["backstageAttachment"]["pollRenderer"]
                             ["totalVotes"]["simpleText"].split("\xa0")[0].replace(".", ""))
            ### --- ### 
            polls.append({"pollId": pollId, "channelId": channelId, "date": date.isoformat(), "likes": likes,
                         "totalVotes": totalVotes, "question": str(pollQuestion), "pollAnswersText": pollAnswersText, "pollAnswersVotesInPercent": pollAnswersVotesInPercent})
            esBody = {"channelId": channelId, "date": date, "likes": likes,
                         "totalVotes": totalVotes, "question": str(pollQuestion), "pollAnswersText": pollAnswersText, "pollAnswersVotesInPercent": pollAnswersVotesInPercent}
            esResp = esClient.index(index="polli", id=pollId, body=esBody)
            if esResp['result'] == "created":
                print(esBody)
            pollIds[pollId] = None
        except KeyError:
            try:
                continuation = post["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
            except KeyError:
                continuation = None
    return continuation

def entry_post_request(channelId, headers):
    response = requests.get("https://www.youtube.com/channel/"+channelId+"/community", headers=headers).content.decode("utf-8")
    response = response.split("var ytInitialData = ")[1]
    response = json.loads(response.split(';</script><link rel="canonical" href="https://www.youtube.com/channel/')[0])
    return response["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][3]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

def request_next_post(payload, headers):
    response = requests.post("https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8", data=json.dumps(payload), headers=headers).json()
    postsResponse = response["onResponseReceivedEndpoints"][0]["appendContinuationItemsAction"]["continuationItems"]
    return postsResponse

def make_payload(channelId, continuation):
    payload = PAYLOAD_INPUT
    return payload

def channel_worker(pollIds, polls, channelId, headers, esClient):
    try:
        postsResponse = entry_post_request(channelId, headers["entryPostHeader"])
        continuation = get_poll(pollIds, polls, postsResponse, esClient)
        print(continuation)
    except:
        continuation = None
    if continuation == None:
            return None
    while True:
        time.sleep(1)
        payload = make_payload(channelId, continuation)
        try:
            postsResponse = request_next_post(payload, headers["nextPostHeader"])
            continuation = get_poll(pollIds, polls, postsResponse, esClient)
        except:
            continuation = None
        if continuation == None:
            break

def make_headers(entryPostHeader,nextPostHeader):
    ### entryPostHeader ###
    headerRawCache = []
    for i in entryPostHeader.split(": "):
        for j in i.split(" | "):
            headerRawCache.append(j)

    entryPostHeader = {}
    lastIndex = 0

    for index in range(2,len(headerRawCache)+1,2):
        data = headerRawCache[lastIndex:index]
        entryPostHeader[data[0]] = data[1]
        lastIndex = index
  
    ### nextPostHeader ###
    headerRawCache = []
    for i in nextPostHeader.split(": "):
        for j in i.split(" | "):
            headerRawCache.append(j)

    nextPostHeader = {}
    lastIndex = 0

    for index in range(2,len(headerRawCache)+1,2):
        data = headerRawCache[lastIndex:index]
        nextPostHeader[data[0]] = data[1]
        lastIndex = index
  
    headers = {}
    headers["entryPostHeader"] = entryPostHeader
    headers["nextPostHeader"] = nextPostHeader

    return headers

def load_channels(fileName):
    with open(fileName, "r") as file:
        return json.load(file)

def export_polls(polls):
    with open("polls_"+str(datetime.datetime.now().isoformat())+".json", "w") as file:
        json.dump({"polls": polls}, file)

def export_poll_ids(pollIds):
    with open("pollIds.json", "w") as file:
        json.dump(pollIds, file)

def main():
    fileName = "channelIds.json"
    esClient = elasticsearchConnect()
    ### ENTRY POINT ###
    entryPostHeader = ENTRYPOSTHEADER_INPUT
    ### NEXT REQUESTS ###
    nextPostHeader = NEXTPOSTHEADER_INPUT
    headers = make_headers(entryPostHeader,nextPostHeader)

    pollIds = {}
    polls = []

    for channelId in load_channels(fileName)["channelIds"]:
        channel_worker(pollIds, polls, channelId, headers, esClient)

    export_polls(polls)
    export_poll_ids(pollIds)

if __name__ == "__main__":
    main()
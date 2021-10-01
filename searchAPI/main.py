from fastapi.responses import JSONResponse
from typing import Optional
import essential
import elasticsearchConnector

### FastAPI and Databases Init ###

app = essential.init()

esClient = elasticsearchConnector.connect()

### Service Functions ###

payload = {
    "query": {
        "function_score": {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "fields": [
                                    "question",
                                    "pollAnswersText.answerText_1",
                                    "pollAnswersText.answerText_2",
                                    "pollAnswersText.answerText_3",
                                    "pollAnswersText.answerText_4",
                                    "pollAnswersText.answerText_5"
                                ]
                            }
                        }
                    ]
                }
            },
            "functions": [
                {
                    "field_value_factor": {
                        "field": "totalVotes",
                    }
                }
            ],
            "boost_mode": "sum"
        }
    }
}


@app.get("/")
async def search(key: str, query: str, channelId: Optional[str] = None, resultsLimit: Optional[int] = 150, totalVotesFactor: Optional[int] = 0):
    if key != "gbdHLPPmHd99FPtS69drSjaFbxhMBhZtyFpkXLHNjNqQs7zssvbpUCRxGUC7XyLx":
        return JSONResponse(content={"results": "KEY ERROR! FUCK YOU!1!!11!!! ..|.."})
    if channelId != None:
        payload["query"]["function_score"]["query"]["bool"]["must"].append(
            {{"match": {"channelId.keyword": channelId}}})
    payload["size"] = resultsLimit
    payload["query"]["function_score"]["functions"][0]["field_value_factor"]["factor"] = totalVotesFactor
    payload["query"]["function_score"]["query"]["bool"]["must"][0]["multi_match"]["query"] = query
    results = esClient.search(index="polli", body=payload)
    return JSONResponse(content={"results": results})

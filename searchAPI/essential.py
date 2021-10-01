from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

### Init essentials ###

def init():
    ### Base init ##timeAndDate#
    app = FastAPI()

    ### CORS ###
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"])
    
    return app
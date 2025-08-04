#
//  main.py
//  OptionCallAgent
//
//  Created by Harsha on 03/08/25.
//

from fastapi import FastAPI
from nse_server import get_options  # assuming you define this

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "OptionCallAgent API is live"}

@app.get("/options")
def read_options():
    return get_options()

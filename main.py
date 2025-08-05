#
#  main.py
#  OptionCallAgent
#
#  Created by Harsha on 03/08/25.
#

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

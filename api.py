import os

import fastapi.responses
import uvicorn
import yaml
from fastapi import FastAPI
app = FastAPI()



@app.get("/pic")
async def root():
    current_path = os.getcwd()
    path = os.path.join(current_path,"output.png")
    return fastapi.responses.FileResponse(path=path,filename="output.png")

@app.get("/")
async def root():
    html_content="""
    <html>
        <body>
            <img src="{}" alt="Image Preview">
        </body>
    </html>""".format("/pic")
    return fastapi.responses.HTMLResponse(content=html_content)

@app.get("/news")
async def news():
    with open("data.yml", 'r',encoding="UTF-8") as stream:
        data = yaml.safe_load(stream)
        t = [[y,n] for n, y in zip(data['news'],data['year'])]
        return {"news": t}

@app.get("/today_ji_yi")
async def today_ji_yi():
    with open("data.yml", 'r',encoding="UTF-8") as stream:
        data = yaml.safe_load(stream)
        return {"today_ji":data['today_ji'],"today_yi":data['today_yi']}

if __name__ == "__main__":
    uvicorn.run("0.0.0.0",port=8090)

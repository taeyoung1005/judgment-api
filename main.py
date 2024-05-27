import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://es01:9200",
    api_key="SjNPS3FvOEJsQTBjRUJSekYzTDQ6OWhZbGtaUG5SUGFiTWhzd09KaFdYQQ==",
    verify_certs=False,
)

app = FastAPI()

data_info = pd.read_csv("data_info.csv", encoding="cp949")


class AccidentTypeRequest(BaseModel):
    accident_type: int


def search_query(search_words: list):
    should = []

    for word in search_words:
        for i in ["사건명", "판례내용", "판시사항", "판결요지", "사건종류명"]:
            should.append({"match": {i: word}})
    query = {
        "query": {"bool": {"should": should}},
        "size": 5,  # Limit to top 5 results for faster response
    }

    response = es.search(index="cases", body=query)

    result = []
    for hit in response["hits"]["hits"]:
        data = hit["_source"]
        data["url"] = (
            f"https://www.law.go.kr/precInfoP.do?mode=0&precSeq={data['판례정보일련번호']}"
        )
        result.append(data)
    return result


@app.post("/judgment")
async def get_judgment(request: AccidentTypeRequest):
    accident_type = request.accident_type
    if accident_type < 0 or accident_type > 434:
        raise HTTPException(
            status_code=400, detail="사고유형은 0 ~ 434 사이의 정수여야 합니다."
        )

    info = data_info[data_info["사고유형"] == accident_type]
    print(info)
    if info.empty:
        raise HTTPException(
            status_code=404, detail="해당 사고 유형의 정보를 찾을 수 없습니다."
        )

    search_terms = [
        info["사고객체"].values[0],
        info["사고장소"].values[0],
        info["사고장소특징"].values[0],
        info["A진행방향"].values[0],
        info["B진행방향"].values[0],
    ]

    judgment_data = search_query(search_terms)

    return JSONResponse(content=judgment_data)

# judgment-api
### 판례 검색 api

법령정보포털 api에서 받은 판례를 elastic search에 저장후 fastapi로 api 서버 구현

```mermaid
graph TD
    A((Start)) --> B([법령정보 API로부터 데이터 가져오기])
    B --> C{데이터 파싱}
    C --> D[(Elasticsearch에 데이터 저장)]
    D --> E{{FastAPI 서버 구현}}
    E --> F[(FastAPI를 통해 Elasticsearch에서 데이터 검색)]
    F --> G((클라이언트에 결과 반환))

    %% 스타일 추가
    style A fill:#f9f,stroke:#333,stroke-width:2px,font-size:10px
    style B fill:#bbf,stroke:#f66,stroke-width:2px,font-size:10px
    style C fill:#fb0,stroke:#333,stroke-width:2px,font-size:10px
    style D fill:#bbf,stroke:#f66,stroke-width:2px,font-size:10px
    style E fill:#fb0,stroke:#333,stroke-width:2px,font-size:10px
    style F fill:#bbf,stroke:#f66,stroke-width:2px,font-size:10px
    style G fill:#f9f,stroke:#333,stroke-width:2px,font-size:10px

    %% 텍스트 스타일 추가
    classDef nodeText fill:#fff,stroke:#000,stroke-width:1px,font-size:10px;
    class A,B,C,D,E,F,G nodeText;

```

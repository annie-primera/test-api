from fastapi import FastAPI, APIRouter, Query
from typing import Optional
from api.schemas import Boss, BossCreate, BossSearchResults

app = FastAPI(
    title="Elden Ring Bosses",
    openapi_url="/openapi.json"
)

api_router = APIRouter()

BOSSES = [
    {
        "id": 1,
        "name": "Morgott",
        "location": "Leyndell"
    },
    {
        "id": 2,
        "name": "Radagon",
        "location": "Erdtree"
    },
    {
        "id": 3,
        "name": "Astel",
        "location": "Lake of Rot"
    }

]


@api_router.get("/", status_code=200)
def root() -> dict:
    """Root Get"""
    return {"msg": "Elden Ring Bosses!"}


@api_router.get("/boss/", status_code=200)
def fetch_boss(*, boss_id: int) -> dict:
    """Fetch a single boss by id"""
    result = [boss for boss in BOSSES if boss["id"] == boss_id]
    if result:
        return result[0]


@api_router.get("/search/", status_code=200, response_model=BossSearchResults)
def search_bosses(
        keyword: Optional[str] = Query(None, min_length=3, exmaple="Morgott"),
        max_results: Optional[int] = 10
) -> dict:
    """Search for bosses based on name"""
    if not keyword:
        return {"results": BOSSES}

    results = filter(lambda boss: keyword.lower() in boss["name"].lower(), BOSSES)
    return {"results": list(results)}


@api_router.post("/boss/", status_code=201, response_model=Boss)
def create_boss(*, boss_in: BossCreate) -> dict:
    """ Create a new boss (in memory only) """
    new_boss_id = len(BOSSES) + 1
    boss_entry = Boss(
        id=new_boss_id,
        name=boss_in.name,
        location=boss_in.location,
    )
    BOSSES.append(boss_entry.dict())
    return boss_entry.dict()


@api_router.get("/health/", status_code=200)
def health_check():
    return "Healthy!"


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="debug")

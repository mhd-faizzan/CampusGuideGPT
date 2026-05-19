import logging
import fcntl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel

from config.settings import RATE_LIMIT, DAILY_LIMIT, ALLOWED_ORIGINS, STATS_SECRET
from services.embedding import encode
from services.vector_db import VectorService
from services.llm_service import LLMService
from utils.prompt_builder import build_prompt
from utils.rate_tracker import is_limit_reached, increment, _load
from utils.sanitizer import sanitize

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="CampusGuideGPT API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectors = VectorService()
llm     = LLMService()


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def stats(secret: str = ""):
    if secret != STATS_SECRET:
        return JSONResponse(status_code=403, content={"error": "forbidden"})
    with open("usage_counter.json", "a+") as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        f.seek(0)
        data = _load(f)
        fcntl.flock(f, fcntl.LOCK_UN)
    return {
        "date":           data["date"],
        "requests_today": data["count"],
        "daily_limit":    DAILY_LIMIT,
        "remaining":      max(0, DAILY_LIMIT - data["count"]),
    }


@app.post("/ask")
@limiter.limit(RATE_LIMIT)
async def ask(request: Request, body: QueryRequest):

    is_valid, result = sanitize(body.question)
    if not is_valid:
        return JSONResponse(status_code=400, content={"error": result})

    question = result

    if is_limit_reached(DAILY_LIMIT):
        logger.warning("daily limit reached")
        return JSONResponse(
            status_code=429,
            content={"error": "daily limit reached, come back tomorrow."}
        )

    try:
        vector = encode(question)
        hits   = vectors.search(vector)
        prompt = build_prompt(question, hits)
        answer = llm.complete(prompt)

        if not answer:
            return JSONResponse(status_code=500, content={"error": "no response from llm"})

        increment()

        return {"answer": answer, "sources": hits}

    except Exception as e:
        logger.error("error in /ask: %s", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
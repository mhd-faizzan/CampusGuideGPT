import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel

from config.settings import RATE_LIMIT, DAILY_LIMIT
from services.embedding import encode
from services.vector_db import VectorService
from services.llm_service import LLMService
from utils.prompt_builder import build_prompt
from utils.rate_tracker import is_limit_reached, increment

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
    allow_origins=["*"],
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


@app.post("/ask")
@limiter.limit(RATE_LIMIT)
async def ask(request: Request, body: QueryRequest):
    question = body.question.strip()

    if not question:
        return JSONResponse(status_code=400, content={"error": "question is empty"})

    # check global daily limit
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

        # only increment on successful response
        increment()

        return {"answer": answer, "sources": hits}

    except Exception as e:
        logger.error("error in /ask: %s", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
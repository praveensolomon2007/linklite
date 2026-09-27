from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import secrets
import string

app = FastAPI(title="LinkLite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

links = {}


class URLRequest(BaseModel):
    url: str


def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


@app.get("/")
def home():
    return {"message": "LinkLite API is running"}


@app.post("/api/shorten")
def shorten_url(request: URLRequest):
    code = generate_code()

    while code in links:
        code = generate_code()

    links[code] = {
        "original_url": request.url,
        "clicks": 0
    }

    return {
        "short_code": code,
        "short_url": f"http://127.0.0.1:8000/{code}"
    }


@app.get("/{code}")
def redirect_url(code: str):
    from fastapi.responses import RedirectResponse

    if code not in links:
        return {"error": "Short URL not found"}

    links[code]["clicks"] += 1

    return RedirectResponse(
        url=links[code]["original_url"]
    )


@app.get("/api/stats/{code}")
def get_stats(code: str):
    if code not in links:
        return {"error": "Short URL not found"}

    return links[code]
import os
import httpx
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv

load_dotenv()

API_KEY = "USE SCRAPE CREATOR API"
BASE_URL = "https://api.scrapecreators.com/v1/linkedin/search/posts"

if not API_KEY:
    raise RuntimeError("SCRAPE_CREATORS_API_KEY is missing in environment variables")

app = FastAPI(title="LinkedIn Keyword Posts API")


def match_keyword(text: str, keyword: str) -> bool:
    """Simple safe keyword matcher (case-insensitive)."""
    return keyword.lower() in (text or "").lower()


@app.get("/linkedin/posts")
async def get_linkedin_posts(
    keyword: str = Query(..., description="Keyword to search in LinkedIn posts"),
    max_posts: int = Query(10, ge=1, le=100, description="Max posts to return"),
):
    headers = {
        "x-api-key": API_KEY
    }

    results = []
    cursor: Optional[str] = None

    try:
        async with httpx.AsyncClient(timeout=30) as client:

            while len(results) < max_posts:
                params = {
                    "query": keyword,
                    "date_posted": "last-year"
                }

                if cursor:
                    params["cursor"] = cursor

                response = await client.get(
                    BASE_URL,
                    headers=headers,
                    params=params
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"API request failed: {response.text}"
                    )

                data = response.json()

                if not data.get("success"):
                    raise HTTPException(
                        status_code=500,
                        detail="API returned unsuccessful response"
                    )

                posts = data.get("posts", [])
                cursor = data.get("cursor")

                # Filter posts by keyword match in description
                for post in posts:
                    description = post.get("description", "")

                    if match_keyword(description, keyword):
                        results.append({
                            "url": post.get("url"),
                            "date": post.get("datePublished"),
                            "description": description,
                            "author": post.get("author", {}).get("name"),
                            "image": post.get("image"),
                        })

                    if len(results) >= max_posts:
                        break

                # Stop if no more pages
                if not cursor:
                    break

        return {
            "keyword": keyword,
            "count": len(results),
            "posts": results
        }

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Network error while calling API: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
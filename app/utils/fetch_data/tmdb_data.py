import json

import requests
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from typing import Callable

from app.config.redis import redis_client
from app.constants.envs import envs


# IMAGE_BASE_URL = "https://image.tmdb.org/t/p/<w200 | w500 | original>/<path>"

CACHE_EXPIRATION = 60 * 60 * 5  # 1 hour

def fetch_TMDB_data(url: str, params: dict = None):
    """
    Fetches data from TMDB API with optional parameters.
    """
    try:
        params = params or {}
        params = {**params, "api_key": envs.TMDB_API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("TMDB ERROR:", str(e))
        raise HTTPException(status_code=500, detail='Error occured while fetching data.')

def fetch_cached_data(cache_key: str, url: str, params: dict = None):
    """
    Fetches data from cache if available, otherwise calls fetch_func to retrieve it.
    """
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data), True  # Returning True to indicate cache hit

    # Cache miss, fetch data using fetch_func
    data = fetch_TMDB_data(url=url, params=params)
    if isinstance(data, HTTPException):
        return data, False  # Propagate the HTTPException if fetch_func returns it

    # Store data in cache
    redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(data))
    return data, False  # Returning False to indicate cache miss

def get_cached_response(cache_key: str, url: str, params: dict = None) -> JSONResponse:
    """
    Retrieves cached data or fetches it if not available, returning a JSONResponse.
    """
    data, is_cache_hit = fetch_cached_data(cache_key, url, params)

    if isinstance(data, HTTPException):
        raise data  # Propagate the HTTPException if fetch_func returns it

    cache_status = "HIT" if is_cache_hit else "MISS"
    return JSONResponse(content=data, headers={"X-Cache": cache_status})

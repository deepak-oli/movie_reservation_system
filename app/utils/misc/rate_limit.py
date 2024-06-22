from fastapi import  Request, HTTPException,status
from functools import wraps
from typing import Callable


from app.config.redis import redis_client

DEFAULT_RATE_LIMIT = 5  # Number of requests
DEFAULT_RATE_LIMIT_WINDOW = 60  # Time window in seconds

async def rate_limit(request: Request, rate_limit_count: int = DEFAULT_RATE_LIMIT, rate_limit_window: int = DEFAULT_RATE_LIMIT_WINDOW):
    client_ip = request.client.host
    endpoint = request.url.path
    redis_key = f"ratelimit:{client_ip}:{endpoint}"

    request_count = redis_client.get(redis_key)
    if request_count is None:
        redis_client.setex(redis_key, rate_limit_window, 1)
    else:
        if int(request_count) >= rate_limit_count:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
                detail="Rate limit exceeded. Try again later after 1 minute."
            )
        redis_client.incr(redis_key)

def rate_limiter(rate_limit_count: int = DEFAULT_RATE_LIMIT, rate_limit_window: int = DEFAULT_RATE_LIMIT_WINDOW):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            await rate_limit(request, rate_limit_count, rate_limit_window)
            return func(request=request, *args, **kwargs)
        return wrapper
    return decorator
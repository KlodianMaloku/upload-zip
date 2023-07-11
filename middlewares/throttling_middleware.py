import redis
from fastapi import HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from settings import REDIS_URL, THROTTLE_LIMIT_PER_MINUTE

client = redis.Redis.from_url(REDIS_URL)

def limiter(key):
    limit = int(THROTTLE_LIMIT_PER_MINUTE)
    req = client.incr(key)
    print("Total number of requests remaining: ", limit - req)
    if req == 1:
        client.expire(key, 60)
        ttl = 60
    else:
        ttl = client.ttl(key)
    if req > limit:
        return {
            "call": False,
            "ttl": ttl
        }
    else:
        return {
            "call": True,
            "ttl": ttl
        }

class ThrottlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next ):
        client_ip = request.client.host
        res = limiter(client_ip)
        if res["call"]:
            response = await call_next(request)
            return response
        else:
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={
                "message": "call limit reached",
                "ttl": res["ttl"]
            })
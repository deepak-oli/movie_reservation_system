import redis

from app.constants.envs import envs

redis_client = redis.Redis(
    host=envs.REDIS_HOST,
    port=envs.REDIS_PORT,
    db=envs.REDIS_DB,
    password=envs.REDIS_PASSWORD,
    decode_responses=True,
    ssl=False  # Enable SSL if necessary
)

def get_redis_client():
    return redis_client

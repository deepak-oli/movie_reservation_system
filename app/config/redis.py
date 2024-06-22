from redis import Redis
from redis.exceptions import ConnectionError, RedisError

from app.constants.envs import envs


def create_redis_client():
    try:
        client = Redis(
            host=envs.REDIS_HOST,
            port=envs.REDIS_PORT,
            db=envs.REDIS_DB,
            password=envs.REDIS_PASSWORD,
            decode_responses=True,
            ssl=False  # Enable SSL if necessary
        )

        # Check if the redis server is running
        if not client.ping():
            raise Exception("Could not connect to Redis server.")
        
        return client
    except (ConnectionError, RedisError) as e:
        raise RuntimeError(f"Failed to connect to Redis: {e}")


# Create the Redis client
redis_client = create_redis_client()

def get_redis_client():
    return redis_client

def verify_redis_connection():
    try:
        _ = redis_client.ping()
        return True
    except:
        return False
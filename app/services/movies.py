from app.config.redis import redis_client
from app.constants.envs import envs
from app.utils.fetch_data.tmdb_data import get_cached_response


CACHE_EXPIRATION = 60 * 60 * 5  # 1 hour
API_URL = envs.TMDB_API_BASE_URL



def get_now_playing_movies(page:int = 1):
    url = f"{API_URL}/movie/now_playing"
    cache_key = f"now_playing:{page}"
    params={"page": page}
    return get_cached_response(cache_key=cache_key, url=url, params=params)

def get_popular_movies(page:int = 1):
    url = f"{API_URL}/movie/popular"
    cache_key = f"popular:{page}"
    params={"page": page}
    return get_cached_response(cache_key=cache_key, url=url, params=params)

def get_top_rated_movies(page:int = 1):
    url = f"{API_URL}/movie/top_rated"
    cache_key = f"top_rated:{page}"
    params={"page": page}
    return get_cached_response(cache_key=cache_key, url=url, params=params)

def get_upcoming_movies(page:int = 1):
    url = f"{API_URL}/movie/upcoming"
    cache_key = f"upcoming:{page}"
    params={"page": page}
    return get_cached_response(cache_key=cache_key, url=url, params=params)

def get_movie_details(movie_id:int):
    url = f"{API_URL}/movie/{movie_id}"
    cache_key = f"movie:{movie_id}"
    return get_cached_response(cache_key=cache_key, url=url)

def get_cast_and_crew(movie_id:int):
    url = f"{API_URL}/movie/{movie_id}/credits"
    cache_key = f"movie:{movie_id}:credits"
    return get_cached_response(cache_key=cache_key, url=url)

def get_movie_keywords(movie_id:int):
    url = f"{API_URL}/movie/{movie_id}/keywords"
    cache_key = f"movie:{movie_id}:keywords"
    return get_cached_response(cache_key=cache_key, url=url)

def get_movie_recommendations(movie_id:int, page:int = 1):
    url = f"{API_URL}/movie/{movie_id}/recommendations"
    cache_key = f"movie:{movie_id}:recommendations:{page}"
    params={"page": page}
    return get_cached_response(cache_key=cache_key, url=url, params=params)

def get_similar_movies(movie_id:int, page:int = 1):
    url = f"{API_URL}/movie/{movie_id}/similar"
    cache_key = f"movie:{movie_id}:similar:{page}"
    params={"page": page}
    return get_cached_response(cache_key=cache_key, url=url, params=params)

def search_movies(query:str, page:int = 1):
    url = f"{API_URL}/search/movie"
    cache_key = f"search_movie:{query}:{page}"
    params={"query": query, "page": page}
    return get_cached_response(cache_key=cache_key, url=url, params=params)

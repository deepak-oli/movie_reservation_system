from fastapi import APIRouter

from app.services import movies as services

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get('/now-playing')
def now_playing(page:int = 1):
    return services.get_now_playing_movies(page)

@router.get('/popular')
def popular(page:int = 1):
    return services.get_popular_movies(page)

@router.get('/top-rated')
def top_rated(page:int = 1):
    return services.get_top_rated_movies(page)

@router.get('/upcoming')
def upcoming(page:int = 1):
    return services.get_upcoming_movies(page)

@router.get('/search')
def search_movies(query:str, page:int = 1):
    return services.search_movies(query, page)

@router.get('/{movie_id}')
def movie_details(movie_id:int):
    return services.get_movie_details(movie_id)

@router.get('/{movie_id}/credits')
def cast_and_crew(movie_id:int):
    return services.get_cast_and_crew(movie_id)

@router.get('/{movie_id}/keywords')
def movie_keywords(movie_id:int):
    return services.get_movie_keywords(movie_id)

@router.get('/{movie_id}/recommendations')
def movie_recommendations(movie_id:int, page:int = 1):
    return services.get_movie_recommendations(movie_id, page)

@router.get('/{movie_id}/similar')
def similar_movies(movie_id:int, page:int = 1):
    return services.get_similar_movies(movie_id, page)



"""
Genre service for handling business logic
"""

import json

from app.logging.logging_constants import LOGGING_GENRE_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import Genre, GenreServiceException

genre_service_logger = SpotifyElectronLogger(LOGGING_GENRE_SERVICE).getLogger()


def get_genres() -> str:
    """Returns all available genres as a JSON string.

    Returns:
        A JSON string containing all genre names and values.

    Raises:
        UnexpectedGenreServiceError: If an error occurs while getting genres.
    """
    try:
        genre_dict = {}
        for genre in Genre:
            genre_dict[genre.name] = genre.value
        genres_json = json.dumps(genre_dict)
    except Exception as exception:
        genre_service_logger.exception("Unexpected error getting genres")
        raise GenreServiceException from exception
    else:
        genre_service_logger.info(f"Obtained genres: {genres_json}")
        return genres_json

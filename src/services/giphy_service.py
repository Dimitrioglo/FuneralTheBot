import httpx

from exceptions.giphy_api_erorr import GiphyAPIError, GiphyNotFound
from ioc.logging_container import LoggingContainer


GIPHY_API_URL = "https://api.giphy.com/v1/gifs/random"
GIPHY_SEARCH_URL = "https://api.giphy.com/v1/gifs/search"


logger = LoggingContainer.logger()


class GiphyService:
    """Service for interacting with the Giphy API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = GIPHY_API_URL,
        search_url=GIPHY_SEARCH_URL,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.search_url = search_url

    async def fetch_random_gif(self) -> str:
        """Fetch a random GIF URL from the Giphy API"""
        params = {"api_key": self.api_key}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
            except httpx.HTTPError as error:
                logger.error("HTTP error while calling Giphy API: %s", error)
                raise GiphyAPIError(
                    f"Giphy API request failed: {error!s}"
                ) from error

            try:
                data = response.json()
                gif_url = (
                    data.get("data", {})
                    .get("images", {})
                    .get("original", {})
                    .get("url")
                )
                if not gif_url:
                    raise GiphyNotFound(
                        "GIF URL not found in Giphy API response"
                    )
                return gif_url
            except GiphyNotFound as error:
                raise error
            except Exception as error:
                logger.error("Error parsing Giphy API response: %s", error)
                raise GiphyAPIError(
                    "Unexpected response structure from Giphy API"
                ) from error

    async def search_gif(self, query: str, limit: int = 3) -> list[str]:
        """Search GIFs by query and return a list of URLs"""
        params = {
            "api_key": self.api_key,
            "q": query,
            "limit": limit,
            "offset": 0,
            "rating": "g",
            "lang": "ru",
        }
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f'Searhing word: {query}')
                response = await client.get(self.search_url, params=params)
                response.raise_for_status()
                data = response.json()
                gifs = [
                    gif.get("images", {}).get("original", {}).get("url")
                    for gif in data.get("data", [])
                    if gif.get("images", {}).get("original", {}).get("url")
                ]
                if not gifs:
                    logger.warning("No GIFs found for query: %s", query)
                    raise GiphyNotFound(
                        "GIF URL not found in Giphy API response"
                    )
                return gifs[1]
            except GiphyNotFound as error:
                raise error
            except httpx.HTTPError as error:
                logger.error("HTTP error while searching Giphy API: %s", error)
                raise GiphyAPIError(
                    f"Giphy API search request failed: {error!s}"
                ) from error
            except Exception as error:
                logger.error(
                    "Error parsing Giphy API search response: %s", error
                )
                raise GiphyAPIError(
                    "Unexpected response structure from Giphy API search"
                ) from error

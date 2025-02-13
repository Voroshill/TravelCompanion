import os
import httpx
from app.error_handling import handle_http_error, handle_request_error, handle_unexpected_error


async def places_from_api(location: str, category: str):
    search_query = f'{category} in {location}'

    url = os.getenv("BASE_URL")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not url or not google_api_key:
        raise ValueError("BASE_URL or GOOGLE_API_KEY not set in environment variables.")

    params = {
        "query": search_query,
        "key": google_api_key
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json().get("results", [])
    except httpx.HTTPStatusError as e:
        return handle_http_error(e)
    except httpx.RequestError as e:
        return handle_request_error(e)
    except Exception as e:
        return handle_unexpected_error(e)


def returning_places(result, category=None):
    places = [{"name": place["name"], "location": place["formatted_address"],
               "types": place.get("types", [])} for place
              in result]

    if category:
        places = [place for place in places if category in place['types']]

    return places

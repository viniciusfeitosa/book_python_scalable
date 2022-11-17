import httpx
from pprint import pprint
import timeit
import asyncio

PLANET_URL = 'https://swapi.dev/api/planets/?format=json'


async def get_planets(client: httpx.AsyncClient, page_url: str) -> list:
    planets = list()
    while page_url:
        resp = await client.get(page_url)
        raw_data = resp.json()
        page_url = raw_data.get('next')
        planets += raw_data.get('results')
    return planets


async def get_hab_name(client: httpx.AsyncClient, url: str) -> str:
    resp = await client.get(url)
    return resp.json().get('name')


async def get_habs_per_planet() -> dict:
    habs_per_planet = dict()
    async with httpx.AsyncClient() as client:
        planets = await get_planets(client, PLANET_URL)
        for planet_info in planets:
            planet_name = planet_info.get('name')
            print(f"collecting data from: {planet_name}")
            tasks = [
                asyncio.ensure_future(get_hab_name(client, resident_url))
                for resident_url in planet_info['residents']
            ]
            habs_per_planet[planet_name] = await asyncio.gather(*tasks)
    pprint(habs_per_planet)
    return habs_per_planet


if __name__ == '__main__':
    starttime = timeit.default_timer()
    print("The start time is:", starttime)
    asyncio.run(get_habs_per_planet())
    print("The time difference is :", timeit.default_timer() - starttime)

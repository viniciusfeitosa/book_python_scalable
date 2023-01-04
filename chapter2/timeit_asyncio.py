import httpx
from pprint import pprint
import timeit
import asyncio


async def get_planets(
    client: httpx.AsyncClient,
    page_url: str
) -> list:
    resp = await client.get(page_url)
    return resp.json().get('results')


async def get_hab_name(client: httpx.AsyncClient, url: str) -> str:
    resp = await client.get(url)
    return resp.json().get('name')


async def get_habs_per_planet() -> dict:
    habs_per_planet = dict()
    planets = list()
    async with httpx.AsyncClient() as client:
        print('get all planets')
        planet_tasks = [
            asyncio.ensure_future(get_planets(
                client=client,
                page_url=f"https://swapi.dev/api/planets/?page={i}&format=json"
            ))
            for i in range(1, 7)
        ]
        for results in await asyncio.gather(*planet_tasks):
            planets += results

        for planet_info in planets:
            planet_name = planet_info.get('name')
            print(f"collecting data from: {planet_name}")
            hab_tasks = [
                asyncio.ensure_future(get_hab_name(client, resident_url))
                for resident_url in planet_info['residents']
            ]
            habs_per_planet[planet_name] = await asyncio.gather(*hab_tasks)
    pprint(habs_per_planet)
    return habs_per_planet


if __name__ == '__main__':
    starttime = timeit.default_timer()
    print("The start time is:", starttime)
    asyncio.run(get_habs_per_planet())
    print("The time difference is :", timeit.default_timer() - starttime)

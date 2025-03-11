import os
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()

api_key = os.getenv("API_KEY")

list = open("cleanedlist.txt")


async def search(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={api_key}"
        ) as response:
            result_json = await response.json()
            if "items" in result_json and result_json["items"]:
                id = result_json["items"][0]["id"]["videoId"]
                print(id)
                return id
            else:
                print("error")
                return None


async def main():
    id_list = ""

    for index, i in enumerate(list):

        link = await (search(i))
        if link:

            if index == 0:
                id_list += f"{link}"
            else:
                id_list += f"\n{link}"


asyncio.run(main())

list.close()

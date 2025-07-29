from typing import Dict, Any, List, Optional
import requests
import aiohttp
import asyncio

class HTTPHandler:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def sync_get(self, url: str, params: Dict[str, Any] = None) -> requests.Response:
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during sync GET request: {e}")
            return None

    def sync_post(self, url: str, data: Dict[str, Any]) -> requests.Response:
        try:
            response = requests.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during sync POST request: {e}")
            return None

    async def async_get(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=self.timeout) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"Error during async GET request: {e}")
                return {}

    async def async_post(self, url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.post(url, json=data, timeout=self.timeout) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"Error during async POST request: {e}")
                return {}

    async def async_request_all(self, urls: List[str]) -> List[Dict[str, Any]]:
        tasks = [self.async_get(url) for url in urls]
        return await asyncio.gather(*tasks)

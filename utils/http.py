

import asyncio
import logging
log = logging.getLogger(__name__)

class AioClient:
	"""Client for interacting with HTTP"""
	def __init__(self, *, user_agent=None, session=None, loop=None):
		import aiohttp
		from utils.loop import get as get_event_loop
		self.__session__ = session or aiohttp.ClientSession(loop=loop or get_event_loop())
		self.headers = {'User-Agent': user_agent or f'XXX 0.0.1 (github.com/YYY/WWW) aiohttp/{aiohttp.__version__}'}
	async def __aenter__(self):
		return self
	async def __aexit__(self, *args):
		return await self.__session__.close()
	async def request(self, method, url, json=False, *, encoding='utf-8', chunk_size=512, max_tries=5, **kwargs):
		import aiohttp
		import asyncio
		import io
		from json.decoder import JSONDecodeError
		if self.__session__.closed:
			self.__session__ = aiohttp.ClientSession()#connector=self.connector)
		for _ in range(max_tries):#reversed(range(max_tries))
			try:
				async with self.__session__.request(method, url, **kwargs) as r:
					#log.debug(f'{r.method} [{r.url}] {r.status}/{r.reason}')
					#r.headers.get('Content-Type', '').startswith('application') and r.headers.get('Content-Type', '').rfind('json')
					if json or r.headers['Content-Type'] == 'application/json':
						try:
							return await r.json()
						except (JSONDecodeError, ValueError, aiohttp.ContentTypeError):
							return await resp.text(encoding=encoding)
					buffer = io.BytesIO()
					async for chunk in r.content.iter_chunked(chunk_size):
						if chunk:
							buffer.write(chunk)
					if buffer:
						return buffer
					return r.content
			except (aiohttp.ServerDisconnectedError, asyncio.TimeoutError) as exc:
				await asyncio.sleep(_)

	async def get(self, url, *, headers={}, json=False, encoding='utf-8', chunk_size=512, max_tries=5, **kwargs):
		"""Make a GET request

		Params
		------
		url : str
			The URL to make the request to
		headers : dict
			Additional headers to send with the request
		json : bool
			Force returning as JSON
		Returns
		-------
		dict [or str]
			If result was not JSON, returns str
		"""
		return await self.request('GET', url, headers={**self.headers, **headers}, json=json, encoding=encoding, chunk_size=chunk_size, max_tries=max_tries, **kwargs)

class Client:
	def __init__(self, *, is_async=False, user_agent=None, session=None, loop=asyncio.get_event_loop()):
		import requests
		self.__session__ = session or requests.Session()
		self.headers = {'User-Agent': user_agent or f'XXX 0.0.1 (github.com/YYY/WWW) requests/{requests.__version__}'}
	def __enter__(self):
		return self
	def __exit__(self, *args):
		return self.__session__.close()
	def request(self, method, url, json=False, *, chunk_size=512, max_tries=5, stream=False, **kwargs):
		"""Makes a HTTP request: DO NOT call this function yourself - use provided methods"""
		from json.decoder import JSONDecodeError
		import io
		import time
		import requests
		for _ in range(max_tries):
			try:
				with self.__session__.request(method, url, stream=stream, **kwargs) as r:
					if json or r.headers['Content-Type'] == 'application/json':
						try:
							return r.json()
						except (JSONDecodeError, ValueError):
							return r.text
					buffer = io.BytesIO()
					for chunk in r.iter_content(chunk_size=chunk_size):
						if chunk:
							buffer.write(chunk)
					if buffer:
						return buffer
					return r.context #r.text
			except (requests.exceptions.ConnectionError) as exc:
				time.sleep(_)

	def get(self, url, *, headers={}, json=False, chunk_size=512, max_tries=5, stream=False, **kwargs):
		return self.request('GET', url, headers={**self.headers, **headers}, json=json, chunk_size=chunk_size, max_tries=max_tries, stream=stream, **kwargs)

def get_url(url, as_json=True, is_async=False):
	'''
	import requests
	for _ in range(5):
		try:
			r = requests.get(url)
			if as_json:
				from json.decoder import JSONDecodeError
				try:
					return r.json()
				except (JSONDecodeError, ValueError):
					pass
			return r.text
		except requests.exceptions.ConnectionError:
			import time
			time.sleep(_)
	return None
	'''
	if is_async:
		async def __get_url__(url, as_json=True):
			async with AioClient() as r:
				return  await r.get(url, json=as_json)
		return __get_url__
	with Client() as r:
		return r.get(url, json=as_json)
	

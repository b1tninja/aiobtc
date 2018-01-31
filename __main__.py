import asyncio
from pprint import pprint

from __init__ import Node

loop = asyncio.get_event_loop()

node = Node()

initial_peers = loop.run_until_complete(node.resolve_seeds())
pprint(initial_peers)

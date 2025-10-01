from redis import Redis
from rq import Queue

reddis_collection = Redis(
    host='valkey',
    port = '6379'
)

q = Queue(connection= reddis_collection)
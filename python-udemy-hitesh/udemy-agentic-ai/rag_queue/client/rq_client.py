from redis import Redis
from rq import Queue

connection = Redis(
    host="localhost",
    port=6379
)
queue = Queue(connection=connection)

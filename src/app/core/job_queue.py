from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

redis_conn = Redis(host="redis", port=6379)
q = Queue(connection=redis_conn)
scheduler = Scheduler(connection=redis_conn)

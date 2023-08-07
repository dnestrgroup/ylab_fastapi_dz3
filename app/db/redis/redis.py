import redis

redis_client = redis.Redis(host="first_app_redis", port=6378, db=0)
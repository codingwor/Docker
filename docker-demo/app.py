from flask import Flask
import redis
import os

# Create Flask app instance
app = Flask(__name__)

# Connect to Redis. Hostname 'redis' = the service name in docker-compose.yml
# Docker's internal DNS resolves 'redis' to that container's IP automatically
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            # incr() atomically increments key 'hits' by 1 and returns new value
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            import time
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello! This page has been viewed {count} times.\n'


if __name__ == "__main__":
    # 0.0.0.0 = listen on all network interfaces (required so Docker can expose it)
    # If you used 127.0.0.1, it would only be reachable INSIDE the container
    app.run(host="0.0.0.0", port=5000, debug=True)

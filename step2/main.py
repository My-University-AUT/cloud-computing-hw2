# compose_flask/app.py
from flask import Flask
from redis import Redis
import os
import requests
import sys

REDIS_PORT=int(os.getenv("REDIS_PORT"))
REDIS_HOST=os.getenv("REDIS_HOST")
FLASK_PORT=int(os.getenv("FLASK_PORT"))
FLASK_HOST=os.getenv("FLASK_HOST")
COIN_NAME=os.getenv("COIN_NAME")
API_KEY=os.getenv("API_KEY")
COIN_URL=os.getenv("COIN_URL")
REDIS_TTL_SECS=int(os.getenv("REDIS_TTL_SECS"))

def callService():
    url = COIN_URL
    headers = {'X-CoinAPI-Key' : API_KEY}
    response = requests.get(url, headers=headers)
    app.logger.debug(response.json()[0])
    foundItem = next((item for item in response.json() if item["name"] == COIN_NAME), {"name":"not_founded_coin", "current_price":"999"})

    return foundItem['price_usd']

print("here are my envs", REDIS_HOST, REDIS_PORT, FLASK_PORT, FLASK_HOST, COIN_NAME)

app = Flask(__name__)
redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
print("here is redis", redis)

@app.route('/')
def hello():
    app.logger.debug(" i got request")
    # coinPrice = callService()
    redis.incr('hits')
    coinPrice = redis.get(COIN_NAME)
    if not coinPrice:
        app.logger.debug("not found in redis")
        coinPrice = callService()
        # ttl unit in seconds
        redis.set(COIN_NAME, coinPrice, REDIS_TTL_SECS)
    else:
        app.logger.debug("found in redis")
    return f'coin: {COIN_NAME} price: {coinPrice}'


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
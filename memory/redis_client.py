import redis
import json
from config import Config

class RedisClient:
    def __init__(self):
        self.use_mock = False
        self.mock_storage = {}
        try:
            self.client = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                db=Config.REDIS_DB,
                decode_responses=True
            )
            self.client.ping()
        except redis.ConnectionError:
            print("⚠️ Redis connection failed. Using in-memory mock.")
            self.use_mock = True

    def store_discussion(self, ticker, discussion_data):
        """Stores the discussion log for a specific ticker with 1 hour expiry."""
        if self.use_mock:
            self.mock_storage[f"discussion:{ticker}"] = json.dumps(discussion_data)
            return
            
        key = f"discussion:{ticker}"
        try:
            self.client.setex(key, 3600, json.dumps(discussion_data))
        except redis.ConnectionError:
            self.use_mock = True
            self.mock_storage[key] = json.dumps(discussion_data)

    def get_discussion(self, ticker):
        """Retrieves the recent discussion for a ticker."""
        key = f"discussion:{ticker}"
        if self.use_mock:
            data = self.mock_storage.get(key)
            return json.loads(data) if data else None
            
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except redis.ConnectionError:
            self.use_mock = True
            data = self.mock_storage.get(key)
            return json.loads(data) if data else None

    def check_connection(self):
        if self.use_mock:
            return False
        try:
            return self.client.ping()
        except redis.ConnectionError:
            return False

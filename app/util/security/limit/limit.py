from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


_limiter = Limiter(key_func=get_remote_address,
                default_limits=["100/minute", "2000/hour"],
                headers_enabled=True, storage_uri='memory://',
                strategy='fixed-window')
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(key_func=get_remote_address,
                default_limits=["3/minute", "10/hour"],
                headers_enabled=True, storage_uri='memory://',
                strategy='fixed-window')
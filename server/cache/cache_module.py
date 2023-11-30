from flask_caching import Cache
# module for Flask cache setup

cache = Cache(config={'CACHE_TYPE': 'simple'})

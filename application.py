from app import create_app

application = create_app()

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(application,
                  key_func=get_remote_address) 

if __name__ == "__main__":
    application.run()

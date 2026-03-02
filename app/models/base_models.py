from datetime import datetime
import pytz
from pydantic import Field

def get_colombia_time():
    return datetime.now(pytz.timezone('America/Bogota'))

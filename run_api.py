import uvicorn
from api import api

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:api", host="localhost", port=8000, reload=True)
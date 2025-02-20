from fastapi import FastAPI

from spaces.common import MAX_REQUEST_BODY_SIZE
from spaces.routes import router_spaces, router_auth

app = FastAPI(max_request_body_size=MAX_REQUEST_BODY_SIZE)

app.include_router(router_spaces, prefix="/spaces", tags=["Spaces"])
app.include_router(router_auth, prefix="/auth", tags=["Authentication"])

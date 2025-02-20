from typing import Literal
from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse

from spaces.deps import GitAuthentication
from spaces.common import MAX_REQUEST_BODY_SIZE

from enum import Enum

router = APIRouter()

GitServicePack = Literal["git-receive-pack", "git-upload-pack"]


@router.post("/init")
def git_init(): ...


@router.get("/{path}/info/refs")
async def git_info(path: str, service: GitServicePack):
    ...
    # path = Path(TEMPDIR.name, path)

    # # Create repo if does does not exist
    # repo = Git(path) if path.exists() else Git.init(path)

    # # Fetch inforefs
    # data = repo.inforefs(service.value)

    # media = f'application/x-{service.value}-advertisement'
    # return StreamingResponse(data, media_type=media)


@router.post("/{path}/{service}")
async def git_packet_service(
    path: str, service: GitServicePack, req: Request, access: GitAuthentication
):
    if (
        req.headers.get("Content-Length")
        and int(req.headers["Content-Length"]) > MAX_REQUEST_BODY_SIZE
    ):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Request body too large",
        )
    ...
    # path = Path(TEMPDIR.name, path)
    # repo = Git(path)

    # # Load data to memory (be careful with huge repos)
    # stream = req.stream()
    # data = [data async for data in stream]
    # data = b''.join(data)

    # # Load service data
    # data = repo.service(service.value, data)

    # media = f'application/x-{service.value}-result'
    # return StreamingResponse(data, media_type=media)

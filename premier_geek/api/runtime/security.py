import cognitojwt

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from runtime.settings import settings
from starlette import status


security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    id_token = credentials.credentials
    try:
        id_token = credentials.credentials
        cognitojwt.decode(id_token, settings.aws_region, settings.user_pool_id, settings.user_pool_client_id)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.") from e
    return True

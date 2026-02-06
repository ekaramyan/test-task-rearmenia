from functools import wraps
import traceback

from fastapi import HTTPException, Response
from views.database.users import User
from views.json.unifided import UnifidedResponse
from fastapi.responses import JSONResponse


def unifided_request(func):

    @wraps(func)
    async def wrapper(_response: Response, *args, **kwargs):

        unifided_resp: UnifidedResponse = UnifidedResponse()

        try:
            result = await func(_response, *args, **kwargs)
            unifided_resp.data = result

        except Exception as e:

            unifided_resp.is_success = False

            if isinstance(e, HTTPException):
                _response.status_code = e.status_code
                unifided_resp.message = e.detail
                unifided_resp = JSONResponse(
                    content=unifided_resp,
                    status_code=e.status_code)
                traceback.print_exc()

            else:
                traceback.print_exc()

        finally:
            return unifided_resp

    return wrapper


def role_secure(roles: list[str] = []):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            user: User = kwargs.get("current_user")
            if user is not None and len(roles) > 0:

                if user["role"]["name"] not in roles:
                    raise HTTPException(
                        status_code=403,
                        detail="Your role does not have access")

            result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator

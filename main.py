import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from controllers.auth import router as auth__router
from controllers.users import router as users__router
from controllers.roles import router as roles__router
from controllers.documents import router as generation__router

from database import AsyncSessionLocal
from models.users_logic import AsyncUserService

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    auth__router,
    users__router,
    roles__router,
    generation__router,
]

for router in routers:
    app.include_router(router, prefix="/api")


@app.get("/api/storage/{file_path:path}")
async def get_media(file_path: str):

    file_path = f"storage/{file_path}"

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="file not found"
        )

    if file_path.endswith((".mp4", ".avi", ".mkv")):
        return FileResponse(file_path, media_type="video/mp4")
    elif file_path.endswith((".jpg", ".jpeg", ".png", ".gif")):
        return FileResponse(file_path, media_type="image/jpeg")
    else:
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={file_path.split('/')[-1]}"  # noqa 501
            }
        )


@app.on_event("startup")
async def startup_event():

    async_session = AsyncSessionLocal()
    user_manager = AsyncUserService(async_session)
    try:
        await user_manager.auto_create_admin()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)

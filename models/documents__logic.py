import asyncio
import base64
import random
from io import BytesIO
from uuid import UUID
from fastapi import HTTPException, status
from PIL import Image
import json
import os
import uuid
from datetime import datetime, timedelta
import aiofiles
import aiohttp
from anyio import value
import requests
from fastapi import Request, UploadFile
from requests import Response
from sqlalchemy import String, and_, distinct, select, func, Sequence, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, with_loader_criteria

from config import get_settings
from views.json.v3.applications import Base64File

settings = get_settings()
CURRENT_HOST = settings.current_host  # noqa 501


class DocumentService:

    def __init__(self, session: AsyncSession):
        self.session = session



    @staticmethod
    def decode_file(base64_file: Base64File) -> tuple[str, bytes]:
        file_bytes = base64.b64decode(base64_file.data)
        filename = base64_file.filename
        return filename, file_bytes

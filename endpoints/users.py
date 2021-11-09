from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from dependency import get_db

router = APIRouter()



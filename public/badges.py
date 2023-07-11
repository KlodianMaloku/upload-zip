
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import SessionLocal, get_db

from models.badges import Badge as BadgeModel
from models.schemas.badges import BadgeCreate, BadgeUpdate, Badge
from users.endpoints import gen_uid


badges_router = APIRouter()

@badges_router.post('/badges/', response_model=Badge)
def create_badge(badge_data: BadgeCreate):
    db = get_db()
    try:
        badge = BadgeModel(uid=gen_uid('BG'), name=badge_data.name, description=badge_data.description)
        db.add(badge)
        db.commit()
        db.refresh(badge)
        return badge
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Badge with the same UID already exists')


@badges_router.get('/badges/{badge_uid}', response_model=Badge)
def get_badge(badge_uid: str):
    db = get_db()
    badge = db.query(BadgeModel).get(badge_uid)
    if not badge:
        raise HTTPException(status_code=404, detail='Badge not found')
    return badge


@badges_router.put('/badges/{badge_uid}', response_model=Badge)
def update_badge(badge_uid: str, badge_data: BadgeUpdate):
    db = get_db()
    badge = db.query(BadgeModel).get(badge_uid)
    if not badge:
        raise HTTPException(status_code=404, detail='Badge not found')
    badge.name = badge_data.name
    badge.description = badge_data.description
    db.commit()
    db.refresh(badge)
    return badge


@badges_router.delete('/badges/{badge_uid}')
def delete_badge(badge_uid: str):
    db = get_db()
    badge = db.query(BadgeModel).get(badge_uid)
    if not badge:
        raise HTTPException(status_code=404, detail='Badge not found')
    db.delete(badge)
    db.commit()
    return {'message': 'Badge deleted successfully'}
from __future__ import annotations

from pydantic import BaseModel, Field


class TrackCreate(BaseModel):
    artist: str
    title: str
    bpm: float = Field(gt=0)
    key: str
    genre: str
    tags: set[str] = Field(default_factory=set)


class TrackResponse(BaseModel):
    id: int
    artist: str
    title: str
    bpm: float
    key: str
    genre: str
    tags: set[str]


class TransitionResponse(BaseModel):
    to_track_id: int
    is_hard_cut: bool


class SetStepResponse(BaseModel):
    track: TrackResponse
    transition: TransitionResponse | None


class SetOrderResponse(BaseModel):
    steps: list[SetStepResponse]

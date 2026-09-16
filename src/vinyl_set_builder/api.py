import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError, InvalidCamelotKeyError
from vinyl_set_builder.domain.models import Track
from vinyl_set_builder.domain.session import GraphBuildSession
from vinyl_set_builder.domain.set_builder import SetOrder, build_set_order
from vinyl_set_builder.repository import TrackRepository


class TrackCreate(BaseModel):
    artist: str
    title: str
    bpm: float = Field(gt=0)
    key: str


class TrackResponse(BaseModel):
    id: int
    artist: str
    title: str
    bpm: float
    key: str


class TransitionResponse(BaseModel):
    to_track_id: int
    is_hard_cut: bool


class SetStepResponse(BaseModel):
    track: TrackResponse
    transition: TransitionResponse | None


class SetOrderResponse(BaseModel):
    steps: list[SetStepResponse]


logger = logging.getLogger(__name__)
router = APIRouter()
repository = TrackRepository()


def _to_track_response(track: Track) -> TrackResponse:
    return TrackResponse(
        id=track.id,
        artist=track.artist,
        title=track.title,
        bpm=track.bpm,
        key=track.key,
    )


@router.post("/tracks", response_model=TrackResponse, status_code=status.HTTP_201_CREATED)
def create_track(payload: TrackCreate) -> TrackResponse:
    try:
        track = repository.add(
            artist=payload.artist,
            title=payload.title,
            bpm=payload.bpm,
            key=payload.key,
        )
    except InvalidCamelotKeyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _to_track_response(track)


@router.get("/tracks", response_model=list[TrackResponse])
def list_tracks() -> list[TrackResponse]:
    return [_to_track_response(track) for track in repository.list_all()]


@router.post("/build-set", response_model=SetOrderResponse)
def build_set() -> SetOrderResponse:
    tracks = repository.list_all()
    try:
        with GraphBuildSession() as session:
            order, transitions = build_set_order(tracks)
        logger.info("построен сет из %d треков за %.4fs", len(tracks), session.duration_seconds)
    except IncompatibleCrateError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    set_order = SetOrder(order, transitions)
    steps = [
        SetStepResponse(
            track=_to_track_response(step.track),
            transition=(
                TransitionResponse(
                    to_track_id=step.transition.to_track.id,
                    is_hard_cut=step.transition.is_hard_cut,
                )
                if step.transition
                else None
            ),
        )
        for step in set_order
    ]
    return SetOrderResponse(steps=steps)

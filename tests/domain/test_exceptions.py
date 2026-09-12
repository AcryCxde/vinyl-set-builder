import pytest

from vinyl_set_builder.domain.exceptions import (
    IncompatibleCrateError,
    InvalidCamelotKeyError,
    VinylSetBuilderError,
)


def test_invalid_camelot_key_error_message_includes_the_bad_key():
    error = InvalidCamelotKeyError("H1")
    assert "H1" in str(error)
    assert error.key == "H1"


def test_invalid_camelot_key_error_is_a_vinyl_set_builder_error():
    assert issubclass(InvalidCamelotKeyError, VinylSetBuilderError)


def test_incompatible_crate_error_is_a_vinyl_set_builder_error():
    assert issubclass(IncompatibleCrateError, VinylSetBuilderError)


def test_incompatible_crate_error_carries_its_message():
    error = IncompatibleCrateError("Need at least 2 tracks")
    assert str(error) == "Need at least 2 tracks"

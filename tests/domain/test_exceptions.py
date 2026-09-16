from vinyl_set_builder.domain.exceptions import (
    IncompatibleCrateError,
    InvalidCamelotKeyError,
    VinylSetBuilderError,
)


def test_invalid_camelot_key_error_reports_the_bad_key_and_is_a_domain_error():
    error = InvalidCamelotKeyError("H1")
    assert "H1" in str(error)
    assert error.key == "H1"
    assert isinstance(error, VinylSetBuilderError)


def test_incompatible_crate_error_carries_its_message_and_is_a_domain_error():
    error = IncompatibleCrateError("Need at least 2 tracks")
    assert str(error) == "Need at least 2 tracks"
    assert isinstance(error, VinylSetBuilderError)

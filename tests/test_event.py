import tempfile

from models.event import (
    create_event,
    get_event_by_id,
    list_events,
    search_events,
    update_event_seats,
)


def test_event_create_list_search_and_persistence(tmp_path):
    event_file = tmp_path / "events.json"

    ok, event = create_event(
        "Winter Concert",
        "2026-09-13",
        "Hall A",
        50,
        str(event_file),
    )

    assert ok is True
    assert event.event_id == "E001"
    assert event.available_seats == 50

    events = list_events(str(event_file))
    assert len(events) == 1

    found = get_event_by_id("E001", str(event_file))
    assert found is not None
    assert found.name == "Winter Concert"

    matches = search_events("concert", str(event_file))
    assert len(matches) == 1

    ok, updated = update_event_seats("E001", -5, str(event_file))
    assert ok is True
    assert updated.available_seats == 45


def test_update_event_seats_cannot_go_negative(tmp_path):
    event_file = tmp_path / "events.json"

    create_event("Small Show", "2026-10-01", "Hall B", 3, str(event_file))

    ok, msg = update_event_seats("E001", -10, str(event_file))
    assert ok is False

    # seats must be unchanged after a rejected update
    unchanged = get_event_by_id("E001", str(event_file))
    assert unchanged.available_seats == 3


def test_update_event_seats_missing_event(tmp_path):
    event_file = tmp_path / "events.json"
    ok, msg = update_event_seats("E999", -1, str(event_file))
    assert ok is False


def test_create_event_rejects_invalid_seats(tmp_path):
    event_file = tmp_path / "events.json"

    ok, msg = create_event("Bad Seats", "2026-10-01", "Hall C", -5, str(event_file))
    assert ok is False

    ok, msg = create_event("Bad Seats", "2026-10-01", "Hall C", "not-a-number", str(event_file))
    assert ok is False


def test_create_event_rejects_invalid_price(tmp_path):
    event_file = tmp_path / "events.json"

    ok, msg = create_event("Bad Price", "2026-10-01", "Hall D", 10, str(event_file), price=-1)
    assert ok is False


def test_create_event_rejects_missing_fields(tmp_path):
    event_file = tmp_path / "events.json"

    ok, msg = create_event("", "2026-10-01", "Hall E", 10, str(event_file))
    assert ok is False


def test_load_events_survives_corrupted_json(tmp_path):
    """
    Regression test for the testing-gap feedback: corrupted JSON should
    not crash the app, it should just be treated as no events.
    """
    event_file = tmp_path / "events.json"
    event_file.write_text("{not valid json!!")

    events = list_events(str(event_file))
    assert events == []


def test_persistence_across_simulated_restart(tmp_path):
    """
    Creates an event, then reads it back via a completely fresh call —
    simulating what happens when the app restarts and reloads from disk.
    """
    event_file = tmp_path / "events.json"
    create_event("Reunion Show", "2026-11-11", "Hall F", 20, str(event_file))

    # simulate "restart" by only ever going through the file, never reusing
    # the in-memory `event` object returned by create_event
    reloaded = get_event_by_id("E001", str(event_file))
    assert reloaded is not None
    assert reloaded.name == "Reunion Show"
    assert reloaded.available_seats == 20
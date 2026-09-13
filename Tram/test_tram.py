import pytest

from Tram.tram import Tram


NORTH = 1
MIDDLE = 500
SOUTH = 1000

def describe_movement_between_stations():
    def test_move_advances_exactly_one_station_without_passing_an_end():
        tram = Tram(location=NORTH, direction="south")
        tram.close()
        tram.lock()

        tram.move()
        first_location = tram.getLocation()
        tram.move()
        second_location = tram.getLocation()
        tram.move()

        assert first_location == MIDDLE
        assert second_location == SOUTH
        assert tram.getLocation() == SOUTH

    def test_reaching_an_end_reverses_direction_before_the_next_move():
        tram = Tram(location=MIDDLE, direction="north")
        tram.close()
        tram.lock()

        tram.move()

        assert tram.getLocation() == NORTH
        assert tram.direction == "south"


def describe_locked_doors():
    def test_open_has_no_effect_while_doors_are_locked():
        tram = Tram()
        tram.close()
        tram.lock()

        result = tram.open()

        assert result is False
        assert tram.door_state == "locked"

    def test_close_has_no_effect_while_doors_are_locked():
        tram = Tram()
        tram.close()
        tram.lock()

        result = tram.close()

        assert result is False
        assert tram.door_state == "locked"


def describe_departure_safety():
    def test_doors_are_locked_before_the_tram_moves():
        tram = Tram(location=NORTH, direction="south")

        tram.move()

        assert tram.departure_door_state == "locked"
        assert tram.getLocation() == MIDDLE


def describe_emergency_button():
    def test_emergency_stops_the_tram_and_unlocks_its_doors():
        tram = Tram(location=250, direction="south")
        tram.close()
        tram.lock()
        tram.start()

        tram.emergency()

        assert tram.in_motion is False
        assert tram.door_state != "locked"
        assert tram.emergency_state is True


def describe_door_buttons():
    def test_open_button_opens_doors_when_they_are_not_locked():
        tram = Tram()
        tram.close()

        opened = tram.open()

        assert opened is True
        assert tram.door_state == "open"

    def test_close_button_closes_doors_during_reset_state():
        tram = Tram()
        tram.emergency()
        tram.reset()

        closed = tram.close()

        assert closed is True
        assert tram.door_state == "closed"


def describe_location_sensor():
    def test_get_location_returns_an_integer_within_track_bounds():
        tram = Tram(location=MIDDLE)

        location = tram.getLocation()

        assert isinstance(location, int)
        assert NORTH <= location <= SOUTH

    def test_get_location_raises_for_a_position_outside_track_bounds():
        tram = Tram(location=MIDDLE)

        tram.location = 0
        with pytest.raises(ValueError, match="location"):
            tram.getLocation()

        tram.location = 1001
        with pytest.raises(ValueError, match="location"):
            tram.getLocation()


def describe_emergency_reset():
    def test_reset_continues_in_the_current_direction_to_the_closest_station():
        tram = Tram(location=400, direction="south")
        tram.emergency()

        tram.reset()
        tram.close()

        assert tram.emergency_state is False
        assert tram.getLocation() == MIDDLE
        assert tram.direction == "south"


def describe_stopping_at_stations():
    def test_tram_always_stops_at_a_station():
        tram = Tram(location=NORTH, direction="south")
        tram.close()
        tram.lock()

        tram.move()

        assert tram.getLocation() in tram.stops
        assert not tram.in_motion

    def test_station_stop_time_is_configurable():
        tram = Tram(dwell_time=12)

        assert tram.dwell_time == 12

        tram.dwell_time = 20

        assert tram.dwell_time == 20

    def test_stopped_tram_at_a_station_has_unlocked_open_doors():
        tram = Tram(location=MIDDLE)

        assert tram.in_motion is False
        assert tram.door_state == "open"

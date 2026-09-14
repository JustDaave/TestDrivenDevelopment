class Tram:
    def __init__(
        self,
        location=1,
        direction="south",
        dwell_time=10,
        stops=None,
        arrival_messages=None,
    ):
        self.location = location
        self.direction = direction.lower()
        self.dwell_time = dwell_time
        self.stops = sorted(stops if stops is not None else [1, 500, 1000])
        self.arrival_messages = arrival_messages or {}

        self.in_motion = False
        self.door_state = "open"
        self.emergency_state = False
        self.reset_state = False
        self.departure_door_state = None
        self.intended_speed = 0
        self.current_speed = 0
        self.brakes = False
        self.brake_tested = False
        self.message = ""
        self.main_console = MainConsole(self)

    def getLocation(self):
        if not isinstance(self.location, int) or not 1 <= self.location <= 1000:
            raise ValueError("location must be between 1 and 1000")
        return self.location

    def open(self):
        if self.door_state == "locked":
            return False
        self.door_state = "open"
        return True

    def close(self):
        if self.door_state == "locked":
            return False

        self.door_state = "closed"

        # After an emergency between stations, closing the doors during a
        # reset lets the tram finish traveling to the next station.
        if self.reset_state and self.location not in self.stops:
            self.lock()
            self.move()
            self.reset_state = False
        return True

    def lock(self):
        if self.door_state != "closed":
            return False
        self.door_state = "locked"
        return True

    def start(self):
        if self.emergency_state or self.door_state != "locked":
            return False
        self.in_motion = True
        return True

    def stop(self):
        self.intended_speed = 0
        self.in_motion = False
        self.update_brakes()
        return True

    def depart(self):
        if self.emergency_state:
            return False
        if self.door_state == "open":
            self.close()
        if self.door_state == "closed":
            self.lock()
        if self.door_state != "locked":
            return False

        self.departure_door_state = self.door_state
        self.intended_speed = 50
        self.brakes = False
        return self.start()

    def arrive(self):
        self.intended_speed = 0
        self.update_brakes()
        self.current_speed = 0
        self.in_motion = False
        self.door_state = "open"
        self.message = self.arrival_messages.get(self.location, "")
        return True

    def move(self):
        if self.emergency_state:
            return False

        if not self.depart():
            return False

        self.current_speed = self.intended_speed
        self.location = self._next_station()

        if self.location == self.stops[0]:
            self.direction = "south"
        elif self.location == self.stops[-1]:
            self.direction = "north"

        self.arrive()
        return True

    def _next_station(self):
        if self.direction == "south":
            stations_ahead = [stop for stop in self.stops if stop > self.location]
            if stations_ahead:
                return min(stations_ahead)
            self.direction = "north"
            return max(stop for stop in self.stops if stop < self.location)

        stations_ahead = [stop for stop in self.stops if stop < self.location]
        if stations_ahead:
            return max(stations_ahead)
        self.direction = "south"
        return min(stop for stop in self.stops if stop > self.location)

    def emergency(self):
        self.in_motion = False
        self.emergency_state = True
        self.intended_speed = 0
        self.brakes = True
        if self.door_state == "locked":
            self.door_state = "closed"
        return True

    def remote_emergency(self):
        return self.emergency()

    def force_open(self):
        self.emergency()
        self.door_state = "open"
        return True

    def reset(self):
        self.emergency_state = False
        self.reset_state = True
        self.brakes = True
        self.brake_tested = True
        return True

    def update_brakes(self):
        self.brakes = self.intended_speed < self.current_speed
        return self.brakes


class MainConsole:
    def __init__(self, tram):
        self.tram = tram

    def start(self):
        return self.tram.start()

    def stop(self):
        return self.tram.stop()

    def open_doors(self):
        return self.tram.open()

    def close_doors(self):
        return self.tram.close()

    def reset(self):
        return self.tram.reset()

class Tram:
    def __init__(self, location=1, direction="south", dwell_time=10):
        self.location = location
        self.direction = direction.lower()
        self.dwell_time = dwell_time
        self.stops = [1, 500, 1000]

        self.in_motion = False
        self.door_state = "open"
        self.emergency_state = False
        self.reset_state = False
        self.departure_door_state = None

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

    def move(self):
        if self.emergency_state:
            return False

        if self.door_state == "open":
            self.close()
        if self.door_state == "closed":
            self.lock()
        if self.door_state != "locked":
            return False

        self.departure_door_state = self.door_state
        self.in_motion = True
        self.location = self._next_station()
        self.in_motion = False

        if self.location == self.stops[0]:
            self.direction = "south"
        elif self.location == self.stops[-1]:
            self.direction = "north"

        self.door_state = "open"
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
        if self.door_state == "locked":
            self.door_state = "closed"
        return True

    def reset(self):
        self.emergency_state = False
        self.reset_state = True
        return True

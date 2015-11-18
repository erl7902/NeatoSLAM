import math
import numpy as np

# field of view of each individual laser reading
laser_fov = .017437326 # already in radians * (np.pi / 180)


class EvidenceGrid:
    """
    Handles the calculations and storage of an evidence grid.
    Each observation updates self.oddsarray which is indexed
    self.oddsarray[y][x]. self.oddsarray holds numbers from 
    0 to inf that are the odds of each tile being occupied.
    """

    def __init__(self, scale, width, height):
        """
        Params:
            scale: the scale of the map in meters per pixel.
            width, height: the dimensions of the grid in tiles.
        """
        self.oddsarray = np.ones((height, width), np.float64)
        self.scale = scale


    def observe_something(self, dist, angle, sparki_x, sparki_y):
        """
        Params:
            dist: the reported distance to the object in m
            angle: the angle the sensor is pointing in a standard
                   coordinate system (0 rad along x axis)
            sparki_x, sparki_y: positions in m
        """
        self._observe(True, dist, angle, sparki_x, sparki_y)

    def observe_nothing(self, angle, sparki_x, sparki_y):
        """
        Params:
            angle: the angle the sensor is pointing in a standard
                   coordinate system (0 rad along x axis)
            sparki_x, sparki_y: positions in m
        """
        self._observe(False, None, angle, sparki_x, sparki_y)


    def _observe(self, observed_something, dist, angle, sparki_x, sparki_y):
        # the left and right limits of sparki's ultrasonic sensor
        left_limit = angle + ultrasonic_fov/2
        right_limit = angle - ultrasonic_fov/2

        # think of the triangle that encloses the sector
        max_range = 2
        triangle_hyp = max_range / math.cos(ultrasonic_fov/2)
        # one triangle point is sparki's center, here are the other two
        # (left and right are from sparki's perspective)
        left_point_y = sparki_y + triangle_hyp * math.sin(left_limit)
        left_point_x = sparki_x + triangle_hyp * math.cos(left_limit)
        right_point_y = sparki_y + triangle_hyp * math.sin(right_limit)
        right_point_x = sparki_x + triangle_hyp * math.cos(right_limit)
        # calculate bounding box
        bot = min(sparki_y, left_point_y, right_point_y)
        top = max(sparki_y, left_point_y, right_point_y)
        left = min(sparki_x, left_point_x, right_point_x)
        right = max(sparki_x, left_point_x, right_point_x)
        # convert bounding box to tiles and clip it to the dimensions of the array
        ymin, xmin = self._meters_to_tile(bot, left)
        ymax, xmax = self._meters_to_tile(top, right)
        ymin = max(ymin, 0)
        ymax = min(ymax, self.oddsarray.shape[0])
        xmin = max(xmin, 0)
        xmax = min(xmax, self.oddsarray.shape[1])

        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                # tile coordinates from origin
                y_m, x_m = self._tile_to_meters(y, x)
                # tile coordinates from sparki
                dy, dx = (y_m - sparki_y, x_m - sparki_x)
                # angle and euclidean distance to the tile
                t_angle = math.atan2(dy, dx)
                t_dist = math.sqrt(dy*dy + dx*dx)

                # the default 1 means the odds are unmodified.
                odds = 1
                if right_limit <= t_angle <= left_limit:
                    if observed_something:
                        # 4 cm band of high obstacle odds at the end of vision
                        if dist - 0.04 <= t_dist <= dist + 0.04:
                            odds = 1.5
                        # decreased odds for anywhere closer
                        elif t_dist <= dist - 0.04:
                            odds = 0.5
                    else:
                        # observed nothing so decrease odds.
                        if t_dist <= max_range:
                            odds = 0.5
                 
                self.oddsarray[y, x] *= odds


    def _meters_to_tile(self, y_m, x_m):
        ycount, xcount = self.oddsarray.shape
        to_y_m = y_m
        to_x_m = x_m
        origin_y = ycount/2
        origin_x = xcount/2
        ytile = int(round(origin_y + to_y_m / self.scale))
        xtile = int(round(origin_x + to_x_m / self.scale))
        return (ytile, xtile)


    def _tile_to_meters(self, y, x):
        ycount, xcount = self.oddsarray.shape
        origin_y = (self.scale * ycount/2)
        origin_x = (self.scale * xcount/2)
        relative_y = self.scale*y - origin_y
        relative_x = self.scale*x - origin_x
        return (relative_y, relative_x)

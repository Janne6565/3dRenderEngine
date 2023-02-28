import time, math


class Point:
    x = None
    y = None
    z = None

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def plus(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def minus(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def scale(self, scale):
        return Point(self.x * scale, self.y * scale, self.z * scale)

    def divide(self, scale):
        return Point(self.x / scale, self.y / scale, self.z / scale)

    def pyta(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def toString(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)


class Line:
    a = None
    b = None

    def __init__(self, a, b):
        self.a = a
        self.b = b


class StraightLine:
    directionalVector = None
    startPoint = None

    def __init__(self, directionalVector, startPoint):
        self.directionalVector = directionalVector
        self.startPoint = startPoint


class Plane:
    range = None  # Calculated from the first Vector
    vector1 = None
    vector2 = None
    vector3 = None

    def __init__(self, range, vector1, vector2, vector3):
        self.range = range
        self.vector1 = vector1
        self.vector2 = vector2.minus(vector1)
        self.vector3 = vector3.minus(vector1)

    def getNormalVect(self):
        x = self.vector2.y * self.vector3.z - self.vector2.z * self.vector3.y
        y = self.vector2.z * self.vector3.x - self.vector2.x * self.vector3.y
        z = self.vector2.x * self.vector3.y - self.vector2.y * self.vector3.x
        return Point(x, y, z)

    def getPointOfCollision(self, straightLine):
        normal = self.getNormalVect()
        normalEquals = self.vector1.x * normal.x + self.vector1.y * normal.y + self.vector1.z * normal.z
        r = (
                    normalEquals
                    - normal.x * straightLine.startPoint.x
                    - normal.y * straightLine.startPoint.y
                    - normal.z * straightLine.startPoint.z
            ) / (
                    normal.x * straightLine.directionalVector.x
                    + normal.y * straightLine.directionalVector.y
                    + normal.z * straightLine.directionalVector.z
            )
        point = straightLine.startPoint.plus(straightLine.directionalVector.scale(r))

        relativeDistance = self.vector1.minus(point)
        distanceXY = relativeDistance.pyta()
        if (distanceXY >= self.range):
            return None

        return point


symbolsByOpacity = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def getStartPoint(x, y, offsetX, offsetY):
    return Point(x - offsetX, 0, y + offsetY)


def getVector(x, y):
    return Point(0, 1, 0)


def getDistance(streightLine, objects):
    firstIntersection = None
    objectFirstIntersection = None

    for plane in objects:
        pointColliding = plane.getPointOfCollision(streightLine)
        if (pointColliding != None):
            distance = streightLine.startPoint.minus(pointColliding).pyta()
            if (firstIntersection == None or distance < firstIntersection):
                firstIntersection = distance
                objectFirstIntersection = plane

    return firstIntersection


def getSymbolByOpacity(opacity, maxSym):
    relative = len(symbolsByOpacity) / maxSym
    if (opacity > maxSym):
        opacity = maxSym
    index = opacity * relative
    return symbolsByOpacity[int(index - 1)]

def renderProject(width, height, objects, offsetX, offsetY):
    timeBefore = time.time()
    map = {}
    maxDistance = 10

    for y in range(width):
        for x in range(height):
            startPoint = getStartPoint(x, y, offsetX, offsetY)
            direction = getVector(x, y)
            distance = getDistance(StraightLine(direction, startPoint), objects)
            if (not x in map):
                map[x] = {}

            map[x][y] = distance

    message = ""
    for x in map:
        for y in map[x]:
            if (map[x][y] == None):
                message += " "
            else:
                message += getSymbolByOpacity(map[x][y], maxDistance)
        message += "\n"
    print(message)



pointZ = 2
while True:
    renderProject(300, 85, [Plane(5, Point(pointZ, 1, 20), Point(0, pointZ ** 2, pointZ * -1), Point(0, 4, pointZ / pointZ))], - pointZ + 40, -130)
    time.sleep(0.1)
    pointZ += 0.3
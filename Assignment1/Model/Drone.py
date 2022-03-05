

class Drone:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def xCoordinate(self):
        return self.__x

    @xCoordinate.setter
    def xCoordinate(self, value):
        self.__x = value

    @property
    def yCoordinate(self):
        return self.__y

    @yCoordinate.setter
    def yCoordinate(self, value):
        self.__y = value



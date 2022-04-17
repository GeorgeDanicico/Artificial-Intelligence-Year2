class Drone:
    def __init__(self,x ,y):
        self.__x = x
        self.__y = y

    def get_coordinates(self):
        return [self.__x, self.__y]

    def set_coordinates(self, x, y):
        self.__x = x
        self.__y = y

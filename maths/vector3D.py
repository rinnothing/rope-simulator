class Vector3D:
    #init from x, y, z
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    #string representation
    def __str__(self):
        return '<%s, %s, %s>' % (self.x, self.y, self.z)

    #copying 
    def copy(self):
        return Vector3D(self.x, self.y, self.z)

    #arithmetic operations
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def __mul__(self, number):
        return Vector3D(self.x * number, self.y * number, self.z * number)

    def __rmul__(self, number):
        return self.__mul__(number)

    def __truediv__(self, number):
        return self.__mul__(number**-1)

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    #length of vector
    @property
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**(1/2)
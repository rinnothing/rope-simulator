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

    #square length of vector
    def lengthsq(self):
        return self.x**2 + self.y**2 + self.z**2

    #length of vector
    @property
    def length(self):
        return self.lengthsq()**(1/2)

    #returns scalar composition
    def scalar(self, vector):
        return self.x*vector.x + self.y*vector.y + self.z*vector.z

    #returns k of projection
    def project_k(self, vector):
        if self.length == 0:
            return 0
        return self.scalar(vector) / self.lengthsq()

    #returns vector projection on this vector
    def project(self, vector):
        return self * self.project_k(vector)

    #returns vector that perpendicular to this vector
    def perpendicular(self, vector):
        return vector - self.project(vector)

    #returns direction of the vector
    def direction(self):
        return self / self.length
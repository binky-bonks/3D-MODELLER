import math
class vector:
    def __init__(self, x, y, z):
      self.x = float(x)
      self.y = float(y)
      self.z = float(z)
    def __sub__(self, other):
      if isinstance(other,vector):
          return vector(self.x - other.x, self.y - other.y, self.z - other.z) 
      return vector(self.x - other, self.y - other, self.z - other)
    def negative(self):
       return vector(-1*self.x, -1*self.y, -1*self.z)
    def __add__(self, other):
       return vector(self.x + other.x, self.y + other.y, self.z + other.z)
    def __mul__(self, scalar):
       self.scalar = float(scalar)
       return vector(scalar * self.x, scalar * self.y, scalar * self.z)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    def dot(self, other):
       return (self.x*other.x) + (self.y*other.y) +(self.z*other.z)
    def magnitude(self):
       return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def normalise(self):
       length = self.magnitude()
       if length == 0:
          return vector(0,0,0)
       return vector(self.x/length, self.y/length, self.z/length)
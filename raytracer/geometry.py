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
    def apply_rotation(self, matrix):
       new_x = matrix[0][0]*self.x + matrix[0][1]*self.y + matrix[0][2]*self.z
       new_y = matrix[1][0]*self.x + matrix[1][1]*self.y + matrix[1][2]*self.z
       new_z = matrix[2][0]*self.x + matrix[2][1]*self.y + matrix[2][2]*self.z
       return vector(new_x, new_y, new_z)
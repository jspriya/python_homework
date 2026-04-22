import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    # Equality 
    def __eq__(self,other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    # String representation
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    
    # Euclidean distance
    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
class Vector(Point):
    def __str__(self):
        return f"Vector<{self.x}, {self.y}>"
    
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Can only add Vector to Vector")
        return Vector(self.x + other.x, self.y + other.y)
    
if __name__ == "__main__":
    p1 = Point(1, 2)
    p2 = Point(4, 6)

    print(p1)  # Point string
    print(p2)
    print("Points equal?", p1 == p2)

    print("Distance between points:", p1.distance(p2))

    v1 = Vector(2,3)
    v2 = Vector(5,7)

    print(v1) 
    print(v2)

    v3 = v1 + v2
    print("v1 + v2 =", v3)

    # Equality still works (inherited)
    v4 = Vector(2, 3)
    print("v1 == v4?", v1 == v4)


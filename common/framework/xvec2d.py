########################################################################
##
## 2D vector class from:
## http://www.pygame.org/wiki/2DVectorClass?parent=CookBook
##
########################################################################

import operator
import math
 
########################################################################
 
class XVec2d(object):
    
    def __init__(self, x_or_pair, y = None):
        if y == None:
            try:
                self.vec = [x_or_pair[0],x_or_pair[1]]
            except TypeError:
                raise TypeError("XVec2d constructor requires a tuple or"
                    " two arguments")
        else:
            self.vec = [x_or_pair,y]
 
    def get_x(self):
        return self.vec[0]
    def set_x(self, value):
        self.vec[0] = value
    x = property(get_x, set_x)
    
    def get_y(self):
        return self.vec[1]
    def set_y(self, value):
        self.vec[1] = value
    y = property(get_y, set_y)
    
    def set(self, x, y):
        self.vec[0] = x
        self.vec[1] = y
        
    # String representaion (for debugging)
    def __repr__(self):
        return 'XVec2d(%s, %s)' % (self.x, self.y)
    
    # Array-style access
    def __len__(self): return 2
 
    def __getitem__(self, key):
        return self.vec[key]
 
    def __setitem__(self, key, value):
        self.vec[key] = value
 
    # Comparison
    def __eq__(self, other):
        return self.vec[0] == other[0] and self.vec[1] == other[1]
    
    def __ne__(self, other):
        return self.vec[0] != other[0] or self.vec[1] != other[1]
 
    def __nonzero__(self):
        return self.vec[0] or self.vec[1]
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a XVec2d"
        try:
            return XVec2d(f(self.vec[0], other[0]),
                         f(self.vec[1], other[1]))
        except TypeError:
            return XVec2d(f(self.vec[0], other),
                         f(self.vec[1], other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a XVec2d"
        try:
            return XVec2d(f(other[0], self.vec[0]),
                         f(other[1], self.vec[1]))
        except TypeError:
            return XVec2d(f(other, self.vec[0]),
                         f(other, self.vec[1]))
 
    def _o1(self, f):
        "Any unary operation on a XVec2d"
        return XVec2d(f(self.vec[0]), f(self.vec[1]))
 
    # Addition
    def __add__(self, other):
        return self._o2(other, operator.add)
    __radd__ = __add__
 
    # Subtraction
    def __sub__(self, other):
        return self._o2(other, operator.sub)
    def __rsub__(self, other):
        return self._r_o2(other, operator.sub)
 
    # Multiplication
    def __mul__(self, other):
        return self._o2(other, operator.mul)
    __rmul__ = __mul__
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return self._o1(operator.neg)
 
    def __pos__(self):
        return self._o1(operator.pos)
 
    def __abs__(self):
        return self._o1(operator.abs)
 
    def __invert__(self):
        return self._o1(operator.invert)
 
    # vectory functions
    def get_length_sqrd(self): 
        return self.vec[0]**2 + self.vec[1]**2
 
    def get_length(self):
        return math.sqrt(self.vec[0]**2 + self.vec[1]**2)    
    def __setlength(self, value):
        self.normalize_return_length()
        self.vec[0] *= value
        self.vec[1] *= value
    length = property(get_length, __setlength, None,
        "gets or sets the magnitude of the vector")
       
    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.vec[0]*cos - self.vec[1]*sin
        y = self.vec[0]*sin + self.vec[1]*cos
        self.vec[0] = x
        self.vec[1] = y
    
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.vec[1], self.vec[0]))
 
    def get_angle_between(self, other):
        cross = self.vec[0]*other[1] - self.vec[1]*other[0]
        dot = self.vec[0]*other[0] + self.vec[1]*other[1]
        return math.degrees(math.atan2(cross, dot))
    
    def __setangle(self, angle_degrees):
        self.vec[0] = self.length
        self.vec[1] = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None,
        "gets or sets the angle of a vector")
        
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return XVec2d(self)
 
    def perpendicular(self):
        return XVec2d(-self.vec[1], self.vec[0])
    
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return XVec2d(-self.vec[1]/length, self.vec[0]/length)
        return XVec2d(self)
        
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.vec[0] /= length
            self.vec[1] /= length
        return length
 
    def dot(self, other):
        return self.vec[0]*other[0] + self.vec[1]*other[1]
        
    def get_distance(self, other):
        return math.sqrt((self.vec[0] - other[0])**2 +
            (self.vec[1] - other[1])**2)
        
    def projection(self, other):
        normal = other.normalized()
        projected_length = self.dot(normal)
        return normal*projected_length
    
    def cross(self, other):
        return self.vec[0]*other[1] - self.vec[1]*other[0]
    
    def interpolate_to(self, other, range):
        return XVec2d(self.vec[0] + (other.vec[0] - self.vec[0])*range,
            self.vec[1] + (other.vec[1] - self.vec[1])*range)
    
    def convert_to_basis(self, x_vector, y_vector):
        return XVec2d(self.dot(x_vector)/x_vector.get_length_sqrd(),
            self.dot(y_vector)/y_vector.get_length_sqrd())
        
########################################################################
## Unit Testing                                                       ##
########################################################################
if __name__ == "__main__":
 
    import unittest
 
    ####################################################################
    class UnitTestXVec2d(unittest.TestCase):
    
        def setUp(self):
            pass
        
        def testCreationAndAccess(self):
            v = XVec2d(111,222)
            self.assert_(v.x == 111 and v.y == 222)
            v.x = 333
            v[1] = 444
            self.assert_(v[0] == 333 and v[1] == 444)
 
        def testMath(self):
            v = XVec2d(111,222)
            self.assert_(v + 1 == XVec2d(112,223))
            self.assert_(v - 2 == [109,220])
            self.assert_(v * 3 == (333,666))
            self.assert_(v / 2.0 == XVec2d(55.5, 111))
            self.assert_(v / 2 == (55, 111))
            self.assert_(v ** XVec2d(2,3) == [12321, 10941048])
            self.assert_(v + [-11, 78] == XVec2d(100, 300))
            self.assert_(v / [11,2] == [10,111])
 
        def testReverseMath(self):
            v = XVec2d(111,222)
            self.assert_(1 + v == XVec2d(112,223))
            self.assert_(2 - v == [-109,-220])
            self.assert_(3 * v == (333,666))
            self.assert_([222,999] / v == [2,4])
            self.assert_([111,222] ** XVec2d(2,3) == [12321, 10941048])
            self.assert_([-11, 78] + v == XVec2d(100, 300))
 
        def testUnary(self):
            v = XVec2d(111,222)
            v = -v
            self.assert_(v == [-111,-222])
            v = abs(v)
            self.assert_(v == [111,222])
 
        def testLength(self):
            v = XVec2d(3,4)
            self.assert_(v.length == 5)
            self.assert_(v.get_length_sqrd() == 25)
            self.assert_(v.normalize_return_length() == 5)
            self.assert_(v.length == 1)
            v.length = 5
            self.assert_(v == XVec2d(3,4))
            v2 = XVec2d(10, -2)
            self.assert_(v.get_distance(v2) == (v - v2).get_length())
            
        def testAngles(self):            
            v = XVec2d(0, 3)
            self.assertEquals(v.angle, 90)
            v2 = XVec2d(v)
            v.rotate(-90)
            self.assertEqual(v.get_angle_between(v2), 90)
            v2.angle -= 90
            self.assertEqual(v.length, v2.length)
            self.assertEquals(v2.angle, 0)
            self.assertEqual(v2, [3, 0])
            self.assert_((v - v2).length < .00001)
            self.assertEqual(v.length, v2.length)
            v2.rotate(300)
            self.assertAlmostEquals(v.get_angle_between(v2), -60)
            v2.rotate(v2.get_angle_between(v))
            angle = v.get_angle_between(v2)
            self.assertAlmostEquals(v.get_angle_between(v2), 0)  
 
        def testHighLevel(self):
            basis0 = XVec2d(5.0, 0)
            basis1 = XVec2d(0, .5)
            v = XVec2d(10, 1)
            self.assert_(v.convert_to_basis(basis0, basis1) == [2, 2])
            self.assert_(v.projection(basis0) == (10, 0))
            self.assert_(basis0.dot(basis1) == 0)
            
        def testCross(self):
            lhs = XVec2d(1, .5)
            rhs = XVec2d(4,6)
            self.assert_(lhs.cross(rhs) == 4)
    
    ########################################################################
 
    unittest.main()
 
    ######################################################################## 

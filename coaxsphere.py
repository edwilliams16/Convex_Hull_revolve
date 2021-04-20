import math
   

class Circle:
    'creates circle on the z-axis in the yz plane'
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.cz = center[2]
        self._left = self.cz - self.radius
        self._right = self.cz + self.radius
    
    def __str__(self):
        return 'Circle('+str(self.center)+ ' ' + str(self.radius) + ')'

    def enclosed(self, circle):
        'return enclsed circle or None'
        selfincircle = (self._left > circle._left) and (self._right < circle._right)
        circleinself = (self._left <= circle._left) and (self._right >= circle._right)
        if selfincircle: return self
        elif circleinself: return circle
        else: return None


    def tangent(self, circle):
        ''' finds tangent angle between self and circle in y>=0 
        Return None if either encloses the other'''
        if self.enclosed(circle):
            return None
        else:
            #theta ccw from z axis
            theta = math.acos(-(circle.radius - self.radius)/(circle.cz - self.cz))
            return theta

    def tangentCoord(self, theta):
        '''returns coords of point at angle theta'''
        return (0., self.radius * math.sin(theta), self.cz + self.radius * math.cos(theta))

class Arc:
    'creates arc from theta1 to theta 2 in the UHP of yz'
    def __init__(self, center, radius, theta1, theta2):
        self.center = center
        self.radius = radius
        self.cz = center[2]
        self.theta1 = theta1
        self.theta2 = theta2

    def __str__(self):
        return 'Arc('+str(self.center)+ ' ' + str(self.radius) + ') ' + str(self.theta1) + ' ' + str(self.theta2) + '\n' +\
            str(self.pt1()) + str(self.pt2())

    def pt1(self):
        return (0, self.radius * math.sin(self.theta1), self.cz + self.radius*math.cos(self.theta1))

    def pt2(self):
        return (0, self.radius * math.sin(self.theta2), self.cz + math.cos(self.theta2))

class Line:
    '''line between two points, defined 3-vectors with x=0'''
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.y1 = point1[1]
        self.z1 = point1[2]
        self.y2 = point2[1]
        self.z2 = point2[2]

    def __str__(self):
        return 'Line(' +str(self.point1) + ', ' + str(self.point2) + ')'

def removeEnclosedCircles(circleList):
    'remove circles in list contained in others'
    deleteIndices = []
    for i in range(len(circleList)):
        for j in range(len(circleList)):
            if i == j: 
                continue
            if circleList[i].enclosed(circleList[j]) == circleList[j]:  #j inside i
                deleteIndices.append(j)
    for i in sorted(deleteIndices, reverse=True):
        del circleList[i]
    return circleList

def hullCoaxialCircles(circleList):
    ''' from a list of Circle find the upper convex hull
    as a list of Arc and Line'''
    cleanList = removeEnclosedCircles(circleList)
    #sort by left edge
    sortList = sorted(cleanList, key = lambda c: c._left)
    nList = len(sortList)
    hullList =[]

    def nextCircle(list, i):
        'return index of next circle in hull after i'
        thmax = 0.0
        jmax = -1
        for j in range(i+1, nList):
            th = list[i].tangent(list[j])
            if th >= thmax:
                jmax = j
                thmax = th
        return (jmax, thmax)

    i = 0
    prevth = math.pi
    while True:
        k, th = nextCircle(sortList, i)
        foundCircle = sortList[k]
        prevCircle = sortList[i]
        hullList.append(Arc(prevCircle.center,prevCircle.radius, prevth, th)) #previous arc
        hullList.append(Line(prevCircle.tangentCoord(th),foundCircle.tangentCoord(th))) #tangent previous to found
        i = k
        prevth = th  
        if k == nList - 1:
            hullList.append(Arc(foundCircle.center,foundCircle.radius,th, 0.))  #final arc
            hullList.append(Line(foundCircle.tangentCoord(0.), hullList[0].pt1())) #close hull along z-axis
            return hullList


""" c1 = Circle((0, 0, 0), 1)
print(c1)
print(c1.tangentCoord(math.pi/2))
c2 = Circle((0,0,10),2)
th = c1.tangent(c2)
print (th*180/math.pi)
th = c2.tangent(c1)
print(th*180/math.pi)
print ((math.asin(1/10)+math.pi/2)*180/math.pi)
th = c1.tangent(c1)
print(th)
c2 = Circle((0,0,2),3)
th = c1.tangent(c2)
print (th*180/math.pi)
c3 = Circle((0,0,15),3)
c4 = Circle((0,0,14),2)
clist = [c1, c2, c3, c4]
for c in clist: print(c, ' ', end='')
print()
cslist = removeEnclosedCircles(clist)
for c in cslist: print(c, ' ', end = '')
print()
 
c1 = Circle((0, 0, 0), 1)
c2 = Circle((0,0,2),3)
c3 = Circle((0,0,15),3)
c4 = Circle((0,0,14),2)
c5 = Circle((0,0,10),4)
print('Construct two circle hull by hand')
th = c1.tangent(c3)
a1 = Arc(c1.center, c1.radius, math.pi, th)
a3 = Arc(c3.center, c3.radius, th, 0.)
l1 = Line(a1.pt2(),a3.pt1())
hull = [a1, l1, a3]
for x in hull: print(x)
print('construct by code')
cList = [c1, c3]
hullList = hullCoaxialCircles(cList)
for x in hullList: print(x)
print('Five circles by code')
cList = [c1, c2, c3, c4, c5]
hullList = hullCoaxialCircles(cList)
for x in hullList: print(x)
"""
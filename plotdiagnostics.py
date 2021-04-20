import numpy as np
import matplotlib.pyplot as plt
import coaxsphere as cx
import math

def plotArc(arc, fmt = ''):
    npts = 20
    th = np.linspace(arc.theta1,arc.theta2,npts)
    zplt = arc.cz + np.cos(th)*arc.radius
    yplt = np.sin(th)*arc.radius
    plt.plot(zplt, yplt, fmt)

def plotLine(line, fmt = ''):
    plt.plot(np.array([line.z1, line.z2]), np.array([line.y1, line.y2]), fmt)


def plotCircle(circle, fmt = ''):
    plotArc(cx.Arc(circle.center, circle.radius, math.pi, 0.), fmt)

def plotList(list, fmt):
    for seg in list:
        if isinstance(seg, cx.Arc):
            plotArc(seg, fmt)
        elif isinstance(seg, cx.Line):
            plotLine(seg, fmt)
        elif isinstance(seg, cx.Circle):
            plotCircle(seg, fmt)
        else:
            print ('Wrong type in plotHull')




''' test code'''
c1 = cx.Circle((0, 0, 0), 1)
c2 = cx.Circle((0,0,2),3)
c3 = cx.Circle((0,0,15),3)
c4 = cx.Circle((0,0,14),2)
c5 = cx.Circle((0,0,10),4)
print('Five circles by code')
cList = [c1, c2, c3, c4, c5]
plotList(cList, '--r')
hullList = cx.hullCoaxialCircles(cList)
for seg in hullList:
    print(seg)
    print()
plotList(hullList,'b')
zmin, zmax, ymin, ymax = plt.axis()
plt.axis([zmin,zmax,0.,zmax - zmin])
plt.title('Convex hull of line of semi-circles')
plt.show()

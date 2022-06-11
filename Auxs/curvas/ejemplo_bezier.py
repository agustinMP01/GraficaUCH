"""
Dibujamos una curva de Bézier.

Autor: Pablo Pizarro R.
"""

from curvas import *

R0 = np.array([[0, 0, 10]]).T
R1 = np.array([[0, 10, 0]]).T
R2 = np.array([[5, 0, 1]]).T
R3 = np.array([[10, 50, 0]]).T

GMb = bezierMatrix(R0, R1, R2, R3)
bezierCurve = evalCurve(GMb, N=50)

#  Definimos la figura para 3D
fig = plt.figure()
ax = fig.gca(projection='3d')

plotCurve(ax, bezierCurve, 'Bezier curve', color=(1, 0, 0))

R0 = np.array([[10, 50, 0]]).T
R1 = np.array([[30, 10, 10]]).T
R2 = np.array([[100, -50, 0]]).T
R3 = np.array([[0, 0, 0]]).T

GMb = bezierMatrix(R0, R1, R2, R3)
bezierCurve2 = evalCurve(GMb, N=50)
plotCurve(ax, bezierCurve2, 'Bezier curve 2')

# Visualizamos los puntos de control
controlPoints = np.concatenate((R0, R1, R2, R3), axis=1)
ax.scatter(controlPoints[0, :], controlPoints[1, :], controlPoints[2, :], color=(1, 0, 0))

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend()
plt.savefig('ex_bezier.png')
plt.show()

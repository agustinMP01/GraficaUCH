"""
Dibujamos una curva de Hermite.

Autor: Pablo Pizarro R.
"""

from curvas import *

# Ejemplo para Hermite
P1 = np.array([[0, 0, 1]]).T
P2 = np.array([[1, 0, 0]]).T
T1 = np.array([[10, 0, 0]]).T
T2 = np.array([[0, 10, 0]]).T

GMh = hermiteMatrix(P1, P2, T1, T2)
print(GMh)

# Largo de la curva
N = 1000

hermiteCurve = evalCurve(GMh, N)

#  Definimos la figura para 3D
fig = plt.figure()
ax = fig.gca(projection='3d')

plotCurve(ax, hermiteCurve, 'Hermite curve', (1, 0, 0))

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend()
plt.savefig('ex_hermite.png')
plt.show()

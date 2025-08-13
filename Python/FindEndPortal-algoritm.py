from math import *

mx1, mz1, malpha, mx2, mz2, mbeta = map(float, input().split())


def decart(angle):
    return angle + 90


def condition(angle, coordinate_x, coordinate_z, c_x, c_z):
    sina, cosa = (round(sin(radians(angle)), 10)), (round(cos(radians(angle)), 10))
    cond = None
    if 0 <= cosa <= 1 and 0 <= sina < 1:
        cond = f'{coordinate_x} >= {c_x}'
    if -1 < cosa <= 0 and 0 <= sina <= 1:
        cond = f'{coordinate_z} >= {c_z}'
    if -1 <= cosa <= 0 and -1 < sina <= 0:
        cond = f'{coordinate_x} <= {c_x}'
    if 0 <= cosa < 1 and -1 <= sina <= 0:
        cond = f'{coordinate_z} <= {c_z}'
    return cond


def calculations(x1, z1, alpha, x2, z2, beta):
    coordinates = []
    if decart(alpha) == decart(beta):
        coordinates.append("incorrect input numbers (the beams are parallel)")
    else:
        x = (z2 - z1 + tan(radians(decart(alpha))) * x1 - tan(radians(decart(beta))) * x2) \
            / (tan(radians(decart(alpha))) - tan(radians(decart(beta))))
        z = ((x1 - x2) * tan(radians(decart(alpha))) * tan(radians(decart(beta))) + tan(radians(decart(alpha))) * z2
             - tan(radians(decart(beta))) * z1) / (tan(radians(decart(alpha))) - tan(radians(decart(beta))))
        if eval(condition(decart(alpha), x, z, x1, z1)) and eval(condition(decart(beta), x, z, x2, z2)):
            coordinates.append(int(x))
            coordinates.append(int(z))
        else:
            coordinates.append("incorrect input numbers (the beams don't intersect)")

            if not (-29999984 <= x <= 29999983 or -29999984 <= z <= 29999983):
                coordinates.append("incorrect input numbers (the portal is out of the world)")

    return coordinates


print(calculations(mx1, mz1, malpha, mx2, mz2, mbeta))
print(3**35)

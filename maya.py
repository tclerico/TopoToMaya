
# this scrip is to be run in the Maya script editor to import all data


import maya.cmds as cmds


def read_in_lines():
    with open('/Users/timc/Documents/points.txt', 'r') as f:
        lines = f.readlines()

    points = []
    for line in lines:
        points.append(line.strip())

    dimensions = points.pop().split(",")
    dim = []
    for d in dimensions:
        dim.append(int(d))

    lines = []
    for p in points:
        positions = p.split(" ")
        line = []
        for pos in positions:
            coords = (int(pos.split(",")[0]), int(pos.split(",")[1]))
            line.append(coords)
        lines.append(line)

    return lines, dim


def to_linear(width, x, y):
    position = ((int(width) + 1) * int(y)) + int(x)
    tr = str(position)
    return tr


def raise_points(lines, dimensions, distance):
    width = dimensions[0]
    height = dimensions[1]
    d = distance

    for line in lines:
        for l in line:
            vtx = to_linear(width, l[0], l[1])
            cmds.select('pPlane1.vtx[' + vtx + ']')
            cmds.move(d, y=True)
        d += distance


def main():
    cmds.softSelect(sse=1, ssd=85.0, ssf=2)
    lines, dimensions = read_in_lines()
    print(dimensions)
    x = dimensions[0]
    y = dimensions[1]
    cmds.polyPlane(width=x, height=y, sx=x, sy=y)
    raise_points(lines, dimensions, 15)


main()


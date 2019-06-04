import matplotlib.pyplot as plt
import matplotlib.patches as patches


# def read_file():  # читает points.txt и возвращает список точек, используются регулярные выражения
#     template = re.compile(r"\-?\d+", re.M)
#     with open("points.txt", "r") as txt_file:
#         points = txt_file.read()
#     string_from_file = template.findall(points)
#     if len(string_from_file) % 2 != 0:
#         string_from_file.pop()
#     points = []
#     while len(points) * 2 != len(string_from_file):
#         point = (int(string_from_file[len(points) * 2]), int(string_from_file[len(points) * 2 + 1]))
#         points.append(point)
#     return points


def read_file():  # читает points.txt и возвращает список точек

    def type_namber(namber):  # определяет тип числа
        if namber[-1] == '.':
            namber = (int(namber[:-1]))
        elif '.' not in namber:
            namber = (int(namber))
        else:
            namber = (float(namber))
        return namber

    with open("points.txt", "r") as txt_file:
        file = txt_file.read()
    nambers_list = []
    namber = ''
    file += ' '
    for i in range(len(file)):
        symbol = file[i]
        if symbol == '-' and len(namber) == 0:
            namber += symbol
        elif symbol in ('1234567890'):
            namber += symbol
        elif symbol in (',.') and (len(namber) > 1 or len(namber) == 1 and namber != '-') and '.' not in namber:
            namber += '.'
        else:
            if len(namber) > 0 and namber != '-':
                nambers_list.append(type_namber(namber))
                namber = ''
    if len(nambers_list) % 2 != 0:
        nambers_list.pop()
    points = []
    while len(points) * 2 != len(nambers_list):
        point = ((nambers_list[len(points) * 2]), (nambers_list[len(points) * 2 + 1]))
        points.append(point)
    return points





def calculation_polygon(points):  # строит выпуклый многоугольник по точкам на координатах

    def distance_calculation(a, b):  # функция измеряет растояние между точками
        return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

    def point_falls(a, b, c):  # падает ли перпендикуляр точки c на отрезок ab
        ba, bc = (a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1])  # координаты векторов выходящих из веришины b
        ac, ab = (c[0] - a[0], c[1] - a[1]), (b[0] - a[0], b[1] - a[1])  # координаты векторов выходящих из веришины a
        if (ba[0] * bc[0] + ba[1] * bc[1]) < 0 or (ac[0] * ab[0] + ac[1] * ab[1]) < 0:  # (P1M,P1P2)<0 или (P2M,P2P1)<0
            fall = False  # перпендикуляр от точки не падает на отрезок
        else:
            fall = True  # перпендикуляр от точки падает на отрезок
        return fall

    def line_accessory(a, b, c):  # определяет лежит ли точка на отреззке, если да -- 0, иначе растояние до отрезка
        ab = distance_calculation(a, b)
        ac = distance_calculation(a, c)
        bc = distance_calculation(b, c)
        if ac + bc == ab:
            dist = 0
        else:
            if ac < bc:
                dist = ac
            else:
                dist = bc
        return dist

    def dist_colcul_point(a, b, c):  # измеряет растояние от прямой до точки
        dy = (b[1] - a[1])  # y2 - y1
        dx = (b[0] - a[0])  # x2 - x1
        d = ((b[0] * a[1]) - (b[1] * a[0]))  # x2*y1 - y2*x1
        distance = (dy * c[0] - dx * c[1] + d) / distance_calculation(a, b)
        return distance

    def triangle_definition(points):  # определение растояний между точками и сортировка их по убыванию
        max_distance = (None, None, 0)  # две точки между которыми самое большое растояние
        for a in range(len(points)):
            for b in range(a + 1, len(points)):
                new_distance = distance_calculation(points[a], points[b])
                if abs(new_distance) > abs(max_distance[2]):
                    max_distance = (points[a], points[b], new_distance)
        point_c = (None, 0)  # третья точка треугольника, котороя находиться дальше других от гипотенузы
        for point in points:
            if point != max_distance[0] and point != max_distance[1]:
                distance = dist_colcul_point(max_distance[0],max_distance[1], point)
                if abs(distance) > abs(point_c[1]):
                    point_c = (point, distance)
        return (max_distance[0],max_distance[1], point_c[0]), max_distance[2]

    def sotr_points(points, ribs_polygon, max_distance):
        other_points = []  # сортировка оставшихся точек по растоянию до треугольника, в порядке убывания
        for point in points:
            if point not in (ribs_polygon[0][0], ribs_polygon[1][0], ribs_polygon[2][0]):
                distance = abs(max_distance)
                for rib in ribs_polygon:
                    new_dist = abs(dist_colcul_point(rib[0], rib[1], point))
                    if new_dist < distance:
                        distance = new_dist
                other_points.append((point, distance))
        other_points.sort(key=lambda element: element[1])
        return other_points

    polygon, max_distance = triangle_definition(points)
    ribs_polygon = [(polygon[0], polygon[1]), (polygon[1], polygon[2]), (polygon[2], polygon[0])]  # ребра треугольника
    other_points = sotr_points(points, ribs_polygon, max_distance)
    while other_points:  # Проверяем где точки относительно polygon
        point = other_points.pop()[0]  # Берем точки из отсортировоного списка в порядке убывания
        rib = None  # выбираем ближайшее ребро
        dist = max_distance  # растояние от точки до ребра
        third_point = None  # третья точка для ориентации
        for r in ribs_polygon:  # перебираем ребра полигона в поисках ближайшего
            if point_falls(r[0], r[1], point):    # падает ли перпендикуляр точки point на ребро r
                new_dist = dist_colcul_point(r[0], r[1], point)
                if new_dist == 0:
                    new_dist = line_accessory(r[0], r[1], point)
                if abs(new_dist) < abs(dist):
                    if polygon[0] not in r:
                        third_point = polygon[0]
                    elif polygon[1] not in r:
                        third_point = polygon[1]
                    else:
                        third_point = polygon[2]
                    dist = new_dist
                    rib = r
        third_dist = dist_colcul_point(rib[0], rib[1], third_point)   # определить с какой стороны отрезка полигон
        if (third_dist < 0 and dist > 0) or (third_dist > 0 and dist < 0):
            rib_a = (rib[0], point)
            rib_b = (point, rib[1])
            index_rib = ribs_polygon.index(rib)
            ribs_polygon.pop(index_rib)
            ribs_polygon.insert(index_rib, rib_b)
            ribs_polygon.insert(index_rib, rib_a)
    return ribs_polygon


def sorted_points(polygon, points):  # возвращает два списка, первый точки полигона, второй точки внутри него
    points_of_polygon = [p[0] for p in polygon]
    points_of_polygon_x = [p[0] for p in points_of_polygon]
    points_of_polygon_y = [p[1] for p in points_of_polygon]
    other_points_x = [p[0] for p in points if p not in points_of_polygon]
    other_points_y = [p[1] for p in points if p not in points_of_polygon]
    return points_of_polygon_x, points_of_polygon_y, other_points_x, other_points_y


fig = plt.figure()
points = read_file()
polygon = calculation_polygon(points)
points_of_polygon_x, points_of_polygon_y, other_points_x, other_points_y = sorted_points(polygon, points)
points_poligon = [p[0] for p in polygon]
polygon_1 = patches.Polygon(points_poligon, facecolor='#c1d1f1', edgecolor='None' )
ax = fig.add_subplot(1, 1, 1)
ax.set_aspect("equal")
ax.grid(True, which='major', linewidth=1, linestyle='-')
ax.add_patch (polygon_1)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.plot(other_points_x, other_points_y, 'o',markerfacecolor='g', markersize=3)
plt.plot(points_of_polygon_x, points_of_polygon_y, 'o',markerfacecolor='r', markersize=3, label='x, y')
for p in polygon:
    x, y = p[0][0], p[0][1]
    plt.text(x + 2, y + 2, str((x, y)), fontsize=7)
plt.show()

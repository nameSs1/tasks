import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Point:
    """ описывает точку на координатной плоскости """
    x, y = None, None  # координаты
    kind = 'outside'  # outside, inside, on атрибут указывает где находится точка: снаружи, внутри, на многоугольнике

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y, self.kind))

    def set_kind(self, kind):
        if kind is None or kind == (0 or 'outside' or 'out'):
            self.kind = 'outside'
        elif kind == ('inside' or 'in'):
            self.kind = 'inside'
        elif kind == ('at' or 'on' or 'to' or 'included'):
            self.kind = 'on'

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y

    def dist_colcul_segment(self, segment):  # измеряет растояние от прямой до точки
        c = (self.x, self.y)
        a, b = segment.get_points()
        coordinates_a, coordinates_b = a.get_coordinates(), b.get_coordinates()
        dy = (coordinates_b[1] - coordinates_a[1])  # y2 - y1
        dx = (coordinates_b[0] - coordinates_a[0])  # x2 - x1
        d = ((coordinates_b[0] * coordinates_a[1]) - (coordinates_b[1] * coordinates_a[0]))  # x2*y1 - y2*x1
        distance = (dy * c[0] - dx * c[1] + d) / Segment.distance_calculation(a, b)
        return distance

    def check_point(self, segment):  # падает ли перпендикуляр точки на отрезок(segment)
        """ проверяет падает ли перпендикуляр точки на отрезок(segment), если нет возвращает None,
            усли падает, то возвращает расстояние до отрезка """
        a, b = segment.get_points()
        a, b = a.get_coordinates(), b.get_coordinates()
        c = (self.x, self.y)
        ba, bc = (a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1])  # координаты векторов выходящих из веришины b
        ac, ab = (c[0] - a[0], c[1] - a[1]), (b[0] - a[0], b[1] - a[1])  # координаты векторов выходящих из веришины a
        if (ba[0] * bc[0] + ba[1] * bc[1]) < 0 or (ac[0] * ab[0] + ac[1] * ab[1]) < 0:  # (P1M,P1P2)<0 или (P2M,P2P1)<0
            return None  # перпендикуляр от точки не падает на отрезок
        else:  # перпендикуляр от точки падает на отрезок
            distance = self.dist_colcul_segment(segment)
            return distance

    @staticmethod
    def find_points(file_name="points.txt"):  # метод ищет координаты точек в указаном файле.txt

        def type_namber(namber):  # определяет тип числа
            if '.' not in namber:
                return int(namber)
            else:
                return float(namber)
        def clean_namber(element):  # очистка данных (скобки, пробелы, запятые)
            element = element.replace(')', '')
            element = element.replace('(', '')
            element = element.rstrip(',')
            element = element.replace(',', '.')
            return element
        with open(file_name, "r") as txt_file:
            file = txt_file.read()
        nambers_list = file.split()
        nambers = []
        for element in nambers_list:
            element = clean_namber(element)
            nambers.append(type_namber(element))
        points = []
        while len(points) * 2 != len(nambers):
            point = ((nambers[len(points) * 2]), (nambers[len(points) * 2 + 1]))
            points.append(point)
        return points


class Segment:
    """ описывает отрезок на координатной плоскости """
    a, b = None, None  # начальная и конечная точки отрезка
    size = None  # длинна отрезка
    status_rib = 'undefined'  # статус, являеться ли отрезок ребром многоугольника
    status_max = 'undefined'  # являеться ли отрезок самым большим

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.size = self.distance_calculation(a, b)

    def __str__(self):
        return str((self.a.get_coordinates(), self.b.get_coordinates(), self.size, self.status_rib, self.status_max))

    def set_points(self, a, b):
        pass

    @staticmethod
    def distance_calculation(a, b):  # метод измеряет растояние между точками
        a = a.get_coordinates()
        b = b.get_coordinates()
        return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

    def size_calculation(self):  # возврашает длинну отрезка
        return Segment.distance_calculation(self.a, self.b)

    def get_points(self):  # метод возвращает координаты точек отрезка
        return self.a, self.b


class Polygon:
    """ описывает выпуклый многоугольник на плоскости """
    points = []
    ribs = []  # ребра многоугольника
    hypotenuse = None
    center = None  # координаты центра окружности вписанной в треугольник

    def __init__(self, points):
        self.points = list(points)
        ribs = [Segment(points[i], points[i + 1]) for i in range(len(points) - 1)]
        ribs.append(Segment(points[-1], points[0]))
        self.ribs = list(ribs)

    def get_coordinates(self):  # возвращает координаты точек многоугольника
        coordinates = [p.get_coordinates() for p in self.points]
        return coordinates

    def find_center(self):  # метод расчитывает центр окружности вписанной в треугольник
        len_ab = Segment.distance_calculation(self.points[0], self.points[1])
        len_bc = Segment.distance_calculation(self.points[1], self.points[2])
        len_ca = Segment.distance_calculation(self.points[2], self.points[0])
        a, b, c = self.points[0].get_coordinates(), self.points[1].get_coordinates(), self.points[2].get_coordinates()
        x0 = (len_bc * a[0] + len_ca * b[0] + len_ab * c[0]) / (len_ca + len_bc + len_ab)
        y0 = (len_bc * a[1] + len_ca * b[1] + len_ab * c[1]) / (len_ca + len_bc + len_ab)
        self.center = Point(x0, y0)
        self.center.kind = 'inside'

    @staticmethod
    def create_max_triangle(points):
        """ вызывает экземпляр класса Polygon, который состоит из трех точек максимально удаленных друг от друга """
        max_distance = (None, None, 0)  # две точки между которыми самое большое растояние
        for a in range(len(points)):
            for b in range(a + 1, len(points)):
                new_distance = Segment.distance_calculation(points[a], points[b])
                if abs(new_distance) > abs(max_distance[2]):
                    max_distance = (points[a], points[b], new_distance)
        point_c = (None, 0)  # третья точка треугольника, котороя находиться дальше других от гипотенузы
        hypotenuse = Segment(max_distance[0],max_distance[1])
        hypotenuse.size = max_distance[2]
        for point in points:
            if point != max_distance[0] and point != max_distance[1]:
                distance = point.dist_colcul_segment(hypotenuse)
                if abs(distance) > abs(point_c[1]):
                    point_c = (point, distance)
        triangle = Polygon((max_distance[0], max_distance[1], point_c[0]))
        triangle.hypotenuse = hypotenuse
        triangle.find_center()
        return triangle

    def sorted_points(self, points):  # сортирует точки относительно многоугольника по их удалению от ближайшего ребра
        other_points = []  # сортировка оставшихся точек по растоянию до треугольника, в порядке убывания
        coordinates_polygon = self.get_coordinates()
        for point in points:
            if point.get_coordinates() not in coordinates_polygon:
                point.distance = self.hypotenuse.size
                point.current_segment = None
                for rib in self.ribs:
                    new_dist = point.check_point(rib)
                    if new_dist is not None and abs(new_dist) < abs(point.distance):
                        point.distance = new_dist
                        point.current_segment = rib
                other_points.append(point)
        other_points.sort(key=lambda point: abs(point.distance))
        return other_points

    def add_points(self, points):
        """ добовляет точки в полигон, если они снаружи. меняет статус точек"""
        sort_points_list = self.sorted_points(points)
        while sort_points_list:
            point = sort_points_list.pop()
            rib = None  # выбираем ближайшее ребро
            dist = self.hypotenuse.size  # растояние от точки до ребра
            for r in self.ribs:
                new_dist = point.check_point(r)
                if new_dist is not None and abs(new_dist) < abs(dist):
                    dist = new_dist
                    rib = r
            center_dist = self.center.dist_colcul_segment(rib)   # определить с какой стороны отрезка полигон
            if (center_dist < 0 and dist > 0) or (center_dist > 0 and dist < 0):
                a, b = rib.get_points()
                rib_a = Segment(a, point)
                rib_b = Segment(point, b)
                index_rib = self.ribs.index(rib)
                index_point = self.points.index(b)
                self.ribs.pop(index_rib)
                self.ribs.insert(index_rib, rib_b)
                self.ribs.insert(index_rib, rib_a)
                self.points.insert(index_point, point)
                point.kind = 'on'
            else:
                point.kind = 'inside'


points_list = [Point(xy[0], xy[1]) for xy in Point.find_points()]
p = Polygon.create_max_triangle(points_list)
p.add_points(points_list)
points_inside_x = [t.get_coordinates()[0] for t in points_list if t.kind == 'inside']  # точки внутри многоугольника
points_inside_y = [t.get_coordinates()[1] for t in points_list if t.kind == 'inside']  # точки внутри многоугольника
points_of_polygon_x = [x[0] for x in p.get_coordinates()]
points_of_polygon_y = [y[1] for y in p.get_coordinates()]
# ------------- вывод многоугольника на экран-------------------------
fig = plt.figure()
polygon_1 = patches.Polygon(p.get_coordinates(), facecolor='#c1d1f1', edgecolor='None' )
ax = fig.add_subplot(1, 1, 1)
ax.set_aspect("equal")
ax.grid(True, which='major', linewidth=1, linestyle='-')
ax.add_patch (polygon_1)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.plot(points_inside_x, points_inside_y, 'o',markerfacecolor='g', markersize=3)
plt.plot(points_of_polygon_x, points_of_polygon_y, 'o',markerfacecolor='r', markersize=3, label='x, y')
for x, y in p.get_coordinates():
    plt.text(x + 2, y + 2, str((x, y)), fontsize=7)
plt.show()

import re
from dataclasses import dataclass
import heapq

INF = float("inf")
#Определяем порядковый номер метрики в картеже для выбора критерия оценки
CRITERION_NAMES = {
    "Д": 0,
    "В": 1,
    "С": 2,
}
#Определяем полное наименование метрики
CRITERION_FULL = {
    "Д": "ДЛИНА",
    "В": "ВРЕМЯ",
    "С": "СТОИМОСТЬ",
}
'''
Создание структуры ребра, в которой отражены:
    точка назначения - to
    длина пути - length
    стоимость пути - cost
'''
@dataclass
class Edge:
    to: int
    length: int
    time: int
    cost: int

    def __str__(self):
        return f" {self.to} (Д={self.length}, В={self.time}, С={self.cost})"

'''
Создание структуры графа, в который содержит словарь adj, где 
u - вершина ребра, из которой оно исходит
adj[u] - ребро из вершины u
Так как граф двунаправленный, то необходимо добавлять два ребра с одинаковой стоимостью, временем и длиной,
то есть из u в v и из v в u
'''
class Graph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, v: int):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u: int, v: int, length: int, time: int, cost: int):
        self.adj[u].append(Edge(v, length, time, cost))
        self.adj[v].append(Edge(u, length, time, cost))

    def __str__(self):
        result = []
        for u in sorted(self.adj):
            edges = ", ".join(str(e) for e in self.adj[u])
            result.append(f"{u}: {edges}")
        return "\n".join(result)

'''
Функция read_input принимает на вход название файла в виде строки и извлекают из него:
1. Названия городов и их идентификаторы
2. Ребра для создания итогового графа, определенного структурой выше
3. Запросы для создания маршрутов и параметры сортировки
'''
def read_input(filename):
    cities = {}
    city_name_to_id = {}
    graph = Graph()
    requests = []

    section = None
    try:
        with open(filename, encoding="utf-8") as f:
            for line in f:
                #Очистка строки от пробелов с начал и конца строки, пустые строки пропускаются
                line = line.strip()
                if not line:
                    continue
                #Название секции с информацией о данных
                if line.startswith("[") and line.endswith("]"):
                    section = line
                    continue
                #Выделение города и его идентификатора из секции с городами(CITIES)
                if section == "[CITIES]":
                    city_id_str, name = line.split(":", 1)
                    city_id = int(city_id_str.strip())
                    name = name.strip()

                    cities[city_id] = name
                    city_name_to_id[name] = city_id
                    graph.add_vertex(city_id)

                # Выделение точек ребра и его основных характеристик в секции ROADS
                elif section == "[ROADS]":
                    left, right = line.split(":")
                    u_str, v_str = left.split("-")

                    u = int(u_str.strip())
                    v = int(v_str.strip())

                    length, time, cost = map(int, right.split(","))

                    graph.add_edge(u, v, length, time, cost)

                # Выделение маршрута и параметров сортировки в секции REQUESTS
                elif section == "[REQUESTS]":
                    path_part, priority_part = line.split("|")

                    start_name, end_name = map(str.strip, path_part.split("->"))
                    priorities = re.findall(r"[ДВС]", priority_part)

                    requests.append((start_name, end_name, priorities))

    except FileNotFoundError:
        raise RuntimeError(f"Файл {filename} не найден")
    except ValueError:
        raise RuntimeError("Ошибка формата входных данных")

    return cities, city_name_to_id, graph, requests

'''
Функция find_optimal_path принимает на вход:
1. Граф, в котором надо найти путь, оптимизированный по параметру criterion
2. Точку отправления - start
3. Точку назначения - end
4. Номер параметра, по которому будет оптимизироваться путь
'''
def find_optimal_path(graph:Graph, start: int, end: int, criterion: int):

    if start not in graph.adj or end not in graph.adj:
        raise ValueError("Начальная или конечная вершина отсутствует в графе")

    if criterion not in (0, 1, 2):
        raise ValueError("Некорректный критерий оптимизации")

    dist = {v: INF for v in graph.adj} #Список минимальных значений по выбранному параметру
    dist[start] = 0 #Начальная точка инициализируется 0, так как в неё не должен алгоритм вернуться
    prev = {} #Кортеж предыдущих значений вершин для восстановления пути

    total_length = None
    total_time = None
    total_cost = None

    pq = [(0, start, 0, 0, 0)] #Инициализация значений для очереди, в стартовой точки расстояние, стоимость и время равны 0


    while pq: #Алгоритм продолжается, пока в очереди есть значения
        cur_weight, u, cur_length, cur_time, cur_cost = heapq.heappop(pq) #В отсортированной по убыванию очереди берется первое значение ребра с наименьшими параметрами

        if cur_weight > dist[u]:
            continue

        if u == end: #Алгоритм завершается, если достигнутна конечная точка
            total_length = cur_length
            total_time = cur_time
            total_cost = cur_cost
            break

        for e in graph.adj[u]: #Рассматриваем ребра для вершины u
            weights = [e.length, e.time, e.cost] #Извлекаем метрики ребра
            new_weight = cur_weight + weights[criterion] #Суммируем текущее значение для достигнутой точки со следующим по оптимизируемой метрике

            if new_weight < dist[e.to]:#Если полученное значение меньше определенного на прошлых шагах минимального, то обновляем минимальное значение
                dist[e.to] = new_weight
                prev[e.to] = u
                heapq.heappush(
                    pq,
                    (new_weight, e.to,cur_length + e.length,cur_time + e.time,cur_cost + e.cost)
                ) #Добавляем в очередь значения полученной новой точки

    return prev, total_length, total_time, total_cost
'''
Функция restore_path восстанавливает путь по предыдущим значения из алгоритма по поиску оптимизированного пути
'''
def restore_path(prev: dict[int, int], start: int, end: int) -> list[int]:
    path = []
    cur = end #Восстановление пути от конечной точки
    visited = set() #Посещенные вершины

    if cur not in prev:
        raise RuntimeError("Путь не существует")

    while cur != start:
        if cur in visited:
            raise RuntimeError("Цикл в prev — путь некорректен")

        visited.add(cur)
        path.append(cur)
        cur = prev[cur] #Для текущей вершины берем значение предыдущей

    path.append(start)
    path.reverse() #Так как восстановление идет от конечной точки, то необходимо перевернуть путь
    return path
'''
Функция для определения положения итогового параметра в зависимости от его порядка из запроса
'''
def compromise_key(result, priorities):
    values = {"Д": result[0], "В": result[1], "С": result[2]}
    return tuple(values[p] for p in priorities)



#Просматриваем запросы для поиска оптимального запроса
try:
    cities, city_name_to_id, graph, requests = read_input("input.txt")

    all_result = []

    for request in requests:

        start_name, end_name, priorities = request

        start_id = city_name_to_id[start_name]
        end_id = city_name_to_id[end_name]
        routes = f"{start_name} -> {end_name} | ({'|'.join(priorities)})\n"

        if start_id == end_id:
            routes += "Вы уже находитесь в конечной точке\n"
            all_result.append(routes)
            continue

        #Для каждой метрики определяем полученные значения
        results_metricks = {}

        for i in priorities:#По приоритетам вычисляем оптимальный путь
            prev, total_length, total_time, total_cost = find_optimal_path(graph, start_id, end_id, CRITERION_NAMES[i])
            #Если не нашлось предыдущих или конечная точка не лежит в предыдущих, то завершаем цикл, так как пути не существует
            try:
                path = restore_path(prev, start_id, end_id)
            except RuntimeError as e:
                routes += f"Ошибка восстановления пути: {e}\n"
                all_result.append(routes)
                break

            results_metricks[i] = (total_length, total_time, total_cost, path)

        if not results_metricks:
            continue

        #Нахождение метрики с компромиссным путем
        best_metricks = min(
            results_metricks.keys(),
            key=lambda k: compromise_key(results_metricks[k], priorities)
        )
        #Преобразование результата в текстовый формат для записи в файл
        for crit in ["Д", "В", "С"]:
            d, t, c, path = results_metricks[crit]
            route = " -> ".join(cities[v] for v in path)
            routes += f"{CRITERION_FULL[crit]}: {route} | Д={d}, В={t}, С={c}\n"

        d, t, c, path = results_metricks[best_metricks]
        route = " -> ".join(cities[v] for v in path)
        routes += f"КОМПРОМИСС: {route} | Д={d}, В={t}, С={c}\n"
        all_result.append(routes)

    # Запись результатов в итоговый файл
    with open("output.txt", "w", encoding="utf-8") as f:
        for block in all_result:
            f.write(block)
            f.write("\n\n")

except Exception as e:
    print(f"Ошибка: {e}\n")





from enum import Enum


class SelectionMechods(Enum):
    BEST = 0
    ROULETTE = 1
    TOURNAMENT = 2
    BEST_STRING = 'Najlepszych'
    ROULETTE_STRING = 'Koło ruletki'
    TOURNAMENT_STRING = 'Selekcja turniejowa'

    ALL_OPTIONS_STRING = [BEST_STRING, ROULETTE_STRING, TOURNAMENT_STRING]


class CrossingMechods(Enum):
    SINGLE_POINT = 0
    DOUBLE_POINT = 1
    TRIPLE_POINT = 2
    UNIFORM = 3
    GRAIN = 4
    SCANNING = 5
    PARTIAL = 6
    MULTIVARIATE = 7
    SINGLE_POINT_STRING = 'Krzyżowanie 1 punktowe'
    DOUBLE_POINT_STRING = 'Krzyżowanie 2 punktowe'
    TRIPLE_POINT_STRING = 'Krzyżowanie 3 punktowe'
    UNIFORM_STRING = 'Krzyżowanie jednorodne'
    GRAIN_STRING = 'Krzyżowanie ziarniste'
    SCANNING_STRING = 'Krzyżowanie skanujące'
    PARTIAL_STRING = 'Krzyżowanie częściowe'
    MULTIVARIATE_STRING = 'Krzyżowanie wielowymiarowe'

    ALL_OPTIONS_STRING = [SINGLE_POINT_STRING,
                          DOUBLE_POINT_STRING,
                          TRIPLE_POINT_STRING,
                          UNIFORM_STRING,
                          GRAIN_STRING,
                          SCANNING_STRING,
                          PARTIAL_STRING,
                          MULTIVARIATE_STRING]


class MutationMechods(Enum):
    EDGE = 0
    SINGLE_POINT = 1
    DOUBLE_POINT = 2
    EDGE_STRING = 'Brzegowa'
    SINGLE_POINT_STRING = '1 punktowa'
    DOUBLE_POINT_STRING = '2 punktowa'

    ALL_OPTIONS_STRING = [EDGE_STRING, SINGLE_POINT_STRING, DOUBLE_POINT_STRING]


class MinMax(Enum):
    MIN = 0
    MAX = 1

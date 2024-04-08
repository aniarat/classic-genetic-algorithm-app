import sys
from Consts.enums import SelectionMechods, CrossingMechods, MutationMechods, MinMax, FunctionsOptions
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLabel, QComboBox, QRadioButton, \
    QHBoxLayout

from Helpers.functions import rastrigin, schwefel
from Helpers.layout import makeSlider
from Helpers.lern import Model


class MainWindow(QWidget):
    populationSize = 40
    numberOfParents = 30
    numberOfChromosome = 24
    numberOfEpoch = 100
    crossingProb = 0.1
    mutationProb = 0.1
    numberOfDimensions = 2
    q = 1
    tournament_size = 1

    selectionName = SelectionMechods.BEST_STRING.value
    crossingName = CrossingMechods.SINGLE_POINT_STRING.value
    mutationName = MutationMechods.EDGE_STRING.value
    minmax = MinMax.MIN
    selection_method = SelectionMechods.BEST
    crossing_method = CrossingMechods.SINGLE_POINT
    mutation_method = MutationMechods.EDGE
    func = FunctionsOptions.RASTRIGIN

    def start_calc(self):
        local_model = Model(number_of_epoch=self.numberOfEpoch,
                            size_of_population=self.populationSize,
                            chromosome_length=self.numberOfChromosome,
                            number_of_parents=self.numberOfParents,
                            crossing_function=self.crossing_method,
                            mutation_function=self.mutation_method,
                            selection_function=self.selection_method,
                            crossing_probability=self.crossingProb,
                            mutation_prob=self.mutationProb,
                            number_of_dimensions=self.numberOfDimensions,
                            func=self.func,
                            title=f'{self.selectionName} - {self.crossingName}',
                            direction=self.minmax,
                            tournament_size=self.tournament_size,
                            q=self.q)
        final_string = ''
        final_string += local_model.getStartString()
        local_model.fitness()
        final_string += local_model.getEndString()
        local_model.getChats()
        self.resLabel.setText(f'Wyniki {final_string}')

    def set_selection_method(self, option: int):
        self.selection_options_label.hide()
        self.selection_options_slider.hide()
        match option:
            case SelectionMechods.BEST.value:
                self.selection_method = SelectionMechods.BEST
                self.selectionName = SelectionMechods.BEST_STRING.value
            case SelectionMechods.ROULETTE.value:
                self.selection_method = SelectionMechods.ROULETTE
                self.selectionName = SelectionMechods.ROULETTE_STRING.value
            case SelectionMechods.TOURNAMENT.value:
                self.selection_options_label.setText(f'Wielkość tunrieju {self.selection_options_slider.value()}')
                self.selection_options_label.show()
                self.selection_options_slider.valueChanged.connect(self.set_tournament_size)
                self.selection_options_slider.show()
                self.selection_method = SelectionMechods.TOURNAMENT
                self.selectionName = SelectionMechods.TOURNAMENT_STRING.value

    def set_crossing_method(self, option: int):
        self.crossing_options_label.hide()
        self.crossing_options_slider.hide()
        match option:
            case CrossingMechods.SINGLE_POINT.value:
                self.crossingName = CrossingMechods.SINGLE_POINT_STRING.value
                self.crossing_method = CrossingMechods.SINGLE_POINT
            case CrossingMechods.DOUBLE_POINT.value:
                self.crossingName = CrossingMechods.DOUBLE_POINT_STRING.value
                self.crossing_method = CrossingMechods.DOUBLE_POINT
            case CrossingMechods.TRIPLE_POINT.value:
                self.crossingName = CrossingMechods.TRIPLE_POINT_STRING.value
                self.crossing_method = CrossingMechods.TRIPLE_POINT
            case CrossingMechods.UNIFORM.value:
                self.crossingName = CrossingMechods.UNIFORM_STRING.value
                self.crossing_method = CrossingMechods.UNIFORM
            case CrossingMechods.GRAIN.value:
                self.crossingName = CrossingMechods.GRAIN_STRING.value
                self.crossing_method = CrossingMechods.GRAIN
            case CrossingMechods.SCANNING.value:
                self.crossingName = CrossingMechods.SCANNING_STRING.value
                self.crossing_method = CrossingMechods.SCANNING
            case CrossingMechods.PARTIAL.value:
                self.crossingName = CrossingMechods.PARTIAL_STRING.value
                self.crossing_method = CrossingMechods.PARTIAL
            case CrossingMechods.MULTIVARIATE.value:
                self.crossingName = CrossingMechods.MULTIVARIATE_STRING.value
                self.crossing_options_label.setText(f'q {self.crossing_options_slider.value()}')
                self.q = self.crossing_options_slider.value()
                self.crossing_options_label.show()
                self.crossing_options_slider.valueChanged.connect(self.set_q)
                self.crossing_options_slider.show()
                self.crossing_method = CrossingMechods.MULTIVARIATE

    def set_mutation_method(self, option: int):
        match option:
            case MutationMechods.EDGE.value:
                self.mutationName = MutationMechods.EDGE_STRING.value
                self.mutation_method = MutationMechods.EDGE
            case MutationMechods.SINGLE_POINT.value:
                self.mutationName = MutationMechods.SINGLE_POINT_STRING.value
                self.mutation_method = MutationMechods.SINGLE_POINT
            case MutationMechods.DOUBLE_POINT.value:
                self.mutationName = MutationMechods.DOUBLE_POINT_STRING.value
                self.mutation_method = MutationMechods.DOUBLE_POINT

    def set_population_size(self, val):
        self.populationSize = val
        self.populationSizeLabel.setText(f'Wielkość populacji {self.populationSize}')

    def set_dimensions_size(self, val):
        self.numberOfDimensions = val
        self.dimensionsSizeLabel.setText(f'Liczba wymiarów {self.numberOfDimensions}')

    def set_number_of_parents(self, val):
        self.numberOfParents = val
        self.numberOfParentsLabel.setText(f'Liczba osobników selekcji {self.numberOfParents}')

    def set_number_of_epoch(self, val):
        self.numberOfEpoch = val
        self.numberOfEpochLabel.setText(f'Liczba epok {self.numberOfEpoch}')

    def set_number_of_chromosome(self, val):
        self.numberOfChromosome = val
        self.numberOfChromosomeLabel.setText(f'Długość chromosomu {self.numberOfChromosome}')

    def set_crossing_prob(self, val):
        self.crossingProb = val / 1000
        self.crossingProbLabel.setText(f'Prawdopodobieństwo krzyżowania {self.crossingProb}')

    def set_mutation_prob(self, val):
        self.mutationProb = val / 1000
        self.mutationLabel.setText(f'Prawdopodobieństwo mutacji {self.mutationProb}')

    def set_q(self, val):
        self.crossing_options_label.setText(f'q {val}')

    def set_tournament_size(self, val):
        self.selection_options_label.setText(f'Wielkość turnieju {val}')
        self.tournament_size = val

    def set_min_max(self):
        if self.min_radio.isChecked():
            self.minmax = MinMax.MIN
        else:
            self.minmax = MinMax.MAX

    def set_function(self):
        if self.rastrigin_radio.isChecked():
            self.func = FunctionsOptions.RASTRIGIN
        else:
            self.func = FunctionsOptions.SCHWEFEK

    def __init__(self):
        super().__init__()

        self.setWindowTitle("OE Proj 2. Wieczorek, Piwko, Ratowska")
        layout_items = []

        function_label = QLabel("Wybierz funkcję:")
        layout_items.append(function_label)

        function_layout = QHBoxLayout()
        self.rastrigin_radio = QRadioButton("Rastrigin")
        self.rastrigin_radio.setChecked(True)
        self.rastrigin_radio.toggled.connect(self.set_function)
        function_layout.addWidget(self.rastrigin_radio)

        self.schwefel_radio = QRadioButton("Schwefel")
        self.schwefel_radio.toggled.connect(self.set_function)
        function_layout.addWidget(self.schwefel_radio)

        function_container = QWidget()  # Tworzymy kontener dla układu w poziomie
        function_container.setLayout(function_layout)  # Ustawiamy układ w poziomie w kontenerze

        layout_items.append(function_container)  # Dodajemy kontener do głównego układu

        # MinMax selection
        minmax_label = QLabel("Szukaj:")
        layout_items.append(minmax_label)

        minmax_layout = QHBoxLayout()
        self.min_radio = QRadioButton("Minimum")
        self.min_radio.setChecked(True)
        self.min_radio.toggled.connect(self.set_min_max)
        minmax_layout.addWidget(self.min_radio)

        self.max_radio = QRadioButton("Maksimum")
        self.max_radio.toggled.connect(self.set_min_max)
        minmax_layout.addWidget(self.max_radio)

        minmax_container = QWidget()  # Tworzymy kontener dla układu w poziomie
        minmax_container.setLayout(minmax_layout)  # Ustawiamy układ w poziomie w kontenerze

        layout_items.append(minmax_container)

        # Number of dimentions
        self.dimensionsSizeLabel = QLabel(f'Liczba wymiarów {self.numberOfDimensions}')
        layout_items.append(self.dimensionsSizeLabel)

        dimensions_size_slider = makeSlider(1, 10, self.numberOfDimensions)
        dimensions_size_slider.valueChanged.connect(self.set_dimensions_size)
        layout_items.append(dimensions_size_slider)

        # Population Size
        self.populationSizeLabel = QLabel(f'Wielkość populacji {self.populationSize}')
        layout_items.append(self.populationSizeLabel)

        population_size_slider = makeSlider(10, 1000, self.populationSize)
        population_size_slider.valueChanged.connect(self.set_population_size)
        layout_items.append(population_size_slider)

        # Parents
        self.numberOfParentsLabel = QLabel(f'Liczba osobników selekcji {self.numberOfParents}')
        layout_items.append(self.numberOfParentsLabel)

        num_of_parents_slider = makeSlider(10, 1000, self.numberOfParents)
        num_of_parents_slider.valueChanged.connect(self.set_number_of_parents)
        layout_items.append(num_of_parents_slider)

        # Chromosome
        self.numberOfChromosomeLabel = QLabel(f'Długość chromosomu {self.numberOfChromosome}')
        layout_items.append(self.numberOfChromosomeLabel)

        num_of_chromosome_slider = makeSlider(1, 64, self.numberOfChromosome)
        num_of_chromosome_slider.valueChanged.connect(self.set_number_of_chromosome)
        layout_items.append(num_of_chromosome_slider)

        # Epoch
        self.numberOfEpochLabel = QLabel(f'Liczba epok {self.numberOfEpoch}')
        layout_items.append(self.numberOfEpochLabel)

        num_of_epoch_slider = makeSlider(1, 10_000, self.numberOfEpoch)
        num_of_epoch_slider.valueChanged.connect(self.set_number_of_epoch)
        layout_items.append(num_of_epoch_slider)

        self.crossingProbLabel = QLabel(f'Prawdopodobieństwo krzyżowania {self.crossingProb}')
        layout_items.append(self.crossingProbLabel)

        crossing_prob_slider = makeSlider(1, 1000, self.crossingProb * 1000)
        crossing_prob_slider.valueChanged.connect(self.set_crossing_prob)
        layout_items.append(crossing_prob_slider)

        # Selection
        selection_method_label = QLabel('Wybierz metodę selekcji')
        layout_items.append(selection_method_label)

        selection_combo_box = QComboBox(self)
        selection_combo_box.addItems(SelectionMechods.ALL_OPTIONS_STRING.value)

        selection_combo_box.currentIndexChanged.connect(self.set_selection_method)
        layout_items.append(selection_combo_box)

        self.selection_options_label = QLabel('')
        self.selection_options_label.hide()
        layout_items.append(self.selection_options_label)
        self.selection_options_slider = makeSlider(1, 10, 1)
        self.selection_options_slider.hide()
        layout_items.append(self.selection_options_slider)

        # Crossing
        selection_method_label = QLabel('Wybierz formę krzyżowania')
        layout_items.append(selection_method_label)

        crossing_combo_box = QComboBox(self)

        crossing_combo_box.addItems(CrossingMechods.ALL_OPTIONS_STRING.value)

        crossing_combo_box.currentIndexChanged.connect(self.set_crossing_method)
        layout_items.append(crossing_combo_box)

        self.crossing_options_label = QLabel('')
        self.crossing_options_label.hide()
        layout_items.append(self.crossing_options_label)
        self.crossing_options_slider = makeSlider(1, 10, 1)
        self.crossing_options_slider.hide()
        layout_items.append(self.crossing_options_slider)

        # Mutations
        mutation_label = QLabel('Wybierz formę mutacji')
        layout_items.append(mutation_label)

        mutation_combo_box = QComboBox(self)

        mutation_combo_box.addItems(MutationMechods.ALL_OPTIONS_STRING.value)

        mutation_combo_box.currentIndexChanged.connect(self.set_mutation_method)
        layout_items.append(mutation_combo_box)

        self.mutationLabel = QLabel(f'Prawdopodobieństwo mutacji {self.mutationProb}')
        layout_items.append(self.mutationLabel)

        mutation_slider = makeSlider(1, 1000, self.mutationProb * 1000)
        mutation_slider.valueChanged.connect(self.set_mutation_prob)
        layout_items.append(mutation_slider)

        # Start
        button = QPushButton("Oblicz")
        button.clicked.connect(self.start_calc)
        layout_items.append(button)

        # retrun of learn
        self.resLabel = QLabel('Wyniki:')
        layout_items.append(self.resLabel)

        layout = QVBoxLayout()

        for item in layout_items:
            layout.addWidget(item)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()

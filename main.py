import sys
from Consts.enums import SelectionMechods, CrossingMechods, MutationMechods, InversionMethods, MinMax
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QSlider, QLabel, QComboBox, QCheckBox, QRadioButton, QHBoxLayout

from Helpers.functions import rastrigin, schwefel
from Helpers.layout import makeSlider
from Helpers.lern import Model

from Helpers.selectionMethods import BestSelection, RouletteWheelSelection, TournamentSelection
from Helpers.crossingMethods import SinglePointCrossover, TwoPointCrossover, ThreePointCrossover, UniformCrossover, \
    GrainCrossover, ScanningCrossover, PartialCopyCrossover, MultivariateCrossover

from Helpers.mutationMethods import EdgeMutation, SinglePointMutation, TwoPointMutation
from Helpers.inversionMethod import InversionMethod

class MainWindow(QWidget):
    populationSize = 40
    numberOfParents = 30
    numberOfChromosome = 24
    numberOfEpoch = 100
    crossingProb = 0.1
    mutationProb = 0.1
    inversionProb = 0.1
    numberOfDimensions = 2

    selectionName = SelectionMechods.BEST_STRING.value
    crossingName = CrossingMechods.SINGLE_POINT_STRING.value
    mutationName = MutationMechods.EDGE_STRING.value
    inversionName = InversionMethods.TWO_POINT_STRING.value
    minmax = MinMax.MIN

    selection_method = BestSelection(2).select
    crossing_method = SinglePointCrossover(2).crossover
    mutation_method = EdgeMutation(2).mutate
    inversion_method = InversionMethod(2).inverse

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
                            inversion_prob = self.inversionProb,
                            inversion_function = self.inversion_method,
                            number_of_dimensions=self.numberOfDimensions,
                            func=rastrigin(self.numberOfDimensions),
                            title=f'{self.selectionName} - {self.crossingName}',
                            direction=self.minmax)
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
                self.selection_method = BestSelection(
                    self.numberOfDimensions).select if self.minmax == MinMax.MIN else BestSelection(
                    self.numberOfDimensions).maxSelect
                self.selectionName = SelectionMechods.BEST_STRING.value
            case SelectionMechods.ROULETTE.value:
                self.selection_method = RouletteWheelSelection(self.numberOfDimensions).select
                self.selectionName = SelectionMechods.ROULETTE_STRING.value
            case SelectionMechods.TOURNAMENT.value:
                self.selection_options_label.setText(f'Wielkość tunrieju {self.selection_options_slider.value()}')
                self.selection_options_label.show()
                self.selection_options_slider.valueChanged.connect(self.set_tournament_size)
                self.selection_options_slider.show()
                self.selection_method = TournamentSelection(
                    self.selection_options_slider.value(),
                    self.numberOfDimensions).select if self.minmax == MinMax.MIN else TournamentSelection(
                    self.selection_options_slider.value(),
                    self.numberOfDimensions).maxSelect
                self.selectionName = SelectionMechods.TOURNAMENT_STRING.value

    def set_crossing_method(self, option: int):
        self.crossing_options_label.hide()
        self.crossing_options_slider.hide()
        match option:
            case CrossingMechods.SINGLE_POINT.value:
                self.crossing_method = SinglePointCrossover(self.numberOfDimensions).crossover
                self.crossingName = CrossingMechods.SINGLE_POINT_STRING.value
            case CrossingMechods.DOUBLE_POINT.value:
                self.crossingName = CrossingMechods.DOUBLE_POINT_STRING.value
                self.crossing_method = TwoPointCrossover(self.numberOfDimensions).crossover
            case CrossingMechods.TRIPLE_POINT.value:
                self.crossingName = CrossingMechods.TRIPLE_POINT_STRING.value
                self.crossing_method = ThreePointCrossover(self.numberOfDimensions).crossover
            case CrossingMechods.UNIFORM.value:
                self.crossingName = CrossingMechods.UNIFORM_STRING.value
                probability = self.crossingProb
                self.crossing_method = UniformCrossover(probability, self.numberOfDimensions).crossover
            case CrossingMechods.GRAIN.value:
                self.crossingName = CrossingMechods.GRAIN_STRING.value
                self.crossing_method = GrainCrossover(self.numberOfDimensions).crossover
            case CrossingMechods.SCANNING.value:
                self.crossingName = CrossingMechods.SCANNING_STRING.value
                num_parents = self.numberOfParents
                self.crossing_method = ScanningCrossover(num_parents, self.numberOfDimensions).crossover
            case CrossingMechods.PARTIAL.value:
                self.crossingName = CrossingMechods.PARTIAL_STRING.value
                self.crossing_method = PartialCopyCrossover(self.numberOfDimensions).crossover
            case CrossingMechods.MULTIVARIATE.value:
                self.crossingName = CrossingMechods.MULTIVARIATE_STRING.value
                self.crossing_options_label.setText(f'q {self.crossing_options_slider.value()}')
                self.crossing_options_label.show()
                self.crossing_options_slider.valueChanged.connect(self.set_q)
                self.crossing_options_slider.show()
                self.crossing_method = MultivariateCrossover(self.crossingProb,
                                                             self.crossing_options_slider.value(),
                                                             self.numberOfDimensions).crossover

    def set_mutation_method(self, option: int):
        match option:
            case MutationMechods.EDGE.value:
                self.mutationName = MutationMechods.EDGE_STRING.value
                self.mutation_method = EdgeMutation(self.numberOfDimensions).mutate
            case MutationMechods.SINGLE_POINT.value:
                self.mutationName = MutationMechods.SINGLE_POINT_STRING.value
                self.mutation_method = SinglePointMutation(self.numberOfDimensions).mutate
            case MutationMechods.DOUBLE_POINT.value:
                self.mutationName = MutationMechods.DOUBLE_POINT_STRING.value
                self.mutation_method = TwoPointMutation(self.numberOfDimensions).mutate

    def set_inversion_method(self, option: int):
        match option:
            case InversionMethods.TWO_POINT.value:
                self.inversionName = InversionMethods.TWO_POINT_STRING.value
                self.inversion_method = InversionMethod(self.numberOfDimensions).inverse

    def set_population_size(self, val):
        self.populationSize = val
        self.populationSizeLabel.setText(f'Wielkość populacji {self.populationSize}')

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

    def set_inversion_prob(self, val):
        self.inversionProb = val / 1000
        self.inversionProbLabel.setText(f'Prawdopodobieństwo inwersji {self.inversionProb}')

    def set_q(self, val):
        self.crossing_options_label.setText(f'q {val}')
        self.crossing_method = MultivariateCrossover(self.crossingProb, val, self.numberOfDimensions).crossover

    def set_tournament_size(self, val):
        self.selection_options_label.setText(f'Wielkość turnieju {val}')
        self.selection_method = TournamentSelection(val, self.numberOfDimensions).select

    def set_min_max(self):
        if self.min_radio.isChecked():
            self.minmax = MinMax.MIN
        else:
            self.minmax = MinMax.MAX

    def set_function(self):
        if self.rastrigin_radio.isChecked():
            self.func = rastrigin(self.numberOfDimensions)
        else:
            self.func = schwefel(self.numberOfDimensions)


    def __init__(self):
        super().__init__()

        self.setWindowTitle("OE Proj 2. Wieczorek, Piwko, Ratowska")
        layout_items = []
        button = QPushButton("Oblicz")
        button.clicked.connect(self.start_calc)
        layout_items.append(button)


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

        # Inversion
        self.inversionProbLabel = QLabel(f'Prawdopodobieństwo inwersji {self.inversionProb}')
        layout_items.append(self.inversionProbLabel)

        inversion_prob_slider = makeSlider(1, 1000, self.inversionProb * 1000)
        inversion_prob_slider.valueChanged.connect(self.set_inversion_prob)
        layout_items.append(inversion_prob_slider)

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

         # Inwersja
        inversion_label = QLabel('Wybierz formę inwersji')
        layout_items.append(inversion_label)

        inversion_combo_box = QComboBox(self)

        inversion_combo_box.addItems(InversionMethods.ALL_OPTIONS_STRING.value)

        inversion_combo_box.currentIndexChanged.connect(self.set_inversion_method)
        layout_items.append(inversion_combo_box)

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

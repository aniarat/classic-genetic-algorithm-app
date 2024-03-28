import sys
from Consts.enums import SelectionMechods, CrossingMechods, MutationMechods
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QSlider, QLabel, QComboBox

from Helpers.layout import makeSlider
from Helpers.lern import lern
from Helpers.mutationMethods import test_mutation

from Helpers.selectionMethods import BestSelection, RouletteWheelSelection, TournamentSelection
from Helpers.crossingMethods import SinglePointCrossover, TwoPointCrossover, ThreePointCrossover, UniformCrossover, \
    GrainCrossover, ScanningCrossover, PartialCopyCrossover, MultivariateCrossover


def f(x):
    return x ** 2 - 4 * x + 3


class MainWindow(QWidget):
    populationSize = 40
    numberOfParents = 10
    numberOfChromosome = 24
    numberOfEpoch = 100
    crossingProb = 0.1
    mutationProb = 0.1

    selection_method = BestSelection().select
    crossing_method = SinglePointCrossover().crossover

    def start_calc(self):
        lern(number_of_epoch=self.numberOfEpoch,
             size_of_population=self.populationSize,
             chromosome_length=self.numberOfChromosome,
             number_of_parents=self.numberOfParents,
             crossing_function=self.crossing_method,
             mutation_function=test_mutation,
             selection_function=self.selection_method,
             F=f)

    def set_selection_method(self, option: int):
        match option:
            case SelectionMechods.BEST.value:
                self.selection_method = BestSelection().select
            case SelectionMechods.ROULETTE.value:
                self.selection_method = RouletteWheelSelection().select
            case SelectionMechods.TOURNAMENT.value:
                tournament_size = 3
                self.selection_method = TournamentSelection(tournament_size).select

    def set_crossing_method(self, option: int):
        match option:
            case CrossingMechods.SINGLE_POINT.value:
                self.crossing_method = SinglePointCrossover().crossover
            case CrossingMechods.DOUBLE_POINT.value:
                self.crossing_method = TwoPointCrossover().crossover
            case CrossingMechods.TRIPLE_POINT.value:
                self.crossing_method = ThreePointCrossover().crossover
            case CrossingMechods.UNIFORM.value:
                probability = self.crossingProb
                self.crossing_method = UniformCrossover(probability).crossover
            case CrossingMechods.GRAIN.value:
                self.crossing_method = GrainCrossover().crossover
            case CrossingMechods.SCANNING.value:
                num_parents = self.numberOfParents
                self.crossing_method = ScanningCrossover(num_parents).crossover
            case CrossingMechods.PARTIAL.value:
                self.crossing_method = PartialCopyCrossover().crossover
            case CrossingMechods.MULTIVARIATE.value:
                probability = self.crossingProb
                q = 3
                self.crossing_method = MultivariateCrossover(probability, q).crossover

    def set_mutation_method(self, option: int):
        # TODO: Dodać implementacje
        match option:
            case MutationMechods.EDGE.value:
                print(option)
            case MutationMechods.SINGLE_POINT.value:
                print(option)
            case MutationMechods.DOUBLE_POINT.value:
                print(option)

    def set_population_size(self, val):
        self.populationSize = val
        self.populationSizeLabel.setText(f'Wielkość populacji {self.populationSize}')

    def set_number_of_parents(self, val):
        self.numberOfParents = val
        self.numberOfParentsLabel.setText(f'Ilość rodziców {self.numberOfParents}')

    def set_number_of_epoch(self, val):
        self.numberOfEpoch = val
        self.numberOfEpochLabel.setText(f'Ilość epok {self.numberOfEpoch}')

    def set_number_of_hromosome(self, val):
        self.numberOfChromosome = val
        self.numberOfChromosomeLabel.setText(f'Długość hromosomu {self.numberOfChromosome}')

    def set_corossing_prob(self, val):
        self.crossingProb = val / 1000
        self.crossingProbLabel.setText(f'Prawdopodobieństwo krzyżowania {self.crossingProb}')

    def set_mutation_prob(self, val):
        self.mutationProb = val / 1000
        self.mutationLabel.setText(f'Prawdopodobieństwo mutacji {self.mutationProb}')

    def __init__(self):
        super().__init__()
        self.selection_function = None
        self.crossing_function = None

        self.setWindowTitle("OE Proj 2. Wieczorek, Piwko, Ratowska")
        layout_items = []
        button = QPushButton("Oblicz")
        button.clicked.connect(self.start_calc)
        layout_items.append(button)

        # Population Size
        self.populationSizeLabel = QLabel(f'Wielkość populacji {self.populationSize}')
        layout_items.append(self.populationSizeLabel)

        population_size_slider = makeSlider(1, 1000, self.populationSize)
        population_size_slider.valueChanged.connect(self.set_population_size)
        layout_items.append(population_size_slider)

        # Parents
        self.numberOfParentsLabel = QLabel(f'Ilość rodziców {self.numberOfParents}')
        layout_items.append(self.numberOfParentsLabel)

        num_of_parents_slider = makeSlider(1, 100, self.numberOfParents)
        num_of_parents_slider.valueChanged.connect(self.set_number_of_parents)
        layout_items.append(num_of_parents_slider)

        # Chromosome
        self.numberOfChromosomeLabel = QLabel(f'Długość hromosomu {self.numberOfChromosome}')
        layout_items.append(self.numberOfChromosomeLabel)

        num_of_chromosome_slider = makeSlider(1, 64, self.numberOfChromosome)
        num_of_chromosome_slider.valueChanged.connect(self.set_number_of_hromosome)
        layout_items.append(num_of_chromosome_slider)

        # Epoch
        self.numberOfEpochLabel = QLabel(f'Ilość epok {self.numberOfEpoch}')
        layout_items.append(self.numberOfEpochLabel)

        num_of_epoch_slider = makeSlider(1, 1000, self.numberOfEpoch)
        num_of_epoch_slider.valueChanged.connect(self.set_number_of_epoch)
        layout_items.append(num_of_epoch_slider)

        self.crossingProbLabel = QLabel(f'Prawdopodobieństwo krzyżowania {self.crossingProb}')
        layout_items.append(self.crossingProbLabel)

        crossing_prob_slider = makeSlider(1, 1000, self.crossingProb * 1000)
        crossing_prob_slider.valueChanged.connect(self.set_corossing_prob)
        layout_items.append(crossing_prob_slider)

        # Selection
        selection_method_label = QLabel('Wybierz metode selekcji')
        layout_items.append(selection_method_label)

        selection_combo_box = QComboBox(self)
        selection_combo_box.addItems(SelectionMechods.ALL_OPTIONS_STRING.value)

        selection_combo_box.currentIndexChanged.connect(self.set_selection_method)
        layout_items.append(selection_combo_box)

        # Crossing
        selection_method_label = QLabel('Wybierz forme krzyżowania')
        layout_items.append(selection_method_label)

        crossing_combo_box = QComboBox(self)

        crossing_combo_box.addItems(CrossingMechods.ALL_OPTIONS_STRING.value)

        crossing_combo_box.currentIndexChanged.connect(self.set_crossing_method)
        layout_items.append(crossing_combo_box)

        # Mutations
        mutation_label = QLabel('Wybierz forme mutacji')
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

        layout = QVBoxLayout()

        for item in layout_items:
            layout.addWidget(item)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()

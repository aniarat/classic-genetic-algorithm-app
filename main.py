import sys
import random
import numpy as np
from Helpers.decimalBinaryMath import binary_to_decimal

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QSlider, QLabel, \
    QRadioButton, QButtonGroup

from Helpers.lern import lern
from Helpers.mutationMethods import test_mutation
from Helpers.parents import initParents, printParents

from Helpers.selectionMethods import BestSelection, RouletteWheelSelection, TournamentSelection
from Helpers.crossingMethods import SinglePointCrossover, TwoPointCrossover, ThreePointCrossover, UniformCrossover, GrainCrossover, ScanningCrossover, PartialCopyCrossover, MultivariateCrossover


def f(x):
    return x**2 - 4*x + 3
class MainWindow(QWidget):
  
    populationSize = 40
    numberOfParents = 10
    numberOfHromosome = 24
    numberOfEpoch = 100
    corssingProb = 0.1
    mutationProb = 0.1
    

    def start_calc(self):
        lern(number_of_epoch = self.numberOfEpoch,
            size_of_population = self.populationSize,
            chromsome_length = self.numberOfHromosome,
            number_of_parents = self.numberOfParents,
            crossing_function = self.crossing_function,
            mutation_function = test_mutation,
            selection_function=self.selection_function,
            F = f)
        
    def set_selection_method(self, button: QRadioButton):
        population = [np.random.randint(0, 2, self.numberOfHromosome) for _ in range(self.populationSize)]
     
        fitness_values = [f(binary_to_decimal(individual)) for individual in population]
     
        match button.text():
            case "Najlepszych":
                selection_method = BestSelection()
            case "Koło ruletki":
                selection_method = RouletteWheelSelection()
            case "Selekcja turniejowa":
                tournament_size = 3
                selection_method = TournamentSelection(tournament_size)

        self.selection_function = selection_method.select(population, fitness_values, self.numberOfParents)
        
    def set_crossing_method(self, button: QRadioButton):
        selected_population = self.selection_function

        match button.text():
            case "Krzyżowanie 1 punktowe":
                crossing_method = SinglePointCrossover()
            case "Krzyżowanie 2 punktowe":
                crossing_method = TwoPointCrossover()
            case "Krzyżowanie 3 punktowe":
                crossing_method = ThreePointCrossover()
            case "Krzyżowanie jednorodne":
                probability = self.corssingProb
                crossing_method = UniformCrossover(probability)
            case "Krzyżowanie ziarniste":
                crossing_method = GrainCrossover()
            case "Krzyżowanie skanujące":
                num_parents = self.numberOfParents
                crossing_method = ScanningCrossover(num_parents)
            case "Krzyżowanie częściowe":
                crossing_method = PartialCopyCrossover()
            case "Krzyżowanie wielowymiarowe":
                probability = self.corssingProb
                q = 3
                crossing_method = MultivariateCrossover(probability, q)

        self.crossing_function = crossing_method.crossover(selected_population)

    def set_mutation_method(self, button: QRadioButton):
        #TODO: Dodać implementacje
        match button.text():
            case "Brzegowa":
                print(button.text())
            case "1 punktowa":
                print(button.text())
            case "2 punktowa":
                print(button.text())
# Test

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
        self.numberOfHromosome = val
        self.numberOfHromosomeLabel.setText(f'Długość hromosomu {self.numberOfHromosome}')
    def set_corossing_prob(self, val):
        self.corssingProb = val/1000
        self.crossingProbLabel.setText(f'Prawdopodobieństwo krzyżowania {self.corssingProb}')
    def set_mutation_prob(self, val):
        self.mutationProb = val/1000
        self.mutationLabel.setText(f'Prawdopodobieństwo mutacji {self.mutationProb}')
    def __init__(self):
        super().__init__()
        self.selection_function = None
        self.crossing_function = None

        self.setWindowTitle("OE Proj 2. Wieczorek, Piwko, Ratowska")
        layoutItems = []
        button = QPushButton("Oblicz")
        button.clicked.connect(self.start_calc)
        layoutItems.append(button)

        #Wielkośc populacji
        self.populationSizeLabel = QLabel(f'Wielkość populacji {self.populationSize}')
        layoutItems.append(self.populationSizeLabel)

        populationSizeSlider = QSlider(Qt.Horizontal)
        populationSizeSlider.setMinimum(1)
        populationSizeSlider.setMaximum(1000)
        populationSizeSlider.setValue(self.populationSize)
        populationSizeSlider.valueChanged.connect(self.set_population_size)
        layoutItems.append(populationSizeSlider)

        # Paretns
        self.numberOfParentsLabel = QLabel(f'Ilość rodziców {self.numberOfParents}')
        layoutItems.append(self.numberOfParentsLabel)

        numOfParentsSlider = QSlider(Qt.Horizontal)
        numOfParentsSlider.setMinimum(1)
        numOfParentsSlider.setMaximum(100)
        numOfParentsSlider.setValue(self.numberOfParents)
        numOfParentsSlider.valueChanged.connect(self.set_number_of_parents)
        layoutItems.append(numOfParentsSlider)

        # Hromosome
        self.numberOfHromosomeLabel = QLabel(f'Długość hromosomu {self.numberOfHromosome}')
        layoutItems.append(self.numberOfHromosomeLabel)

        numOfHromosomeSlider = QSlider(Qt.Horizontal)
        numOfHromosomeSlider.setMinimum(1)
        numOfHromosomeSlider.setMaximum(64)
        numOfHromosomeSlider.setValue(self.numberOfHromosome)
        numOfHromosomeSlider.valueChanged.connect(self.set_number_of_hromosome)
        layoutItems.append(numOfHromosomeSlider)


        # Epoch
        self.numberOfEpochLabel = QLabel(f'Ilość epok {self.numberOfEpoch}')
        layoutItems.append(self.numberOfEpochLabel)

        numOfEpochSlider = QSlider(Qt.Horizontal)
        numOfEpochSlider.setMinimum(1)
        numOfEpochSlider.setMaximum(1000)
        numOfEpochSlider.setValue(self.numberOfEpoch)
        numOfEpochSlider.valueChanged.connect(self.set_number_of_epoch)
        layoutItems.append(numOfEpochSlider)

        self.crossingProbLabel = QLabel(f'Prawdopodobieństwo krzyżowania {self.corssingProb}')
        layoutItems.append(self.crossingProbLabel)

        corssingProbSlider = QSlider(Qt.Horizontal)
        corssingProbSlider.setMinimum(1)
        corssingProbSlider.setMaximum(1000)
        corssingProbSlider.setValue(self.corssingProb*1000)
        corssingProbSlider.valueChanged.connect(self.set_corossing_prob)
        layoutItems.append(corssingProbSlider)


        # Metoda Selekcji
        selectinMetchodLabel = QLabel('Wybierz metode selekcji')
        layoutItems.append(selectinMetchodLabel)
        selectionMetchodGroup = QButtonGroup(self)

        rMs1 = QRadioButton("Najlepszych", self)
        rMs2 = QRadioButton("Koło ruletki", self)
        rMs3 = QRadioButton("Selekcja turniejowa", self)
        rMs1.setChecked(True)
        selectionMetchodGroup.addButton(rMs1)
        selectionMetchodGroup.addButton(rMs2)
        selectionMetchodGroup.addButton(rMs3)

        selectionMetchodGroup.buttonClicked.connect(self.set_selection_method)

        layoutItems.append(rMs1)
        layoutItems.append(rMs2)
        layoutItems.append(rMs3)


        # Krzyżowanie
        selectinMetchodLabel = QLabel('Wybierz forme krzyżowania')
        layoutItems.append(selectinMetchodLabel)
        crossingGroup = QButtonGroup(self)

        rK1 = QRadioButton("Krzyżowanie 1 punktowe", self)
        rK2 = QRadioButton("Krzyżowanie 2 punktowe", self)
        rK3 = QRadioButton("Krzyżowanie 3 punktowe", self)
        rK4 = QRadioButton("Krzyżowanie jednorodne", self)
        rK5 = QRadioButton("Krzyżowanie ziarniste", self)
        rK6 = QRadioButton("Krzyżowanie skanujące", self)
        rK7 = QRadioButton("Krzyżowanie częściowe", self)
        rK8 = QRadioButton("Krzyżowanie wielowymiarowe", self)
        rK1.setChecked(True)
        crossingGroup.addButton(rK1)
        crossingGroup.addButton(rK2)
        crossingGroup.addButton(rK3)
        crossingGroup.addButton(rK4)
        crossingGroup.addButton(rK5)
        crossingGroup.addButton(rK6)
        crossingGroup.addButton(rK7)
        crossingGroup.addButton(rK8)

        crossingGroup.buttonClicked.connect(self.set_crossing_method)

        layoutItems.append(rK1)
        layoutItems.append(rK2)
        layoutItems.append(rK3)
        layoutItems.append(rK4)
        layoutItems.append(rK5)
        layoutItems.append(rK6)
        layoutItems.append(rK7)
        layoutItems.append(rK8)


        


        # Mutacje
        mutationLabel = QLabel('Wybierz forme mutacji')
        layoutItems.append(mutationLabel)
        mutationGroup = QButtonGroup(self)

        rMut1 = QRadioButton("Brzegowa", self)
        rMut2 = QRadioButton("1 punktowa", self)
        rMut3 = QRadioButton("2 punktowa", self)
        rMut1.setChecked(True)
        mutationGroup.addButton(rMut1)
        mutationGroup.addButton(rMut2)
        mutationGroup.addButton(rMut3)

        mutationGroup.buttonClicked.connect(self.set_mutation_method)

        layoutItems.append(rMut1)
        layoutItems.append(rMut2)
        layoutItems.append(rMut3)
        self.mutationLabel = QLabel(f'Prawdopodobieństwo mutacji {self.mutationProb}')
        layoutItems.append(self.mutationLabel)

        mutationSlider = QSlider(Qt.Horizontal)
        mutationSlider.setMinimum(1)
        mutationSlider.setMaximum(1000)
        mutationSlider.setValue(self.mutationProb*1000)
        mutationSlider.valueChanged.connect(self.set_mutation_prob)
        layoutItems.append(mutationSlider)

        layout = QVBoxLayout()

        for item in layoutItems:
            layout.addWidget(item)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


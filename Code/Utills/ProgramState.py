
from Neuron.Neuron import PerceptronSigmoid
class programStates:
    def __init__(self):     
        self.perceptron = PerceptronSigmoid(eta=0.001, epochs=400, isVisibility=True)
        self.sciezka_do_obrazka = None
        self.ImageLoaderObject =  None
        self.status_label = None
    pass

ProgramStates = programStates()
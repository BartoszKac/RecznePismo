from Neuron import PerceptronSigmoid
from Utills.LoadData import Loader
from Utills.WeightSave import WeightManager
import numpy as np

loader = Loader('data/letters-train-images', 'data/letters-train-labels')
#loader1 =  Loader('data/Timage','data/Ttest') 
#loader = Loader('data/mnist-train-images', 'data/mnist-train-labels')


X = np.array([
    [2, 4,  20],
    [4, 3, -10],
    [5, 6,  13],
    [5, 4,   8],
    [3, 4,   5],
])

# Zamiana etykiet z [-1, 1] na [0, 1]WWWWWWWWWWWWWWW
#y = np.array([1, 0, 0, 1, 0])
xx = loader.getVector()
yy = loader.getClasTarget()
perceptron = PerceptronSigmoid(eta=0.001, epochs=15, isVisibility=True)
#print(perceptron.CountClass(loader.getClasTarget()))
#print("Pierwsza litera ",loader1.getVector(0).size)

#x = np.random.rand(len(perceptron.CountClass(loader.getClasTarget()) ),len(loader.getVector(0)) )
#print(np.round(x,11))
perceptron.fit(xx, yy)
#print("Final weights:", perceptron.w)
wm = WeightManager("WagiCyfrA-z")

wm.save_weights(perceptron.w)
#perceptron.w = wm.load_weights()
#perceptron.predict(loader1.getVector(0))
#print(perceptron.w)

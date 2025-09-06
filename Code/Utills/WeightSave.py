import numpy as np

class WeightManager:
    def __init__(self, filename="weights.npy"):
        self.filename = filename

    def save_weights(self, weights):
       
        if not isinstance(weights, np.ndarray) or weights.ndim != 2:
            raise ValueError("Podana zmienna musi być macierzą 2D typu numpy.ndarray.")
        
        np.save(self.filename, weights)
        print(f"Wagi zapisane do pliku: {self.filename}")

    def load_weights(self):
      
        try:
            weights = np.load(self.filename)
            print(f"Wagi odczytane z pliku: {self.filename}")
            return weights
        except FileNotFoundError:
            print(f"Plik {self.filename} nie istnieje.")
            return None

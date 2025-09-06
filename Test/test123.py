import numpy as np
import matplotlib.pyplot as plt
from LoadData import Loader
from WeightSave import WeightManager

class PerceptronSigmoid:
    def __init__(self, eta, epochs, isVisibility=False):
        self.eta = eta
        self.epochs = epochs
        self.isVisibility = isVisibility
        self.list_of_Error = []
        self.w = np.empty((0, 0))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict(self, x):
        if len(x.shape) == 1:
            x = np.append(x, 1)  # dodaj bias
        total_simulation = np.dot(x, self.w)
        y_pred = self.sigmoid(total_simulation)
        return y_pred

    def predict_class(self, x):
        y_pred = self.predict(x)
        predicted_class = np.argmax(y_pred) + 1  # Zakładamy klasy od 1
        return predicted_class, y_pred

    def CountClass(self, Y):
        return list(np.unique(Y.astype(int)))

    def fit(self, X, Y):
        all_classes = self.CountClass(Y)
        self.list_of_Error = []

        ones = np.ones((X.shape[0], 1))
        x_1 = np.append(X.copy(), ones, axis=1)

        self.w = np.random.rand(x_1.shape[1], len(all_classes))

        for e in range(self.epochs):
            total_loss = 0.0
            for i, (x, y_target) in enumerate(zip(x_1, Y)):
                y_pred = self.predict(x)

                y_target = int(y_target)
                y_true = np.zeros(len(all_classes))
                y_true[y_target - 1] = 1

                error = y_true - y_pred
                delta_w = self.eta * error * x[:, np.newaxis]
                self.w += delta_w
                total_loss += np.sum(error ** 2)

            self.list_of_Error.append(total_loss)
            if self.isVisibility:
                print(f"Epoch: {e}, weights shape: {self.w.shape}, loss: {total_loss:.4f}")
            if total_loss < 0.05:
                return


# =========================
# GŁÓWNY PROGRAM
# =========================

loader = Loader('data/Timage', 'data/Ttest')
loader.sort_images_and_labels()

perceptron = PerceptronSigmoid(eta=0.1, epochs=100)
wm = WeightManager("zapisanewagi.npy")
perceptron.w = wm.load_weights()

index = 1002


test_vector = loader.getVector(index)
image = loader.getImage(index)

predicted_class, probabilities = perceptron.predict_class(test_vector)

true_class = int(loader.getClasTarget()[index])
true_letter = chr(true_class + 64)
predicted_letter = chr(predicted_class + 64)

print(f"Index: {index}")

print(f"Przewidywana litera: {predicted_letter} (klasa: {predicted_class})")
print(f"Prawdopodobieństwa: {np.round(probabilities, 2)}")

plt.imshow(image, cmap='gray')
plt.title(f"Index: {index} | Przewidywana: {predicted_letter}")
plt.axis('off')
plt.show()

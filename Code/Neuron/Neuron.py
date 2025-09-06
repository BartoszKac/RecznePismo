import numpy as np
import matplotlib.pyplot as plt




class PerceptronSigmoid:
    def __init__(self, eta=0, epochs=0, isVisibility=False):
        self.eta = eta
        self.epochs = epochs
        self.isVisibility = isVisibility
        self.list_of_Error = []
        self.w = np.empty((0, 0))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict(self, x):
        total_simulation = np.dot(x, self.w)
        y_pred = self.sigmoid(total_simulation)
        return y_pred

    def CountClass(self, Y):
        allClass = []
        for i in range(Y.size):
            if Y[i] not in allClass:
                allClass.append(int(Y[i]))
        return allClass

    def fit(self, X, Y):
        all_classes = sorted(self.CountClass(Y))  # np. [10, 11, 12, ...] zamiast [A,B,C...]
        class_to_index = {cls: idx for idx, cls in enumerate(all_classes)}

        ones = np.ones((X.shape[0], 1))
        x_1 = np.append(X.copy(), ones, axis=1)

        self.w = np.random.rand(x_1.shape[1], len(all_classes))

        for e in range(self.epochs):
            total_loss = 0.0
            correct_predictions = 0

            for i, (x, y_target) in enumerate(zip(x_1, Y)):
                y_pred = self.predict(x)
                y_target_index = class_to_index[int(y_target)]

                y_true = np.zeros(len(all_classes))
                y_true[y_target_index] = 1

                predicted_class = np.argmax(y_pred)
                true_class = np.argmax(y_true)

                if predicted_class == true_class:
                    correct_predictions += 1

                error = y_true - y_pred
                delta_w = self.eta * error * x[:, np.newaxis]
                self.w += delta_w

                total_loss += np.sum(error ** 2)

            self.list_of_Error.append(total_loss)
            accuracy = correct_predictions / len(Y) * 100

            print(f"Epoka {e + 1}: Trafność: {accuracy:.2f}%, Błąd: {total_loss:.4f}")

            if self.isVisibility:
                print(f"(DEBUG) Epoka: {e}, rozmiar wag: {self.w.shape}, błąd: {total_loss:.4f}")

            if total_loss < 0.05:
                break






            
     
        

            
            



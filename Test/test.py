import idx2numpy
import matplotlib.pyplot as plt
import numpy as np

# Ścieżki do plików EMNIST Letters (upewnij się, że masz te pliki)
image_file = 'emnist-letters-train-images-idx3-ubyte'
label_file = 'emnist-letters-train-labels-idx1-ubyte'

# Wczytanie danych
images = idx2numpy.convert_from_file(image_file)
labels = idx2numpy.convert_from_file(label_file)
superx = labels.size - 1
print("".join(chr(i + 64) for i in labels)) 
single_image = images[0].reshape(-1)

print(single_image)  # (784,)
# Odwrócenie obrazu i obrót (standardowo EMNIST ma obrazy „bokiem”)
def fix_image(img):
  return np.flip(np.rot90(img, k=3)
, axis=1)

# Przykład: wyświetl 10 obrazków z etykietami

plt.imshow(fix_image(images[superx]), cmap='gray')
plt.title(f"Label: {chr(labels[0] + 64)}")  # bo 1 = 'A', 2 = 'B', ...
plt.axis('off')
plt.show()

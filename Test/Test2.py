import matplotlib.pyplot as plt
from Code.Utills.LoadData import Loader
import numpy as np

def CountClass( Y):
    return list(np.unique(Y.astype(int)))

#loader = Loader('data/image', 'data/labels')
loader =  Loader('data/Timage','data/Ttest') 

loader.sort_images_and_labels()
#print(loader.getVector(1))
target = loader.getClasTarget()



target = CountClass(target)
# Jeśli target to liczby, zamień je na odpowiadające znaki ASCII
x = np.char.array([chr(int(x+64)) for x in target])  # Zamiana kodów ASCII na znaki

print(x)  # Tablica znaków (char)

plt.imshow(loader.getImage(0), cmap='gray')
plt.show()

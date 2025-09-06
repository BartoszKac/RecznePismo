import matplotlib.pyplot as plt
import numpy as np
from Code.Utills.LoadData import Loader  
from Code.Neuron import PerceptronSigmoid
from Code.Utills.WeightSave import WeightManager

PIXEL_SIZE = 28

def create_horizontal_collage(images, total_images):
    collage_height = PIXEL_SIZE
    collage_width = total_images * PIXEL_SIZE
    
    collage = np.zeros((collage_height, collage_width), dtype=np.uint8)

    for idx, img in enumerate(images):
        start_x = idx * PIXEL_SIZE
        collage[0:PIXEL_SIZE, start_x:start_x + PIXEL_SIZE] = img
    return collage

if __name__ == "__main__":
   

    loader = Loader('data/Timage','data/Ttest') 
    #perceptron = PerceptronSigmoid(eta=0.001, epochs=20, isVisibility=True)
    #wm = WeightManager("zapisanewagi.npy")
    #perceptron.w = wm.load_weights()
    selected_indices = [0, 10, 20, 30]  

    images_list = [loader.getImage(idx) for idx in selected_indices]

    collage_image = create_horizontal_collage(images_list, len(images_list))

    plt.imshow(collage_image, cmap='gray')
    plt.axis('off')
    plt.show()
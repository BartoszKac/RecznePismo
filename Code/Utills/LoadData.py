import idx2numpy
import numpy as np

PIXEL_SIZE = 28 
MAX_VALUE = 255 


class Loader:
    


    def __init__(self,sourceImages=None,sourceLabel=None):
        self.sourceImages = sourceImages
        self.sourceLabel = sourceLabel
        
        self.images = idx2numpy.convert_from_file(self.sourceImages)
        self.label = idx2numpy.convert_from_file(self.sourceLabel)

     

        fixed_images = []

        for image in self.images:
            fixed = np.flip(np.rot90(image,k=3),axis = 1)
            fixed_images.append(fixed)

        self.images = np.array(fixed_images)

        self.arrayImage = self.images.reshape(self.images.shape[0],-1)


    def security(self, id, size):
         if id is None:
            return False  
         if id >= size:
            print("\033[91mZa duże id\033[0m")
            return True
         return False

         
    def getVector(self,id=None):
       if self.security(id,self.arrayImage.size) is True:
           return
       
       if id is None:
           return self.arrayImage / MAX_VALUE
       else:
           return self.arrayImage[id] / MAX_VALUE
       
    def getClasTarget(self,id=None):
        if self.security(id,self.label.size) is True:
           return
         
        if id is None:
           return self.label 
        else:
           return self.label[id]
    
    def getImage(self, id=None):
         if self.security(id, self.images.size) is True:
             return

         if id is None:
             return self.images  
         else:
              return self.images[id].reshape(PIXEL_SIZE,PIXEL_SIZE)

        
    def sort_images_and_labels(self):
         paired = list(zip(self.label, self.images))  # ← użyj oryginalnych obrazków 28x28!
         paired.sort(key=lambda x: x[0]) 

         labelTuple, imagesTuple = zip(*paired)

         self.label = np.array(labelTuple)
         self.images = np.array(imagesTuple)
         self.arrayImage = self.images.reshape(self.images.shape[0], -1)
    
    @staticmethod
    def getTrueValue(id_=None):
        if 0 <= id_ <= 9:
           return chr(id_ + 48)
        elif 10 <= id_ <= 35:
            return chr(id_ - 10 + 65)
        elif 36 <= id_ <= 61:
            return chr(id_ - 36 + 97)
        else:
            return '?'

    @staticmethod
    def getTrueValue_letters(id_=None):
        if id_ is None or id_ < 1 or id_ > 26:
             return '?'
        return chr(id_ - 1 + 65)  # 'A' = 65 w ASCII
    
    
    @staticmethod
    def index_to_letter(index):
        """
        Zamienia indeks 0-25 na literę 'A'-'Z'.
        """
        if 0 <= index < 26:
            return chr(ord('A') + index)
        return '?'

   
        


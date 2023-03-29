import os 
import random
from shutil import move

os.chdir(os.path.abspath(os.path.join(os.getcwd(), 'ImageGeneration', 'Images')))
imagesList = os.listdir(os.getcwd())
random.shuffle(imagesList)

trainList = imagesList[0:11312] # 80%
testList = imagesList[11313:14140] # 20%

os.mkdir('Train')
os.mkdir('Test')


for image in trainList:
    move(image, os.path.join('Train', image))

for image in testList:
    move(image, os.path.join('Test', image))

print('Done')

                             

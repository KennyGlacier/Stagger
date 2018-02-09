# -*- coding: utf-8 -*-

import stagger
import pickle
from PIL import Image, ImageDraw
from functools import partial

class GeneratePaths(object):
    def __init__(self):
        system = self.create_system()
        self.save_binary('test.pickle', system)
        data = self.load_binary('test.pickle')
        self.save_png('test.png', data, 50)
    
    
    def create_system(self):
        #(length, joint = 0)
        self.bar1 = stagger.Bar(35, 30)
        self.bar2 = stagger.Bar(40)

        #(x, y, r, speed = 1, initial = 0)
        self.drive1 = stagger.Anchor(-20, -20, 10, 6, 0)
        self.drive2 = stagger.Anchor(15, -22, 6, 3, 180)
        
        self.motionSystem = stagger.Two_Bar(self.drive1, self.drive2, self.bar1, self.bar2)

        inputRange = list(map((lambda x: x * self.motionSystem.stepSize), range(0,360)))
        
        return list(map(self.motionSystem.end_path, inputRange))

    def save_binary(self, filename, data):
        with open(filename, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


    def load_binary(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data

    def save_png(self, filename, data, scaling):
        data, boundingBox = self.reposition(data, scaling)
        
        im = Image.new('L', boundingBox, 255)

        draw = ImageDraw.Draw(im)
        
        for i in range(len(data) - 1):
            draw.line(data[i] + data[i + 1], fill=128)
        del draw

        im.save(filename, "PNG")

    def reposition(self, data, scaling = 1):
        '''Returns data, boundingBox'''
        xMin = data[0][0]
        yMin = data[0][1]
        xMax = data[0][0]
        yMax = data[0][1]

        for i in range(len(data)):
            if data[i][0] < xMin:
                xMin = data[i][0]
            if data[i][1] < yMin:
                yMin = data[i][1]
            if data[i][0] > xMax:
                xMax = data[i][0]
            if data[i][1] > yMax:
                yMax = data[i][1]
                
        repoData = []
        
        for i in range(len(data)):
            repoData.append(
                (int((data[i][0] - xMin) * scaling),
                (int((data[i][1] - yMin) * scaling) )))
            
        return repoData, (int((xMax - xMin) * scaling), int((yMax - yMin) * scaling))

        
if __name__ == '__main__':
    main = GeneratePaths()
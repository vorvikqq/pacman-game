import pygame
from vector import Vector
from constants import *
import numpy as np
from random import randint

class Node(object):
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.neighbors = {
            LEFT: None,
            RIGHT: None,
            UP: None,
            DOWN: None,
            PORTAL:None
        }

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

    def readMazeFile(self, textfile):
        # Читання даних з файлу рівня і повернення як масиву
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        # Створення таблиці вузлів на основі даних рівня
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                # Якщо символ є вузлом, додаємо його в таблицю
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col + xoffset, row + yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    """
        A method for creating a home for ghosts
    """
    def createHomeNodes(self, xoffset, yoffset):
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey

    """
        Method for connecting created home nodes
    """
    def connectHomeNodes(self, homekey, otherkey, direction):     
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]


    def constructKey(self, x, y):
        # Формуємо ключ для вузла на основі координат
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectNodes(self, key1, key2, direction1, direction2):
        # З'єднуємо два вузли в обраному напрямку
        self.nodesLUT[key1].neighbors[direction1] = self.nodesLUT[key2]
        self.nodesLUT[key2].neighbors[direction2] = self.nodesLUT[key1]

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        currentKey  = self.constructKey(col + xoffset, row + yoffset)
                        self.connectNodes(key, currentKey, RIGHT, LEFT)
                        key = currentKey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        # Транспонуємо дані для зручності з'єднання по вертикалі
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        currentKey  = self.constructKey(col + xoffset, row + yoffset)
                        self.connectNodes(key, currentKey, DOWN, UP)
                        key = currentKey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def getStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    #temp method for testing

    def getRandomStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[randint(0, len(nodes) - 1)]

    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def render(self, screen):
        # Рендеринг всіх вузлів і їх з'єднань на екрані
        for node in self.nodesLUT.values():
            self.renderConnections(screen, node)
            self.renderNode(screen, node)

    def renderConnections(self, screen, node):
        # Рендеринг з'єднань між вузлами
        for neighbor in node.neighbors.values():
            if neighbor:
                pygame.draw.line(screen, WHITE, node.position.asTuple(), neighbor.position.asTuple(), 4)

    def renderNode(self, screen, node):
        # Рендеринг кожного вузла
        pygame.draw.circle(screen, RED, node.position.asInt(), 12)
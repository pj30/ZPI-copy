# -*- coding: utf-8 -*-

import pygame
import numpy as np
import main_func as mf
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = str(650) + "," + str(50)

class WaterRectangle(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, gameDisplay, color): #rysuje pixel/kwadrat wody
        pygame.draw.rect(gameDisplay, color, [self.x, self.y, self.width, self.height])

    def draw_force(self, gameDisplay, img):
        gameDisplay.blit(img, (self.x,self.y))


class WaterRectangleMatrix(object):

    def __init__(self, dimensions, width, height):
        self.dimensions = dimensions
        self.width = width
        self.height = height

    def fill(self): # tworzy macierz cząstek wody
        water_rectangle_matrix = np.empty((self.dimensions[0], self.dimensions[1]), dtype = object)
        x = 0
        y = 0
        for dim1 in range(self.dimensions[0]):
            for dim2 in range(self.dimensions[1]):
                water_rectangle = WaterRectangle(dim1 * self.width, dim2 * self.height, self.width, self.height)
                water_rectangle_matrix[dim1, dim2] = water_rectangle
        return water_rectangle_matrix


class windowFor2D():

    def __init__(self, N, beta_parm, visc_parm, diff_parm, dt_parm, num_of_scenario):

        self.fluid = mf.step( N, visc_parm, diff_parm, dt_parm)
        self.beta = beta_parm
        self.dimensions = [N+2, N+2]
        self.fluid.num_of_scenario = num_of_scenario
        self.num_of_scenario = num_of_scenario

    def run(self):
        pygame.init() #inicjalizacja pygame
        width = 10
        height = 10
        display_width = width * self.dimensions[0]
        display_height = height * self.dimensions[1]
        blue = (0, 0, 255)
        blue2 = (0, 100, 255)
        blue3 = (0, 255, 255)
        white = (255, 255, 255)
        black = (0, 0, 0)

        gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('2d')
        clock = pygame.time.Clock()

        water_rectangle = WaterRectangleMatrix(self.dimensions, width, height) #tworzy objekt macierzy cząsteczek wody
        water_rectangle_matrix = water_rectangle.fill() #wypełnia w.w. obiekt

        visualisation_exit = False

        if self.num_of_scenario == 1:
            self.fluid.flood_scenario_1()
        elif self.num_of_scenario == 2:
            self.fluid.flood_scenario_2()
        elif self.num_of_scenario == 3:
            self.fluid.flood_scenario_3()
        elif self.num_of_scenario == 4:
            self.fluid.flood_scenario_4()

        force_up = pygame.image.load('force_up.png')
        force_down = pygame.image.load('force_down.png')
        force_left = pygame.image.load('force_left.png')
        force_right = pygame.image.load('force_right.png')
        # fig = plt.figure()
        time = 0
        start = False
        #dens, A, B = self.fluid.step() #pobiera macierz gęstości
        show_force = False
        while not(visualisation_exit):
            #print time
            time += self.fluid.dt
            #if time > 4:
            if self.num_of_scenario == 1:
                self.fluid.force_scenario_1()
            elif self.num_of_scenario == 2:
                self.fluid.force_scenario_2()
            elif self.num_of_scenario == 3:
                self.fluid.force_scenario_3()
            elif self.num_of_scenario == 4:
                self.fluid.force_scenario_4()

            #if dens[1:66, 1:50].sum() > 0.1:
            if self.num_of_scenario == 1:
                dens, A, B = self.fluid.step2()
            else:
                dens, A, B = self.fluid.step()
            # print(dens.max(),dens.min())
            #print dens[1:66, 1:50].sum()
            #if dens[1:66, 1:50].sum() < 15.:
                #while not(visualisation_exit):
                    #print time
                    #for event in pygame.event.get():
                        #if event.type == pygame.QUIT:
                            #visualisation_exit = True
            # np.savetxt("2.txt", dens, fmt='%5.3f', delimiter=' ', newline='\n')
            # fig.clf()
            # plt.quiver(A, B)
            # time.sleep(1)
            gameDisplay.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    visualisation_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if not(show_force):
                            show_force = True
                        else:
                            show_force = False

            #rysowanie
            for x in range(self.dimensions[0]):
                for y in range(self.dimensions[1]):
                    water_rectangle_matrix[x, y].draw(gameDisplay, (0,255 - np.min([int(np.floor(dens[x, y]*255)),255]) , 255))
                    #jesli gęstość w danym punkcie jest większa niż zadany parametr "BETA" to rysuje cząsteczkę wody, w przeciwnym wypadku rysuje puste pole
                    if x != 32:
                        if self.num_of_scenario == 1:
                            water_rectangle_matrix[x, 50].draw(gameDisplay,(0,0,0))
            if show_force:
                for x in range(self.dimensions[0]):
                    for y in range(self.dimensions[1]):
                        if A[x, y] >= .75:
                            water_rectangle_matrix[x, y].draw_force(gameDisplay, pygame.transform.scale(force_right, (int(731/(A[x,y]*50)),int(1332/(A[x,y]*50)))))
                        elif A[x, y] <= -.75:
                            water_rectangle_matrix[x, y].draw_force(gameDisplay, pygame.transform.scale(force_left, (int(731/(A[x,y]*-50)),int(1332/(A[x,y]*-50)))))
                        if B[x, y] >= .75:
                            water_rectangle_matrix[x, y].draw_force(gameDisplay, pygame.transform.scale(force_down, (int(1332/(B[x,y]*50)),int(731/(B[x,y]*50)))))
                        elif B[x, y] <= -.75:
                            water_rectangle_matrix[x, y].draw_force(gameDisplay, pygame.transform.scale(force_up, (int(1332/(B[x,y]*-50)),int(731/(B[x,y]*-50)))))
            pygame.display.update()
            #clock.tick(10)
            #raw_input()

visc = 0.000001
diff = 0.00001
dt = 1 / 15.0
N = 64
beta = .5
print("Ktory scenario?\n")
num_of_scenario = int(raw_input())
disp = windowFor2D(N, beta, visc, diff, dt, num_of_scenario)
disp.run()

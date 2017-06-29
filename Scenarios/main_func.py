# -*- coding: utf-8 -*-

import functions
import numpy as np


class step(functions.Step):

    def __init__(self, N, visc, diff, dt):
        functions.Step.__init__(self, N)
        self.size = (N + 2)
        self.u = np.zeros((self.size, self.size))
        self.v = np.zeros((self.size, self.size))
        self.dens = np.zeros((self.size, self.size))
        self.dens_prev = np.zeros((self.size, self.size))
        self.u_prev = np.zeros((self.size, self.size))
        self.v_prev = np.zeros((self.size, self.size))
        self.visc = visc
        self.diff = diff
        self.dt = dt
        self.bor = np.ones((self.size, self.size))
        self.fill_bor()

    def step(self):
        self.u, self.v = self.vel_step( self.u, self.v, self.u_prev, self.v_prev, self.visc, self.dt)
        self.dens = self.dens_step( self.dens, self.dens_prev, self.u, self.v, self.diff, self.dt)
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.dens_prev = np.zeros((self.size, self.size))
        self.u_prev = np.zeros((self.size, self.size))
        self.v_prev = np.zeros((self.size, self.size))

        self.dens[1: self.N + 1, 1: self.N + 1] -= (d1 - self.sum_dens) * (self.dens[1 : self.N + 1, 1 : self.N + 1] / d1 *1.0)

        return self.dens , self.u, self.v

    def step2(self):
        self.u, self.v = self.vel_step2( self.u, self.v, self.u_prev, self.v_prev, self.visc, self.dt)
        self.dens = self.dens_step2( self.dens, self.dens_prev, self.u, self.v, self.diff, self.dt)
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.dens_prev = np.zeros((self.size, self.size))
        self.u_prev = np.zeros((self.size, self.size))
        self.v_prev = np.zeros((self.size, self.size))

        self.dens[1: self.N + 1, 1: self.N + 1] -= (d1 - self.sum_dens) * (self.dens[1 : self.N + 1, 1 : self.N + 1] / d1 *1.0)

        return self.dens , self.u, self.v

    def force_scenario_1(self):
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.v_prev[1: self.N + 1, 1: self.N + 1] = 0.15 * np.absolute(self.dens[1: self.N + 1, 1: self.N + 1]) #gravity

    def flood_scenario_1(self):
        self.dens[0:self.size, 0:self.size] = 0
        self.dens[1:66 , 30 : 50] = 1
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()

    def fill_bor(self):
        self.bor[:, 0] = 0
        self.bor[:, self.size-1] = 0
        self.bor[0, :] = 0
        self.bor[self.size - 1,:] = 0
        for i in range(self.size):
            self.bor[i,50] = 0
        self.bor[32,50] = 1

    def force_scenario_2(self):
        self.v_prev[12:18, 32] = 45
        self.v_prev[46:52, 32] = -45
        self.u_prev[32, 12:18] = -45
        self.u_prev[32, 46:52] = 45

    def flood_scenario_2(self):
        self.dens[0:self.size, 0:self.size] = 0.4
        self.dens[20:45 , 20 : 45] = 1
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()

    def force_scenario_3(self):
        self.radius = 4.0
        self.circle_step = 12.0
        for i in range (0,int(round(self.circle_step))):
            #promień- odległość siły od środka
            k = i / (self.circle_step+1.0)
            x = int(round(32.0 + np.cos(2.0*np.pi*k)*self.radius))
            y = int(round(32.0 + np.sin(2.0*np.pi*k)*self.radius))
            self.v_prev[x,y] = np.sin(2.0*np.pi*k)*250.0
            self.u_prev[x,y] = np.cos(2.0*np.pi*k)*250.0

    def flood_scenario_3(self):
        self.dens[0:self.size, 0:self.size] = 0.4
        self.dens[20:45 , 20 : 45] = 0.7
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()

    def force_scenario_4(self):
        d1 = self.dens[1 : self.N + 1, 1 : self.N + 1].sum()
        self.v_prev[1: self.N + 1, 1: self.N + 1] = 0.15 * np.absolute(self.dens[1: self.N + 1, 1: self.N + 1])
        self.u_prev[8, 0:self.size] = 30    # ustawienia sil
        self.u_prev[57, 0:self.size] = -30

    def flood_scenario_4(self):
        self.dens[0:18, 0:self.size] = 0.4
        self.dens[48:self.size, 0:self.size] = 0.7
        self.sum_dens = self.dens[1: self.N + 1, 1: self.N + 1].sum()

# -*- coding: utf-8 -*-


class Functions(object):

    def __init__(self, N):
        self.N =N

    def add_source(self, x, s, dt):
        x += dt * s
        return x

    def diffuse(self, b, x, x0, diff, dt):

        N = self.N
        if diff != 0.0:
            a = dt * diff * N * N
            for k in range(0, 20):
                x[1:N + 1, 1:N + 1] = (x0[1:N + 1, 1:N + 1] + (
                (a * (x[0:N, 1:N + 1] + x[2:N + 2, 1:N + 1] + x[1:N + 1, 0:N] + x[1:N + 1, 2:N + 2])) / (1 + (4.0 * a))))
                x = self.set_bnd(b, x)
        else:
            x[1:N + 1, 1:N + 1] = x0[1:N + 1, 1:N + 1] + 0
            x = self.set_bnd(b, x)
        return x

    def set_bnd(self,  b, x):
        N = self.N
        if b == 1:
            x[0, :] = -x[1, :]
            x[N + 1, :] = -x[N, :]
        else:
            x[0, :] = x[1, :]
            x[N + 1, :] = x[N, :]

        if b == 2:
            x[:, 0] = -x[:, 1]
            x[:, N + 1] = -x[:, N]
        else:
            x[:, 0] = x[:, 1]
            x[:, N + 1] = x[:, N]

        x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
        x[0, N + 1] = 0.5 * (x[1, N + 1] + x[0, N])
        x[N + 1, 0] = 0.5 * (x[N, 0] + x[N + 1, 1])
        x[N + 1, N + 1] = 0.5 * (x[N, N + 1] + x[N + 1, N])
        return x

    def advect(self,  b, d, d0, u, v, dt):
        N = self.N
        dt0 = dt * N
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                x = i - dt0 * u[i, j]
                y = j - dt0 * v[i, j]
                if x < float(0.5):
                    x = 0.5
                if x > N + 0.5:
                    x = N + 0.5
                i0 = int(x)
                i1 = i0 + 1
                if y < float(0.5):
                    y = 0.5
                if y > N + 0.5:
                    y = N + 0.5
                j0 = int(y)
                j1 = j0 + 1

                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1

                d[i, j] = s0 * (t0 * d0[i0, j0] + t1 * d0[i0, j1]) + s1 * (t0 * d0[i1, j0] + t1 * d0[i1, j1])
        d = self.set_bnd(b, d)
        return d

    def project(self,  u, v, p, div):
        N = self.N
        h = 1.0 / N

        div[1:N + 1, 1:N + 1] = -0.5 * h * (u[2:N + 2, 1:N + 1] - u[0:N, 1:N + 1] +
                                            v[1:N + 1, 2:N + 2] - v[1:N + 1, 0:N])
        p[1:N + 1, 1:N + 1] = 0
        div = self.set_bnd(0, div)
        p = self.set_bnd(0, p)

        for k in range(0, 20):
            p[1:N + 1, 1:N + 1] = (div[1:N + 1, 1:N + 1] + p[0:N, 1:N + 1] + p[2:N + 2, 1:N + 1]+
                                    p[1:N + 1, 0:N] + p[1:N + 1,2:N + 2]) / 4
            p = self.set_bnd(0, p)





        u[1:N + 1, 1:N + 1] -= 0.5 * (p[2:N + 2, 1:N + 1] - p[0:N, 1: N + 1]) / h
        v[1:N + 1, 1:N + 1] -= 0.5 * (p[1:N + 1, 2:N + 2] - p[1:N + 1, 0:N]) / h
        u = self.set_bnd(1, u)
        v = self.set_bnd(2, v)
        return u, v, p, div

    def advect2(self, b, d, d0, u, v, dt):
        N = self.N
        dt0 = dt * N
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                x = i - dt0 * u[i, j]
                y = j - dt0 * v[i, j]
                if x < float(0.5):
                    x = 0.5
                if x > N + 0.5:
                    x = N + 0.5
                i0 = int(x)
                i1 = i0 + 1
                if y < float(0.5):
                    y = 0.5
                if y > N + 0.5:
                    y = N + 0.5
                j0 = int(y)
                j1 = j0 + 1

                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1

                d[i, j] = s0 * (t0 * d0[i0, j0] * self.bor[i0, j0] + t1 * d0[i0, j1] * self.bor[i0, j1]) + s1 * (
                    t0 * d0[i1, j0] * self.bor[i1, j0] + t1 * d0[i1, j1] * self.bor[i1, j1])
        d = self.set_bnd(b, d)
        return d

    def project2(self,  u, v, p, div):
        N = self.N
        h = 1.0 / N

        div[1:N + 1, 1:N + 1] = -0.5 * h * (
            self.bor[2:N + 2, 1:N + 1] * u[2:N + 2, 1:N + 1] - self.bor[1:N + 1, 0:N] * u[0:N, 1:N + 1] +
            self.bor[1:N + 1, 0:N] * v[1:N + 1, 2:N + 2] - self.bor[1:N + 1, 0:N] * v[1:N + 1, 0:N])
        p[1:N + 1, 1:N + 1] = 0
        div = self.set_bnd(0, div)
        p = self.set_bnd(0, p)

        for k in range(0, 20):
            p[1:N + 1, 1:N + 1] = (div[1:N + 1, 1:N + 1] + self.bor[0:N, 1:N + 1] * p[0:N, 1:N + 1] +
                                    self.bor[2:N + 2,1:N + 1] * p[2:N + 2,1:N + 1] +
                                    self.bor[1:N + 1, 0:N] * p[1:N + 1, 0:N] +
                                    self.bor[1:N + 1, 2:N + 2] * p[1:N + 1,2:N + 2]) / (
                                    self.bor[0:N, 1:N + 1] + self.bor[2:N + 2,1:N + 1] +
                                    self.bor[1:N + 1, 0:N] + self.bor[1:N + 1, 2:N + 2])
            p = self.set_bnd(0, p)

        u[1:N + 1, 1:N + 1] -= 0.5 * (p[2:N + 2, 1:N + 1] * self.bor[2:N + 2, 1:N + 1] - p[0:N, 1: N + 1] * self.bor[0:N, 1: N + 1]) / h
        v[1:N + 1, 1:N + 1] -= 0.5 * (p[1:N + 1, 2:N + 2] * self.bor[1:N + 1, 2:N + 2] - p[1:N + 1, 0:N] * self.bor[1:N + 1, 0:N]) / h
        u = self.set_bnd(1, u)
        v = self.set_bnd(2, v)
        return u, v, p, div

    def diffuse2(self, b, x, x0, diff, dt):
        #
        N = self.N
        if diff != 0.0:
            a = dt * diff * N * N
            for k in range(0, 20):
                x[1:N + 1, 1:N + 1] = (self.bor[1:N + 1, 1:N + 1]*x0[1:N + 1, 1:N + 1] + ((a * (
                    self.bor[0:N, 1:N + 1]*x[0:N, 1:N + 1] + self.bor[2:N + 2, 1:N + 1]*x[2:N + 2, 1:N + 1] +
                    self.bor[1:N + 1, 0:N]*x[1:N + 1, 0:N] + self.bor[1:N + 1, 2:N + 2]*x[1:N + 1, 2:N + 2])) /
                    (1 + ((self.bor[0:N, 1:N + 1] + self.bor[2:N + 2,1:N + 1] +
                    self.bor[1:N + 1, 0:N] + self.bor[1:N + 1, 2:N + 2]) * a))))
                x = self.set_bnd(b, x)
        else:
            x[1:N + 1, 1:N + 1] = x0[1:N + 1, 1:N + 1] + 0
            x = self.set_bnd(b, x)
        return x




class Step(Functions):

    def __init__(self, N):
        Functions.__init__(self, N)

    def dens_step(self,  x, x0, u, v, diff, dt):
        N = self.N
        x = self.add_source(x, x0, dt)
        x0, x = x, x0  # swap(x0, x)
        x = self.diffuse(0, x, x0, diff, dt)
        x0, x = x, x0  # swap(x0, x)
        x = self.advect(0, x, x0, u, v, dt)
        return x

    def vel_step(self,  u, v, u0, v0, visc, dt):
        N = self.N
        u = self.add_source(u, u0, dt)
        v = self.add_source(v, v0, dt)

        u0, u = u, u0  # swap(u0, u)
        u = self.diffuse(1, u, u0, visc, dt)
        v0, v = v, v0  # swap(v0, v)
        v = self.diffuse(2, v, v0, visc, dt)
        u, v, u0, v0 = self.project(u, v, u0, v0)

        u, u0 = u0, u  # swap(u0, u)
        v, v0 = v0, v  # swap(v0, v)

        u = self.advect(1, u, u0, u0, v0, dt)
        v = self.advect(2, v, v0, u0, v0, dt)
        u, v, u0, v0 = self.project(u, v, u0, v0)
        return u, v

    def dens_step2(self,  x, x0, u, v, diff, dt):
        N = self.N
        x = self.add_source(x, x0,
                       dt)  # do zdefiniowanej wczesniej funkcji wchodza 3 zmienne, a w materialach wchodza 4 zmienne?
        x0, x = x, x0  # swap(x0, x)
        x = self.diffuse2(0, x, x0, diff, dt)
        x0, x = x, x0  # swap(x0, x)
        x = self.advect2(0, x, x0, u, v, dt)
        return x

    def vel_step2(self,  u, v, u0, v0, visc, dt):
        N = self.N
        u = self.add_source(u, u0, dt)
        v = self.add_source(v, v0, dt)

        u0, u = u, u0  # swap(u0, u)
        u = self.diffuse2(1, u, u0, visc, dt)
        v0, v = v, v0  # swap(v0, v)
        v = self.diffuse2(2, v, v0, visc, dt)
        u, v, u0, v0 = self.project2(u, v, u0, v0)

        u, u0 = u0, u  # swap(u0, u)
        v, v0 = v0, v  # swap(v0, v)

        u = self.advect2(1, u, u0, u0, v0, dt)
        v = self.advect2(2, v, v0, u0, v0, dt)
        u, v, u0, v0 = self.project2(u, v, u0, v0)
        return u, v

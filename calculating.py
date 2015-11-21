from math import *


class IntegralNumerical(object):

    data = []

    def __init__(self, path=None, equation=None, a=0, b=0, delta=0):
        self.path = path
        self.equation = equation
        self.a = float(a)
        self.b = float(b)
        self.delta = float(delta)
        if self.path is not None:
            self.data = self.get_file_data()
        else:
            self.data = self.get_eq_data()

    def get_file_data(self):
            the_file = open(self.path, 'r')
            domain = []
            fx = []
            for line in the_file:
                x_y = str(line).split(',')
                domain.append(float(x_y[0]))
                fx.append(float(x_y[1][0:-2]))
            return zip(domain, fx)

    def get_eq_data(self):
        if (self.equation and self.a and self.b and self.delta)is not None:
            fx = []
            domain = []
            len_section = int((self.b-self.a)/self.delta)
            for section_id in range(len_section + 1):
                domain.append(self.a+self.delta*section_id)
            for x in domain:
                result = eval(self.equation)
                fx.append(result)
            return zip(domain, fx)
        else:
            raise ValueError('a , b , delta and equation must set for instance of this class')

    def section_width(self):
        if len(self.data) < 2:
            raise ValueError('data of input is not correct')
        else:
            width = self.data[0][0] - self.data[1][0]
            if width < 0:
                width *= -1
            return width

    def left_hand(self):
        h = self.section_width()
        result = 0
        for index in range(len(self.data) - 1):
            result += h * self.data[index][1]
        return result

    def right_hand(self):
        h = self.section_width()
        result = 0
        for index in range(1, len(self.data)):
            result += h * self.data[index][1]
        return result

    def trapezoidal(self):
        h = self.section_width()
        length = len(self.data)
        result = 0
        for index in range(length):
            if index == (0 or length - 1):
                result += h * (self.data[index][1] / 2)
            else:
                result += h * self.data[index][1]
        return result

    def mid_point(self):
        if (self.equation and self.a and self.b)is not None:
            x = (self.a + self.b) / 2
            fx = eval(self.equation)
            return (self.b - self.a) * fx
        else:
            raise NameError('mid point method can not use for data of table')

    def simpson(self):
        h = self.section_width()
        length = len(self.data)
        result = 0
        c = 4
        for index in range(length):
            if c == 2:
                c = 4
            else:
                c = 2
            if (index == 0) or (index == (length - 1)):
                result += (h/3) * self.data[index][1]
            else:
                result += (h/3) * (self.data[index][1] * c)
        return result
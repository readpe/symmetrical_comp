import math, cmath


class Phasor(object):
    # Phasor class with mag and angle (degrees)
    def __init__(self, mag, ang):
        self.mag = round(mag, 8)
        self.ang = round(ang, 8)

    def rect(self):
        # Returns the rectangular form of the phasor
        return cmath.rect(self.mag, math.radians(self.ang))

    def conj(self):
        # Returns the conjugate form of the phasor
        return Phasor.from_rect(self.rect().conjugate())

    def real(self):
        # Returns real component
        return self.rect().real

    def imag(self):
        # Returns imaginary component
        return self.rect().imag

    def __sub__(self, other):
        # Override subtraction method
        x = self.rect()
        if isinstance(other, Phasor):
            y = other.rect()
        elif isinstance(other, (int, float, complex)):
            y = other

        return Phasor.from_rect(x - y)

    def __add__(self, other):
        # Override addition method
        x = self.rect()
        if isinstance(other, Phasor):
            y = other.rect()
        elif isinstance(other, (int, float, complex)):
            y = complex(other)

        return Phasor.from_rect(x + y)

    def __mul__(self, other):
        # Override multiplication method
        x = self.rect()
        if isinstance(other, Phasor):
            y = other.rect()
        elif isinstance(other, (int, float, complex)):
            y = complex(other)
            
        return Phasor.from_rect(x * y)

    def __rmul__(self, other):
        # Override right multiplication method
        x = self.rect()
        if isinstance(other, Phasor):
            y = other.rect()
        elif isinstance(other, (int, float, complex)):
            y = complex(other)
            
        return Phasor.from_rect(x * y)

    def __truediv__(self, other):
        # Override division method
        x = self.rect()
        if isinstance(other, Phasor):
            y = other.rect()
        elif isinstance(other, (int, float, complex)):
            y = complex(other)
        try:
            return Phasor.from_rect(x / y)
        except ZeroDivisionError:
            return Phasor(0.0, 0.0)

    def __str__(self):
        # String representation of phasor
        return '{:0.2f}@{:0.2f}'.format(self.mag, self.ang)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_rect(rect):
        # Creates Phasor instance from rectangular argument
        r, phi = cmath.polar(rect)
        return Phasor(r, math.degrees(phi))

    @staticmethod
    def a():
        # Returns unit phasor 1@120
        return Phasor(1, 120)

    @staticmethod
    def a2():
        # Returns unit phasor 1@240
        return Phasor(1, 240)

class ThreePhase(object):
    # Three phase class containing three Phasor class objects for each phase
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def phph(self):
        # Returns phase-phase quantities 'ab', 'bc', 'ca'
        return (self.a - self.b, self.b - self.c, self.c - self.a)

    def get_seq(self):
        # Returns the sequential components in a tuple (seq0, seq1, seq2)
        seq0 = (1/3) * (self.a + self.b + self.c)
        seq1 = (1/3) * (self.a + (Phasor.a() * self.b) + (Phasor.a2() * self.c))
        seq2 = (1/3) * (self.a + (Phasor.a2() * self.b) + (Phasor.a() * self.c))
        return (seq0, seq1, seq2)

class Terminal(object):
    # A terminal class associate ThreePhase voltage and current objects
    def __init__(self, v_threephase, i_threephase):
        self.v = v_threephase
        self.i = i_threephase
    
    def zph(self, ph='a'):
        # Single phase impedance, argument is 'a', 'b', or 'c'
        vph = getattr(self.v, ph)
        iph = getattr(self.i, ph)
        return vph / iph

    def zphph(self, ph1='a', ph2='b'):
        # Returns phase-phase impedance, argument is first phase, second phase 'a', 'b', or 'c'
        vph1 = getattr(self.v, ph1)
        iph1 = getattr(self.i, ph1)
        vph2 = getattr(self.v, ph2)
        iph2 = getattr(self.i, ph2)
        return (vph1 - vph2) / (iph1 - iph2)
   
    def z2(self):
        # Returns negative sequence impedance Z2
        v2 = self.v.get_seq()[2]
        i2 = self.i.get_seq()[2]
        return v2 / i2

    def power(self):
        # Calculates single phase and three phase power
        Sa = self.v.a * self.i.a.conj()
        Sb = self.v.b * self.i.b.conj()
        Sc = self.v.c * self.i.c.conj()
        S = Sa + Sb + Sc
        return (Sa, Sb, Sc, S)

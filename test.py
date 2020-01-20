from symmetrical_comp import Phasor, ThreePhase, Terminal

Va = Phasor(66.395e3, 0)
Vb = Phasor(66.395e3, 240)
Vc = Phasor(66.395e3, 120)

V3ph = ThreePhase(Va, Vb, Vc)

Ia = Phasor(100, 30)
Ib = Phasor(100, 270)
Ic = Phasor(100, 150)

I3ph = ThreePhase(Ia, Ib, Ic)

term = Terminal(V3ph, I3ph)
P = term.power()
Za = term.zph('a')
Zab = term.zphph('a', 'b')
Z2 = term.z2()

print('Vab = {}, Vbc = {}, Vca = {}'.format(*V3ph.phph()))
print('Iab = {}, Ibc = {}, Ica = {}'.format(*I3ph.phph()))
print('V0 = {}, V1 = {}, V2 = {}'.format(*V3ph.get_seq()))
print('I0 = {}, I1 = {}, I2 = {}'.format(*I3ph.get_seq()))
print('Pa = {}, Pb = {}, Pc = {}, Pt = {}'.format(*P))

from math import log

### CONCRETE
concrete_dict = {
    'C12/15': {'fck': 12, 'fckcube': 15, 'fcm': 20, 'fctm': 1.6, 'fctk005': 1.1, 'fctk095': 2.0, 'Ecm': 27*10**3, 'epsilonc1': 1.8*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C16/20': {'fck': 16, 'fckcube': 16, 'fcm': 24, 'fctm': 1.9, 'fctk005': 1.3, 'fctk095': 2.5, 'Ecm': 29*10**3, 'epsilonc1': 1.9*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C20/25': {'fck': 20, 'fckcube': 20, 'fcm': 28, 'fctm': 2.2, 'fctk005': 1.5, 'fctk095': 2.9, 'Ecm': 30*10**3, 'epsilonc1': 2.0*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C25/30': {'fck': 25, 'fckcube': 25, 'fcm': 33, 'fctm': 2.6, 'fctk005': 1.8, 'fctk095': 3.3, 'Ecm': 31*10**3, 'epsilonc1': 2.1*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C30/37': {'fck': 30, 'fckcube': 30, 'fcm': 38, 'fctm': 2.9, 'fctk005': 2.0, 'fctk095': 3.8, 'Ecm': 33*10**3, 'epsilonc1': 2.2*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C35/45': {'fck': 35, 'fckcube': 35, 'fcm': 43, 'fctm': 3.2, 'fctk005': 2.2, 'fctk095': 4.2, 'Ecm': 34*10**3, 'epsilonc1': 2.25*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C40/50': {'fck': 40, 'fckcube': 40, 'fcm': 48, 'fctm': 3.5, 'fctk005': 2.5, 'fctk095': 4.6, 'Ecm': 35*10**3, 'epsilonc1': 2.3*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C45/55': {'fck': 45, 'fckcube': 45, 'fcm': 53, 'fctm': 3.8, 'fctk005': 2.7, 'fctk095': 4.9, 'Ecm': 36*10**3, 'epsilonc1': 2.4*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C50/60': {'fck': 50, 'fckcube': 60, 'fcm': 58, 'fctm': 4.1, 'fctk005': 2.9, 'fctk095': 5.3, 'Ecm': 37*10**3, 'epsilonc1': 2.45*10**-3, 'epsiloncu1': 3.5*10**-3, 'epsilonc2': 2.0*10**-3, 'epsiloncu2': 3.5*10**-3, 'n': 2, 'epsilonc3': 1.75*10**-3, 'epsiloncu3': 3.5*10**-3},
    'C55/67': {'fck': 55, 'fckcube': 67, 'fcm': 63, 'fctm': 4.2, 'fctk005': 3.0, 'fctk095': 5.5, 'Ecm': 38*10**3, 'epsilonc1': 2.5*10**-3, 'epsiloncu1': 3.2*10**-3, 'epsilonc2': 2.2*10**-3, 'epsiloncu2': 3.1*10**-3, 'n': 1.75, 'epsilonc3': 1.8*10**-3, 'epsiloncu3': 3.1*10**-3},
    'C60/75': {'fck': 60, 'fckcube': 75, 'fcm': 68, 'fctm': 4.4, 'fctk005': 3.1, 'fctk095': 5.7, 'Ecm': 39*10**3, 'epsilonc1': 2.6*10**-3, 'epsiloncu1': 3.0*10**-3, 'epsilonc2': 2.3*10**-3, 'epsiloncu2': 2.9*10**-3, 'n': 1.6, 'epsilonc3': 1.9*10**-3, 'epsiloncu3': 2.9*10**-3},
    'C70/85': {'fck': 70, 'fckcube': 85, 'fcm': 78, 'fctm': 4.6, 'fctk005': 3.2, 'fctk095': 6.0, 'Ecm': 41*10**3, 'epsilonc1': 2.7*10**-3, 'epsiloncu1': 2.8*10**-3, 'epsilonc2': 2.4*10**-3, 'epsiloncu2': 2.7*10**-3, 'n': 1.45, 'epsilonc3': 2.0*10**-3, 'epsiloncu3': 2.7*10**-3},
}

### REINFORCEMENT STEEL
reinforcement_steel_dict = {
    'St0S-b': {'fyk': 220, 'ftk': 300, 'class': 'A-0'},
    'St3S-b': {'fyk': 240, 'ftk': 320, 'class': 'A-I'},
    'PB240': {'fyk': 240, 'ftk': 265, 'class': 'A-I'},
    'PB300': {'fyk': 300, 'class': 'A-I'},
    '18G2-b': {'fyk': 365, 'ftk': 480, 'class': 'A-II'},
    '20G2Y-b': {'fyk': 365, 'ftk': 480, 'class': 'A-II'},
    'RB300': {'fyk': 300, 'class': 'A-II'},
    '34GS': {'fyk': 410, 'ftk': 550, 'class': 'A-III'},
    '25G2S': {'fyk': 395, 'ftk': 530, 'class': 'A-III'},
    'RB400': {'fyk': 400, 'ftk': 440, 'class': 'A-III'},
    'RB400W': {'fyk': 400, 'ftk': 440, 'class': 'A-III'},
    '20G2VY-b': {'fyk': 490, 'ftk': 590, 'class': 'A-IIIN'},
    'RB500': {'fyk': 500, 'ftk': 550},
    'RB500W': {'fyk': 500, 'ftk': 550},
    'B500A': {'fyk': 500, 'ftk': 550},
    'B500B': {'fyk': 500, 'ftk': 550},
    'BSt500S(A)': {'fyk': 500, 'ftk': 550},
    'BSt500S(B)': {'fyk': 500, 'ftk': 550},
    'BSt500KR(A)': {'fyk': 500, 'ftk': 550},
    'B500SP': {'fyk': 500, 'ftk': 575},
    'K500B-T': {'fyk': 500},
    'K500C-T': {'fyk': 500}
}

### STEEL
steel_dict = {
    'S235': {'fyk': 235, 'fuk': 360},
    'S275': {'fyk': 275, 'fuk': 430},
    'S355': {'fyk': 355, 'fuk': 510},
    'S450': {'fyk': 440, 'fuk': 550},
}

wood_dict = {}


class Concrete:
    def __init__(self, concrete_class):
        self.concrete_class = concrete_class
        self.fck = concrete_dict[concrete_class]['fck']  # MPa
        self.fckcube = concrete_dict[concrete_class]['fckcube']  # MPa
        self.fcm = concrete_dict[concrete_class]['fcm']  # MPa
        self.fctm = concrete_dict[concrete_class]['fctm']  # MPa
        self.fctk005 = concrete_dict[concrete_class]['fctk005']  # MPa
        self.fctk095 = concrete_dict[concrete_class]['fctk095']  # MPa
        self.Ecm = concrete_dict[concrete_class]['Ecm']  # MPa
        self.epsilonc3 = concrete_dict[concrete_class]['epsilonc3']
        self.epsiloncu3 = concrete_dict[concrete_class]['epsiloncu3']
        self.fcm = self.fck + 8  # MPa
        if self.fck <= 50: 
            self.fctm = 0.3 * self.fck**(2 / 3)  # MPa
        else:
            self.fctm = 2.12 * log(1 + 0.1 * self.fcm)  # MPa
        self.fctk005 = 0.7 * self.fctm  # MPa
        self.fctk095 = 1.3 * self.fctm  # MPa
        self.Ecm = 22 * (0.1 * self.fcm)**(0.3)  # GPa
    
    def design_values(self, material_factor, alfa_cc=1, alfa_ct=1):
        self.fcd = alfa_cc * self.fck / material_factor  # MPa
        self.fctd = alfa_ct * self.fctk005 / material_factor  # MPa


class ReinforcementSteel:
    def __init__(self, steel_class):
        self.steel_class = steel_class
        self.fyk = reinforcement_steel_dict[steel_class]['fyk']  # MPa
        if 'ftk' in reinforcement_steel_dict[steel_class]:
            self.ftk = reinforcement_steel_dict[steel_class]['ftk']  # MPa
        self.Es = 200 * 10**3  # MPa

    def design_values(self, material_factor):
        self.fyd = self.fyk / material_factor  # MPa

### OTHER
partial_material_factor_dict = {
    'PN-EN': {'gammac': 1.4, 'gammas': 1.15},
    'SS-EN': {'gammac': 1.5, 'gammas': 1.15}
}
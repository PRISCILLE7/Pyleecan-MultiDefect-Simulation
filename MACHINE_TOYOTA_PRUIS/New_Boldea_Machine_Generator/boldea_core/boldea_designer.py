"""
Module de dimensionnement selon l'approche de Boldea
Intègre les lois d'échelle et ratios géométriques optimaux
"""

import numpy as np

class BoldeaDesigner:
    """
    Classe principale pour le dimensionnement des machines selon Boldea
    """
    
    def __init__(self):
        # Coefficients optimaux de Boldea (empiriques)
        self.K_D = 0.15      # Coefficient diamètre
        self.K_L = 0.10      # Coefficient longueur
        self.K_slot = 0.1    # Coefficient hauteur d'encoche
        self.K_magnet = 0.8  # Coefficient aimant
        self.K_airgap = 0.001 # Entrefer standard (1mm)
        
        # Ratios géométriques optimaux
        self.optimal_D_L_ratio = 1.5  # Ratio diamètre/longueur optimal
        self.optimal_slot_ratio = 0.8  # Ratio largeur/hauteur encoche
        
    def calculate_machine_dimensions(self, power_rated, speed_rated, pole_pairs, 
                                   machine_type='IPMSM', application='traction'):
        """
        Calcul des dimensions principales selon Boldea
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
            pole_pairs (int): Nombre de paires de pôles
            machine_type (str): Type de machine (IPMSM, SPMSM, SynRel, Hybrid)
            application (str): Type d'application (traction, wind, industrial, aerospace)
        
        Returns:
            dict: Dictionnaire avec toutes les dimensions calculées
        """
        
        # Ajuster coefficients selon l'application
        self._adjust_coefficients_for_application(application)
        
        # Dimensions de base selon Boldea
        D = self.K_D * (power_rated / speed_rated)**(1/3)
        L = self.K_L * (power_rated / speed_rated)**(1/3)
        
        # Ajuster ratio D/L si nécessaire
        if D/L < self.optimal_D_L_ratio:
            D = L * self.optimal_D_L_ratio
        elif D/L > 3.0:  # Limite supérieure
            D = L * 3.0
        
        # Pas polaire optimal
        tau_p = np.pi * D / (2 * pole_pairs)
        
        # Nombre d'encoches optimal selon Boldea
        Zs = self._calculate_optimal_slots(pole_pairs, machine_type)
        
        # Hauteur d'encoche proportionnelle au pas polaire
        slot_height = self.K_slot * tau_p
        
        # Largeur d'encoche selon ratio optimal
        slot_width = slot_height * self.optimal_slot_ratio
        
        # Épaisseur d'aimant selon type de machine
        magnet_thickness = self._calculate_magnet_thickness(tau_p, machine_type)
        
        # Entrefer adaptatif selon application
        air_gap = self._calculate_adaptive_airgap(application, D)
        
        return {
            'D': D,
            'L': L,
            'tau_p': tau_p,
            'Zs': Zs,
            'slot_height': slot_height,
            'slot_width': slot_width,
            'magnet_thickness': magnet_thickness,
            'air_gap': air_gap,
            'D_L_ratio': D/L,
            'application': application,
            'machine_type': machine_type
        }
    
    def calculate_rotor_dimensions(self, D, L, pole_pairs, magnet_thickness, 
                                 machine_type='IPMSM', air_gap=0.001):
        """
        Calcul des dimensions rotor selon Boldea
        
        Args:
            D (float): Diamètre de la machine
            L (float): Longueur active
            pole_pairs (int): Nombre de paires de pôles
            magnet_thickness (float): Épaisseur des aimants
            machine_type (str): Type de machine
            air_gap (float): Entrefer
        
        Returns:
            dict: Dictionnaire avec les dimensions rotor
        """
        
        # Rayon extérieur rotor (avec entrefer)
        R_rotor = D/2 - air_gap
        
        # Rayon intérieur rotor (pour arbre)
        R_shaft = R_rotor * 0.4  # 40% du rayon rotor (standard)
        
        # Largeur des pôles/aimants selon type de machine
        if machine_type == 'IPMSM':
            pole_width = tau_p * 0.8  # 80% du pas polaire
        elif machine_type == 'SPMSM':
            pole_width = tau_p * 0.9  # 90% du pas polaire
        elif machine_type == 'SynRel':
            pole_width = tau_p * 0.7  # 70% du pas polaire
        else:  # Hybrid
            pole_width = tau_p * 0.75  # Compromis
        
        # Calculer tau_p si pas fourni
        tau_p = np.pi * D / (2 * pole_pairs)
        
        return {
            'R_ext': R_rotor,
            'R_int': R_shaft,
            'L': L,
            'pole_width': pole_width,
            'magnet_thickness': magnet_thickness,
            'tau_p': tau_p,
            'pole_pairs': pole_pairs
        }
    
    def calculate_stator_dimensions(self, D, L, slot_height, slot_width, Zs):
        """
        Calcul des dimensions stator selon Boldea
        
        Args:
            D (float): Diamètre de la machine
            L (float): Longueur active
            slot_height (float): Hauteur des encoches
            slot_width (float): Largeur des encoches
            Zs (int): Nombre d'encoches
        
        Returns:
            dict: Dictionnaire avec les dimensions stator
        """
        
        # Rayon extérieur stator
        R_stator_ext = D/2
        
        # Rayon intérieur stator (avec encoches)
        R_stator_int = R_stator_ext - slot_height
        
        # Vérifier que les encoches tiennent
        slot_area = slot_height * slot_width
        available_area = np.pi * (R_stator_ext**2 - R_stator_int**2) / Zs
        
        if slot_area > available_area * 0.8:  # 80% de l'espace disponible
            # Ajuster les dimensions des encoches
            slot_height = available_area * 0.8 / slot_width
        
        return {
            'R_ext': R_stator_ext,
            'R_int': R_stator_int,
            'L': L,
            'slot_height': slot_height,
            'slot_width': slot_width,
            'Zs': Zs,
            'slot_area': slot_area,
            'available_area_per_slot': available_area
        }
    
    def _adjust_coefficients_for_application(self, application):
        """Ajuster les coefficients selon l'application"""
        
        application_factors = {
            'traction': {'K_D': 1.0, 'K_L': 1.0},      # Standard
            'wind': {'K_D': 1.2, 'K_L': 0.8},          # Plus large, moins long
            'industrial': {'K_D': 0.9, 'K_L': 1.1},     # Plus long, moins large
            'aerospace': {'K_D': 0.8, 'K_L': 1.3}       # Très long, compact
        }
        
        if application in application_factors:
            factors = application_factors[application]
            self.K_D *= factors['K_D']
            self.K_L *= factors['K_L']
    
    def _calculate_optimal_slots(self, pole_pairs, machine_type):
        """Calculer le nombre optimal d'encoches selon Boldea"""
        
        # Base : 6 encoches par pôle (règle de Boldea)
        base_slots = 6 * pole_pairs
        
        # Ajustements selon le type de machine
        if machine_type == 'IPMSM':
            return base_slots
        elif machine_type == 'SPMSM':
            return base_slots
        elif machine_type == 'SynRel':
            return base_slots
        elif machine_type == 'Hybrid':
            return base_slots + 2  # Plus d'encoches pour la flexibilité
        
        return base_slots
    
    def _calculate_magnet_thickness(self, tau_p, machine_type):
        """Calculer l'épaisseur optimale des aimants"""
        
        if machine_type == 'IPMSM':
            return self.K_magnet * tau_p * 0.3  # 30% du pas polaire
        elif machine_type == 'SPMSM':
            return self.K_magnet * tau_p * 0.2  # 20% du pas polaire
        elif machine_type == 'SynRel':
            return 0  # Pas d'aimants
        elif machine_type == 'Hybrid':
            return self.K_magnet * tau_p * 0.25  # 25% du pas polaire
        
        return self.K_magnet * tau_p * 0.25
    
    def _calculate_adaptive_airgap(self, application, D):
        """Calculer l'entrefer adaptatif selon l'application"""
        
        # Entrefer de base : 0.1% du diamètre
        base_airgap = D * 0.001
        
        # Ajustements selon application
        application_factors = {
            'traction': 1.0,      # Standard
            'wind': 1.2,          # Plus grand pour robustesse
            'industrial': 1.1,    # Légèrement plus grand
            'aerospace': 0.8      # Plus petit pour performance
        }
        
        factor = application_factors.get(application, 1.0)
        return base_airgap * factor

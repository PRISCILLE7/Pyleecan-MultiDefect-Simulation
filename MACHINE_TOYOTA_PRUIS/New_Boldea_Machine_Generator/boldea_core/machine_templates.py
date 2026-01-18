"""
Templates de machines selon l'approche de Boldea
Configurations prédéfinies pour différents types d'applications
"""

import numpy as np

class MachineTemplates:
    """
    Templates de machines selon l'approche de Boldea
    """
    
    def __init__(self):
        # Applications supportées
        self.applications = ['traction', 'wind', 'industrial', 'aerospace']
        
        # Types de machines supportés
        self.machine_types = ['IPMSM', 'SPMSM', 'SynRel', 'Hybrid']
    
    def get_traction_template(self, power_rated, speed_rated):
        """
        Template pour application traction (véhicules électriques)
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Configuration du template
        """
        
        # Déterminer le nombre de pôles selon la puissance
        if power_rated < 50000:      # < 50kW
            pole_pairs = 2
        elif power_rated < 150000:   # 50-150kW
            pole_pairs = 3
        elif power_rated < 300000:   # 150-300kW
            pole_pairs = 4
        else:                         # > 300kW
            pole_pairs = 5
        
        # Ntcoil adaptatif selon la puissance
        if power_rated < 50000:
            ntcoil_options = [5, 7, 10]
        elif power_rated < 150000:
            ntcoil_options = [7, 10, 12]
        elif power_rated < 300000:
            ntcoil_options = [10, 12, 15]
        else:
            ntcoil_options = [12, 15, 18]
        
        return {
            'application': 'traction',
            'machine_type': 'IPMSM',  # IPMSM standard pour traction
            'pole_pairs': pole_pairs,
            'ntcoil_options': ntcoil_options,
            'characteristics': {
                'high_torque': True,
                'wide_speed_range': True,
                'efficiency_priority': True,
                'compact_design': True
            }
        }
    
    def get_wind_template(self, power_rated, speed_rated):
        """
        Template pour application éolienne
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Configuration du template
        """
        
        # Éolien : beaucoup de pôles, vitesse lente
        if power_rated < 100000:     # < 100kW
            pole_pairs = 8
        elif power_rated < 500000:   # 100-500kW
            pole_pairs = 12
        elif power_rated < 1000000:  # 500kW-1MW
            pole_pairs = 16
        else:                         # > 1MW
            pole_pairs = 20
        
        # Ntcoil adaptatif pour éolien
        if power_rated < 100000:
            ntcoil_options = [8, 10, 12]
        elif power_rated < 500000:
            ntcoil_options = [10, 12, 15]
        elif power_rated < 1000000:
            ntcoil_options = [12, 15, 18]
        else:
            ntcoil_options = [15, 18, 20]
        
        return {
            'application': 'wind',
            'machine_type': 'IPMSM',  # IPMSM pour éolien
            'pole_pairs': pole_pairs,
            'ntcoil_options': ntcoil_options,
            'characteristics': {
                'high_torque': True,
                'low_speed': True,
                'robustness_priority': True,
                'maintenance_friendly': True
            }
        }
    
    def get_industrial_template(self, power_rated, speed_rated):
        """
        Template pour application industrielle
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Configuration du template
        """
        
        # Industriel : pôles modérés
        if power_rated < 75000:      # < 75kW
            pole_pairs = 2
        elif power_rated < 200000:   # 75-200kW
            pole_pairs = 3
        elif power_rated < 500000:   # 200-500kW
            pole_pairs = 4
        else:                         # > 500kW
            pole_pairs = 6
        
        # Ntcoil adaptatif pour industriel
        if power_rated < 75000:
            ntcoil_options = [6, 8, 10]
        elif power_rated < 200000:
            ntcoil_options = [8, 10, 12]
        elif power_rated < 500000:
            ntcoil_options = [10, 12, 15]
        else:
            ntcoil_options = [12, 15, 18]
        
        return {
            'application': 'industrial',
            'machine_type': 'IPMSM',  # IPMSM pour industriel
            'pole_pairs': pole_pairs,
            'ntcoil_options': ntcoil_options,
            'characteristics': {
                'standard_performance': True,
                'cost_effective': True,
                'reliability_priority': True,
                'easy_manufacturing': True
            }
        }
    
    def get_aerospace_template(self, power_rated, speed_rated):
        """
        Template pour application aérospatiale
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Configuration du template
        """
        
        # Aérospatial : pôles modérés, haute performance
        if power_rated < 50000:      # < 50kW
            pole_pairs = 2
        elif power_rated < 150000:   # 50-150kW
            pole_pairs = 3
        elif power_rated < 300000:   # 150-300kW
            pole_pairs = 4
        else:                         # > 300kW
            pole_pairs = 5
        
        # Ntcoil adaptatif pour aérospatial
        if power_rated < 50000:
            ntcoil_options = [8, 10, 12]
        elif power_rated < 150000:
            ntcoil_options = [10, 12, 15]
        elif power_rated < 300000:
            ntcoil_options = [12, 15, 18]
        else:
            ntcoil_options = [15, 18, 20]
        
        return {
            'application': 'aerospace',
            'machine_type': 'IPMSM',  # IPMSM haute performance
            'pole_pairs': pole_pairs,
            'ntcoil_options': ntcoil_options,
            'characteristics': {
                'high_efficiency': True,
                'lightweight': True,
                'high_reliability': True,
                'performance_priority': True
            }
        }
    
    def get_synrel_template(self, power_rated, speed_rated):
        """
        Template pour machine à réluctance synchrone
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Configuration du template
        """
        
        # SynRel : plus de pôles pour la réluctance
        if power_rated < 75000:      # < 75kW
            pole_pairs = 3
        elif power_rated < 200000:   # 75-200kW
            pole_pairs = 4
        elif power_rated < 500000:   # 200-500kW
            pole_pairs = 6
        else:                         # > 500kW
            pole_pairs = 8
        
        # Ntcoil adaptatif pour SynRel
        if power_rated < 75000:
            ntcoil_options = [6, 8, 10]
        elif power_rated < 200000:
            ntcoil_options = [8, 10, 12]
        elif power_rated < 500000:
            ntcoil_options = [10, 12, 15]
        else:
            ntcoil_options = [12, 15, 18]
        
        return {
            'application': 'industrial',  # SynRel principalement industriel
            'machine_type': 'SynRel',
            'pole_pairs': pole_pairs,
            'ntcoil_options': ntcoil_options,
            'characteristics': {
                'no_magnets': True,
                'cost_effective': True,
                'high_speed_capability': True,
                'simple_construction': True
            }
        }
    
    def get_hybrid_template(self, power_rated, speed_rated):
        """
        Template pour machine hybride (IPMSM + SynRel)
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Configuration du template
        """
        
        # Hybride : compromis entre IPMSM et SynRel
        if power_rated < 100000:     # < 100kW
            pole_pairs = 3
        elif power_rated < 250000:   # 100-250kW
            pole_pairs = 4
        elif power_rated < 500000:   # 250-500kW
            pole_pairs = 5
        else:                         # > 500kW
            pole_pairs = 6
        
        # Ntcoil adaptatif pour hybride
        if power_rated < 100000:
            ntcoil_options = [7, 9, 11]
        elif power_rated < 250000:
            ntcoil_options = [9, 11, 13]
        elif power_rated < 500000:
            ntcoil_options = [11, 13, 16]
        else:
            ntcoil_options = [13, 16, 19]
        
        return {
            'application': 'traction',  # Hybride principalement pour traction
            'machine_type': 'Hybrid',
            'pole_pairs': pole_pairs,
            'ntcoil_options': ntcoil_options,
            'characteristics': {
                'dual_torque': True,      # Couple magnétique + réluctance
                'wide_speed_range': True,
                'high_efficiency': True,
                'complex_control': True
            }
        }
    
    def get_template_by_application(self, application, power_rated, speed_rated):
        """
        Obtenir le template approprié selon l'application
        
        Args:
            application (str): Type d'application
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Configuration du template
        """
        
        if application == 'traction':
            return self.get_traction_template(power_rated, speed_rated)
        elif application == 'wind':
            return self.get_wind_template(power_rated, speed_rated)
        elif application == 'industrial':
            return self.get_industrial_template(power_rated, speed_rated)
        elif application == 'aerospace':
            return self.get_aerospace_template(power_rated, speed_rated)
        else:
            raise ValueError(f"Application '{application}' non supportée")
    
    def get_all_templates(self, power_rated, speed_rated):
        """
        Obtenir tous les templates disponibles pour une puissance/vitesse donnée
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
        
        Returns:
            dict: Tous les templates disponibles
        """
        
        templates = {}
        
        # Templates par application
        for app in self.applications:
            templates[app] = self.get_template_by_application(app, power_rated, speed_rated)
        
        # Templates spéciaux
        templates['SynRel'] = self.get_synrel_template(power_rated, speed_rated)
        templates['Hybrid'] = self.get_hybrid_template(power_rated, speed_rated)
        
        return templates
    
    def suggest_machine_type(self, power_rated, speed_rated, requirements):
        """
        Suggérer le type de machine optimal selon les exigences
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
            requirements (dict): Exigences spécifiques
        
        Returns:
            dict: Suggestion de machine optimale
        """
        
        suggestions = []
        
        # Analyser chaque type selon les exigences
        all_templates = self.get_all_templates(power_rated, speed_rated)
        
        for machine_type, template in all_templates.items():
            score = 0
            
            # Score selon les caractéristiques
            if requirements.get('high_efficiency', False) and template['characteristics'].get('high_efficiency', False):
                score += 20
            
            if requirements.get('cost_effective', False) and template['characteristics'].get('cost_effective', False):
                score += 15
            
            if requirements.get('high_torque', False) and template['characteristics'].get('high_torque', False):
                score += 15
            
            if requirements.get('lightweight', False) and template['characteristics'].get('lightweight', False):
                score += 15
            
            if requirements.get('simple_control', False) and not template['characteristics'].get('complex_control', False):
                score += 10
            
            suggestions.append({
                'machine_type': machine_type,
                'template': template,
                'score': score
            })
        
        # Trier par score décroissant
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        
        return suggestions

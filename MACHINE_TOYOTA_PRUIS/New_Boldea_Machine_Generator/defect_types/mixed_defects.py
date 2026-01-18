"""
Module Defects Types - Défauts mixtes réalistes
Génère des défauts combinant thermiques, mécaniques et électriques
"""

import numpy as np
import random
from typing import Dict, List, Any, Optional
from thermal_defects import ThermalDefectGenerator
from mechanical_defects import MechanicalDefectGenerator
from electrical_defects import ElectricalDefectGenerator

class MixedDefectGenerator:
    """Générateur de défauts mixtes réalistes"""
    
    def __init__(self):
        """Initialisation du générateur"""
        self.thermal_gen = ThermalDefectGenerator()
        self.mechanical_gen = MechanicalDefectGenerator()
        self.electrical_gen = ElectricalDefectGenerator()
        
        # Types de défauts mixtes
        self.mixed_defect_types = {
            'thermal_mechanical': 'Défaut thermo-mécanique',
            'thermal_electrical': 'Défaut thermo-électrique',
            'mechanical_electrical': 'Défaut mécanico-électrique',
            'cascade_failure': 'Défaillance en cascade',
            'aging_related': 'Défaut lié au vieillissement',
            'overload_induced': 'Défaut induit par surcharge',
            'environmental': 'Défaut environnemental',
            'maintenance_related': 'Défaut lié à la maintenance'
        }
        
        # Scénarios de défauts mixtes
        self.mixed_scenarios = {
            'thermal_mechanical': {
                'hotspot_bearing_wear': 'Point chaud + usure roulement',
                'thermal_deformation_vibration': 'Déformation thermique + vibration',
                'cooling_failure_misalignment': 'Défaillance refroidissement + mauvais alignement'
            },
            'thermal_electrical': {
                'overheating_insulation': 'Surchauffe + dégradation isolation',
                'thermal_gradient_winding': 'Gradient thermique + défaut enroulement',
                'hotspot_demagnetization': 'Point chaud + démagnétisation'
            },
            'mechanical_electrical': {
                'vibration_winding': 'Vibration + défaut enroulement',
                'eccentricity_phase_unbalance': 'Excentricité + déséquilibre phase',
                'bearing_wear_eddy_current': 'Usure roulement + courants de Foucault'
            },
            'cascade_failure': {
                'thermal_cascade': 'Cascade thermique',
                'mechanical_cascade': 'Cascade mécanique',
                'electrical_cascade': 'Cascade électrique'
            }
        }
    
    def generate_thermal_mechanical_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut thermo-mécanique"""
        severity_factor = severity / 5.0
        
        # Choisir le scénario
        scenario = random.choice(list(self.mixed_scenarios['thermal_mechanical'].keys()))
        
        # Générer les défauts individuels
        thermal_defect = self.thermal_gen.generate_random_thermal_defect(machine_dims, severity)
        mechanical_defect = self.mechanical_gen.generate_random_mechanical_defect(machine_dims, severity)
        
        # Interactions entre défauts
        interaction_factor = 1 + severity_factor * 0.5
        
        # Impact combiné
        combined_impact = {
            'temperature_rise': (thermal_defect['impact'].get('temperature_rise', 0) + 
                               mechanical_defect['impact'].get('thermal_stress', 0)) * interaction_factor,
            'vibration': (thermal_defect['impact'].get('vibration', 0) + 
                         mechanical_defect['impact'].get('vibration', 0)) * interaction_factor,
            'efficiency_loss': (thermal_defect['impact'].get('efficiency_loss', 0) + 
                              mechanical_defect['impact'].get('efficiency_loss', 0)) * interaction_factor,
            'structural_stress': mechanical_defect['impact'].get('structural_stress', 0) * interaction_factor
        }
        
        return {
            'defect_type': 'thermal_mechanical',
            'severity': severity,
            'description': f'Défaut thermo-mécanique: {self.mixed_scenarios["thermal_mechanical"][scenario]}',
            'scenario': scenario,
            'thermal_defect': thermal_defect,
            'mechanical_defect': mechanical_defect,
            'interaction_factor': interaction_factor,
            'impact': combined_impact,
            'failure_mode': 'progressive_thermal_mechanical'
        }
    
    def generate_thermal_electrical_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut thermo-électrique"""
        severity_factor = severity / 5.0
        
        # Choisir le scénario
        scenario = random.choice(list(self.mixed_scenarios['thermal_electrical'].keys()))
        
        # Générer les défauts individuels
        thermal_defect = self.thermal_gen.generate_random_thermal_defect(machine_dims, severity)
        electrical_defect = self.electrical_gen.generate_random_electrical_defect(machine_dims, severity)
        
        # Interactions entre défauts
        interaction_factor = 1 + severity_factor * 0.6
        
        # Impact combiné
        combined_impact = {
            'temperature_rise': (thermal_defect['impact'].get('temperature_rise', 0) + 
                               electrical_defect['impact'].get('temperature_rise', 0)) * interaction_factor,
            'efficiency_loss': (thermal_defect['impact'].get('efficiency_loss', 0) + 
                              electrical_defect['impact'].get('efficiency_loss', 0)) * interaction_factor,
            'safety_risk': electrical_defect['impact'].get('safety_risk', 0) * interaction_factor,
            'thermal_stress': thermal_defect['impact'].get('thermal_stress', 0) * interaction_factor
        }
        
        return {
            'defect_type': 'thermal_electrical',
            'severity': severity,
            'description': f'Défaut thermo-électrique: {self.mixed_scenarios["thermal_electrical"][scenario]}',
            'scenario': scenario,
            'thermal_defect': thermal_defect,
            'electrical_defect': electrical_defect,
            'interaction_factor': interaction_factor,
            'impact': combined_impact,
            'failure_mode': 'thermal_electrical_coupling'
        }
    
    def generate_mechanical_electrical_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut mécanico-électrique"""
        severity_factor = severity / 5.0
        
        # Choisir le scénario
        scenario = random.choice(list(self.mixed_scenarios['mechanical_electrical'].keys()))
        
        # Générer les défauts individuels
        mechanical_defect = self.mechanical_gen.generate_random_mechanical_defect(machine_dims, severity)
        electrical_defect = self.electrical_gen.generate_random_electrical_defect(machine_dims, severity)
        
        # Interactions entre défauts
        interaction_factor = 1 + severity_factor * 0.4
        
        # Impact combiné
        combined_impact = {
            'vibration': (mechanical_defect['impact'].get('vibration', 0) + 
                         electrical_defect['impact'].get('vibration', 0)) * interaction_factor,
            'efficiency_loss': (mechanical_defect['impact'].get('efficiency_loss', 0) + 
                              electrical_defect['impact'].get('efficiency_loss', 0)) * interaction_factor,
            'torque_ripple': (mechanical_defect['impact'].get('torque_ripple', 0) + 
                             electrical_defect['impact'].get('torque_ripple', 0)) * interaction_factor,
            'bearing_load': mechanical_defect['impact'].get('bearing_load', 0) * interaction_factor
        }
        
        return {
            'defect_type': 'mechanical_electrical',
            'severity': severity,
            'description': f'Défaut mécanico-électrique: {self.mixed_scenarios["mechanical_electrical"][scenario]}',
            'scenario': scenario,
            'mechanical_defect': mechanical_defect,
            'electrical_defect': electrical_defect,
            'interaction_factor': interaction_factor,
            'impact': combined_impact,
            'failure_mode': 'mechanical_electrical_interaction'
        }
    
    def generate_cascade_failure_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut en cascade"""
        severity_factor = severity / 5.0
        
        # Type de cascade
        cascade_type = random.choice(list(self.mixed_scenarios['cascade_failure'].keys()))
        
        # Nombre d'étapes de cascade
        cascade_steps = random.randint(2, 4)
        
        # Générer la séquence de défauts
        cascade_sequence = []
        current_severity = severity
        
        for step in range(cascade_steps):
            # Réduire la gravité à chaque étape
            step_severity = max(1, int(current_severity * (1 - step * 0.2)))
            
            # Choisir le type de défaut selon l'étape
            if step == 0:  # Premier défaut
                defect_type = random.choice(['thermal', 'mechanical', 'electrical'])
            else:  # Défauts induits
                defect_type = random.choice(['thermal', 'mechanical', 'electrical'])
            
            # Générer le défaut
            if defect_type == 'thermal':
                defect = self.thermal_gen.generate_random_thermal_defect(machine_dims, step_severity)
            elif defect_type == 'mechanical':
                defect = self.mechanical_gen.generate_random_mechanical_defect(machine_dims, step_severity)
            else:  # electrical
                defect = self.electrical_gen.generate_random_electrical_defect(machine_dims, step_severity)
            
            cascade_sequence.append({
                'step': step + 1,
                'defect_type': defect_type,
                'defect': defect,
                'severity': step_severity
            })
            
            current_severity = step_severity
        
        # Impact total de la cascade
        total_impact = {}
        for step in cascade_sequence:
            for impact_type, impact_value in step['defect']['impact'].items():
                if impact_type not in total_impact:
                    total_impact[impact_type] = 0
                total_impact[impact_type] += impact_value * (1 + step['step'] * 0.1)
        
        return {
            'defect_type': 'cascade_failure',
            'severity': severity,
            'description': f'Défaillance en cascade {cascade_type}: {cascade_steps} étapes',
            'cascade_type': cascade_type,
            'cascade_steps': cascade_steps,
            'cascade_sequence': cascade_sequence,
            'impact': total_impact,
            'failure_mode': 'progressive_cascade',
            'time_to_failure': severity * (10 - cascade_steps * 2)  # heures
        }
    
    def generate_aging_related_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut lié au vieillissement"""
        severity_factor = severity / 5.0
        
        # Âge de la machine (années)
        machine_age = random.uniform(5, 20)
        
        # Facteur de vieillissement
        aging_factor = 1 + (machine_age - 5) / 15 * severity_factor
        
        # Types de défauts liés au vieillissement
        aging_defects = []
        
        # Défaut thermique lié au vieillissement
        thermal_defect = self.thermal_gen.generate_random_thermal_defect(machine_dims, severity)
        thermal_defect['aging_factor'] = aging_factor
        aging_defects.append(('thermal', thermal_defect))
        
        # Défaut mécanique lié au vieillissement
        mechanical_defect = self.mechanical_gen.generate_random_mechanical_defect(machine_dims, severity)
        mechanical_defect['aging_factor'] = aging_factor
        aging_defects.append(('mechanical', mechanical_defect))
        
        # Défaut électrique lié au vieillissement
        electrical_defect = self.electrical_gen.generate_random_electrical_defect(machine_dims, severity)
        electrical_defect['aging_factor'] = aging_factor
        aging_defects.append(('electrical', electrical_defect))
        
        # Impact combiné avec facteur de vieillissement
        combined_impact = {}
        for defect_type, defect in aging_defects:
            for impact_type, impact_value in defect['impact'].items():
                if impact_type not in combined_impact:
                    combined_impact[impact_type] = 0
                combined_impact[impact_type] += impact_value * aging_factor
        
        return {
            'defect_type': 'aging_related',
            'severity': severity,
            'description': f'Défauts liés au vieillissement après {machine_age:.1f} ans',
            'machine_age': machine_age,
            'aging_factor': aging_factor,
            'aging_defects': aging_defects,
            'impact': combined_impact,
            'failure_mode': 'aging_induced',
            'maintenance_recommendation': 'replacement_consideration'
        }
    
    def generate_overload_induced_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut induit par surcharge"""
        severity_factor = severity / 5.0
        
        # Type de surcharge
        overload_type = random.choice(['thermal', 'mechanical', 'electrical', 'combined'])
        
        # Facteur de surcharge
        overload_factor = 1 + severity_factor * 2  # 1x à 3x la charge nominale
        
        # Durée de surcharge
        overload_duration = random.uniform(0.5, 8.0)  # heures
        
        # Défauts induits par la surcharge
        induced_defects = []
        
        if overload_type in ['thermal', 'combined']:
            # Surcharge thermique
            thermal_defect = self.thermal_gen.generate_overload_defect(machine_dims, severity)
            thermal_defect['overload_factor'] = overload_factor
            thermal_defect['overload_duration'] = overload_duration
            induced_defects.append(('thermal', thermal_defect))
        
        if overload_type in ['mechanical', 'combined']:
            # Surcharge mécanique
            mechanical_defect = self.mechanical_gen.generate_random_mechanical_defect(machine_dims, severity)
            mechanical_defect['overload_factor'] = overload_factor
            mechanical_defect['overload_duration'] = overload_duration
            induced_defects.append(('mechanical', mechanical_defect))
        
        if overload_type in ['electrical', 'combined']:
            # Surcharge électrique
            electrical_defect = self.electrical_gen.generate_random_electrical_defect(machine_dims, severity)
            electrical_defect['overload_factor'] = overload_factor
            electrical_defect['overload_duration'] = overload_duration
            induced_defects.append(('electrical', electrical_defect))
        
        # Impact combiné
        combined_impact = {}
        for defect_type, defect in induced_defects:
            for impact_type, impact_value in defect['impact'].items():
                if impact_type not in combined_impact:
                    combined_impact[impact_type] = 0
                combined_impact[impact_type] += impact_value * overload_factor
        
        return {
            'defect_type': 'overload_induced',
            'severity': severity,
            'description': f'Défauts induits par surcharge {overload_type} de {overload_factor:.1f}x pendant {overload_duration:.1f}h',
            'overload_type': overload_type,
            'overload_factor': overload_factor,
            'overload_duration': overload_duration,
            'induced_defects': induced_defects,
            'impact': combined_impact,
            'failure_mode': 'overload_induced',
            'recovery_possible': overload_duration < 2.0
        }
    
    def generate_environmental_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut environnemental"""
        severity_factor = severity / 5.0
        
        # Type d'environnement
        environment_types = {
            'humid': 'Environnement humide',
            'dusty': 'Environnement poussiéreux',
            'corrosive': 'Environnement corrosif',
            'high_temp': 'Température élevée',
            'vibration': 'Vibrations ambiantes',
            'electromagnetic': 'Interférences électromagnétiques'
        }
        
        environment_type = random.choice(list(environment_types.keys()))
        
        # Facteur environnemental
        env_factor = 1 + severity_factor * 0.8
        
        # Défauts induits par l'environnement
        env_defects = []
        
        if environment_type in ['humid', 'corrosive']:
            # Défauts électriques
            electrical_defect = self.electrical_gen.generate_insulation_degradation_defect(machine_dims, severity)
            electrical_defect['environment_factor'] = env_factor
            env_defects.append(('electrical', electrical_defect))
        
        if environment_type in ['dusty', 'high_temp']:
            # Défauts thermiques
            thermal_defect = self.thermal_gen.generate_random_thermal_defect(machine_dims, severity)
            thermal_defect['environment_factor'] = env_factor
            env_defects.append(('thermal', thermal_defect))
        
        if environment_type in ['vibration', 'electromagnetic']:
            # Défauts mécaniques
            mechanical_defect = self.mechanical_gen.generate_random_mechanical_defect(machine_dims, severity)
            mechanical_defect['environment_factor'] = env_factor
            env_defects.append(('mechanical', mechanical_defect))
        
        # Impact combiné
        combined_impact = {}
        for defect_type, defect in env_defects:
            for impact_type, impact_value in defect['impact'].items():
                if impact_type not in combined_impact:
                    combined_impact[impact_type] = 0
                combined_impact[impact_type] += impact_value * env_factor
        
        return {
            'defect_type': 'environmental',
            'severity': severity,
            'description': f'Défauts environnementaux: {environment_types[environment_type]}',
            'environment_type': environment_type,
            'environment_factor': env_factor,
            'env_defects': env_defects,
            'impact': combined_impact,
            'failure_mode': 'environment_induced',
            'protection_recommendation': f'Protection contre {environment_type}'
        }
    
    def generate_maintenance_related_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut lié à la maintenance"""
        severity_factor = severity / 5.0
        
        # Type de problème de maintenance
        maintenance_issues = {
            'improper_lubrication': 'Lubrification incorrecte',
            'wrong_torque': 'Serrage incorrect',
            'contamination': 'Contamination lors maintenance',
            'replacement_error': 'Erreur de remplacement',
            'calibration_error': 'Erreur de calibration',
            'cleaning_issue': 'Problème de nettoyage'
        }
        
        maintenance_issue = random.choice(list(maintenance_issues.keys()))
        
        # Facteur de maintenance
        maintenance_factor = 1 + severity_factor * 0.6
        
        # Défauts induits par la maintenance
        maintenance_defects = []
        
        if maintenance_issue in ['improper_lubrication', 'contamination']:
            # Défauts mécaniques
            mechanical_defect = self.mechanical_gen.generate_bearing_wear_defect(machine_dims, severity)
            mechanical_defect['maintenance_factor'] = maintenance_factor
            maintenance_defects.append(('mechanical', mechanical_defect))
        
        if maintenance_issue in ['wrong_torque', 'replacement_error']:
            # Défauts mécaniques
            mechanical_defect = self.mechanical_gen.generate_misalignment_defect(machine_dims, severity)
            mechanical_defect['maintenance_factor'] = maintenance_factor
            maintenance_defects.append(('mechanical', mechanical_defect))
        
        if maintenance_issue in ['calibration_error', 'cleaning_issue']:
            # Défauts électriques
            electrical_defect = self.electrical_gen.generate_random_electrical_defect(machine_dims, severity)
            electrical_defect['maintenance_factor'] = maintenance_factor
            maintenance_defects.append(('electrical', electrical_defect))
        
        # Impact combiné
        combined_impact = {}
        for defect_type, defect in maintenance_defects:
            for impact_type, impact_value in defect['impact'].items():
                if impact_type not in combined_impact:
                    combined_impact[impact_type] = 0
                combined_impact[impact_type] += impact_value * maintenance_factor
        
        return {
            'defect_type': 'maintenance_related',
            'severity': severity,
            'description': f'Défaut lié à la maintenance: {maintenance_issues[maintenance_issue]}',
            'maintenance_issue': maintenance_issue,
            'maintenance_factor': maintenance_factor,
            'maintenance_defects': maintenance_defects,
            'impact': combined_impact,
            'failure_mode': 'maintenance_induced',
            'corrective_action': f'Révision procédure {maintenance_issue}'
        }
    
    def generate_random_mixed_defect(self, machine_dims: Dict[str, float], severity: Optional[int] = None) -> Dict[str, Any]:
        """Génère un défaut mixte aléatoire"""
        if severity is None:
            severity = random.randint(1, 5)
        
        defect_type = random.choice(list(self.mixed_defect_types.keys()))
        
        if defect_type == 'thermal_mechanical':
            return self.generate_thermal_mechanical_defect(machine_dims, severity)
        elif defect_type == 'thermal_electrical':
            return self.generate_thermal_electrical_defect(machine_dims, severity)
        elif defect_type == 'mechanical_electrical':
            return self.generate_mechanical_electrical_defect(machine_dims, severity)
        elif defect_type == 'cascade_failure':
            return self.generate_cascade_failure_defect(machine_dims, severity)
        elif defect_type == 'aging_related':
            return self.generate_aging_related_defect(machine_dims, severity)
        elif defect_type == 'overload_induced':
            return self.generate_overload_induced_defect(machine_dims, severity)
        elif defect_type == 'environmental':
            return self.generate_environmental_defect(machine_dims, severity)
        elif defect_type == 'maintenance_related':
            return self.generate_maintenance_related_defect(machine_dims, severity)
        else:
            raise ValueError(f"Type de défaut mixte inconnu: {defect_type}")
    
    def generate_mixed_defect_batch(self, machine_dims: Dict[str, float], 
                                  num_defects: int = 5,
                                  severity_distribution: Optional[Dict[int, float]] = None) -> List[Dict[str, Any]]:
        """Génère un lot de défauts mixtes"""
        if severity_distribution is None:
            severity_distribution = {1: 0.2, 2: 0.3, 3: 0.3, 4: 0.15, 5: 0.05}
        
        defects = []
        
        for _ in range(num_defects):
            # Choisir la gravité selon la distribution
            severity = np.random.choice(
                list(severity_distribution.keys()),
                p=list(severity_distribution.values())
            )
            
            # Générer le défaut
            defect = self.generate_random_mixed_defect(machine_dims, severity)
            defects.append(defect)
        
        return defects
    
    def get_defect_statistics(self, defects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcule les statistiques des défauts mixtes"""
        if not defects:
            return {'total_defects': 0, 'average_severity': 0}
        
        severities = [d['severity'] for d in defects]
        defect_types = [d['defect_type'] for d in defects]
        
        # Compter les types
        type_counts = {}
        for defect_type in defect_types:
            type_counts[defect_type] = type_counts.get(defect_type, 0) + 1
        
        # Analyser les interactions
        interaction_factors = []
        failure_modes = []
        
        for defect in defects:
            if 'interaction_factor' in defect:
                interaction_factors.append(defect['interaction_factor'])
            if 'failure_mode' in defect:
                failure_modes.append(defect['failure_mode'])
        
        # Calculer les impacts moyens
        total_impact = {}
        for defect in defects:
            for impact_type, impact_value in defect['impact'].items():
                if impact_type not in total_impact:
                    total_impact[impact_type] = []
                total_impact[impact_type].append(impact_value)
        
        avg_impacts = {}
        for impact_type, impact_values in total_impact.items():
            avg_impacts[impact_type] = np.mean(impact_values)
        
        return {
            'total_defects': len(defects),
            'average_severity': np.mean(severities),
            'severity_distribution': {i: severities.count(i) for i in range(1, 6)},
            'type_distribution': type_counts,
            'average_impacts': avg_impacts,
            'interaction_factors': interaction_factors,
            'failure_modes': list(set(failure_modes))
        }
    
    def get_defect_recommendations(self, defects: List[Dict[str, Any]]) -> List[str]:
        """Génère des recommandations basées sur les défauts mixtes"""
        recommendations = []
        
        if not defects:
            return ["Aucun défaut mixte détecté - machine en bon état"]
        
        # Analyser les défauts par gravité
        high_severity = [d for d in defects if d['severity'] >= 4]
        medium_severity = [d for d in defects if 2 <= d['severity'] <= 3]
        
        if high_severity:
            recommendations.append("⚠️  Défauts mixtes critiques détectés - analyse approfondie requise")
        
        if medium_severity:
            recommendations.append("🔧 Défauts mixtes modérés détectés - surveillance renforcée")
        
        # Recommandations spécifiques par type
        defect_types = [d['defect_type'] for d in defects]
        
        if 'cascade_failure' in defect_types:
            recommendations.append("🔄 Analyser la séquence de défaillance pour identifier la cause racine")
        
        if 'aging_related' in defect_types:
            recommendations.append("⏰ Évaluer la nécessité de remplacement ou rénovation")
        
        if 'overload_induced' in defect_types:
            recommendations.append("⚡ Réviser les conditions de charge et les protections")
        
        if 'environmental' in defect_types:
            recommendations.append("🌍 Améliorer la protection environnementale et l'isolation")
        
        if 'maintenance_related' in defect_types:
            recommendations.append("🔧 Réviser les procédures de maintenance et former le personnel")
        
        # Recommandations générales pour défauts mixtes
        recommendations.append("🔍 Effectuer une analyse croisée thermique-mécanique-électrique")
        recommendations.append("📊 Surveiller les paramètres de performance et les tendances")
        
        return recommendations

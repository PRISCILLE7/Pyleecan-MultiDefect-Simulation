"""
Module de validation selon les critères de Boldea
Vérifie la cohérence physique des machines générées
"""

import numpy as np

class BoldeaValidator:
    """
    Classe de validation des machines selon les critères de Boldea
    """
    
    def __init__(self):
        # Limites physiques selon Boldea
        self.limits = {
            'D_L_ratio': {'min': 1.2, 'max': 3.0, 'optimal': 1.5},
            'tau_p': {'min': 0.02, 'max': 0.15},  # m
            'slot_fill_factor': {'min': 0.3, 'max': 0.7},  # %
            'magnet_thickness_ratio': {'min': 0.15, 'max': 0.35},  # % du pas polaire
            'air_gap_ratio': {'min': 0.0005, 'max': 0.002},  # % du diamètre
            'flux_density': {'max': 1.8}  # Tesla (limite de saturation)
        }
        
        # Coefficients de validation
        self.validation_score = 0.0
        self.warnings = []
        self.errors = []
    
    def validate_machine_design(self, machine_dims, machine_type='IPMSM'):
        """
        Validation complète d'une machine selon Boldea
        
        Args:
            machine_dims (dict): Dimensions de la machine
            machine_type (str): Type de machine
        
        Returns:
            dict: Résultats de validation
        """
        
        self.validation_score = 0.0
        self.warnings = []
        self.errors = []
        
        # Validation des dimensions principales
        self._validate_main_dimensions(machine_dims)
        
        # Validation des ratios géométriques
        self._validate_geometric_ratios(machine_dims)
        
        # Validation spécifique au type de machine
        self._validate_machine_specific(machine_dims, machine_type)
        
        # Calcul du score final
        self._calculate_validation_score()
        
        return {
            'score': self.validation_score,
            'warnings': self.warnings,
            'errors': self.errors,
            'is_valid': len(self.errors) == 0,
            'quality_level': self._get_quality_level()
        }
    
    def _validate_main_dimensions(self, dims):
        """Validation des dimensions principales"""
        
        # Vérifier que toutes les dimensions sont positives
        required_dims = ['D', 'L', 'Zs', 'slot_height', 'slot_width']
        for dim in required_dims:
            if dim in dims and dims[dim] <= 0:
                self.errors.append(f"Dimension {dim} doit être positive: {dims[dim]}")
        
        # Vérifier la cohérence des rayons
        if 'R_ext' in dims and 'R_int' in dims:
            if dims['R_ext'] <= dims['R_int']:
                self.errors.append("Rayon extérieur doit être > rayon intérieur")
        
        # Vérifier le nombre d'encoches
        if 'Zs' in dims and 'pole_pairs' in dims:
            Zs = dims['Zs']
            p = dims['pole_pairs']
            if Zs % (2 * p) != 0:
                self.warnings.append(f"Nombre d'encoches {Zs} non divisible par {2*p}")
    
    def _validate_geometric_ratios(self, dims):
        """Validation des ratios géométriques"""
        
        # Ratio D/L
        if 'D' in dims and 'L' in dims:
            D_L_ratio = dims['D'] / dims['L']
            optimal = self.limits['D_L_ratio']['optimal']
            min_ratio = self.limits['D_L_ratio']['min']
            max_ratio = self.limits['D_L_ratio']['max']
            
            if D_L_ratio < min_ratio:
                self.warnings.append(f"Ratio D/L = {D_L_ratio:.2f} < {min_ratio} (machine trop longue)")
            elif D_L_ratio > max_ratio:
                self.warnings.append(f"Ratio D/L = {D_L_ratio:.2f} > {max_ratio} (machine trop large)")
            elif abs(D_L_ratio - optimal) < 0.1:
                self.validation_score += 20  # Bonus pour ratio optimal
        
        # Pas polaire
        if 'tau_p' in dims:
            tau_p = dims['tau_p']
            min_tau = self.limits['tau_p']['min']
            max_tau = self.limits['tau_p']['max']
            
            if tau_p < min_tau:
                self.warnings.append(f"Pas polaire = {tau_p:.3f}m < {min_tau}m (trop petit)")
            elif tau_p > max_tau:
                self.warnings.append(f"Pas polaire = {tau_p:.3f}m > {max_tau}m (trop grand)")
        
        # Entrefer
        if 'air_gap' in dims and 'D' in dims:
            air_gap_ratio = dims['air_gap'] / dims['D']
            min_ratio = self.limits['air_gap_ratio']['min']
            max_ratio = self.limits['air_gap_ratio']['max']
            
            if air_gap_ratio < min_ratio:
                self.warnings.append(f"Entrefer = {air_gap_ratio:.4f} < {min_ratio} (trop petit)")
            elif air_gap_ratio > max_ratio:
                self.warnings.append(f"Entrefer = {air_gap_ratio:.4f} > {max_ratio} (trop grand)")
    
    def _validate_machine_specific(self, dims, machine_type):
        """Validation spécifique au type de machine"""
        
        if machine_type == 'IPMSM':
            self._validate_ipmsm(dims)
        elif machine_type == 'SPMSM':
            self._validate_spmsm(dims)
        elif machine_type == 'SynRel':
            self._validate_synrel(dims)
        elif machine_type == 'Hybrid':
            self._validate_hybrid(dims)
    
    def _validate_ipmsm(self, dims):
        """Validation spécifique IPMSM"""
        
        if 'magnet_thickness' in dims and 'tau_p' in dims:
            magnet_ratio = dims['magnet_thickness'] / dims['tau_p']
            min_ratio = self.limits['magnet_thickness_ratio']['min']
            max_ratio = self.limits['magnet_thickness_ratio']['max']
            
            if magnet_ratio < min_ratio:
                self.warnings.append(f"Épaisseur aimant = {magnet_ratio:.2f} < {min_ratio} (trop mince)")
            elif magnet_ratio > max_ratio:
                self.warnings.append(f"Épaisseur aimant = {magnet_ratio:.2f} > {max_ratio} (trop épais)")
    
    def _validate_spmsm(self, dims):
        """Validation spécifique SPMSM"""
        
        # Pour SPMSM, vérifier que les aimants ne sont pas trop épais
        if 'magnet_thickness' in dims and 'tau_p' in dims:
            magnet_ratio = dims['magnet_thickness'] / dims['tau_p']
            if magnet_ratio > 0.25:  # Limite plus stricte pour SPMSM
                self.warnings.append(f"Épaisseur aimant SPMSM = {magnet_ratio:.2f} > 0.25 (trop épais)")
    
    def _validate_synrel(self, dims):
        """Validation spécifique SynRel"""
        
        # Pour SynRel, vérifier les pôles saillants
        if 'pole_depth' in dims and 'pole_width' in dims:
            aspect_ratio = dims['pole_depth'] / dims['pole_width']
            if aspect_ratio < 0.3:
                self.warnings.append(f"Ratio profondeur/largeur pôle = {aspect_ratio:.2f} < 0.3 (pôles trop plats)")
            elif aspect_ratio > 0.7:
                self.warnings.append(f"Ratio profondeur/largeur pôle = {aspect_ratio:.2f} > 0.7 (pôles trop profonds)")
    
    def _validate_hybrid(self, dims):
        """Validation spécifique Hybrid"""
        
        # Pour Hybrid, vérifier le compromis entre aimants et réluctance
        if 'magnet_thickness' in dims and 'tau_p' in dims:
            magnet_ratio = dims['magnet_thickness'] / dims['tau_p']
            if magnet_ratio < 0.2 or magnet_ratio > 0.3:
                self.warnings.append(f"Épaisseur aimant Hybrid = {magnet_ratio:.2f} (hors plage optimale [0.2, 0.3])")
    
    def _calculate_validation_score(self):
        """Calculer le score de validation"""
        
        # Score de base
        self.validation_score = 50.0
        
        # Bonus pour chaque validation réussie
        if len(self.warnings) == 0:
            self.validation_score += 20
        
        if len(self.errors) == 0:
            self.validation_score += 30
        
        # Bonus pour ratios optimaux
        # (déjà ajouté dans _validate_geometric_ratios)
        
        # Limiter le score à 100
        self.validation_score = min(100.0, self.validation_score)
    
    def _get_quality_level(self):
        """Déterminer le niveau de qualité"""
        
        if self.validation_score >= 90:
            return "Excellent"
        elif self.validation_score >= 80:
            return "Très bon"
        elif self.validation_score >= 70:
            return "Bon"
        elif self.validation_score >= 60:
            return "Acceptable"
        else:
            return "À améliorer"
    
    def generate_validation_report(self, machine_dims, machine_type='IPMSM'):
        """Générer un rapport de validation complet"""
        
        validation_result = self.validate_machine_design(machine_dims, machine_type)
        
        report = f"""
=== RAPPORT DE VALIDATION BOLDEA ===
Machine: {machine_type}
Score: {validation_result['score']:.1f}/100
Niveau: {validation_result['quality_level']}
Statut: {' VALIDE' if validation_result['is_valid'] else ' INVALIDE'}

=== DIMENSIONS PRINCIPALES ===
"""
        
        for key, value in machine_dims.items():
            if isinstance(value, float):
                report += f"{key}: {value:.4f}\n"
            else:
                report += f"{key}: {value}\n"
        
        if validation_result['warnings']:
            report += "\n=== AVERTISSEMENTS ===\n"
            for warning in validation_result['warnings']:
                report += f"  {warning}\n"
        
        if validation_result['errors']:
            report += "\n=== ERREURS ===\n"
            for error in validation_result['errors']:
                report += f" {error}\n"
        
        report += f"\n=== RECOMMANDATIONS ===\n"
        if validation_result['score'] < 70:
            report += " Considérer une refonte des dimensions\n"
        elif validation_result['score'] < 85:
            report += " Ajuster certains ratios géométriques\n"
        else:
            report += " Design conforme aux critères Boldea\n"
        
        return report

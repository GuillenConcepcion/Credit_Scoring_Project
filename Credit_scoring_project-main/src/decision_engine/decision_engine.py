"""
==============================================================================
Credit Risk Intelligent Decision Engine (Motor de Decisiones Inteligente)
==============================================================================
Author: Guillén Concepción (Senior Data Scientist & MLOps Engineer)
Architecture: Production-grade Banking Policy Decisioning & Risk-Based Pricing Engine
Compliant with: Basel II/III IRB Framework, IFRS 9 ECL & Fair Lending Practices
==============================================================================
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple


class DecisionStatus(str, Enum):
    AUTO_APPROVE = "APROBACIÓN AUTOMÁTICA"
    STANDARD_APPROVE = "APROBADO ESTÁNDAR"
    MANUAL_REVIEW = "REVISIÓN MANUAL (COMITÉ DE RIESGOS)"
    CONDITIONAL_APPROVE = "APROBACIÓN CONDICIONADA (GARANTÍA / CO-DEUDOR)"
    HARD_DECLINE = "RECHAZO DIRECTO (POLÍTICA KNOCKOUT)"
    SCORE_DECLINE = "RECHAZADO POR SCORE / CAPACIDAD"


class RiskTier(str, Enum):
    TIER_A = "Tier A - Riesgo Mínimo (Prime)"
    TIER_B = "Tier B - Riesgo Bajo"
    TIER_C = "Tier C - Riesgo Medio (Near-Prime)"
    TIER_D = "Tier D - Riesgo Elevado (Subprime)"
    TIER_E = "Tier E - Riesgo Crítico"


@dataclass
class ApplicantProfile:
    """Perfil del solicitante para el motor de decisiones."""
    person_income: float
    person_age: float
    person_emp_length: float
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    person_home_ownership: str  # RENT, OWN, MORTGAGE, OTHER
    cb_person_default_on_file: str  # Y, N
    loan_intent: Optional[str] = "PERSONAL"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionResult:
    """Resultado estructurado de la decisión de crédito."""
    decision: DecisionStatus
    tier: RiskTier
    credit_score: int
    probability_of_default: float
    expected_loss: float
    approved_limit: float
    recommended_interest_rate: float
    interest_rate_spread_bps: int
    knockouts_triggered: List[str]
    positive_drivers: List[str]
    negative_drivers: List[str]
    policy_notes: str
    underwriting_checklist: List[str]


class IntelligentDecisionEngine:
    """
    Motor de Decisiones Inteligente para Evaluación de Crédito y Pricing de Riesgo.
    Combina:
      1. Reglas Duras de Política (Knockouts / Hard Cutoffs)
      2. Scoring Calibrado (FICO Scale 300 - 850)
      3. Matriz Multidimensional de Políticas (Score x DTI x Buró)
      4. Pricing Dinámico Basado en Riesgo (Risk-Based Pricing & Spreads)
      5. Cálculo de Pérdida Esperada (Expected Loss = PD * LGD * EAD)
      6. Dimensionamiento Inteligente de Líneas de Crédito
    """

    def __init__(
        self,
        base_score: int = 600,
        pdo: int = 20,
        base_odds: float = 50.0,
        lgd_unsecured: float = 0.55,
        target_cost_of_funds: float = 5.50
    ):
        self.base_score = base_score
        self.pdo = pdo
        self.base_odds = base_odds
        self.lgd_unsecured = lgd_unsecured
        self.target_cost_of_funds = target_cost_of_funds

        # Factor y Offset para la escala FICO
        self.factor = self.pdo / math.log(2.0)
        self.offset = self.base_score - self.factor * math.log(1.0 / self.base_odds)

    def evaluate_knockouts(self, profile: ApplicantProfile) -> List[str]:
        """
        Evalúa reglas de exclusión automática (Knockouts / Hard Filters).
        Cualquier infracción detiene el proceso y emite rechazo inmediato.
        """
        knockouts = []

        if profile.person_age < 18:
            knockouts.append("KO-01: Minoría de edad legal (< 18 años).")
        elif profile.person_age > 80:
            knockouts.append("KO-02: Edad excede límite de póliza de seguro de desgravamen (> 80 años).")

        if profile.person_income < 8000:
            knockouts.append("KO-03: Ingreso anual inferior al umbral mínimo de subsistencia ($8,000 USD).")

        if profile.loan_percent_income > 0.65:
            knockouts.append("KO-04: Ratio Préstamo/Ingreso crítico (> 65% de endeudamiento patrimonial).")

        return knockouts

    def calculate_score(self, pd: float) -> int:
        """
        Transforma una probabilidad de incumplimiento calibrada a Score FICO (300 a 850).
        Fórmula: Score = Offset - Factor * ln(Odds)
        """
        p = min(max(pd, 0.0001), 0.9999)
        odds = p / (1.0 - p)
        raw_score = self.offset - self.factor * math.log(odds)
        return int(round(min(max(raw_score, 300.0), 850.0)))

    def determine_tier(self, score: int) -> RiskTier:
        """Asigna el tramo de riesgo regulatorio según el score."""
        if score >= 750:
            return RiskTier.TIER_A
        elif score >= 670:
            return RiskTier.TIER_B
        elif score >= 600:
            return RiskTier.TIER_C
        elif score >= 530:
            return RiskTier.TIER_D
        else:
            return RiskTier.TIER_E

    def evaluate(
        self,
        profile: ApplicantProfile,
        pd_model_estimate: Optional[float] = None
    ) -> DecisionResult:
        """
        Ejecución integral de la evaluación de decisión inteligente.
        """
        # 1. Reglas de Exclusión Dura (Knockouts)
        knockouts = self.evaluate_knockouts(profile)
        if knockouts:
            pd = 0.85
            score = self.calculate_score(pd)
            tier = RiskTier.TIER_E
            el = profile.loan_amnt * pd * self.lgd_unsecured
            return DecisionResult(
                decision=DecisionStatus.HARD_DECLINE,
                tier=tier,
                credit_score=score,
                probability_of_default=pd,
                expected_loss=el,
                approved_limit=0.0,
                recommended_interest_rate=profile.loan_int_rate,
                interest_rate_spread_bps=0,
                knockouts_triggered=knockouts,
                positive_drivers=[],
                negative_drivers=knockouts,
                policy_notes="Solicitud denegada automáticamente por incumplimiento de políticas rectoras duras.",
                underwriting_checklist=["Cierre de expediente por regla Knockout."]
            )

        # 2. Estimación de Probabilidad de Default si no es provista
        if pd_model_estimate is not None:
            pd = pd_model_estimate
        else:
            # Aproximación heurística calibrada basada en coeficientes del modelo
            logit = -2.1
            logit += (profile.loan_percent_income - 0.17) * 4.5
            logit += (profile.loan_int_rate - 11.0) * 0.14
            logit += -0.000015 * (profile.person_income - 65000)
            if profile.cb_person_default_on_file.upper() == "Y":
                logit += 0.85
            if profile.person_home_ownership.upper() == "OWN":
                logit -= 0.65
            elif profile.person_home_ownership.upper() == "RENT":
                logit += 0.35
            pd = 1.0 / (1.0 + math.exp(-logit))

        score = self.calculate_score(pd)
        tier = self.determine_tier(score)

        # 3. Factor Drivers (Explicabilidad y Fair Lending)
        positives = []
        negatives = []

        if profile.loan_percent_income < 0.15:
            positives.append("Ratio DTI bajo (<15%): Excelente margen de capacidad de pago.")
        elif profile.loan_percent_income > 0.35:
            negatives.append("Ratio DTI elevado (>35%): Presión sobre el flujo financiero disponible.")

        if profile.cb_person_default_on_file.upper() == "N":
            positives.append("Historial impecable en buró crediticio sin morosidades previas.")
        else:
            negatives.append("Antecedente de incumplimiento registrado en buró (Default histórico).")

        if profile.person_home_ownership.upper() == "OWN":
            positives.append("Inmueble propio: Respaldo patrimonial y arraigo habitacional.")
        elif profile.person_home_ownership.upper() == "RENT":
            negatives.append("Régimen de alquiler: Mayor vulnerabilidad ante shocks de gasto corriente.")

        if profile.person_emp_length >= 5:
            positives.append(f"Alta estabilidad laboral ({int(profile.person_emp_length)} años de antigüedad).")
        elif profile.person_emp_length <= 1:
            negatives.append("Antigüedad laboral reciente (<= 1 año en el empleo actual).")

        # 4. Matriz de Decisión y Política
        dti = profile.loan_percent_income
        has_bureau_default = profile.cb_person_default_on_file.upper() == "Y"

        if tier == RiskTier.TIER_A:
            decision = DecisionStatus.AUTO_APPROVE
            limit_factor = 1.25
            spread_bps = 150  # +1.50%
            notes = "Cliente Prime. Aprobación inmediata STP (Straight-Through Processing). Límite con ampliación preventiva."
            checklist = ["Validación digital de identidad (KYC/AML)", "Firma electrónica del contrato"]

        elif tier == RiskTier.TIER_B:
            if dti <= 0.28:
                decision = DecisionStatus.STANDARD_APPROVE
                limit_factor = 1.00
                spread_bps = 250  # +2.50%
                notes = "Perfil sólido de bajo riesgo. Aprobación estándar bajo condiciones de mercado."
                checklist = ["Comprobante de ingresos de los últimos 3 meses", "Validación biométrica"]
            else:
                decision = DecisionStatus.MANUAL_REVIEW
                limit_factor = 0.90
                spread_bps = 300
                notes = "Score favorable pero ratio DTI moderadamente alto. Derivado a verificación de estabilidad."
                checklist = ["Revisión de estados de cuenta bancarios", "Análisis de endeudamiento consolidado"]

        elif tier == RiskTier.TIER_C:
            if not has_bureau_default and dti <= 0.32:
                decision = DecisionStatus.MANUAL_REVIEW
                limit_factor = 0.80
                spread_bps = 450
                notes = "Riesgo moderado. Requiere confirmación de capacidad de servicio de deuda y teléfono de empleador."
                checklist = ["Llamada de confirmación laboral", "Recibos de nómina timbrados", "Inspección de buró detallada"]
            else:
                decision = DecisionStatus.CONDITIONAL_APPROVE
                limit_factor = 0.65
                spread_bps = 550
                notes = "Aprobación sujeta a colateral prendario, reducción de monto o co-titular solvente."
                checklist = ["Incorporación de aval solvente", "Pagaré notarial o garantía líquida"]

        elif tier == RiskTier.TIER_D:
            if not has_bureau_default and profile.person_home_ownership.upper() in ["OWN", "MORTGAGE"]:
                decision = DecisionStatus.CONDITIONAL_APPROVE
                limit_factor = 0.50
                spread_bps = 750
                notes = "Alto riesgo mitigado parcialmente por arraigo habitacional. Requiere reducción drástica del monto."
                checklist = ["Garantía hipotecaria / prendaria", "Aval con score Tier A/B", "Monto recortado al 50%"]
            else:
                decision = DecisionStatus.SCORE_DECLINE
                limit_factor = 0.0
                spread_bps = 0
                notes = "Solicitud rechazada por exceso de riesgo de crédito y solvencia comprometida."
                checklist = ["Emisión de carta de declinación conforme a normativa Fair Lending."]

        else:  # TIER_E
            decision = DecisionStatus.SCORE_DECLINE
            limit_factor = 0.0
            spread_bps = 0
            notes = "Riesgo crítico. Probabilidad de incumplimiento inaceptable para la política institucional."
            checklist = ["Archivo en lista de exclusión temporal (cooldown 6 meses)."]

        # 5. Pricing y Límites
        recommended_rate = round(self.target_cost_of_funds + (spread_bps / 100.0), 2)
        approved_limit = round(profile.loan_amnt * limit_factor, 2)
        expected_loss = round(approved_limit * pd * self.lgd_unsecured, 2)

        return DecisionResult(
            decision=decision,
            tier=tier,
            credit_score=score,
            probability_of_default=round(pd, 4),
            expected_loss=expected_loss,
            approved_limit=approved_limit,
            recommended_interest_rate=recommended_rate,
            interest_rate_spread_bps=spread_bps,
            knockouts_triggered=[],
            positive_drivers=positives,
            negative_drivers=negatives,
            policy_notes=notes,
            underwriting_checklist=checklist
        )

from enum import Enum


class RiskTolerances(str, Enum):
    """Represents the risk tolerances available to be used in strategies."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

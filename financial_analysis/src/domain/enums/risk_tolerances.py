from enum import Enum


class RiskTolerances(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

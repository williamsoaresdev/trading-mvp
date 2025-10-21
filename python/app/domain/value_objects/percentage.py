"""
Percentage Value Object.
"""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Percentage:
    """
    Value object representing percentage values.
    
    Stores as decimal (0.0 to 1.0) but can display as percentage.
    """
    
    value: Decimal
    
    def __post_init__(self):
        """Validate percentage value."""
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, 'value', Decimal(str(self.value)))
        
        if self.value < 0:
            raise ValueError("Percentage cannot be negative")
        
        if self.value > 1:
            raise ValueError("Percentage cannot exceed 100% (1.0)")
    
    def __str__(self) -> str:
        """String representation as percentage."""
        return f"{(self.value * 100):.2f}%"
    
    def __add__(self, other: 'Percentage') -> 'Percentage':
        """Add two percentages."""
        result = self.value + other.value
        if result > 1:
            raise ValueError("Sum of percentages cannot exceed 100%")
        return Percentage(result)
    
    def __sub__(self, other: 'Percentage') -> 'Percentage':
        """Subtract two percentages."""
        result = self.value - other.value
        if result < 0:
            raise ValueError("Subtraction would result in negative percentage")
        return Percentage(result)
    
    def __mul__(self, factor: float) -> 'Percentage':
        """Multiply percentage by a factor."""
        if factor < 0:
            raise ValueError("Cannot multiply percentage by negative factor")
        result = self.value * Decimal(str(factor))
        if result > 1:
            raise ValueError("Result cannot exceed 100%")
        return Percentage(result)
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, Percentage):
            return False
        return self.value == other.value
    
    def __lt__(self, other: 'Percentage') -> bool:
        """Less than comparison."""
        return self.value < other.value
    
    def __le__(self, other: 'Percentage') -> bool:
        """Less than or equal comparison."""
        return self.value <= other.value
    
    def __gt__(self, other: 'Percentage') -> bool:
        """Greater than comparison."""
        return self.value > other.value
    
    def __ge__(self, other: 'Percentage') -> bool:
        """Greater than or equal comparison."""
        return self.value >= other.value
    
    @classmethod
    def from_percent(cls, percent: float) -> 'Percentage':
        """Create from percentage value (0-100)."""
        if percent < 0 or percent > 100:
            raise ValueError("Percent must be between 0 and 100")
        return cls(Decimal(str(percent / 100)))
    
    @classmethod
    def from_decimal(cls, decimal_value: float) -> 'Percentage':
        """Create from decimal value (0.0-1.0)."""
        return cls(Decimal(str(decimal_value)))
    
    @classmethod
    def zero(cls) -> 'Percentage':
        """Create zero percentage."""
        return cls(Decimal('0'))
    
    @classmethod
    def one_hundred(cls) -> 'Percentage':
        """Create 100% percentage."""
        return cls(Decimal('1'))
    
    @property
    def as_percent(self) -> float:
        """Get as percentage (0-100)."""
        return float(self.value * 100)
    
    @property
    def as_decimal(self) -> float:
        """Get as decimal (0.0-1.0)."""
        return float(self.value)
    
    @property
    def is_zero(self) -> bool:
        """Check if percentage is zero."""
        return self.value == 0
    
    @property
    def is_full(self) -> bool:
        """Check if percentage is 100%."""
        return self.value == 1
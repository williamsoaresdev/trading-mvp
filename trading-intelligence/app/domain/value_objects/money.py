"""
Money Value Object.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class Money:
    """
    Value object representing money amounts.
    
    Uses Decimal for precise financial calculations.
    """
    
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        """Validate money amount."""
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))
        
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a 3-character code")
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.amount:.2f} {self.currency}"
    
    def __add__(self, other: 'Money') -> 'Money':
        """Add two money amounts."""
        self._check_same_currency(other)
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other: 'Money') -> 'Money':
        """Subtract two money amounts."""
        self._check_same_currency(other)
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Subtraction would result in negative amount")
        return Money(result, self.currency)
    
    def __mul__(self, factor: float) -> 'Money':
        """Multiply money by a factor."""
        if factor < 0:
            raise ValueError("Cannot multiply money by negative factor")
        return Money(self.amount * Decimal(str(factor)), self.currency)
    
    def __truediv__(self, divisor: float) -> 'Money':
        """Divide money by a divisor."""
        if divisor <= 0:
            raise ValueError("Cannot divide money by zero or negative number")
        return Money(self.amount / Decimal(str(divisor)), self.currency)
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency
    
    def __lt__(self, other: 'Money') -> bool:
        """Less than comparison."""
        self._check_same_currency(other)
        return self.amount < other.amount
    
    def __le__(self, other: 'Money') -> bool:
        """Less than or equal comparison."""
        self._check_same_currency(other)
        return self.amount <= other.amount
    
    def __gt__(self, other: 'Money') -> bool:
        """Greater than comparison."""
        self._check_same_currency(other)
        return self.amount > other.amount
    
    def __ge__(self, other: 'Money') -> bool:
        """Greater than or equal comparison."""
        self._check_same_currency(other)
        return self.amount >= other.amount
    
    def _check_same_currency(self, other: 'Money') -> None:
        """Check if two money objects have the same currency."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot operate on different currencies: {self.currency} vs {other.currency}")
    
    def round(self, places: int = 2) -> 'Money':
        """Round to specified decimal places."""
        rounded_amount = self.amount.quantize(
            Decimal('0.' + '0' * places),
            rounding=ROUND_HALF_UP
        )
        return Money(rounded_amount, self.currency)
    
    @classmethod
    def zero(cls, currency: str = "USD") -> 'Money':
        """Create zero money amount."""
        return cls(Decimal('0'), currency)
    
    @classmethod
    def from_float(cls, amount: float, currency: str = "USD") -> 'Money':
        """Create from float amount."""
        return cls(Decimal(str(amount)), currency)
    
    @property
    def is_zero(self) -> bool:
        """Check if amount is zero."""
        return self.amount == 0
    
    @property
    def float_amount(self) -> float:
        """Get amount as float (for compatibility)."""
        return float(self.amount)
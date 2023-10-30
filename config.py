from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    advance_notice: int  # Assuming RelayBlockNumber is an integer type
    interlude_length: int  # Assuming BlockNumber is an integer type
    leadin_length: int  # Assuming BlockNumber is an integer type
    region_length: int  # Assuming Timeslice is an integer type
    ideal_bulk_proportion: float  # Assuming Perbill is a floating-point type
    limit_cores_offered: Optional[int]  # Assuming CoreIndex is an integer type
    renewal_bump: float  # Assuming Perbill is a floating-point type
    contribution_timeout: int  # Assuming Timeslice is an integer type

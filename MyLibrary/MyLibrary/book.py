from dataclasses import dataclass, field
from MyLibrary.random_number_utils import RandomNumberUtils

@dataclass(frozen=True, order=True, slots=True) 
class Book:
  
    name: str 
    category: str
    id: str = field(default_factory=RandomNumberUtils.generate_random_id)

    
    @property
    def search_string(self):
        return f"{self.name} {self.category}"

from dataclasses import dataclass, field

@dataclass
class demo_dao:
    id: str
    first_name: str
    last_name: str
    email: str
    company_size: str
    industry: str
    product_link: str
    created_at: int
    
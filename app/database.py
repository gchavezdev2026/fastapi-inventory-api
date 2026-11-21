from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.schemas import ProductCreate, ProductUpdate, ProductResponse


class InventoryDatabase:
    def __init__(self):
        self._products: Dict[int, dict] = {}
        self._counter: int = 0
        self._seed_data()

    def _seed_data(self):
        initial_products = [
            {
                "name": "Laptop Pro 15",
                "description": "Laptop de alto rendimiento para desarrolladores",
                "price": 1299.99,
                "stock": 15,
                "category": "Electrónica"
            },
            {
                "name": "Ratón Inalámbrico Ergonomico",
                "description": "Ratón óptico bluetooth con diseño ergonómico",
                "price": 35.50,
                "stock": 50,
                "category": "Accesorios"
            },
            {
                "name": "Teclado Mecánico RGB",
                "description": "Teclado mecánico con switches brown y retroiluminación RGB",
                "price": 89.90,
                "stock": 30,
                "category": "Accesorios"
            },
            {
                "name": "Monitor 4K 27 pulgadas",
                "description": "Monitor IPS 4K con tasa de refresco de 144Hz",
                "price": 450.00,
                "stock": 10,
                "category": "Electrónica"
            }
        ]
        for p in initial_products:
            self.create(ProductCreate(**p))

    def reset(self):
        self._products.clear()
        self._counter = 0

    def get_all(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        results = list(self._products.values())

        if category:
            results = [p for p in results if p["category"].lower() == category.lower()]
        if min_price is not None:
            results = [p for p in results if p["price"] >= min_price]
        if max_price is not None:
            results = [p for p in results if p["price"] <= max_price]
        if search:
            query = search.lower()
            results = [
                p for p in results
                if query in p["name"].lower() or (p["description"] and query in p["description"].lower())
            ]

        return results[skip : skip + limit]

    def get_by_id(self, product_id: int) -> Optional[dict]:
        return self._products.get(product_id)

    def create(self, product_in: ProductCreate) -> dict:
        self._counter += 1
        now = datetime.now(timezone.utc)
        product_dict = product_in.model_dump()
        product_dict.update({
            "id": self._counter,
            "created_at": now,
            "updated_at": now
        })
        self._products[self._counter] = product_dict
        return product_dict

    def update(self, product_id: int, product_in: ProductUpdate, partial: bool = False) -> Optional[dict]:
        if product_id not in self._products:
            return None
        
        current = self._products[product_id]
        update_data = product_in.model_dump(exclude_unset=partial if partial else False)
        
        updated_dict = current.copy()
        for field, value in update_data.items():
            if value is not None or not partial:
                updated_dict[field] = value
        
        updated_dict["updated_at"] = datetime.now(timezone.utc)
        self._products[product_id] = updated_dict
        return updated_dict

    def delete(self, product_id: int) -> bool:
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False


db = InventoryDatabase()

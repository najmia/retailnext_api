from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(title="RetailNext Inventory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Variant(BaseModel):
    color: str
    size: str
    stock: int

class StoreAvailability(BaseModel):
    storeId: str
    name: str
    location: str
    inStock: bool
    stockCount: int

class InventoryResponse(BaseModel):
    sku: str
    totalStock: int
    lastUpdated: str
    variants: List[Variant]
    storeAvailability: List[StoreAvailability]

# Mock data
MOCK_INVENTORY = {
    "DRESS-001": InventoryResponse(
        sku="DRESS-001",
        totalStock=45,
        lastUpdated="2024-01-15T10:30:00Z",
        variants=[
            Variant(color="Black", size="S", stock=8),
            Variant(color="Black", size="M", stock=12),
            Variant(color="Red", size="S", stock=5),
            Variant(color="Red", size="L", stock=20)
        ],
        storeAvailability=[
            StoreAvailability(storeId="NYC-001", name="Manhattan Store", location="New York", inStock=True, stockCount=25),
            StoreAvailability(storeId="LA-001", name="Beverly Hills Store", location="Los Angeles", inStock=True, stockCount=20)
        ]
    ),
    "JEANS-002": InventoryResponse(
        sku="JEANS-002",
        totalStock=30,
        lastUpdated="2024-01-15T09:15:00Z",
        variants=[
            Variant(color="Blue", size="28", stock=10),
            Variant(color="Blue", size="30", stock=15),
            Variant(color="Black", size="32", stock=5)
        ],
        storeAvailability=[
            StoreAvailability(storeId="NYC-001", name="Manhattan Store", location="New York", inStock=True, stockCount=18),
            StoreAvailability(storeId="LA-001", name="Beverly Hills Store", location="Los Angeles", inStock=True, stockCount=12)
        ]
    )
}

@app.get("/inventory/{sku}", response_model=InventoryResponse)
async def get_inventory(sku: str, storeId: Optional[str] = Query(None)):
    if sku not in MOCK_INVENTORY:
        return {"error": "SKU not found"}
    
    inventory = MOCK_INVENTORY[sku]
    
    if storeId:
        filtered_stores = [store for store in inventory.storeAvailability if store.storeId == storeId]
        inventory.storeAvailability = filtered_stores
    
    return inventory
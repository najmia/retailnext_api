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
    "OKT001": InventoryResponse(
        sku="OKT001",
        totalStock=24,
        lastUpdated="2024-01-15T10:30:00Z",
        variants=[
            Variant(color="Green", size="46", stock=8),
            Variant(color="Green", size="52", stock=16)
        ],
        storeAvailability=[
            StoreAvailability(storeId="MUN-001", name="Munich Store", location="Munich", inStock=True, stockCount=24)
        ]
    ),
    "OKT002": InventoryResponse(
        sku="OKT002",
        totalStock=31,
        lastUpdated="2024-01-15T09:15:00Z",
        variants=[
            Variant(color="Burgundy", size="32", stock=10),
            Variant(color="Burgundy", size="38", stock=21)
        ],
        storeAvailability=[
            StoreAvailability(storeId="MUN-001", name="Munich Store", location="Munich", inStock=True, stockCount=31)
        ]
    ),
    "OKT003": InventoryResponse(
        sku="OKT003",
        totalStock=21,
        lastUpdated="2024-01-15T08:45:00Z",
        variants=[
            Variant(color="Multicolor", size="One Size", stock=21)
        ],
        storeAvailability=[
            StoreAvailability(storeId="VIE-001", name="Vienna Store", location="Vienna", inStock=True, stockCount=21)
        ]
    ),
    "OKT015": InventoryResponse(
        sku="OKT015",
        totalStock=134,
        lastUpdated="2024-01-15T11:20:00Z",
        variants=[
            Variant(color="Burgundy", size="One Size", stock=134)
        ],
        storeAvailability=[
            StoreAvailability(storeId="MUN-001", name="Munich Store", location="Munich", inStock=True, stockCount=134)
        ]
    ),
    "OKT024": InventoryResponse(
        sku="OKT024",
        totalStock=12,
        lastUpdated="2024-01-15T12:10:00Z",
        variants=[
            Variant(color="Brown", size="One Size", stock=12)
        ],
        storeAvailability=[
            StoreAvailability(storeId="INN-001", name="Innsbruck Store", location="Innsbruck", inStock=True, stockCount=12)
        ]
    )
}

@app.get("/")
async def root():
    return {"message": "RetailNext Inventory API is running"}

@app.get("/inventory/{sku}", response_model=InventoryResponse)
async def get_inventory(sku: str, storeId: Optional[str] = Query(None)):
    if sku not in MOCK_INVENTORY:
        return {"error": "SKU not found"}
    
    inventory = MOCK_INVENTORY[sku]
    
    if storeId:
        filtered_stores = [store for store in inventory.storeAvailability if store.storeId == storeId]
        inventory.storeAvailability = filtered_stores
    
    return inventory
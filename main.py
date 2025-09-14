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
    ),
    "D-2025-EM-301": InventoryResponse(
        sku="D-2025-EM-301",
        totalStock=45,
        lastUpdated="2024-01-15T13:00:00Z",
        variants=[
            Variant(color="Emerald", size="32", stock=15),
            Variant(color="Emerald", size="36", stock=18),
            Variant(color="Emerald", size="40", stock=12)
        ],
        storeAvailability=[
            StoreAvailability(storeId="MUN-001", name="Munich Store", location="Munich", inStock=True, stockCount=45)
        ]
    ),
    "D-2025-BL-302": InventoryResponse(
        sku="D-2025-BL-302",
        totalStock=38,
        lastUpdated="2024-01-15T13:15:00Z",
        variants=[
            Variant(color="Blush", size="34", stock=12),
            Variant(color="Blush", size="38", stock=16),
            Variant(color="Blush", size="42", stock=10)
        ],
        storeAvailability=[
            StoreAvailability(storeId="VIE-001", name="Vienna Store", location="Vienna", inStock=True, stockCount=38)
        ]
    ),
    "D-2025-SB-303": InventoryResponse(
        sku="D-2025-SB-303",
        totalStock=52,
        lastUpdated="2024-01-15T13:30:00Z",
        variants=[
            Variant(color="Sapphire Blue", size="32", stock=18),
            Variant(color="Sapphire Blue", size="36", stock=20),
            Variant(color="Sapphire Blue", size="40", stock=14)
        ],
        storeAvailability=[
            StoreAvailability(storeId="MUN-001", name="Munich Store", location="Munich", inStock=True, stockCount=52)
        ]
    ),
    "D-2025-BG-304": InventoryResponse(
        sku="D-2025-BG-304",
        totalStock=29,
        lastUpdated="2024-01-15T13:45:00Z",
        variants=[
            Variant(color="Burgundy", size="34", stock=10),
            Variant(color="Burgundy", size="38", stock=12),
            Variant(color="Burgundy", size="42", stock=7)
        ],
        storeAvailability=[
            StoreAvailability(storeId="INN-001", name="Innsbruck Store", location="Innsbruck", inStock=True, stockCount=29)
        ]
    ),
    "D-2025-SG-305": InventoryResponse(
        sku="D-2025-SG-305",
        totalStock=41,
        lastUpdated="2024-01-15T14:00:00Z",
        variants=[
            Variant(color="Sage Green", size="32", stock=14),
            Variant(color="Sage Green", size="36", stock=15),
            Variant(color="Sage Green", size="40", stock=12)
        ],
        storeAvailability=[
            StoreAvailability(storeId="VIE-001", name="Vienna Store", location="Vienna", inStock=True, stockCount=41)
        ]
    ),
    "D-2019-GO-849": InventoryResponse(
        sku="D-2019-GO-849",
        totalStock=41,
        lastUpdated="2024-01-15T14:15:00Z",
        variants=[
            Variant(color="Gold", size="32", stock=12),
            Variant(color="Gold", size="36", stock=16),
            Variant(color="Gold", size="42", stock=13)
        ],
        storeAvailability=[
            StoreAvailability(storeId="VIE-001", name="Vienna Store", location="Vienna", inStock=True, stockCount=41)
        ]
    ),
    "D-2024-BU-532": InventoryResponse(
        sku="D-2024-BU-532",
        totalStock=31,
        lastUpdated="2024-01-15T14:30:00Z",
        variants=[
            Variant(color="Burgundy", size="32", stock=10),
            Variant(color="Burgundy", size="36", stock=12),
            Variant(color="Burgundy", size="42", stock=9)
        ],
        storeAvailability=[
            StoreAvailability(storeId="MUN-001", name="Munich Store", location="Munich", inStock=True, stockCount=31)
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

@app.get("/stock/{sku}")
async def get_stock_all_stores(sku: str):
    if sku not in MOCK_INVENTORY:
        return {"error": "SKU not found"}
    
    inventory = MOCK_INVENTORY[sku]
    return {
        "sku": sku,
        "totalStock": inventory.totalStock,
        "stores": [{
            "storeId": store.storeId,
            "storeName": store.name,
            "location": store.location,
            "stock": store.stockCount
        } for store in inventory.storeAvailability]
    }
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

class StoreVariant(BaseModel):
    color: str
    size: str
    stock: int

class StoreInventory(BaseModel):
    storeId: str
    name: str
    location: str
    variants: List[StoreVariant]
    totalStock: int

class InventoryResponse(BaseModel):
    sku: str
    totalStock: int
    lastUpdated: str
    stores: List[StoreInventory]

# Mock data
MOCK_INVENTORY = {
    "D-2025-EM-301": InventoryResponse(
        sku="D-2025-EM-301",
        totalStock=67,
        lastUpdated="2024-09-14T22:00:00Z",
        stores=[
            StoreInventory(
                storeId="MUN-001",
                name="Munich Store",
                location="Munich",
                totalStock=35,
                variants=[
                    StoreVariant(color="Emerald", size="32", stock=8),
                    StoreVariant(color="Emerald", size="36", stock=15),
                    StoreVariant(color="Emerald", size="40", stock=12)
                ]
            ),
            StoreInventory(
                storeId="VIE-001",
                name="Vienna Store",
                location="Vienna",
                totalStock=32,
                variants=[
                    StoreVariant(color="Emerald", size="32", stock=7),
                    StoreVariant(color="Emerald", size="36", stock=18),
                    StoreVariant(color="Emerald", size="40", stock=7)
                ]
            )
        ]
    ),
    "ACC-2023-GO-667": InventoryResponse(
        sku="ACC-2023-GO-667",
        totalStock=71,
        lastUpdated="2024-09-14T22:00:00Z",
        stores=[
            StoreInventory(
                storeId="VIE-001",
                name="Vienna Store",
                location="Vienna",
                totalStock=68,
                variants=[
                    StoreVariant(color="Gold", size="One Size", stock=68)
                ]
            ),
            StoreInventory(
                storeId="MUN-001",
                name="Munich Store",
                location="Munich",
                totalStock=3,
                variants=[
                    StoreVariant(color="Gold", size="One Size", stock=3)
                ]
            )
        ]
    ),
    "D-2024-BU-532": InventoryResponse(
        sku="D-2024-BU-532",
        totalStock=43,
        lastUpdated="2024-09-14T22:00:00Z",
        stores=[
            StoreInventory(
                storeId="MUN-001",
                name="Munich Store",
                location="Munich",
                totalStock=21,
                variants=[
                    StoreVariant(color="Burgundy", size="36", stock=0),
                    StoreVariant(color="Burgundy", size="42", stock=9)
                ]
            ),
            StoreInventory(
                storeId="VIE-001",
                name="Vienna Store",
                location="Vienna",
                totalStock=22,
                variants=[
                    StoreVariant(color="Burgundy", size="32", stock=10),
                    StoreVariant(color="Burgundy", size="36", stock=8),
                    StoreVariant(color="Burgundy", size="42", stock=4)
                ]
            )
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
        filtered_stores = [store for store in inventory.stores if store.storeId == storeId]
        inventory.stores = filtered_stores
        inventory.totalStock = sum(store.totalStock for store in filtered_stores)
    
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
            "stock": store.totalStock,
            "variants": [{
                "color": variant.color,
                "size": variant.size,
                "stock": variant.stock
            } for variant in store.variants]
        } for store in inventory.stores]
    }
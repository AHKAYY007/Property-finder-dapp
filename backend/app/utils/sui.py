from typing import Optional
import aiohttp
from app.core.config import settings

async def verify_signature(message: str, signature: str) -> bool:
    """Verify a Sui signature"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.SUI_RPC_URL}",
            json={
                "jsonrpc": "2.0",
                "method": "sui_verifySignature",
                "params": [message, signature],
                "id": 1
            }
        ) as response:
            result = await response.json()
            return result.get("result", {}).get("is_valid", False)

async def get_object(object_id: str) -> Optional[dict]:
    """Get a Sui object by ID"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.SUI_RPC_URL}",
            json={
                "jsonrpc": "2.0",
                "method": "sui_getObject",
                "params": [object_id],
                "id": 1
            }
        ) as response:
            result = await response.json()
            return result.get("result", {}).get("data")

async def get_owned_objects(address: str, object_type: Optional[str] = None) -> list:
    """Get objects owned by an address"""
    params = [address]
    if object_type:
        params.append({"StructType": object_type})
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.SUI_RPC_URL}",
            json={
                "jsonrpc": "2.0",
                "method": "sui_getOwnedObjects",
                "params": params,
                "id": 1
            }
        ) as response:
            result = await response.json()
            return result.get("result", {}).get("data", []) 
"""
WebSocket endpoint for streaming notifications to the frontend.
Handles verification code notifications and heartbeat keep-alive.
"""

import asyncio

import structlog
from fastapi import WebSocket

from skyvern.forge.sdk.routes.routers import base_router, legacy_base_router
from skyvern.forge.sdk.routes.streaming.auth import auth

LOG = structlog.get_logger()

HEARTBEAT_INTERVAL = 30


async def _notification_stream(
    websocket: WebSocket,
    apikey: str | None = None,
    token: str | None = None,
) -> None:
    """Stream notifications to the authenticated frontend client."""
    organization_id = await auth(apikey=apikey, token=token, websocket=websocket)

    if not organization_id:
        LOG.warning("WebSocket notification stream: authentication failed.")
        return

    LOG.info(
        "WebSocket notification stream connected.",
        organization_id=organization_id,
    )

    try:
        while True:
            await websocket.send_json({"type": "heartbeat"})
            await asyncio.sleep(HEARTBEAT_INTERVAL)
    except Exception:
        LOG.info(
            "WebSocket notification stream disconnected.",
            organization_id=organization_id,
        )


@base_router.websocket("/stream/notifications")
async def notification_stream_v1(
    websocket: WebSocket,
    apikey: str | None = None,
    token: str | None = None,
) -> None:
    return await _notification_stream(websocket, apikey=apikey, token=token)


@legacy_base_router.websocket("/stream/notifications")
async def notification_stream_legacy(
    websocket: WebSocket,
    apikey: str | None = None,
    token: str | None = None,
) -> None:
    return await _notification_stream(websocket, apikey=apikey, token=token)

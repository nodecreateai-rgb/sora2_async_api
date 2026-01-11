"""Proxy management module"""
from typing import Optional
from ..core.database import Database
from ..core.models import ProxyConfig

class ProxyManager:
    """Proxy configuration manager"""

    def __init__(self, db: Database):
        self.db = db

    async def get_proxy_url(self, token_id: Optional[int] = None, proxy_url: Optional[str] = None) -> Optional[str]:
        """Get proxy URL for a token, with fallback to global proxy

        Args:
            token_id: Token ID (optional). If provided, returns token-specific proxy if set,
                     otherwise falls back to global proxy.
            proxy_url: Direct proxy URL (optional). If provided, returns this proxy URL directly.

        Returns:
            Proxy URL string or None
        """
        # If proxy_url is directly provided, use it
        if proxy_url:
            return proxy_url

        # If token_id is provided, try to get token-specific proxy first
        if token_id is not None:
            token = await self.db.get_token(token_id)
            if token and token.proxy_url:
                return token.proxy_url

        # Fall back to global proxy
        config = await self.db.get_proxy_config()
        if config.proxy_enabled and config.proxy_url:
            return config.proxy_url
        return None

    async def update_proxy_config(self, enabled: bool, proxy_url: Optional[str]):
        """Update proxy configuration"""
        await self.db.update_proxy_config(enabled, proxy_url)

    async def get_proxy_config(self) -> ProxyConfig:
        """Get proxy configuration"""
        return await self.db.get_proxy_config()

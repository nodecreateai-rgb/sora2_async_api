"""Token lock manager for image generation"""
import asyncio
import time
from typing import Dict, Optional
from ..core.logger import debug_logger


class TokenLock:
    """Token lock manager for image generation (single-threaded per token)"""
    
    def __init__(self, lock_timeout: int = 300):
        """
        Initialize token lock manager
        
        Args:
            lock_timeout: Lock timeout in seconds (default: 300s = 5 minutes)
        """
        self.lock_timeout = lock_timeout
        self._locks: Dict[int, float] = {}  # token_id -> lock_timestamp
        self._lock = asyncio.Lock()  # Protect _locks dict
    
    async def acquire_lock(self, token_id: int) -> bool:
        """
        Try to acquire lock for image generation
        
        Args:
            token_id: Token ID
            
        Returns:
            True if lock acquired, False if already locked
        """
        async with self._lock:
            current_time = time.time()
            
            # Check if token is locked
            if token_id in self._locks:
                lock_time = self._locks[token_id]
                
                # Check if lock expired
                if current_time - lock_time > self.lock_timeout:
                    # Lock expired, remove it
                    debug_logger.log_info(f"Token {token_id} lock expired, releasing")
                    del self._locks[token_id]
                else:
                    # Lock still valid
                    remaining = self.lock_timeout - (current_time - lock_time)
                    debug_logger.log_info(f"Token {token_id} is locked, remaining: {remaining:.1f}s")
                    return False
            
            # Acquire lock
            self._locks[token_id] = current_time
            debug_logger.log_info(f"Token {token_id} lock acquired")
            return True
    
    async def release_lock(self, token_id: int):
        """
        Release lock for token
        
        Args:
            token_id: Token ID
        """
        async with self._lock:
            if token_id in self._locks:
                del self._locks[token_id]
                debug_logger.log_info(f"Token {token_id} lock released")
    
    async def is_locked(self, token_id: int) -> bool:
        """
        Check if token is locked
        
        Args:
            token_id: Token ID
            
        Returns:
            True if locked, False otherwise
        """
        async with self._lock:
            if token_id not in self._locks:
                return False
            
            current_time = time.time()
            lock_time = self._locks[token_id]
            
            # Check if expired
            if current_time - lock_time > self.lock_timeout:
                # Expired, remove lock
                del self._locks[token_id]
                return False
            
            return True
    
    async def cleanup_expired_locks(self):
        """Clean up expired locks"""
        async with self._lock:
            current_time = time.time()
            expired_tokens = []
            
            for token_id, lock_time in self._locks.items():
                if current_time - lock_time > self.lock_timeout:
                    expired_tokens.append(token_id)
            
            for token_id in expired_tokens:
                del self._locks[token_id]
                debug_logger.log_info(f"Cleaned up expired lock for token {token_id}")
            
            if expired_tokens:
                debug_logger.log_info(f"Cleaned up {len(expired_tokens)} expired locks")
    
    def get_locked_tokens(self) -> list:
        """Get list of currently locked token IDs"""
        return list(self._locks.keys())

    def set_lock_timeout(self, timeout: int):
        """Set lock timeout in seconds"""
        self.lock_timeout = timeout
        debug_logger.log_info(f"Lock timeout updated to {timeout} seconds")


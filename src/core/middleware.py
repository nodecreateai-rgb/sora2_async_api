"""Middleware for request/response logging"""
import time
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response as StarletteResponse
from .logger import debug_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all API requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log it"""
        start_time = time.time()
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Read request body
        body = None
        body_bytes = b""
        try:
            # Check if request has body
            if request.method in ["POST", "PUT", "PATCH"]:
                body_bytes = await request.body()
                if body_bytes:
                    try:
                        body = json.loads(body_bytes.decode('utf-8'))
                    except json.JSONDecodeError:
                        body = body_bytes.decode('utf-8', errors='ignore')
                    
                    # Recreate request with body for downstream handlers
                    async def receive():
                        return {"type": "http.request", "body": body_bytes}
                    request._receive = receive
        except Exception as e:
            debug_logger.logger.error(f"Error reading request body: {e}")
        
        # Log request
        debug_logger.log_api_request(
            method=request.method,
            path=request.url.path,
            headers=dict(request.headers),
            body=body,
            client_ip=client_ip
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Handle streaming responses
            if isinstance(response, StreamingResponse):
                # For streaming responses, we can't read the body easily
                # Just log the headers and status
                debug_logger.log_api_response(
                    status_code=response.status_code,
                    path=request.url.path,
                    headers=dict(response.headers),
                    body="<Streaming Response>",
                    duration_ms=duration_ms
                )
                return response
            
            # Read response body for non-streaming responses
            response_body = None
            try:
                # Try to get response body from different response types
                response_body_bytes = None
                
                # Check if it's a JSONResponse (FastAPI)
                if hasattr(response, 'body') and response.body:
                    response_body_bytes = response.body
                elif hasattr(response, 'render'):
                    # Try to render the response
                    try:
                        rendered = await response.render()
                        if isinstance(rendered, bytes):
                            response_body_bytes = rendered
                    except:
                        pass
                
                # If we still don't have body, try reading from iterator
                if response_body_bytes is None and hasattr(response, 'body_iterator'):
                    response_body_bytes = b""
                    async for chunk in response.body_iterator:
                        response_body_bytes += chunk
                    
                    # Recreate response with the body we read
                    response = StarletteResponse(
                        content=response_body_bytes,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=getattr(response, 'media_type', None)
                    )
                
                # Parse response body
                if response_body_bytes:
                    try:
                        if isinstance(response_body_bytes, bytes):
                            response_body = json.loads(response_body_bytes.decode('utf-8'))
                        else:
                            response_body = json.loads(str(response_body_bytes))
                    except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
                        if isinstance(response_body_bytes, bytes):
                            response_body = response_body_bytes.decode('utf-8', errors='ignore')
                        else:
                            response_body = str(response_body_bytes)
                        # Limit length
                        if len(response_body) > 5000:
                            response_body = response_body[:5000] + "... (truncated)"
            except Exception as e:
                debug_logger.logger.error(f"Error reading response body: {e}")
                response_body = "<Unable to read response body>"
            
            # Log response (including error responses)
            debug_logger.log_api_response(
                status_code=response.status_code,
                path=request.url.path,
                headers=dict(response.headers),
                body=response_body,
                duration_ms=duration_ms
            )
            
            # If it's an error response, also log as error
            if response.status_code >= 400:
                error_msg = f"HTTP {response.status_code} Error"
                if response_body:
                    if isinstance(response_body, dict):
                        error_msg = response_body.get("error", {}).get("message", str(response_body))
                    else:
                        error_msg = str(response_body)
                debug_logger.log_api_error(
                    path=request.url.path,
                    error_message=error_msg,
                    status_code=response.status_code,
                    client_ip=client_ip
                )
            
            return response
            
        except Exception as e:
            # Log error
            duration_ms = (time.time() - start_time) * 1000
            debug_logger.log_api_error(
                path=request.url.path,
                error_message=str(e),
                status_code=500,
                client_ip=client_ip
            )
            raise

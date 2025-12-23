#!/usr/bin/env python3
"""
LangChain tools with automatic SPIRE authentication.

Wraps tool execution with SPIFFE identity, mTLS, and audit logging.
"""

from langchain.tools import BaseTool
from typing import Optional, Type, Any
from pydantic import BaseModel, Field
from spiffe import SpiffeClient
import requests
import logging
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SPIREAuthenticatedTool(BaseTool):
    """
    Base class for LangChain tools with SPIRE authentication.
    
    All tools inheriting from this automatically get:
    - mTLS authentication
    - SPIFFE ID in request headers
    - SVID rotation (automatic every 5 minutes)
    - Connection pooling
    
    Usage:
        class MyTool(SPIREAuthenticatedTool):
            name = "my_tool"
            description = "Does something authenticated"
            
            def _run(self, query: str) -> str:
                return self._run_authenticated(
                    "https://api.example.com/endpoint",
                    method="GET",
                    params={"q": query}
                )
    """
    
    # Class-level SPIRE client (shared across all tool instances)
    _spiffe_client: Optional[SpiffeClient] = None
    _session: Optional[requests.Session] = None
    _rotation_thread_started: bool = False
    
    @classmethod
    def initialize_spire(cls):
        """Initialize SPIRE client (call once at application startup)"""
        if cls._spiffe_client is not None:
            logger.info("SPIRE already initialized")
            return
        
        logger.info("🔐 Initializing SPIRE for LangChain tools...")
        
        # Create SPIRE client
        cls._spiffe_client = SpiffeClient()
        
        # Create HTTP session with SPIRE credentials
        cls._session = requests.Session()
        cls._update_session_credentials()
        
        # Start background SVID rotation thread
        if not cls._rotation_thread_started:
            threading.Thread(target=cls._rotation_worker, daemon=True).start()
            cls._rotation_thread_started = True
            logger.info("✅ SPIRE initialized successfully")
    
    @classmethod
    def _update_session_credentials(cls):
        """Update session with current SVID credentials"""
        svid = cls._spiffe_client.fetch_x509_svid()
        bundle = cls._spiffe_client.fetch_x509_bundles()
        
        # Set client certificate and CA bundle
        cls._session.cert = (svid.cert_path, svid.private_key_path)
        cls._session.verify = bundle.get_bundle_for_trust_domain('example.com').path
        
        logger.debug("Updated session credentials")
    
    @classmethod
    def _rotation_worker(cls):
        """Background thread that rotates SVID every 5 minutes"""
        while True:
            time.sleep(300)  # 5 minutes
            try:
                cls._update_session_credentials()
                logger.info("🔄 SVID rotated successfully")
            except Exception as e:
                logger.error(f"❌ SVID rotation failed: {e}")
    
    def _run_authenticated(
        self, 
        url: str, 
        method: str = "GET", 
        **kwargs
    ) -> Any:
        """
        Make authenticated request with SPIRE credentials.
        
        Args:
            url: API endpoint URL
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional requests arguments (params, json, etc.)
        
        Returns:
            JSON response from API
        
        Raises:
            RuntimeError: If SPIRE not initialized
            requests.HTTPError: If API returns error status
        """
        if self._spiffe_client is None:
            raise RuntimeError(
                "SPIRE not initialized. Call SPIREAuthenticatedTool.initialize_spire() first."
            )
        
        # Get current SPIFFE ID
        svid = self._spiffe_client.fetch_x509_svid()
        spiffe_id = str(svid.spiffe_id)
        
        # Add SPIFFE ID to request headers
        headers = kwargs.get('headers', {})
        headers['X-SPIFFE-ID'] = spiffe_id
        kwargs['headers'] = headers
        
        # Log tool execution
        logger.info(
            f"🔧 Tool '{self.name}' executing: {method} {url} "
            f"(SPIFFE ID: {spiffe_id})"
        )
        
        # Make authenticated request
        response = self._session.request(method, url, **kwargs)
        response.raise_for_status()
        
        return response.json()


# Example tool implementation
class CustomerDataInput(BaseModel):
    """Input schema for CustomerDataTool"""
    customer_id: str = Field(description="Customer ID to fetch")


class CustomerDataTool(SPIREAuthenticatedTool):
    """
    Fetch customer data with SPIRE authentication.
    
    This tool authenticates using mTLS with SPIFFE credentials
    before accessing the customer API.
    """
    
    name: str = "get_customer_data"
    description: str = "Fetch customer information by ID"
    args_schema: Type[BaseModel] = CustomerDataInput
    
    def _run(self, customer_id: str) -> str:
        """Fetch customer data from authenticated API"""
        try:
            data = self._run_authenticated(
                f"https://customer-api.example.com/customers/{customer_id}",
                method="GET"
            )
            return str(data)
        except requests.HTTPError as e:
            return f"Error fetching customer data: {e}"


# Example usage
if __name__ == "__main__":
    # Initialize SPIRE once at application startup
    SPIREAuthenticatedTool.initialize_spire()
    
    # Create tool instance
    customer_tool = CustomerDataTool()
    
    # Use tool (SPIRE authentication happens automatically)
    result = customer_tool._run(customer_id="12345")
    print(f"Result: {result}")

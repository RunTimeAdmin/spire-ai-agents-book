#!/usr/bin/env python3
"""
Simple AI agent with SPIRE integration.

Demonstrates:
- Fetching SVID from SPIRE agent
- Displaying SPIFFE ID
- Basic error handling
"""

from spiffe import SpiffeClient
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Fetch SVID and display SPIFFE ID"""
    
    try:
        # Initialize SPIRE client
        # Connects to /tmp/spire-agent/public/api.sock by default
        client = SpiffeClient()
        logger.info("✅ SPIRE client initialized")
        
        # Fetch X.509-SVID
        svid = client.fetch_x509_svid()
        
        # Display SPIFFE ID
        print(f"\n🔐 My SPIFFE ID: {svid.spiffe_id}")
        
        # Show certificate details
        not_after = svid.leaf.not_valid_after
        print(f"📅 Certificate expires: {not_after.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Calculate time until expiry
        time_until_expiry = not_after - datetime.utcnow()
        hours_until_expiry = time_until_expiry.total_seconds() / 3600
        print(f"⏰ Time until expiry: {hours_until_expiry:.1f} hours")
        
        # Show trust domain
        trust_domain = str(svid.spiffe_id).split('://')[1].split('/')[0]
        print(f"🌐 Trust domain: {trust_domain}")
        
        logger.info("✅ SVID successfully fetched")
        
        return 0
        
    except FileNotFoundError:
        logger.error("❌ SPIRE agent socket not found")
        logger.error("   Make sure SPIRE agent is running")
        logger.error("   Expected socket: /tmp/spire-agent/public/api.sock")
        return 1
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

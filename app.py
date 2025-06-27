# JUGGERNAUT AI - MAIN SYSTEM (FIXED VERSION)
# This is now the FIXED version with correct model paths
# RTX 4070 SUPER Optimized - NO DEMO MODE

import os
import sys
import logging
from pathlib import Path

# Import the fixed system
try:
    # Import from the fixed version
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from juggernaut_real_fixed import app, logger
    
    if __name__ == "__main__":
        logger.info("Starting Juggernaut AI - FIXED VERSION")
        logger.info("Using REAL Gemma model with correct paths")
        logger.info("RTX 4070 SUPER optimized")
        
        # Start the fixed system
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
        
except ImportError as e:
    print(f"ERROR: Could not import fixed system: {e}")
    print("Please ensure juggernaut_real_fixed.py exists")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Failed to start system: {e}")
    sys.exit(1)


#!/usr/bin/env python3
"""
Standalone Celery worker startup script for Mock Cloud API
This script can be run independently from the main API
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.worker import celery_app

if __name__ == "__main__":
    print("Starting Mock Cloud API Celery Worker...")
    print("Worker will process VM and volume creation tasks")
    print("Press Ctrl+C to stop the worker")
    
    try:
        # Start the worker
        celery_app.start()
    except KeyboardInterrupt:
        print("\nWorker stopped by user")
    except Exception as e:
        print(f"Worker error: {e}")
        sys.exit(1)

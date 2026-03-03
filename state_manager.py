"""
Firestore-based state management for the Autonomous Strategy Evolution Framework.
Manages persistence of strategies, performance data, and system state.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import json
from dataclasses import asdict, is_dataclass

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_query import FieldFilter

from config import Config, config

class StateManager:
    """
    Manages all state persistence and retrieval using Firebase Firestore.
    Implements proper error handling, retry logic, and data validation.
    """
    
    def __init__(self, config: Config = config):
        """Initialize Firebase connection and Firestore client"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._initialize_firebase()
        self.db: Optional[FirestoreClient] = None
        
    def _initialize_firebase(self) -> None:
        """Initialize Firebase Admin SDK with proper error handling"""
        try:
            # Check if Firebase app already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.config.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
                self.logger.info("Firebase Admin SDK initialized successfully")
            else:
                self.logger.info("Firebase Admin SDK already initialized")
                
            self.db = firestore.client()
            self.logger.info(f"Firestore client connected to project: {self.db.project}")
            
        except FileNotFoundError as e:
            self.logger.error(f"Firebase credentials file not found: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Invalid Firebase credentials: {e}")
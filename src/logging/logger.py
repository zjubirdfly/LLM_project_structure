from service.util.constants import LOGGING_PARENT_FOLDER, LOGGING_SERVICE_NAME
from loguru import logger as loguru_logger
from typing import Dict, Any
import re
from pathlib import Path
import sys
import json

class Logger:
    @staticmethod
    def get_next_filename(folder: str, prefix: str) -> str:
        """
        Generate a unique filename by finding the largest existing number and adding 1.
        If no existing files found, starts from 1.
        
        Args:
            folder (str): The folder path where the file will be saved
            prefix (str): The prefix for the filename
            
        Returns:
            str: Path to the log file
        """
        # Create folder if it doesn't exist
        log_dir = Path(folder)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all files with the given prefix
        pattern = re.compile(rf"{re.escape(prefix)}_(\d+)\.json")
        max_num = 0
        
        # Look through existing files to find the largest number
        for file in log_dir.glob(f"{prefix}_*.json"):
            match = pattern.match(file.name)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
        
        # Use the next number after the largest found
        next_num = max_num + 1
        return str(log_dir / f"{prefix}_{next_num}.json")
    
    @staticmethod
    def log_json(folder: str, file_prefix: str, data: Dict[str, Any]) -> str:
        full_folder = Path(LOGGING_PARENT_FOLDER) / Path(folder)
        log_file = Logger.get_next_filename(str(full_folder), file_prefix)
        
        # this saves the raw json string to the file without extra formatting from loguru
        try:
            log_id = loguru_logger.add(log_file, format="{message}")
            loguru_logger.info(json.dumps(data)) 
        finally:
            loguru_logger.remove(log_id)
        
        return log_file

def _configure_loguru_once():
    if getattr(loguru_logger, "_is_configured", False):
        return
    # Remove all default handlers (stdout/stderr)
    loguru_logger.remove()
    loguru_logger._is_configured = True  # monkey-patch flag onto logger object

_configure_loguru_once()
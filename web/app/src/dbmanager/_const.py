from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Section to edit
NONE_LABEL = "Empty"

# Funcs
def check_dir(dir_path):
    if not Path.exists(dir_path) or not Path.is_dir(dir_path):
        logger.critical(f"{dir_path} dir is invalid or missing")
        
def check_file(file_path, is_critical: bool):
    """If `is_critical` then critical error. Else info and create file"""
    if not Path.exists(file_path) or not Path.is_file(file_path):
        if is_critical:
            logger.critical(f"{file_path} file is invalid or missing.")
        else:
            with open(file_path, 'w'): pass
            if not Path.exists(file_path) or not Path.is_file(file_path):
                logger.critical(f"{file_path} file is invalid or missing. Creation attempt failed.")
            else:
                logger.info(f"{file_path} was created.")

# Processing section
## Parent dir
parent_dir = Path(__file__).parent

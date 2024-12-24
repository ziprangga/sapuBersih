import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from src.clean_junk_logic import JunkFileCleaner
from src.utility import ResourceManager as util

"""
Unit tests for the application entry point.
"""

from src import main


def test_main_module_import() -> None:
    """
    Verify that the main module can be imported.
    """
    assert main is not None
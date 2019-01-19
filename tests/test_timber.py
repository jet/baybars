from baybars.timber import get_logger


import pytest


def test_initialization_logger():
  basic_logger = get_logger('test')
  assert hasattr(basic_logger, 'info')
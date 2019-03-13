import datetime

import pytest

from baybars import era


def test_timestamp():
	''' Test timestamp format. '''
	date_string = era.get_timestamp_in_string_format()
	assert len(date_string) == 14
	date = datetime.datetime.strptime(date_string, era.DATETIME_FORMAT)
	assert isinstance(date, datetime.datetime)

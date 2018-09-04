import pytest
import sys

sys.path.append('..')

from date import DateTime

class TestDateTime:
  
  @pytest.mark.parametrize('start_time, end_time, elapsed', [
    (1495755358, 1535755358, '1 year'),
    (1490055358, 1495755358, '2 months'),
    (1489144348, 1490055358, '10 days'),
    (1489062348, 1489144348, '22 hours'),
    (1489046950, 1489050490, '59 minutes'),
    (1489046949, 1489046950, '1 second')
  ])
  def test_elapsed(self, start_time, end_time, elapsed):
    assert DateTime.elapsed(start_time, end_time) == elapsed

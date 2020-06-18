from typing import Callable, List, Union

import pandas as pd

StatFunction = Callable[[pd.Series], float]
"""A callable statistic function."""

StatList = List[Union[str, StatFunction]]
"""A list of statistics."""

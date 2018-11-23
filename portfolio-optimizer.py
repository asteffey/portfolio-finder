import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#get data from csv
historic_returns = pd.read_csv("historic_data.csv").set_index("Year") / 100
historic_returns = historic_returns.drop(labels='USA-REIT',axis=1)

breakpoint()
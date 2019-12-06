import pandas as pd
df = pd.read_csv("datasetbooks.csv")
df.to_hdf('./datasetbooks.h5', 'test')
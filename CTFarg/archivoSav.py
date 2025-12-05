import pyreadstat
import os

df, meta = pyreadstat.read_sav(os.path.join(os.path.dirname(__file__), 'tloz-totk.sav'))
print(df.head())
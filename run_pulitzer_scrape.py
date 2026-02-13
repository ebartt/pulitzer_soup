from extract_list import get_data
import pandas as pd

dattest = pd.DataFrame(get_data())
dattest.to_csv('pulitzer_list_dirty.csv', index=False)
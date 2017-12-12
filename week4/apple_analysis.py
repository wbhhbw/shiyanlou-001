import pandas as pd

def quarter_volume():
	data = pd.read_csv('/home/shiyanlou/apple.csv', header=0)
	i = pd.to_datetime(data['Date'])
	volume_data = pd.Series(list(data['Volume']), index=i)
	second_volume = volume_data.resample('3MS').sum().sort_values()[-2]
	return second_volume

from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas as pd
import time

def analysis(file):
	source_data = pd.read_json(file)
	plot_data = source_data[['user_id','minutes']].groupby('user_id').sum()
	return plot_data

def plot(plot_data):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_title('StudyData')
	ax.set_xlabel('User ID')
	ax.set_ylabel('Study Time')
	x = plot_data.index
	y = plot_data.minutes
	ax.plot(x,y)
	return fig
	
if __name__ == '__main__':
	plot_data = analysis('/home/shiyanlou/Code/user_study.json')
	fig = plot(plot_data)
	plt.show()

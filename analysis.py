import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

def secs2human(secs):
	return str(datetime.timedelta(seconds=secs))

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	args = parser.parse_args()

	df = pd.read_csv('stats.csv')
	df['hour connected'] = pd.Series([None if np.isnan(x) else datetime.datetime.fromtimestamp(int(x)).hour for x in df['connected']], index=df.index)
	df['hour disconnected'] = pd.Series([None if np.isnan(x) else datetime.datetime.fromtimestamp(int(x)).hour for x in df['disconnected']], index=df.index)
	#print df['name'].value_counts()

	overview = pd.pivot_table(
		df,
		index=["name"],
		values=['online'],
		aggfunc=[len,lambda x: secs2human(np.sum(x)), np.sum],
		margins=True
	)
	overview.sort_values(by=('sum','online'),ascending=False,inplace=True)
	print overview
	overview.to_html('overview.html')
	
	conns = pd.pivot_table(df,index=["hour connected"],columns='name',values='connected',aggfunc=[len])
	plot = conns.plot(kind='bar', stacked=True, figsize=(20,10),fontsize=10)
	fig = plot.get_figure()
	fig.savefig("connected.png")
	
	disconns = pd.pivot_table(df,index=["hour disconnected"],columns='name',values='connected',aggfunc=[len])
	plot = disconns.plot(kind='bar', stacked=True, figsize=(20,10),fontsize=10)
	fig = plot.get_figure()
	fig.savefig("disconnected.png")

	#import code
	#code.interact(local=locals())
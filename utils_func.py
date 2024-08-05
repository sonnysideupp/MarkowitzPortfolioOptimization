import yfinance as yf

#get the historical prices for a stock
def get_ticker_data(symbol: str, start=None, end=None):
	try:
		ticker = yf.Ticker(symbol)
		hist = ticker.history(start=start, end=end, interval='1d').Close
		hist = hist[~hist.isna()]
		
		#day-to-day price difference
		diffs = hist.diff()
		pct_change = hist.pct_change()
		hist = hist.reset_index()
		hist['price_change'] = diffs.values
		hist['pct_change'] = pct_change.values
		
		#cast datetime to date
		hist.Date = hist.Date.apply(lambda d: d.date())
	except:
		return None
	return hist.dropna()


def get_sharpe_ratio(r, rf_rate, sd):
	return (r - rf_rate) / sd


def find_max_sharpe_ratio(returns, stds, rf_rate):
	sharp_return = returns[0]
	sharp_std = stds[0]
	sharpe_ratio = get_sharpe_ratio(sharp_return, rf_rate, sharp_std,) 
	for (ret, std) in zip(returns, stds):
		new_sharpe_ratio = get_sharpe_ratio(ret, rf_rate,  std)
		if new_sharpe_ratio > sharpe_ratio:
			sharpe_ratio = new_sharpe_ratio
			sharp_return = ret
			sharp_std = std
	return sharp_return, sharp_std


def find_max_sharpe_ratio_weights(returns, stds, weights, rf_rate):
	sharp_weights = weights[0]
	sharpe_ratio = get_sharpe_ratio(returns[0], rf_rate, stds[0]) 
	for (ret, std, wt) in zip(returns, stds, weights):
		new_sharpe_ratio = get_sharpe_ratio(ret, rf_rate,  std)
		if new_sharpe_ratio > sharpe_ratio:
			sharpe_ratio = new_sharpe_ratio
			sharp_weights = wt
	return sharp_weights
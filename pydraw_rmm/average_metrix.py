from painter import *
import numpy as np

# Cредняя корреляция + 50% перцентиль + 100% перцентиль

def getAllMetrixMembers(var_name, year_start, var_num):
	metrics = []
	years = np.arange(year_start, year_start+var_num, 1, dtype=int) # year_start ... year_end - 1
	for year in years:
		print("year: ",year)
		metric_text_file = f'/home/leonid/Desktop/MSU/mj0-rmm/mjo-rmm/mjo-rmm_{var_name}_{year}1230.txt' 
		print("path metric: ", metric_text_file)
		with open(metric_text_file) as f1:
			next(f1)
			for line in f1:
				if line != ['']:
					# print(line)
					metrics.append(float(line))
	metrics = np.array_split(metrics, var_num)
	return metrics

def getMetricPercentile(metrics, percentile):
	perc_metrics = []
	for day in range(0, len(metrics[0])): # days to draw
		dayly_metric = getDaylyMetric(metrics, len(metrics), day)
		perc_metrics.append(np.percentile(dayly_metric, percentile))
	return perc_metrics

def getDaylyMetric(pc1_all_memb, memb_to_draw, day): # memb_to_draw = years
	dayly_metric = []
	for j in range(0, memb_to_draw): # i-th day in all months
		dayly_metric.append(pc1_all_memb[j][day])
	return dayly_metric

def getMetricMean(metrics):
	mean_metric = []
	for day in range(0, len(metrics[0])): # days to draw
		dayly_metric = getDaylyMetric(metrics, len(metrics), day)
		mean_metric.append(np.mean(dayly_metric))
	return mean_metric


cor_metrics = getAllMetrixMembers("cor", 1992, 4)
print("cor_metrics: ", cor_metrics)
metric_perc_50 = getMetricPercentile(cor_metrics, 50)
print("metric_perc_50: ", metric_perc_50)
metric_perc_100 = getMetricPercentile(cor_metrics, 100)
print("metric_perc_100: ", metric_perc_100)
mean_metric = getMetricMean(cor_metrics)
print("mean_metric: ", mean_metric)

fig, ax = plt.subplots()
plt.xlabel('days')
plt.ylabel('Corr')
for cor in cor_metrics:
	plt.plot(np.arange(len(cor)), cor, color='black', ms=2.5,  linewidth=0.5)

plt.plot(np.arange(len(mean_metric)), mean_metric, marker='.', color='red', ms=2.5,  linewidth=1.2, label='Mean')
plt.plot(np.arange(len(metric_perc_50)), metric_perc_50, marker='.', color='blue', ms=2.5,  linewidth=1.2, label='50 percentile')
plt.plot(np.arange(len(metric_perc_100)), metric_perc_100, marker='.', color='green', ms=2.5,  linewidth=1.2, label='100 percentile')

plt.legend()
# plt.show()
metric_png_file = f'/home/leonid/Desktop/MSU/mj0-rmm/mjo-rmm/mjo-rmm_cor'
saveFig(metric_png_file)
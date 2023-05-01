import datetime as dt
import requests
import schedule
import time
import json

def weather_request():
	
	url_for_Moscow = 'https://api.open-meteo.com/v1/forecast?latitude=55.7558&longitude=37.6176&\
	&hourly=temperature_2m,relativehumidity_2m,precipitation,windspeed_10m&past_days=0&'
	#parameters: Temperature (2 m), Relative Humidity (2 m), Precipitation (rain + showers + snow), Wind Speed (10 m)

	response = requests.get(url_for_Moscow)
	data = response.json()
	
	temperature = data['hourly']['temperature_2m']
	precipitation = data['hourly']['precipitation']
	windspeed_10m = data['hourly']['windspeed_10m']
	hours = data['hourly']['time']

	file = open('report.txt', 'w')

	file.write('Chronological order:\n')
	for hour in range(len(hours)):
		hour_report = (f"{data['hourly']['time'][hour]},temperature ={temperature[hour]},precipitation ={precipitation[hour]},windspeed_10m ={windspeed_10m[hour]}\n")
		file.write(hour_report)
	file.close()

	#делаю список температур по дням и часам 
	file = open('report.txt','r')
	dry_list = file.readlines()
	dry_list = dry_list[1:]
	
	days_hour_list = [[0] for i in range(7)]
	for day in range(1,8):
		for hour in range(1,25):
			days_hour_list[day-1].append(dry_list[((day-1)*24)+hour-1].split(sep=','))
	file.close()

	#достаю температуру по дням
	all_days_max_temp = []
	for day in range(len(days_hour_list)):
		day_temp = [day+1]
		for hour in range(1,25):
			day_temp.append(days_hour_list[day][hour][1])
		all_days_max_temp.append(day_temp)
	all_days_max_temp = sorted(all_days_max_temp)

	#достаю максимальные температуры по дням и сортирую их
	temp_each_day = []
	for day in all_days_max_temp:
		max_of_day = [f'day - {day[0]}', max(day[1:])]
		max_of_day[1] = float(max_of_day[1][max_of_day[1].index('=')+1:])
		max_of_day[0] = int(max_of_day[0][-1])
		temp_each_day.append(max_of_day)
	rate = sorted(temp_each_day, key=lambda x:x[1], reverse=True)

	#расставляю данные по дням по температуре
	days_sorted_by_temp = []
	for day in range(7):
		days_sorted_by_temp.append(days_hour_list[rate[day][0] - 1][1:])

	file = open('report.txt', 'a')
	file.write(f'\nMax temperature order\n')
	for day in days_sorted_by_temp:
		for hour in day:
			string = " ".join(hour)
			file.write(f'{string}')
	file.close()

	#для отчета о завершении работы скрипта в консоли:
	#print('done')

#для частоты работы 1 раз в час
#нужно раскомментить 'time.sleep(3600)' и закомментить 'time.sleep(5)'
#для проверки оставляю 'time.sleep(5)'


schedule.every(5).seconds.do(weather_request)
schedule.every().hour.do(weather_request)

while True:
	schedule.run_pending()
	time.sleep(5)
	#time.sleep(3600)
		

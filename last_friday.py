from datetime import *

from_year=date(2019,1,1)
last_year=date(2019,1,31)
years=[years for years in range(from_year.year,last_year.year+1)]
months=[months for months in range(12)]
last_friday=[]

total_fridays=[(from_year+timedelta(days=x)) for x in range((last_year-from_year).days) if((from_year+timedelta(days=x)).strftime('%w')=='5')]

for year in years:
  for month in months:
    fridays = [friday for friday in total_fridays if friday.month == month and friday.year==year]
    if fridays!=[]:
      last_friday.append(fridays)

for friday in last_friday:
    print(friday[-1])  


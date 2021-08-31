from datetime import * 

sdate=date(2020,4,5)
edate=date(2020,12,12)
years = [i for i in range(sdate.year, edate.year+1)]
nos=[i for i in range(1,13)]
month_wise=[]

#[(sdate+timedelta(days=x)) for x in range((edate-sdate).days)]
z=[(sdate+timedelta(days=x)) for x in range((edate-sdate).days) if((sdate+timedelta(days=x)).strftime('%w')=='5')]

for y in years:
  for m in nos:
    wise = [a for a in z if a.month == m and a.year==y]
    if wise!=[]:
      month_wise.append(wise)
 
for a in month_wise:
  print(a[-1])
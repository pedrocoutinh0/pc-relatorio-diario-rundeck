from datetime import datetime, timedelta, date

class UtilDates:
    def result_execution_time(self, current_time):
      new_current_time = datetime.now()
      execution_time = (new_current_time - datetime.strptime(current_time,"%d/%m/%Y %H:%M:%S")).total_seconds()
      return str(execution_time)
    
    def time_now(self):
      now = datetime.now() - timedelta(hours=3)
      return str(now.strftime("%d/%m/%Y %H:%M:%S"))
    
    def day_month_year(self):
      date_now = date.today()
      day=str(date_now.day).zfill(2)
      month=str(date_now.month).zfill(2)
      year=str(date_now.year)
      return {"day": day, "month": month, "year": year}

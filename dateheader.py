import datetime
from dateutil.parser import parse
import sys
class dateHeader():
    def __init__(self, arguments):
        self.arguments = arguments
    def validateArgs(self):
        args = self.arguments
        if len(args) > 1:
            # проверить это datetime или нет
            # если да - проверить одна или нет
            if len(args) == 2:
                # одно число
                try:
                    possible_date = parse(args[1], dayfirst=True)
                except:
                    return [False, False]
                start_date = end_date = str(possible_date.day) + '/' +str(possible_date.month) + '/'+ str(possible_date.year)
                return [start_date, end_date]
            elif len (args) == 3:
                try:
                    possible_first_date = parse(args[1], dayfirst=True)
                    possible_second_date = parse(args[2], dayfirst=True)
                except:
                    return [False, False]
                # check wich day is 
                if possible_first_date > possible_second_date:
                    start_date = str(possible_second_date.day) + '/' +str(possible_second_date.month) + '/'+ str(possible_second_date.year)
                    end_date = str(possible_first_date.day) + '/' +str(possible_first_date.month) + '/'+ str(possible_first_date.year)
                    

                elif possible_first_date < possible_second_date:
                    start_date = str(possible_first_date.day) + '/' +str(possible_first_date.month) + '/'+ str(possible_first_date.year)
                    end_date  = str(possible_second_date.day) + '/' +str(possible_second_date.month) + '/'+ str(possible_second_date.year)
                else:
                    start_date = end_date = str(possible_first_date.day) + '/' +str(possible_first_date.month) + '/'+ str(possible_first_date.year)
                return [start_date, end_date]
               

        else:
            # проверить за сегодня и 10 дней назад
            now = datetime.datetime.now()
            year = str(now.year)
            month = str(now.month)
            day = str(now.day)
            today = day+'/'+month+'/'+year # today
            ten_days_ago = now - datetime.timedelta(days=10)
            ten_days_ago_str = str(ten_days_ago.day) +'/'+str(ten_days_ago.month)+'/'+str(ten_days_ago.year)
            print("Getting date range from ", today, "and",ten_days_ago_str)
            start_date = ten_days_ago_str
            end_date = today
            return [start_date, end_date]

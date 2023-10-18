from src.app import App
from src.shared.utils.dates import UtilDates
from src.shared.utils.colors import bcolors

if __name__ == '__main__':
    try:
        dates = UtilDates()
        datestart = dates.time_now()
        
        print(f'##### {bcolors.BLUE}JOB STARTED AT{bcolors.ENDC}: {datestart} #####')
        app = App()
        print(f'\n##### {bcolors.BLUE}JOB FINISHED IN{bcolors.ENDC}: {dates.result_execution_time(datestart)} #####')
    except Exception as error:
        print(f'\n##### {bcolors.RED}JOB FAILED AT{bcolors.ENDC}: {dates.time_now()} #####', str(error))

from src.shared.utils.colors import bcolors
from src.shared.utils.dates import UtilDates
from src.modules.sendemail import sendEmail

class App:
    def __init__(self):
        self.execute()

    def execute(self) -> None:
        # DEFINE CLASSES
        dates = UtilDates()

        # YOUR CODE OR SERVICE HERE
        datestart = dates.time_now()
        print(f'\n{bcolors.BLUE}[SERVICE SENDEMAIL]{bcolors.ENDC} - START AT {datestart}')
        sendemail = sendEmail().execute()
        print(f'\n{bcolors.BLUE}[SERVICE SENDEMAIL]{bcolors.ENDC} - FINISHED AT {dates.result_execution_time(datestart)}')


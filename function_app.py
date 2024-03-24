import logging
import azure.functions as func
from shared import twitbot

app = func.FunctionApp()

@app.schedule(schedule="0 0 12 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def MissouriLegislationTracker(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    twitbot.main()
    logging.info('Python timer trigger function executed.')
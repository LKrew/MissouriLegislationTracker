import logging
import azure.functions as func
from shared import twitbot

app = func.FunctionApp()

@app.schedule(schedule="0 0 18 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def MissouriLegislationTracker(myTimer: func.TimerRequest) -> None:

    twitbot.main()
    logging.info('Run Completed')
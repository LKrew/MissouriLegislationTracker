import logging
import azure.functions as func
from shared import get_bills, send_posts

app = func.FunctionApp()

@app.schedule(schedule="0 */20 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def MissouriLegislationTracker(myTimer: func.TimerRequest) -> None:

    run_result = send_posts.post_bill()
    logging.info(run_result)

@app.timer_trigger(schedule="0 0 */12 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def PopulateDb(myTimer: func.TimerRequest) -> None:
    logging.info("Getting New Bill")
    get_bills.main()
    logging.info("Bills Uploaded to DB")
import logging
import azure.functions as func
from shared import executive_order_handler, get_bills, send_posts
from shared.account_config import EOAccountConfig, MOAccountConfig, USAccountConfig

app = func.FunctionApp()
##############################################
#                   MISSOURI                 #
##############################################
@app.schedule(schedule="0 */20 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def MissouriLegislationTracker(myTimer: func.TimerRequest) -> None:
    logging.info("Creating Post")
    account_config = MOAccountConfig()
    run_result = send_posts.post_bill(account_config)
    logging.info(run_result)

@app.timer_trigger(schedule="0 40 13-17 * * * ", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def PopulateMoDb(myTimer: func.TimerRequest) -> None:
    logging.info("Getting New Missouri Bills")
    account_config = MOAccountConfig()
    get_bills.main(account_config)
    logging.info("Bills Uploaded to MO DB")
    
#####################################
#           US CONGRESS             #
#####################################   
@app.schedule(schedule="7 */20 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def USCongressTracker(myTimer: func.TimerRequest) -> None:
    logging.info("Creating Post")
    account_config = USAccountConfig()
    run_result = send_posts.post_bill(account_config)
    logging.info(run_result)

@app.timer_trigger(schedule="0 20 13-17 * * * ", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def PopulateUsDb(myTimer: func.TimerRequest) -> None:
    logging.info("Getting New Federal Bills")
    account_config = USAccountConfig()
    get_bills.main(account_config)
    logging.info("Bills Uploaded to US DB")
    
#####################################
#        Executive Orders           #
#####################################

@app.schedule(schedule="14 */20 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def ExecutiveOrdersTracker(myTimer: func.TimerRequest) -> None:
    logging.info("Creating Post")
    account_config = EOAccountConfig()
    run_result = executive_order_handler.post_order(account_config)
    logging.info(run_result)
    
@app.timer_trigger(schedule="0 0 13-17 * * * ", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def PopulateEoDb(myTimer: func.TimerRequest) -> None:
    logging.info("Getting New Executive Orders")
    account_config = EOAccountConfig()
    executive_order_handler.store_executive_orders(account_config)
    logging.info("Executive Orders Uploaded to US DB")
import json
import requests
import sys, getopt
import datetime
import smtplib

# gets all events from transactons for the given day
def main(argv):
    
    #url = 'http://localhost:3000/api/queries/getDailyEvents'
    url = 'http://35.224.160.182:3000/api/queries/getDailyEvents'

    velocityEmailBody = """ Hello,\nOur records show that you have triggered a High Velocity Warning,
    meaning that you have submitted more than 3 transactions within the last 5 minutes. If this
    is true, please disregard this message. Otherwise, please contact aar319@lehigh.edu as soon as possible.
    \n\t- HawKoin's High Powered Security Team 
    \n\n Transaction ID: """
    txnThreshEmailBody = """ Hello,\nOur records show that you have triggered a Transaction Threshold Breach Warning,
    meaning that you have submitted a transaction worth more than your set maximum. If this
    was you, please disregard this message. Otherwise, please contact aar319@lehigh.edu as soon as possible.
    \n\t- HawKoin's High Powered Security Team 
    \n\n Transaction ID: """
    lowBalEmailBody = """ Hello,\nOur records show that you have triggered a Low Balance Alert,
    meaning that your balance is below your set minimum. This could lead to insufficient funds for future transactions.
    You may want to consider adding more funds to your HawKoin wallet.
    \n\t- HawKoin's High Powered Security Team 
    \n\n Transaction ID: """
    
    try:

        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours=24)

        dateStr = earlier.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # DESIRED FORMAT FOR DATE TIME (NODE) = 2018-11-12T20:47:56.049Z
        # WHAT I HAVE IN PYTHON =               2018-11-11 21:21:33.252392

        extendedURL = url + '?stamp=' + dateStr

        response = requests.get(extendedURL)

        json_string = response.json()
        formatted_json = json.dumps(json_string, sort_keys=True, indent=4, separators=(',',': '))

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("hawkoin.alerts@gmail.com", "Sharonisanode")

        for item in json_string:
            txnID = item['transactionId']
            if item['eventsEmitted']:
                for event in item['eventsEmitted']:
                    if event['$class'] == 'org.hawkoin.network.VelocityWarning':
                        msg = "\r\n".join([
                                "From: hawkoin.alerts@gmail.com",
                                "Subject: HawKoin: Velocity Warning",
                                "",
                                velocityEmailBody + txnID
                        ])
                        if event['info']['email']:
                            server.sendmail("hawkoin.alerts@gmail.com", event['info']['email'], msg)
                            note = 'Sent Velocity Warning to ' + event['info']['email']
                            print(note)
                    elif event['$class'] == 'org.hawkoin.network.LowBalanceAlert':
                        msg = "\r\n".join([
                                "From: hawkoin.alerts@gmail.com",
                                "Subject: HawKoin: Low Balance Alert",
                                "",
                                lowBalEmailBody + txnID
                        ])
                        if event['info']['email']:
                            server.sendmail("hawkoin.alerts@gmail.com", event['info']['email'], msg)
                            note = 'Sent Low Balance Alert to ' + event['info']['email']
                            print(note)
                    elif event['$class'] == 'org.hawkoin.network.TransactionThreshBreach':
                        msg = "\r\n".join([
                                "From: hawkoin.alerts@gmail.com",
                                "Subject: HawKoin: Transaction Threshold Breach",
                                "",
                                txnThreshEmailBody + txnID
                        ])
                        if event['info']['email']:
                            server.sendmail("hawkoin.alerts@gmail.com", event['info']['email'], msg,)
                            note = 'Sent Transaction Limit Breach Notification to ' + event['info']['email']
                            print(note)
        
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("***Error***: Timeout")
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("***Error***: URL is bad")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print (e)
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
    


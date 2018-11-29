import json
import requests
import sys, getopt


def main(argv):
    amount = 0
    fromType = ''
    fromID = -1
    toType = ''
    toID = -1
    try:
        opts, args = getopt.getopt(argv,"ha:f:F:", ["amount=", "fromType=", "fromID="])
    except getopt.GetoptError as e:
        print ('transferFunds.py -a <amount> -f <fromType> -F <fromID>')
        print(e)
        sys.exit(2)
    if len(sys.argv) == 1:
        print ('transferFunds.py -a <amount> -f <fromType> -F <fromID>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('transferFunds.py -a <amount> -f <fromType> -F <fromID>')
            sys.exit()
        elif opt in ("-a", "--amount"):
            amount = arg
        elif opt in ("-f", "--fromType"):
            fromType = arg
        elif opt in ("-F", "--fromID"):
            fromID = arg

    
    # url = 'http://localhost:3000/api/org.hawkoin.network.DeleteFunds'
    url = 'http://35.224.160.182:3000/api/org.hawkoin.network.DeleteFunds'
    
    fromUser = 'resource:org.hawkoin.network.' + fromType + '#' + fromID

    json_payload = {
        '$class': 'org.hawkoin.network.DeleteFunds',
        'amount': amount,
        'fromUser': fromUser,
    }

    try:
        response = requests.post(url, json=json_payload)

        status = response.status_code
       
        if(status == 500):
            json_string = response.text
            parsed_json = json.loads(json_string)
            print(parsed_json['error']['message'])
        else:
            print('Successful removal of funds from ', fromID)

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
    except:
        print("*** ERROR *** Unable to remove funds. Unknown Error")

if __name__ == '__main__':
    main(sys.argv[1:])
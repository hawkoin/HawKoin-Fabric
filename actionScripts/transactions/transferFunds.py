import json
import requests
import sys, getopt


def main(argv):
    amount = 0
    authToken = " "
    fromType = ''
    fromID = -1
    toType = ''
    toID = -1
    try:
        opts, args = getopt.getopt(argv,"ha:A:f:F:t:T:", ["amount=", "authToken=", "fromType=", "fromID=", "toType=", "toID="])
    except getopt.GetoptError as e:
        print ('transferFunds.py -a <amount> -A <authToken> -f <fromType> -F <fromID> -t <toType> -T <toID> ')
        print(e)
        sys.exit(2)
    if len(sys.argv) == 1:
        print ('transferFunds.py -a <amount> -A <authToken> -f <fromType> -F <fromID> -t <toType> -T <toID> ')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('transferFunds.py -a <amount> -A <authToken> -f <fromType> -F <fromID> -t <toType> -T <toID> ')
            sys.exit()
        elif opt in ("-a", "--amount"):
            amount = arg
        elif opt in ("-A", "--authToken"):
            authToken = arg
        elif opt in ("-f", "--fromType"):
            fromType = arg
        elif opt in ("-F", "--fromID"):
            fromID = arg
        elif opt in ("-t", "--toType"):
            toType = arg
        elif opt in ("-T", "--toID"):
            toID = arg

    
    url = 'http://localhost:3000/api/org.hawkoin.network.TransferFunds'
    
    fromUser = 'resource:org.hawkoin.network.' + fromType + '#' + fromID
    toUser = 'resource:org.hawkoin.network.' + toType + '#' + toID

    json_payload = {
        '$class': 'org.hawkoin.network.TransferFunds',
        'amount': amount,
        'authToken': authToken,
        'fromUser': fromUser,
        'toUser': toUser
    }

    try:
        response = requests.post(url, json=json_payload)

        status = response.status_code
       
        if(status == 500):
            json_string = response.text
            parsed_json = json.loads(json_string)
            print(parsed_json['error']['message'])
        else:
            print('Successful transfer from', fromType, fromID, 'to', toType, toID)

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
        print("*** ERROR *** Unable to transfer funds. Unknown error.")

if __name__ == '__main__':
    main(sys.argv[1:])
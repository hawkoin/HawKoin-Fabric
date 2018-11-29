import json
import requests
import sys, getopt


def main(argv):
    
    amount = 5
    userType = ''
    userID = -1

    try:
        opts, args = getopt.getopt(argv,"ha:t:i:", ["amount=", "type=", "id="])
    except getopt.GetoptError as e:
        print ('changeLowBalAlert.py -a <amount> -t <type> -i <id>')
        print(e)
        sys.exit(2)
    if len(sys.argv) == 1:
        print ('changeLowBalAlert.py -a <amount> -t <type> -i <id>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('changeLowBalAlert.py -a <amount> -t <type> -i <id>')
            sys.exit()
        elif opt in ("-a", "--amount"):
            amount = arg
        elif opt in ("-t", "--type"):
            userType = arg
        elif opt in ("-i", "--is"):
            userID = arg

    
    # url = 'http://localhost:3000/api/org.hawkoin.network.ChangeLowBalAlert'
    url = 'http://35.224.160.182:3000/api/org.hawkoin.network.ChangeLowBalAlert'
    
    userString = 'resource:org.hawkoin.network.' + userType + '#' + userID


    json_payload = {
        "$class": "org.hawkoin.network.ChangeLowBalAlert",
        "thresh": amount,
        "user": userString
    }

    try:
        response = requests.post(url, json=json_payload)
        
        status = response.status_code

        if(status == 500):
            json_string = response.text
            parsed_json = json.loads(json_string)
            print(parsed_json['error']['message'])
        else:
            print('Successfully changed threshold to ', amount)

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
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return "***Error***: " + str(e)
    except:
        print("*** ERROR *** Unable to change threshold")


if __name__ == '__main__':
    main(sys.argv[1:])
import json
import requests
import sys, getopt


def main(argv):
    
    userType = ''
    userID = -1
    newFirst = "null"
    newLast = "null"
    newEmail = "null"
    newAddress = "null"
    newCity = "null"
    newState = "null"
    newZip = "null"

    try:
        opts, args = getopt.getopt(argv,"ht:i:fleacsz", ["type=", "id=", "first=", "last=", "email=", "address=", "city=", "state=", "zip="])
    except getopt.GetoptError as e:
        print ('changeContactInfo.py -t [type] -i [id] -f [newFirst] -l [newLast] -e [newEnail] -a [newAddress] -c [newCity] -s [newState] -z [newZip]')
        print(e)
        sys.exit(2)
    if len(sys.argv) == 1:
        print ('changeContactInfo.py -t [type] -i [id] -f [newFirst] -l [newLast] -e [newEnail] -a [newAddress] -c [newCity] -s [newState] -z [newZip]')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print ('changeContactInfo.py -t [type] -i [id] -f [newFirst] -l [newLast] -e [newEnail] -a [newAddress] -c [newCity] -s [newState] -z [newZip]')
            sys.exit()
        elif opt in ("-t", "--type"):
            userType = arg
        elif opt in ("-i", "--id"):
            userID = arg
        elif opt in ("-f", "--first"):
            newFirst = arg
        elif opt in ("-l", "--last"):
            newLast = arg
        elif opt in ("-e", "--email"):
            newEmail = arg
        elif opt in ("-a", "--address"):
            newAddress = arg
        elif opt in ("-c", "--city"):
            newCity = arg
        elif opt in ("-s", "--state"):
            newState = arg
        elif opt in ("-z", "--zip"):
            newZip = arg


    url = 'http://localhost:3000/api/org.hawkoin.network.ChangeContactInfo'
    
    userString = 'resource:org.hawkoin.network.' + userType + '#' + userID

    json_payload = {
        "$class": "org.hawkoin.network.ChangeContactInfo",
        "newFirst": newFirst,
        "newLast": newLast,
        "newEmail": newEmail,
        "newAdd": newAddress,
        "newCity": newCity,
        "newState": newState,
        "newZip": newZip,
        "user": userString
    }

    try:
        response = requests.post(url, json=json_payload)
        
        status = response.status_code

        if(status != 200):
            json_string = response.text
            parsed_json = json.loads(json_string)
            print(parsed_json['error']['message'])
        else:
            print('Successfully updated contact information for', userType, userID)

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
        print("*** ERROR *** Unable to update user info")


if __name__ == '__main__':
    main(sys.argv[1:])
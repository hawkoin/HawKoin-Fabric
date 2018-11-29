import json
import requests
import sys, getopt


def main(argv):

    # url = 'http://localhost:3000/api/org.hawkoin.network.DemoMode'
    url = 'http://35.224.160.182:3000/api/org.hawkoin.network.DemoMode'
    

    json_payload = {
            '$class': 'org.hawkoin.network.DemoMode',
            'id': 'activated'                                                     
            }

    try:
        response = requests.post(url, json=json_payload)

        status = response.status_code

        if(status != 200):
            json_string = response.text
            parsed_json = json.loads(json_string)
            statusCode = parsed_json['error']['statusCode']
            if(statusCode == 500):
                deleteResponse = requests.delete(url+'/activated')
                if (deleteResponse.status_code == 204):
                    print('Successfully disabled demo mode')

            #print(parsed_json['error']['message'])
        elif (status == 200):
            print('Successfully enabled demo mode')

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
        print("*** ERROR *** Unable to post Student")


if __name__ == '__main__':
    main(sys.argv[1:])

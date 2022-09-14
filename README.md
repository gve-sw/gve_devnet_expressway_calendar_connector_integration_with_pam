# gve_devnet_expressway_calendar_connector_integration_with_pam
This prototype automates password update between PAM(Password Access Manager) and the calendar connector on Cisco expressway. It utilizes (1) BeyondInsight and Password Safe REST API to retrieve the password and (2) python to configure that password on the calendar connector and (3) Linux cron job to schedule this process to run every seven days or as set by the administrator.  

## Prototype Overview

![/IMAGES/Overview.png](/IMAGES/Overview.png)
#

To use the BeyondInsight and Password Safe REST API, the administrator needs to create an API registration that’ll generate an API key that can be used to interact programmatically with PAM. For more information on creating API registration, refer to the document [here](https://www.beyondtrust.com/docs/beyondinsight-password-safe/ps/admin/configure-api-registration.htm).


The administrator then needs to fill in the following PAM-related information in the main.py script: 
```
base=<your base IP_address>
apikey=<the API key configured in BeyondInsight for your application>
runas=<the username of a BeyondInsight user that has been granted permission to use the API key>
systemName=<name of the managed system>
accountName=<name of the managed account>
```
In order to be able to access the Cisco expressway via ssh using the default port, the administrator needs to add the following information to the main.py script: 

```
e_host=<the IP address of the expressway>
e_username=<username>
e_password=<password>
```

Once all the information are filled, the main.py script will be run to achieve the following tasks: 
1. Interact programmatically with PAM system and retrieve the configured password. 
2. Connect to the expressway via ssh and use the retrieved password from task 1 to configure the password on the Calendar connector. 
3. Send an email to a specified email address to indicate the status of running the script using SMTP.


The main.py script uses the following xcommand to update the password:
```
xcommand cafe c_cal update_calendar_exchange_config '{"service_record_id": "<service_record_id>", "password": "<password>", "emailAddress": "<emailAddress>"}’
```

The parameters to the command are: 
* service_record_id [REQUIRED]: same as Service Record ID on the Microsoft Exchange Configuration web UI record modification page.
* password [OPTIONAL]: same as Service Account Password on the Microsoft Exchange Configuration web UI record modification page.
* emailAddress [OPTIONAL]: same as Email Address on the Microsoft Exchange Configuration web UI record modification page.


Every-time the main.py script is ran, an email is sent to a specified email address indicating the status of the process. To fully automate the solution, a Linux cron job is used so that the main.py script will run every Sunday which is compliant with the frequency of which the password on the PAM system will be changed. 



## Contacts
* Roaa Alkhalaf
* Stien Vanderhallen

## Solution Components
* Expressway
*  Webex
*  BeyondInsight and Password Safe REST API



## Installation/Configuration

The following commands are executed in the terminal.

1. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). 
Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html). 

2. Access the created virtual environment folder

        $ cd your_venv

3. Clone this repository

        $ git clone https://wwwin-github.cisco.com/gve/gve_devnet_expressway_calendar_connector_integration_with_pam 



4. Access the folder `gve_devnet_expressway_calendar_connector_integration_with_pam`

        $ cd gve_devnet_expressway_calendar_connector_integration_with_pam

5. Install the dependencies:

        $ pip install -r requirements.txt



## Usage

The password will be updated automatically based on the specified time in the crontab. For a manual fetch of the password, type the following command in the terminal: 

```
python3 main.py
```

To change the schedule of when the script will run, modify the crontab file.


# 

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.

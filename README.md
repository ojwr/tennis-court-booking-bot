<div id="top"></div>


<!-- ABOUT THE PROJECT -->

<h3 align="center">Kennington Park Tennis Booking Bot</h3> 
<br />

### Usage

Command line arguements for script:<br />
  - argv[1] = Time of court booking (8-21) <br />
  - argv[2] = OPTIONAL: Day of court booking (1-31) <br />
  - argv[3] = OPTIONAL: Month of court booking (1-12) <br />
  - argv[4] = OPTIONAL: Year of court booking <br />

If no date is specified then a court one week into the future will be booked. 

Courts are available a week in advance with new bookings opening at 8pm every evening. Example cron command for booking a court every monday evening at 9pm:
   ```sh
   1 20 * * 1 cd /Path/to/directory/containing/script && python3 booking-bot-script.py 21
   ```

### Requirements

Selenium Webrowser: https://www.selenium.dev/documentation/getting_started/installing_browser_drivers/ <br />
webdriver-manager: https://pypi.org/project/webdriver-manager/


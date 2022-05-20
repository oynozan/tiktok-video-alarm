#If you want to test it, don't forget to install libraries below.
#If you are using "pip", run the commands:

"""
pip install selenium
pip install win10toast
pip install colorama
pip install win10toast
pip install chromedriver-autoinstaller
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Style
from win10toast import ToastNotifier
from fake_useragent import UserAgent
import chromedriver_autoinstaller
from datetime import datetime
from time import sleep
import os

url = "https://www.tiktok.com/@INSERT_HERE_USER_NAME" #Tiktok account URL of User
delay = 30 #Check every 30 seconds if new video has uploaded

#Colorama configuration
init(autoreset=True)

#That variable check if current operating system is Windows
isOsWindows = os.name == "nt"

#Windows notification configuration
toast = ToastNotifier()

#Fake user-agent configuration. I will use a random user-agent to access tiktok.com
ua = UserAgent()

#Functions
def ContainerLoaded():
	while True:
		try:
			driver.find_elements_by_css_selector(".video-feed")[0]
			break
		except: pass
		sleep(.5)

def logTime():
	#This function returns a string contains hour and minute as Hour:Minute format
	currentHourAndMinute = datetime.now().strftime("%H:%M")
	return f"{Fore.GREEN}[{currentHourAndMinute}]{Style.RESET_ALL}"

def removeLastLine():
	#This line deletes the last output from terminal magically
	print ("\033[A                             \033[A")

""" SELENIUM SETUP """
#I use Chrome as Selenium Browser
chromedriver_autoinstaller.install() #Install chromedriver automatically
options = Options()
options.add_argument('--log-level=3') #Suspend info logs
options.add_argument(f"user-agent={ua.random}") #Using a random user-agent to access tiktok.com without any crawler bot limitations.

#If you want to see what happens in Browser, just remove the line below. It makes Chrome run in the background without a window.
#If the refresh count stuck at 0, probably it asks for a ReCaptcha confirmation. You can see what happens in browser if you commentize it.
options.headless = True

driver = webdriver.Chrome(options=options)
driver.set_window_size(1080, 720)
driver.get(url)

#Variables that will be used in while loop
lastVideoUrl, previousURL = "", ""; loopCounter = 0

print(f"{logTime()} - {Fore.YELLOW}App Started")
print(f"{Fore.RED}Use CTRL+C combination to exit.\n")

while True:

	removeLastLineToChangeRefreshCount = True

	#Output of how many times did page refreshed
	print(f"{logTime()} - Refresh Count: {Fore.GREEN}{loopCounter}")
	loopCounter+=1

	#Wait till container loads
	ContainerLoaded()

	#This statement checks if URL before refresh page is equal to URL after refresh page
	#If previousURL is not equal to lastVideoURL that would mean there is another video in container.
	#Every new video upload takes place of first video on videos container (.video-feed class in page source)
	if (previousURL != lastVideoUrl):
		print(f"{logTime()} - {Fore.YELLOW}New Tiktok video has been uploaded!")
		if (isOsWindows):
			#Desktop notification for Windows
			toast.show_toast("USER has uploaded a new Tiktok", lastVideoUrl, duration=5)
		removeLastLineToChangeRefreshCount = False #New last line is not refreshing count so I will pass the loop step without removing last line

	previousURL = lastVideoUrl

	""" LAST VIDEO URL """
	videoContainer = driver.find_elements_by_css_selector(".video-feed")[0]
	lastVideoUrl = videoContainer.find_elements_by_css_selector(".video-feed-item .video-feed-item-wrapper")[0].get_attribute("href")

	#On First step in loop, previousURL and lastVideoURL should be equal.
	#Because in next steps a statement will check if they are not equal each other.
	if (loopCounter == 1):
		previousURL = lastVideoUrl

	#Refresh every 30 seconds
	sleep(delay)
	driver.refresh()

	#Remove the last line from terminal to make change in refresh count look dynamically
	if removeLastLineToChangeRefreshCount: removeLastLine()
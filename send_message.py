import pywhatkit

#pywhatkit.add_driver_path(path="./chromedriver.exe")

def send_message(message: str):
    print("Sending message")
    try:
        pywhatkit.sendwhatmsg_instantly(phone_no="+919811994960", message=message, tab_close=True, close_time=3)
    except Exception as e:
        print(e)

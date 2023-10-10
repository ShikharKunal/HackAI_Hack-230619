from tkinter import *
from uagents import Agent, Context
import requests
from tkinter import font

# This is the base url of the website Open WeatherMap from which we obtain our temperature data
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Please create an account on OpenWeatherMap website and go to my API keys and paste your API key below.
# I have pasted mine below but please add yours for smooth functioning of the code
API = "637062faf98453ddf7b99adc7c96625e"

# This is our uagent which will periodically obtain temperature information using the API key
pdsv = Agent(name="pdsv", seed="pdsv recovery phase")

# Creating a GUI using Tkinter library of Python
root = Tk()

# Defining the title and size of our GUI window
root.title("Temperature Alert Agent")
root.geometry("450x300")
root.minsize(width=450, height=300)
root.maxsize(width=450, height=300)

# This is for the background colour of the window
root.config(bg="lightcyan")

Label(text="fetch.ai" , font="Serif 35 bold",pady=25, bg="lightcyan", fg="black").grid(row=1, column=3)

city_label = Label(text="City : ", font="Helvetica 13 bold", pady=7,padx=20, bg="lightcyan", fg="blue").grid(row=2, column=2)
temp_min_label = Label(text="Minimum Temperature : ", font="Helvetica 13 bold", pady=7, bg="lightcyan", fg="blue",padx=20).grid(row=3, column=2)
temp_max_label = Label(text="Maximum Temperature : ", font="Helvetica 13 bold", pady=7,padx=20, bg="lightcyan", fg="blue").grid(row=4, column=2)

city_value = StringVar()
temp_min_value = StringVar()
temp_max_value = StringVar()

city_name = Entry(textvariable=city_value,bg="white",fg="black",insertbackground="black").grid(row=2, column=3)
temp_min_name = Entry(textvariable=temp_min_value,bg="white",fg="black",insertbackground="black").grid(row=3, column=3)
temp_max__name = Entry(textvariable=temp_max_value,bg="white",fg="black",insertbackground="black").grid(row=4, column=3)

# This is the functionality of the SUBMIT button which means when the button is clicked 
# this function will get executed
def perform():

    # Storing the values using get function
    CITY = city_value.get()
    MIN_TEMP = temp_min_value.get()
    MAX_TEMP = temp_max_value.get()

    # Since the main window's function is over, we destroy it
    root.destroy()

    # Just afer the uagent starts it will set some variables in storage function
    @pdsv.on_event("startup")
    async def take_input(ctx: Context):
        ctx.storage.set("city", CITY)
        ctx.storage.set("min_temp", MIN_TEMP)
        ctx.storage.set("max_temp", MAX_TEMP)
    
    # Function to convert temperature in kelvin to temperature in celcius
    def temp_convert(t):
        return t - 273.15

    # This is the periodic function executed by the the uagent
    @pdsv.on_interval(period=1.0)
    async def alert(ctx: Context):

        # Obtaining the value of city using storage function
        CITY = ctx.storage.get("city")

        # Creating url to get response from the Open Weather Map website
        url = BASE_URL + "q=" + CITY + "&APPID=" + API

        # This is the response we got
        response = requests.get(url).json()

        # This is the temperature in kelvin
        t = response['main']['temp']

        # Converting temperature into celcius scale
        t_celsius = temp_convert(t)

        # Displaying the current temperature of the specified city
        ctx.logger.info(f"Current temperature in {CITY} is {t_celsius:.2f}°C")

        # Obtaining min and max temperatures from storage function
        temp_min = ctx.storage.get("min_temp")
        temp_max = ctx.storage.get("max_temp")
             
        # This is the function which creates the ALERT dialog box
        def alert_box(s):
            root3 = Tk()

            # Defining the alert box dimensions
            root3.geometry("600x249")
            root3.minsize(width=600, height=249)
            root3.maxsize(width=600, height=249)

            # Background colour
            root3.config(bg="paleturquoise1")
            custom_font1 = font.Font(family="Helvetica", size=55, weight="bold", slant="italic")
            Label(text="ALERT!", font=custom_font1, fg="red", pady=30,bg="paleturquoise1").pack()
            custom_font2 = font.Font(family="Helvetica", size=15, weight="bold", slant="italic")
            Label(text=s, font=custom_font2, fg="black", pady=10,bg="paleturquoise1").pack()

            # Function to destroy the window after 1 second
            def destroy_window():
                root3.destroy()
            
            # After every 1000 milliseconds it will call destroy_window function
            # But after 1st call the root3 will get destroyed
            root3.after(1000, destroy_window)
            root3.mainloop()
        
        # Checking if the current temperature is within the specified temperature range
        if float(t_celsius) <= float(temp_min):
            str1 = f"ALERT! {CITY}'s temperature is less than {float(temp_min):.2f}°C."
            alert_box(str1)
        elif float(t_celsius) >= float(temp_max):
            str2 = f"ALERT! {CITY}'s temperature is greater than {float(temp_max):.2f}°C."
            alert_box(str2)
        else:
            # Printing No danger in output console
            ctx.logger.info(f"No danger")

    # Callin our uagent to start execution
    if __name__ == "__main__":
        pdsv.run()

Button(text="SUBMIT", command = perform, fg="black").grid(row=5, column=3)

root.mainloop()
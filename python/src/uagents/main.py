from tkinter import *
from uagents import Agent, Context
import requests
from tkinter import font

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API = "637062faf98453ddf7b99adc7c96625e"

pdsv = Agent(name="pdsv", seed="pdsv recovery phase")

root = Tk()


root.title("Temperature Alert Agent")
root.geometry("450x300")
root.minsize(width=450, height=300)
root.maxsize(width=450, height=300)
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

def perform():
    CITY = city_value.get()
    MIN_TEMP = temp_min_value.get()
    MAX_TEMP = temp_max_value.get()
    root.destroy()

    @pdsv.on_event("startup")
    async def take_input(ctx: Context):
        ctx.storage.set("city", CITY)
        ctx.storage.set("min_temp", MIN_TEMP)
        ctx.storage.set("max_temp", MAX_TEMP)
    
    def temp_convert(t):
        return t - 273.15

    @pdsv.on_interval(period=1.0)
    async def alert(ctx: Context):
        CITY = ctx.storage.get("city")
        url = BASE_URL + "q=" + CITY + "&APPID=637062faf98453ddf7b99adc7c96625e"
        response = requests.get(url).json()
        t = response['main']['temp']
        t_celsius = temp_convert(t)
        ctx.logger.info(f"Current temperature in {CITY} is {t_celsius:.2f}°C")

        temp_min = ctx.storage.get("min_temp")
        temp_max = ctx.storage.get("max_temp")
             

        def alert_box(s):
            root3 = Tk()
            root3.geometry("600x249")
            root3.minsize(width=600, height=249)
            root3.maxsize(width=600, height=249)
            root3.config(bg="paleturquoise1")
            custom_font1 = font.Font(family="Helvetica", size=55, weight="bold", slant="italic")
            Label(text="ALERT!", font=custom_font1, fg="red", pady=30,bg="paleturquoise1").pack()
            custom_font2 = font.Font(family="Helvetica", size=15, weight="bold", slant="italic")
            Label(text=s, font=custom_font2, fg="black", pady=10,bg="paleturquoise1").pack()
            def destroy_window():
                root3.destroy()
            root3.after(1000, destroy_window)
            root3.mainloop()
        
        if float(t_celsius) <= float(temp_min):
            str1 = f"ALERT! {CITY}'s temperature is less than {float(temp_min):.2f}°C."
            alert_box(str1)
        elif float(t_celsius) >= float(temp_max):
            str2 = f"ALERT! {CITY}'s temperature is greater than {float(temp_max):.2f}°C."
            alert_box(str2)
        else:
            ctx.logger.info(f"No danger")

           
    
    if __name__ == "__main__":
        pdsv.run()

Button(text="SUBMIT", command = perform, bg="blue", fg="white").grid(row=5, column=3)

root.mainloop()
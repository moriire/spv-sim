import PySimpleGUI as psg
import json
import toml
import time
import math
import sys

def create_text(text):
    with open("spvs.txt", "w") as txt:
        txt.write(text)
    txt.close()

def create_csv(text):
    with open("spvs.csv", "w") as txt:
        txt.write(text)
    txt.close()

icon="assets/s.ico"
settings=toml.load("settings.toml")
feel=settings['feel']
color=psg.ChangeLookAndFeel(feel)
themes=("DarkGrey2", "DarkBlue", "Kayak", "Reds", "DarkBlue")
#list(psg.LOOK_AND_FEEL_TABLE.keys())("LightBrown7", "DarkGrey2", "DarkBrown", "DarkBlue", "DarkAmber", "Kayak", "Reds", "DarkBlue")
font=settings['font']
pad=tuple(settings['pad'])
pgf=settings['pgf']
size=tuple(settings['size'])
#print(settings)
def change_settings(key, value):
    settings[key]=value
    wt = open("settings.toml", "w")
    return toml.dump(settings, wt)

def load(key, value):
    settings[key] = value
    wt = open("settings.toml", "w")
    return toml.dump(settings, wt)
    
version="{name}\nVersion-{version}".format(name="Solar PV Simulator", version=1.0)
solar_type=("Monocrystalline", "Polycrystalline", "Amorphous", "Hybrid")
pgf=settings['pgf']#Power generation fsctor for Nigeria
device_list={"100W light bulb (Incandescent)":100, "22 Inch LED TV":17, '25" colour TV':150, '3" belt sander':1000,
             "32 Inch LED TV":20, "42 Inch LED TV":60, "46 Inch LED TV":70, "49 Inch LED TV":85, "55 Inch LED TV":116,
             "60W light bulb (Incandescent)":60, "65 Inch LED TV":130, "82 Inch LED TV":290, '9" disc sander':1200,
             "Air Cooler":80, "Air Fryer":1500, "Air Purifier":30, "Amazon Echo":3, "Amazon Echo Dot":2, "Amazon Echo Show":2,
             "American-Style Fridge Freezer":40, "American-Style Fridge Freezer-2":60, "American-Style Fridge Freezer-3":80,
             "Apple TV":3, "Aquarium Pump":20, "AV Receiver":450, "Bathroom Towel Heater":80, "Bathroom Towel Heater-1":150,
             "Ceiling Fan":70, "Chromebook":45, "Chromecast":2, "Clock radio":2, "Clothes Dryer":1000, "Coffee Maker":800, "Coffee Maker-1":1400,
             "Computer Monitor": 30, "Cooker Hood":30, "Corded Drill":850, "Corded Electric Handheld Leaf Blower":2500, "Cordless Drill Charger":150,
             "Curling Iron":35, "DAB Mains Radio":9, "Deep Freezer":19, "Dehumidifier":240, "Desktop Computer":100, "Desktop Computer-1":450,
             "Dishwasher":1500, "Domestic Water Pump":300, "DVD Player":45, "Electric Blanket":200, "Electric Boiler":4000, "Electric Boiler":14000,
             "Electric Doorbell Transformer":2, "Electric Heater Fan":2500, "Electric Kettle":1200, "Electric Kettle-1":3000, "Electric Mower":3599,
             "Electric Pressure Cooker":1000, "Electric Shaver":20, "Electric stove":2000, "Electric Tankless Water Heater":7700,
             "Electric Thermal Radiator":500, "Espresso Coffee Machine":1500, "EV Car Charger":7000, "EV Home Charger":3000,
             "Evaporative Air Conditioner":2600, "External Hard Drive":3, "Extractor Fan":12, "Fluorescent Lamp":45,
             "Food Blender":400, "Food Dehydrator":800, "Freezer":50, "Fridge":100, "Fridge-1":220, "Fridge / Freezer":150, "Fridge / Freezer":400,
             "Fryer":1000, "Game Console":160, "Gaming PC":300, "Gaming PC-1":600, "Garage Door Opener":350, "Google Home Mini":15,
             "Guitar Amplifier":25, "Hair Blow Dryer":2000, "Hand Wash Oversink Water Heater":3000, "Heated Bathroom Mirror":75, "Heated Hair Rollers":400,
             "Home Air Conditioner":1500, "Home Air Conditioner-1":3500, "Home Internet Router":5, "Home Internet Router-1":15,
             "Home Phone":3, "Home Phone-1":5, "Home Sound System":95, "Hot Water Dispenser":1250, "Hot Water Immersion Heater":3000,
             "Humidifier":40, "Inkjet Printer":20, "Inkjet Printer-1":30, "Inverter Air conditioner":1500, "Iron":1000,
             "Jacuzzi":3000, "Jacuzzi-1":4500, "Jacuzzi-2":7500, "Kitchen Extractor Fan":200, "Laptop Computer":50, "Laptop Computer-1":75, "Laptop Computer-2":100,
             "Laser Printer":750, "LED Christmas Lights":5, "LED Light Bulb":7, "LED Light Bulb-1":10, "Oven":2150, "Paper Shredder":200,
             "Pedestal Fan":60, "Phone Charger":4, "Phone Charger-1":7, "Playstation 4":90, "Playstation 5":200, "Portable Air Conditioner":1200,
             "Projector":270, "Refrigerator":200, "Scanner":15, "Sewing Machine":80, "Singer Sewing Machine":100, "Steam Iron":2500,
             "Table Fan":10, "Table Fan-1":20, "Table Fan-2":25, "Tablet Charger":15,
             "laptop":60, "Bulb":100}

device_listx={'100W light bulb (Incandescent)[100W]': 100,'22 Inch LED TV[17W]': 17,'25" colour TV[150W]': 150,'3" belt sander[1000W]': 1000,'32 Inch LED TV[20W]': 20,'42 Inch LED TV[60W]': 60,'46 Inch LED TV[70W]': 70, '49 Inch LED TV[85W]': 85, '55 Inch LED TV[116W]': 116, '60W light bulb (Incandescent)[60W]': 60, '65 Inch LED TV[130W]': 130, '82 Inch LED TV[290W]': 290, '9" disc sander[1200W]': 1200, 'Air Cooler[80W]': 80, 'Air Fryer[1500W]': 1500, 'Air Purifier[30W]': 30, 'Amazon Echo[3W]': 3, 'Amazon Echo Dot[2W]': 2, 'Amazon Echo Show[2W]': 2, 'American-Style Fridge Freezer[40W]': 40, 'American-Style Fridge Freezer-2[60W]': 60, 'American-Style Fridge Freezer-3[80W]': 80, 'Apple TV[3W]': 3, 'Aquarium Pump[20W]': 20, 'AV Receiver[450W]': 450, 'Bathroom Towel Heater[80W]': 80, 'Bathroom Towel Heater-1[150W]': 150, 'Ceiling Fan[70W]': 70, 'Chromebook[45W]': 45, 'Chromecast[2W]': 2, 'Clock radio[2W]': 2, 'Clothes Dryer[1000W]': 1000, 'Coffee Maker[800W]': 800, 'Coffee Maker-1[1400W]': 1400, 'Computer Monitor[30W]': 30, 'Cooker Hood[30W]': 30, 'Corded Drill[850W]': 850, 'Corded Electric Handheld Leaf Blower[2500W]': 2500, 'Cordless Drill Charger[150W]': 150, 'Curling Iron[35W]': 35, 'DAB Mains Radio[9W]': 9, 'Deep Freezer[19W]': 19, 'Dehumidifier[240W]': 240, 'Desktop Computer[100W]': 100, 'Desktop Computer-1[450W]': 450, 'Dishwasher[1500W]': 1500, 'Domestic Water Pump[300W]': 300, 'DVD Player[45W]': 45, 'Electric Blanket[200W]': 200, 'Electric Boiler[14000W]': 14000, 'Electric Doorbell Transformer[2W]': 2, 'Electric Heater Fan[2500W]': 2500, 'Electric Kettle[1200W]': 1200, 'Electric Kettle-1[3000W]': 3000, 'Electric Mower[3599W]': 3599, 'Electric Pressure Cooker[1000W]': 1000, 'Electric Shaver[20W]': 20, 'Electric stove[2000W]': 2000, 'Electric Tankless Water Heater[7700W]': 7700, 'Electric Thermal Radiator[500W]': 500, 'Espresso Coffee Machine[1500W]': 1500, 'EV Car Charger[7000W]': 7000, 'EV Home Charger[3000W]': 3000, 'Evaporative Air Conditioner[2600W]': 2600, 'External Hard Drive[3W]': 3, 'Extractor Fan[12W]': 12, 'Fluorescent Lamp[45W]': 45, 'Food Blender[400W]': 400, 'Food Dehydrator[800W]': 800, 'Freezer[50W]': 50, 'Fridge[100W]': 100, 'Fridge-1[220W]': 220, 'Fridge / Freezer[400W]': 400, 'Fryer[1000W]': 1000, 'Game Console[160W]': 160, 'Gaming PC[300W]': 300, 'Gaming PC-1[600W]': 600, 'Garage Door Opener[350W]': 350, 'Google Home Mini[15W]': 15, 'Guitar Amplifier[25W]': 25, 'Hair Blow Dryer[2000W]': 2000, 'Hand Wash Oversink Water Heater[3000W]': 3000, 'Heated Bathroom Mirror[75W]': 75, 'Heated Hair Rollers[400W]': 400, 'Home Air Conditioner[1500W]': 1500, 'Home Air Conditioner-1[3500W]': 3500, 'Home Internet Router[5W]': 5, 'Home Internet Router-1[15W]': 15, 'Home Phone[3W]': 3, 'Home Phone-1[5W]': 5, 'Home Sound System[95W]': 95, 'Hot Water Dispenser[1250W]': 1250, 'Hot Water Immersion Heater[3000W]': 3000, 'Humidifier[40W]': 40, 'Inkjet Printer[20W]': 20, 'Inkjet Printer-1[30W]': 30, 'Inverter Air conditioner[1500W]': 1500, 'Iron[1000W]': 1000, 'Jacuzzi[3000W]': 3000, 'Jacuzzi-1[4500W]': 4500, 'Jacuzzi-2[7500W]': 7500, 'Kitchen Extractor Fan[200W]': 200, 'Laptop Computer[50W]': 50, 'Laptop Computer-1[75W]': 75, 'Laptop Computer-2[100W]': 100, 'Laser Printer[750W]': 750, 'LED Christmas Lights[5W]': 5, 'LED Light Bulb[7W]': 7, 'LED Light Bulb-1[10W]': 10, 'Oven[2150W]': 2150, 'Paper Shredder[200W]': 200, 'Pedestal Fan[60W]': 60, 'Phone Charger[4W]': 4, 'Phone Charger-1[7W]': 7, 'Playstation 4[90W]': 90, 'Playstation 5[200W]': 200, 'Portable Air Conditioner[1200W]': 1200, 'Projector[270W]': 270, 'Refrigerator[200W]': 200, 'Scanner[15W]': 15, 'Sewing Machine[80W]': 80, 'Singer Sewing Machine[100W]': 100, 'Steam Iron[2500W]': 2500, 'Table Fan[10W]': 10, 'Table Fan-1[20W]': 20, 'Table Fan-2[25W]': 25, 'Tablet Charger[15W]': 15, 'laptop[60W]': 60,'Bulb[100W]': 100}

v=[]
battery_ah = tuple(range(100, 10001, 100))
menu=[
    ["&Export",["&CSV","&Text",]],
    ["&About",["&About", ]],
    ["!&Help",["!&Tutorial",]],
    ["&Settings", ["&Load", ["Normal", "Extended"], ["&Theme", [themes ]]]]
    ]
    
header=[
    [psg.Menu(menu, key="menu_key")],
    [psg.Text("Solar PV Simulator", size=(200, 1), font="Helvetica 40", justification="center")],
    ]

#+[[psg.OptionMenu(solar_type, default_value=solar_type[0], size=(30,2), key="s_type", pad=pad)],]


battery_text=[[psg.Text(text, font=font, pad=pad, size=size)]
          for text in (
              "Backup Period(hours):",
              "Available battery(Ah)",
              "Battery Nominal Voltage:",
              "Required Battery Size(Ah):",
              "Battery no:",
                      )
          ]

battery_input=[
    [psg.Combo(list(range(3,73,3)), default_value=3, key="no_of_hours", font=font, pad=pad)],
    [psg.Input(100,  key="battery_ah", font=font, pad=pad, size=size)],
    [psg.Radio(f"{rad}-Volts", default=(True if rad==24 else False), enable_events=True, key=f"{rad}v"
                , group_id="battery_voltage", font=font, pad=pad) for rad in (12, 24, 48)],
     
    [psg.Input(0,  key="battery_capacity", font=font, pad=pad, size=size)],
    ]+[
        [psg.Input(0,  key=input, font=font, readonly=True, pad=pad, size=size)]
           for input in (
               "battery_no",
               )
    ]


pv_text=[[psg.Text(text, font=font, pad=pad, size=size)]
          for text in (
              "Panel Voltage(V):",
              "Available PV Size(Wp):",
              "PV Energy Demand(Watt-hr/day):",
              "PV Capacity(Wp):",
              "Module no:",
              "Current(SC):",
              "Config:"
                      )
          ]

pv_input=[[psg.Radio(f"{rad}-Volts", default=(True if rad==12 else False), enable_events=True, key=f"panel_{rad}v"
                , group_id="panel_voltage", font=font, pad=pad) for rad in (12, 24)],]+[
        [psg.Input(110 if input=="available_module" else 8 if input=="short_circuit_current" else "Series" if input=="panel_config" else 0,  key=input, font=font, readonly=True, pad=pad, size=size)]
          for input in (
              "available_module",
                  "pv_energy_demand",
                  "pv_capacity",
                  "pv_count",
                  "short_circuit_current",
                  "panel_config"
                      )
          ]

misc_text=[[psg.Text(text, font=font, pad=pad, size=size)]
          for text in (
              "Charge Controller:",
              "Inverter/UPS Rating(Watt):",
              "Charge Controller Size:",
              "charging Current(A):",
              "charging Time(Pb-Acid-Hr):"
              
                      )
          ]

misc_input=[
    [psg.Combo(("PWM", "MPPT"), default_value="PWM",
               key="charge_controller_type", font=font, pad=pad, readonly=True if input in ("charging_current",) else False)],
    ]+[
        [psg.Input(0,  key=input, font=font, readonly=True, pad=pad, size=size)]
        for input in (
                      "inverter_size",
                      "charge_controller",
                      "charging_current",
                      "charging_time",
                      )
    ]


col_11=[[psg.Column(battery_text), psg.Column(battery_input)],]
col_12=[[psg.Column(pv_text), psg.Column(pv_input)],]
col_13=[[psg.Column(misc_text), psg.Column(misc_input)],]


col_01=[
    [psg.Text("Available Load")],
    [psg.LBox(tuple(device_list.keys()),
              size=(28,12),
              select_mode = psg.LISTBOX_SELECT_MODE_MULTIPLE,
             enable_events=True,
              key="utility",
              font=font
              ),
     ],
     [psg.Text("KWH(Watt-hrs/day):", font=font, pad=pad, size=(27, 1),),]
    ]


col_02=[
     [psg.Text("Selected Load")],
     [psg.LBox(v, size=(28,12), key="utility_to", font=font)],
     [psg.Input(0,  key="kwh", font=font, readonly=True, pad=pad, size=(27,1))]
    ]

col_10=[
    [psg.Column(col_01),
    psg.Button(">>>",  key="send"),
     psg.Column(col_02)],
    ]

col_1=[
    [psg.Frame("PV Module", col_12, font=("Helvetica", 18))],
    [psg.Frame("Misc", col_13, font=("Helvetica", 18))],
    ]

col_0=[[psg.Frame("Load Parameters", col_10, font=("Helvetica", 18))],
       [psg.Frame("Battery", col_11, font=("Helvetica", 18))],
       ]
layout=[
    [psg.Column(layout=header)],
    [psg.Column( col_0, pad=pad),
     psg.Column(col_1, vertical_alignment="top", pad=pad, element_justification="center")],   
    
    ]

win = psg.Window("Solar PV Simulator", layout=layout, finalize=True, icon=icon)
WHR=0
TEXT=""
WATT=0
win.maximize()
while True:
    v=[]
    btn, entry=win.Read(3000)
    try:
        kwh=float(entry['kwh'])*1000
        utility_from=entry["utility"]
        battery_voltage = 24 if entry["24v"] else 12 if entry["12v"] else 48 if entry["48v"] else 0
        panel_voltage = 24 if entry["panel_24v"] else 12
        avalable_module=int(entry["available_module"]) 

    except TypeError:
        psg.PopupError("Critical Error:Something Went Wrong\nYour SPV-SIM is will shut down!", icon=icon)
        sys.exit()
        win.close()
    except:
        kwh=0
        utility_from=[]
        battery_voltage = 24
        panel_voltage = 12
        avalable_module=110
        
    if len(utility_from)>0 and btn == 'send':
        win.FindElement("utility_to")(utility_from)
        for u_f in utility_from:
            units=psg.popup_get_text(f"How many {u_f}",
                                   title=u_f, default_text=2, icon=icon)
            whr=psg.popup_get_text(f"{u_f}- is expected to run for how many hours",
                                   title=u_f, default_text=6)
            WHR += device_list[u_f]*int(whr)*int(units)#*1.3
            win.find_element("kwh")(f"{WHR/1000}")
        WATT=sum(map(lambda d:device_list[d], utility_from))
            
    elif btn=="Text":
        text="Parameters, Value\n"
        for t in entry:
            text+=f"{t.replace('_', ' ').upper()}, {entry[t]}\n"
        create_text(text=text)

    elif btn=="CSV":
        text=f"KWH/day: {WHR}\n"
        for t in entry:
            text+=f"{t.replace('_', ' ').upper()}: {entry[t]}\n"
        create_csv(text=text)

    elif btn=="About":
        psg.PopupOK(version, no_titlebar=True, icon=icon)

    elif btn in themes:
        if change_settings("feel", btn):
            psg.PopupAutoClose("App will restart to effect theme changes", icon=icon)
            win.close()
            
    elif btn in ["Normal", "Extended"]:
        if load("load_type", btn):
            if  btn=="Normal":
                device_list = device_list
            elif btn=="Extended":
                device_list = device_listx
            win.find_element("utility")(device_list)

    elif btn=='kwh':
        WHR=int(entry['kwh'])*1000

    elif entry['charge_controller_type']=='MPPT':
        psg.PopupOK("This Operation is disabled", icon=icon)
        
        
    else:
        win.find_element("battery_capacity")(f"{round((kwh*int(entry['no_of_hours']))/(0.51*battery_voltage if battery_voltage else 0),2)}")
        win.find_element("kwh")(f"{WHR/1000}")
        win.find_element("inverter_size")(f"{WATT*1.3}")
        win.find_element("charge_controller")(f"{float(entry['short_circuit_current'])*panel_voltage*1.25}")
        win.find_element("battery_capacity")(f"{round((kwh*int(entry['no_of_hours']))/(0.51*battery_voltage), 2)}")
        win.find_element("pv_energy_demand")(f"{round(kwh*1.3, 2)}")
        win.find_element("battery_no")(f"{math.ceil(kwh/(float(entry['battery_ah'])*battery_voltage))}")
        win.find_element("pv_capacity")(f"{round((kwh*1.3)/pgf, 2)}")
        win.find_element("pv_count")(f"{math.ceil((kwh*1.3)/(pgf*avalable_module))}")
        win.find_element("charging_current")(f"{float(entry['battery_capacity'])/10}")
        win.find_element("charging_time")(f"{(float(entry['battery_capacity'])*1.4)/float(entry['charging_current'])}"
                                          if float(entry['charging_current'])>0 else 0)
        win.find_element("panel_config")(
            "Series" if battery_voltage>panel_voltage else 'parallel' if battery_voltage==panel_voltage else psg.PopupOK("Invalid OPeration"))
        feel=settings['feel']
        color
psg.PopupError("Critical Error:Something Went Wrong\nYour SPV-SIM is will shut down!", icon=icon)
sys.exit()
win.close()

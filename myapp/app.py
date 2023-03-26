
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import itertools
import sys
import os 
#cwd = os.getcwd()
#print("CWD",cwd)
#print(sys.path)
#sys.path.append(cwd)
#print(sys.path)
from py3dbp import Packer, Bin, Item, Painter
import time
start = time.time()
import redishUtils as re
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shiny import App, reactive, render, ui
from asyncio import sleep

# TODO: Export Config, Import Config
# TODO: remove item from packing list table
# TODO: epose Truck selection?

# Hardcode trucks for starters.
TwentyFootTruckHalf = [(41, 202, 60), 'TwentyFootTruckHalf']
TwentyFootTowerTruckHalf = [(41, 202, 71), 'TwentyFootTruckHalf']
TwentyFootTruck = [(82, 202, 71), 'TwentyFootTruck']

dfItemDefn = pd.read_csv(Path(__file__).parent / "itemDefinitions.csv")
dfItemDefnList = dfItemDefn.values.tolist()

df = pd.read_csv(Path(__file__).parent / "packlist.csv")
# look up item number from item df, add item friendly name.
df['Name'] = ""
df['Color'] = ""
for index, row in df.iterrows():
    tmp = row["item"]
    df.loc[index, "Name"] = dfItemDefn.loc[tmp,"Name"]
    df.loc[index, "Color"] = dfItemDefn.loc[tmp,"Color"]

dflist = df.values.tolist()

choices_names = list(map(lambda x: (x[4]), dfItemDefnList))

result_string = ""

# app_ui = ui.page_fluid(
#     ui.row(
#     ui.column(3, 
#         ui.panel_title("Edit Items"),
#         ui.input_numeric("stopnum", "Stop", value=1, min=1, max=20),
#         ui.input_text("Customer","Customer Name", value="cust1"),
#         ui.input_select("itemselect", "Item", choices_names),
#         ui.input_numeric("numitems", "Number", value=10),
#         ui.output_text_verbatim("sel"),
#         ui.p(ui.input_action_button("addItemToStop", "Add Item to Stop")),
#         ui.p(ui.input_action_button("resetme", "Reset list")),
#         ),
#     ui.column(3,
#         ui.panel_title("Pack List"),
#         ui.output_table("packlist"),
#         ),
#     ui.column(3,
#         ui.panel_title("Result"),
#         ui.output_plot("plot"),
#         ui.output_text_verbatim("outtxt"),
#         )
#     )
# )
app_ui = ui.page_fluid(
    ui.panel_title("Does it fit?"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_numeric("stopnum", "Stop", value=1, min=1, max=20),
            ui.input_text("Customer","Customer Name", value="cust1"),
            ui.input_select("itemselect", "Item", choices_names),
            ui.input_numeric("numitems", "Number", value=10),
            ui.output_text_verbatim("sel"),
            ui.p(ui.input_action_button("addItemToStop", "Add Item to Stop")),
            ui.p(ui.input_action_button("resetme", "Reset list")),
            #ui.input_file("file1", "Upload Config File", multiple=False),
            #ui.download_button("download", "Download Config File"),
        ),
        ui.panel_main(
            #ui.p(ui.input_action_button("calculate", "Recalculate Fit")),
            ui.output_plot("plot"),
            ui.output_text_verbatim("outtxt"),
            ui.output_table("packlist"),
            ui.output_text_verbatim("compute"),
        ),
    ),
)

def server(input, output, session):
    reactive_item_list = reactive.Value(dflist)
    reactive_output_text = reactive.Value(result_string)

    @output
    @render.text
    def sel():
        return f"Add {input.numitems()} of {input.itemselect()} to Stop {input.Stopnum()} for {input.Customer()}"
    
    @output
    @render.table
    def packlist():
        df = pd.DataFrame(reactive_item_list(),
                          columns = ['Stop','item','Count','Customer','Name','Color'])
        df = df.drop(columns=('item'))
        df = df.sort_values(by=['Stop'])
        return df
    
    @reactive.Effect
    @reactive.event(input.addItemToStop)
    def add_Item_To_Stop():
        theItemNum = dfItemDefn.loc[dfItemDefn['Name'] == input.itemselect(),'item'].item()
        theItemColor = dfItemDefn.loc[dfItemDefn['Name'] == input.itemselect(),'Color'].item()
        reactive_item_list.set(reactive_item_list() + 
                [[input.stopnum(),theItemNum,input.numitems(),input.Customer(),input.itemselect(),theItemColor]])

    @reactive.Effect
    @reactive.event(input.resetme)
    def resetTheList():
        reactive_item_list.set([])

    @output
    @render.plot(alt="A histogram")
    def plot() -> object:
        #input.calculate()
        # initialize the session
        packer = Packer()
        # add the truck
        re.addTruck(packer, TwentyFootTruckHalf)
        # loop through items list and add each
        df = pd.DataFrame(reactive_item_list(),
                          columns = ['Stop','item','Count','Customer','Name','Color'])
        #print(df)
        for index, row in df.iterrows():
            itemnum = row["item"]
            #print(itemnum)
            item = dfItemDefn.iloc[itemnum] # item,W,D,H,Name,renderColor
            xlist = list([(item["W"].item(),item["D"].item(),item["H"].item()), item["Name"],item["Color"]])
            re.addTotes(packer, xlist, df.loc[index,"Count"].item(), df.loc[index,"Stop"].item())
        painter, retstr = re.packAndPrintResults(packer)
        reactive_output_text.set(retstr)
        fig = painter.returnPlotAndItems()
        return fig
    
    @output
    @render.text
    def outtxt():
        return reactive_output_text()

    @output
    @render.text
    @reactive.event(input.addItemToStop)
    async def compute():
        with ui.Progress(min=1, max=15) as p:
            p.set(message="Calculation in progress", detail="This may take a while...")

            for i in range(1, 15):
                p.set(i, message="Computing")
                await sleep(0.1)

        return ""
    
app = App(app_ui, server)

import PySimpleGUI as sg
from novel_downloader import get_novel
import types


sg.theme('DarkAmber')   



layout = [  [sg.Text('URL') ,sg.InputText()],
            [sg.Text('Title'), sg.InputText()],
            [sg.Text("folder"),sg.InputText(),sg.FolderBrowse()],
            [sg.Multiline(key="-LOG-",size=(80,20),default_text="\n")],
            [sg.Button("start"),sg.Button("exit")] 
            ]

window = sg.Window('novel downloader', layout)
sg.cprint_set_output_destination(window,"-LOG-")
worker:types.GeneratorType = None
while True:
    event, values = window.read(500)
    if event == sg.WIN_CLOSED or event == 'exit': 
        break
    elif event == "start":
        url = values[0]
        title = values[1]
        folder = values[2]
        worker = get_novel(url,title,folder)
    if worker and  isinstance(worker, types.GeneratorType):
        res  = next(worker)
        if res :
            sg.cprint(f"getting chapter: {res}")
        else :    
            next(worker)
            worker=None
            sg.cprint("creating book ...")


window.close()
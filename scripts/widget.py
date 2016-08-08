import ipywidgets as widgets
from IPython.display import display



def text_field():
    text = widgets.Text()
    display(text)
    
    def handle_submit(sender):
        print(text.value)
        
    text.on_submit(handle_submit)
    return text
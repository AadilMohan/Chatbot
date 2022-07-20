#Creating GUI with tkinter
import tkinter
#import link_GUI_decision_engine

import LUIS_link_chatbot_GUI

from tkinter import *
import pandas as pd

class GUI_class():

        def _create_csv():
            list_headers = ['Count_send','objective','age','risk_profile','is_Emergency_corpus','income','saving','amount', 'time_horizon' ,'payment_mode','bond','equity','gold','commodity']
            df_data = [[0, 'text',0, 'text', False, 0, 0, 0, 0, 'text',0,0,0,0]]
            df = pd.DataFrame(df_data,columns=list_headers)
            df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)




        def send():
            msg = GUI_class.EntryBox.get("1.0",'end-1c').strip()
            GUI_class.EntryBox.delete("0.0",END)

            if msg != '':
                GUI_class.ChatLog.config(state=NORMAL)
                GUI_class.ChatLog.insert(END, "You: " + msg + '\n\n')
                GUI_class.ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

                res = LUIS_link_chatbot_GUI.chat_terminal_link(msg)
                GUI_class.ChatLog.insert(END, "Bot: " + res + '\n\n')

                GUI_class.ChatLog.config(state=DISABLED)
                GUI_class.ChatLog.yview(END)


        base = Tk()
        base.title("Money Manager")
        base.geometry("400x500")
        base.resizable(width=TRUE, height=TRUE)

        #Create Chat window

        ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial")

        ChatLog.config(state=DISABLED)

        #Bind scrollbar to Chat window
        scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
        ChatLog['yscrollcommand'] = scrollbar.set

        #Create Button to send message
        SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                            bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                            command= send )

        #Create the box to enter message
        EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
        #EntryBox.bind("<Return>", send)


        #Place all components on the screen
        scrollbar.place(x=376, y=6, height=386)
        ChatLog.place(x=6, y=6, height=386, width=370)
        EntryBox.place(x=128, y=401, height=90, width=265)
        SendButton.place(x=6, y=401, height=90)
if __name__ == '__main__':
    GUI_obj = GUI_class()
    GUI_class._create_csv()
    GUI_class.base.mainloop()




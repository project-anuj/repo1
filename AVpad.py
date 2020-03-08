import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import os

main_application = tk.Tk()
main_application.geometry('1200x400')
main_application.title('AVpad Text Editor')

###################  main menu functionality  ##################


#---variable---
url =''
changed=False

#---------------------------file functionality----------------------------------
#---new functionality---
def new_file(event=None):
    global url
    url=''
    text_editor.delete(1.0,'end')

#--- open functionality---
def open_file(event=None):
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd(),title="Select File",filetypes=(('Text File','*.txt'),('All files','*.*')))
    try:
        with open(url,'r') as fr:
            text_editor.delete(1.0,'end')
            text_editor.insert(1.0,fr.read())
    except FileNotFoundError:
        return
    except:
        return
    main_application.title(os.path.basename(url))

#----------save functionality---------------------
def save(event=None):
    global url
    try:
        if url:
            content = str(text_editor.get(1.0,'end'))
            with open(url,'w',encoding='utf-8') as fw:
                fw.write(content)
                fw.close()
        else:
            content = text_editor.get(1.0,'end')
            url = filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','*.txt'),('All Files','*.*')))
            url.write(content)
            url.close()
    except:
        return
#---------save as functionality------------------------
def save_as(event=None):
    global url
    try:

        content = str(text_editor.get(1.0,'end'))
        url = filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','*.txt'),('All Files','*.*')))
        url.write(content)
        url.close()
    except:
        return

#-----------------exit functionality---------------------
def exit_file(event=None):
    try:
        if changed:
            mbox = messagebox.askyesnocancel('Warning','Do you want to save this file ?')
            if mbox is True:
                save()
                main_application.destroy()
            elif mbox is False:
                main_application.destroy()
        else:
            main_application.destroy()
    except:
        return
#-------------------------------------End file functionality-------------------------------------

#-----------------------------------Edit functionality--------------------------------------------
find_input=''
replace_input=''
def find(event=None):
    global find_input,replace_input
    word = find_input.get()
    text_editor.tag_remove('match','1.0',tk.END)
    if word:
        start_pos = '1.0'
        while True:
            start_pos = text_editor.search(word, start_pos,stopindex=tk.END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos,len(word))
            text_editor.tag_add('match',start_pos,end_pos)
            start_pos= end_pos
            text_editor.tag_config('match', foreground='red',background='yellow')

def replace():
    global find_input,replace_input
    word = find_input.get()
    replace_text = replace_input.get()
    content = text_editor.get(1.0,'end')
    new_content = content.replace(word,replace_text)
    text_editor.delete(1.0,'end')
    text_editor.insert(1.0,new_content)

def find_func(event=None):
    global find_input,replace_input

    find_dialogue = tk.Toplevel()
    find_dialogue.geometry('350x150+500+200')
    find_dialogue.title('Find')
    find_dialogue.resizable(0,0)
    

    find_frame = ttk.LabelFrame(find_dialogue,text='Find/Replace')
    find_frame.pack(pady=20)

    text_find_label = ttk.Label(find_frame,text='Find :')
    text_replace_label = ttk.Label(find_frame,text='Replace :')
    text_find_label.grid(row=0,column=0, padx=4, pady=4)
    text_replace_label.grid(row=1,column=0, padx=4, pady=4)

    
    find_input = ttk.Entry(find_frame,width=30)
    replace_input = ttk.Entry(find_frame,width=30)
    find_input.grid(row=0,column=1, padx=4,pady =4)
    replace_input.grid(row=1,column=1, padx=4,pady =4)

    find_button = ttk.Button(find_frame,text='Find',command=find)
    replace_button = ttk.Button(find_frame,text='Replace',command=replace)
    find_button.grid(row=2,column=0,padx=8,pady=4)
    replace_button.grid(row=2,column=1,padx=8,pady=4)

    find_dialogue.mainloop()
#--------------------------------End Edit functionality-------------------------------------------
#---------------  End main menu functionality  -----------------

#########################  main menu  ##########################
main_menu = tk.Menu()

#--  file  --

file = tk.Menu(main_menu, tearoff= False)
file.add_command(label='New',accelerator='Ctrl+N',command=new_file)
file.add_command(label='Open',accelerator='Ctrl+O',command=open_file)
file.add_command(label='Save',accelerator='Ctrl+S',command=save)
file.add_command(label='Save As..',accelerator='Ctrl+Alt+S',command=save_as)
file.add_command(label='Exit',accelerator='Ctrl+X',command=exit_file)

#--  edit  --

edit = tk.Menu(main_menu, tearoff= False)
edit.add_command(label='Copy',accelerator='Ctrl+C',command=lambda:text_editor.event_generate("<Control c>") )
edit.add_command(label='Paste',accelerator='Ctrl+V',command=lambda:text_editor.event_generate("<Control v>"))
edit.add_command(label='Cut',accelerator='Ctrl+X',command=lambda:text_editor.event_generate("<Control x>"))
edit.add_command(label='Clear All',accelerator='Ctrl+Alt+X',command=lambda:text_editor.delete(1.0,'end'))
edit.add_command(label='Find',accelerator='Ctrl+F',command=find_func)

#-- view --
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar = False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP,fill=tk.X)
        text_editor.pack(fill=tk.BOTH, expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar=True
def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar = False
    else:
        status_bar.pack()
        show_statusbar=True
view = tk.Menu(main_menu, tearoff= False)
view.add_checkbutton(label='Tool Bar',variable=show_toolbar,command=hide_toolbar)
view.add_checkbutton(label='Status Bar',variable=show_statusbar,command=hide_statusbar)

#-- color theme --

color_theme = tk.Menu(main_menu, tearoff= False)

color_dict={
    'Light Default' : ('#000000','#ffffff'),
    'Light Plus': ('#474747','#e0e0e0'),
    'Dark': ('#c4c4c4','#2d2d2d'),
    'Red' : ('#2d2d2d','#ffe8e8'),
    'Monokai' : ('#d3b774','#474747'),
    'Night Blue' : ('#ededed','#6b9dc2')
}
themechoice = tk.StringVar()
def change_theme():
    chosen_theme = themechoice.get()
    color_tuple = color_dict.get(chosen_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    text_editor.config(background=bg_color,foreground=fg_color)

for i in color_dict:
    color_theme.add_radiobutton(label = i,variable = themechoice,command=change_theme)


    
# cascade
main_menu.add_cascade(label='File',menu=file)
main_menu.add_cascade(label='Edit',menu=edit)
main_menu.add_cascade(label='View',menu=view)
main_menu.add_cascade(label='Color Theme',menu=color_theme)

#-----------------------  End main menu  -----------------------

#########################  tool bar  ###########################
tool_bar = ttk.Label(main_application)
tool_bar.pack(side=tk.TOP, fill=tk.X)

#---  font  ---
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar, width=30, textvariable=font_family,state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0,column=0, padx=5)

#---  font size  ---
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar,width =14, textvariable = size_var, state='readonly')
font_size['values'] = tuple(range(8,80,2))
font_size.current(2)
font_size.grid(row=0,column=1,padx=5) 

#---  bold button  --
bold_icon = tk.PhotoImage(file='C:\\Users\sai baba\Downloads\\bold.png')
bold_btn = ttk.Button(tool_bar, image=bold_icon)
bold_btn.grid(row=0,column = 3,padx=5)

#---  italic button  --
italic_icon = tk.PhotoImage(file='C:\\Users\sai baba\Downloads\\italics.png')
italic_btn = ttk.Button(tool_bar, image=italic_icon)
italic_btn.grid(row=0,column = 4,padx=5)

#---  underline button  --
underline_icon = tk.PhotoImage(file='C:\\Users\sai baba\Downloads\\underline.png')
underline_btn = ttk.Button(tool_bar, image=underline_icon)
underline_btn.grid(row=0,column = 5,padx=5)

#---  color button  --
color_icon = tk.PhotoImage(file='C:\\Users\sai baba\Downloads\\text.png')
color_btn = ttk.Button(tool_bar, image=color_icon)
color_btn.grid(row=0,column = 6,padx=5) 

#---  align left  --
left_icon = tk.PhotoImage(file='C:\\Users\sai baba\Downloads\\left-text-alignment-option.png')
left_btn = ttk.Button(tool_bar, image=left_icon)
left_btn.grid(row=0,column = 7,padx=5) 

#---  align center  --
center_icon = tk.PhotoImage(file='C:\\Users\sai baba\Downloads\\center-text.png')
center_btn = ttk.Button(tool_bar, image=center_icon)
center_btn.grid(row=0,column = 8,padx=5) 

#---  align right  --
right_icon = tk.PhotoImage(file='C:\\Users\sai baba\Downloads\\right-text-alignment.png')
right_btn = ttk.Button(tool_bar, image=right_icon)
right_btn.grid(row=0,column = 9,padx=5) 

#------------------------  End tool bar  -----------------------

#########################  text editor  ########################
text_editor = tk.Text(main_application)
text_editor.config(wrap='word', relief=tk.FLAT)

scroll_bar = tk.Scrollbar(main_application)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)
text_editor.focus_set()
text_editor.pack(expand=True, fill='both')


#-------- font  functionality  -----------
current_font_family = 'Arial'
current_font_size = 12
text_editor.configure(font=(current_font_family,current_font_size))

def change_font(event=None):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.configure(font=(current_font_family,current_font_size))

def change_fontsize(event=None):
    global current_font_size
    current_font_size= font_size.get()
    text_editor.configure(font=(current_font_family,current_font_size))

font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_fontsize)


#-------------bold button----------
def change_bold():
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal':
        text_editor.configure(font=(current_font_family,current_font_size,'bold'))
    if text_property.actual()['weight'] == 'bold':
        text_editor.configure(font=(current_font_family,current_font_size,'normal'))

bold_btn.configure(command=change_bold)

#------------italic button------------
def change_italic():
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['slant'] == 'roman':
        text_editor.configure(font=(current_font_family,current_font_size,'italic'))
    if text_property.actual()['slant'] == 'italic':
        text_editor.configure(font=(current_font_family,current_font_size,'roman'))

italic_btn.configure(command = change_italic)

#-------------underline functionality----------------
def change_underline():
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['underline'] == 0:
        text_editor.configure(font=(current_font_family,current_font_size,'underline'))
    if text_property.actual()['underline'] == 1:
        text_editor.configure(font=(current_font_family,current_font_size,'normal'))

underline_btn.configure(command = change_underline)

#---------------color chooser functionality -------------
def change_color():
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

color_btn.configure(command=change_color)

#-------------alignment functionality---------------------
#----left----
def align_left():
    text_content = text_editor.get(1.0,tk.END)
    text_editor.tag_config('left', justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content, 'left')

left_btn.configure(command = align_left)

#----center----
def align_center():
    text_content = text_editor.get(1.0,'end')
    text_editor.tag_config('center', justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content, 'center')

center_btn.configure(command = align_center)

#----right----
def align_right():
    text_content = text_editor.get(1.0,'end')
    text_editor.tag_config('right', justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content, 'right')

right_btn.configure(command = align_right)
#------------------------  End text editor  -----------------------

#########################  main status bar  ####################

status_bar = ttk.Label(main_application,text = 'Status Bar')
status_bar.pack(side=tk.BOTTOM)

def change_editor(event=None):
    global changed
    if text_editor.edit_modified():
        changed=True
        words = len(text_editor.get(1.0,'end-1c').split())
        characters = len(text_editor.get(1.0,'end-1c').replace(' ',''))
        lines = text_editor.get(1.0,'end').count('\n')
        status_bar.config(text=f"Characters : {characters-lines+1}    Words : {words}   Lines : {lines}")
        text_editor.edit_modified(False)

text_editor.bind("<<Modified>>",change_editor)

#------------------------  End status bar  ---------------------


main_application.config(menu = main_menu)

def clear(event=None):
    text_editor.delete(1.0,'end')

# #-------short cut key--------
main_application.bind("<Control-n>",new_file)
main_application.bind("<Control-o>",open_file)
main_application.bind("<Control-s>",save)
main_application.bind("<Control-x>",exit_file)
main_application.bind("<Control-Alt-s>",save_as)
main_application.bind("<Control-Alt-x>",clear)
main_application.bind("<Control-f>",find_func)
main_application.mainloop()
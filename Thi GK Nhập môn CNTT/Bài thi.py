import warnings
warnings.filterwarnings("ignore")

import customtkinter as ctk
from PIL import Image, ImageTk, ImageEnhance
from tkinter import messagebox
import re

APP_WIDTH = 1000
APP_HEIGHT = 850 

n = 0
bishops = []

app = ctk.CTk() 
app.title("Safe Squares Solver")
app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
app.resizable(False, False)

try:
    app.iconbitmap("icon_app.ico")
except:
    pass

canvas = ctk.CTkCanvas(app, width=APP_WIDTH, height=APP_HEIGHT, highlightthickness=0)
canvas.pack(fill="both", expand=True)

bg_image_ref = None
entry_n = None
txt_coords = None

def set_background(is_dark=False):
    global bg_image_ref
    canvas.delete("all")
    try:

        pil_img = Image.open("background_app.png").resize((APP_WIDTH, APP_HEIGHT), Image.Resampling.LANCZOS)
        
        if is_dark:
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(0.3)
            
        bg_image_ref = ImageTk.PhotoImage(pil_img)
        canvas.create_image(0, 0, image=bg_image_ref, anchor="nw")
    except:
        color = "#1a1a1a" if is_dark else "#2b2b2b"
        canvas.configure(bg=color)

def create_outlined_text(canvas, x, y, text, font, text_color="white", outline_color="black", outline_width=2):

    for dx, dy in [(-outline_width, -outline_width), (-outline_width, outline_width),
                   (outline_width, -outline_width), (outline_width, outline_width),
                   (0, -outline_width), (0, outline_width), (-outline_width, 0), (outline_width, 0)]:
        canvas.create_text(x + dx, y + dy, text=text, fill=outline_color, font=font, justify="center")
    canvas.create_text(x, y, text=text, fill=text_color, font=font, justify="center")

def create_rounded_button_on_canvas(canvas, x, y, width, height, corner_radius, 
                                    text, text_font, command,
                                    fg_color, hover_color, border_color, border_width):
    x1, y1 = x - width / 2, y - height / 2
    x2, y2 = x + width / 2, y + height / 2
    r = corner_radius

    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r,
              x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2,
              x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    
    btn_bg = canvas.create_polygon(points, fill=fg_color, outline=border_color, width=border_width, smooth=True)
    btn_text = canvas.create_text(x, y, text=text, font=text_font, fill="white")
    
    btn_tag = f"custom_btn_{x}_{y}"
    canvas.addtag_withtag(btn_tag, btn_bg)
    canvas.addtag_withtag(btn_tag, btn_text)

    def on_enter(e):
        canvas.itemconfig(btn_bg, fill=hover_color)
        canvas.config(cursor="hand2") 
    def on_leave(e):
        canvas.itemconfig(btn_bg, fill=fg_color)
        canvas.config(cursor="")
        
    canvas.tag_bind(btn_tag, "<Enter>", on_enter)
    canvas.tag_bind(btn_tag, "<Leave>", on_leave)
    canvas.tag_bind(btn_tag, "<Button-1>", lambda e: command()) 

def setup_result_screen():
    set_background(is_dark=True)

    canvas.create_text(500, 40, text=f"RESULT (N={n}x{n})", fill="white", font=("Arial", 25, "bold"))

    diagonal1 = set() 
    diagonal2 = set() 

    for r, c in bishops:
        diagonal1.add(r - c)
        diagonal2.add(r + c)

    safe_squares = 0
    
    board_state = []
    
    for r in range(n):
        row_data = []
        for c in range(n):

            is_bishop_here = (r, c) in bishops 

            is_threatened = (r - c) in diagonal1 or (r + c) in diagonal2
            
            if not is_threatened and not is_bishop_here:
                safe_squares += 1
                status = "safe"
            else:
                status = "bishop" if is_bishop_here else "danger"
            
            row_data.append(status)
        board_state.append(row_data)

    avail_w = 900
    avail_h = 550
    
    raw_size = min(avail_w / n, avail_h / n)
    size = min(raw_size, 60) 
    size = max(size, 2)      
    
    board_pixel_w = n * size
    board_pixel_h = n * size
    start_x = (APP_WIDTH - board_pixel_w) / 2
    start_y = 100 + (avail_h - board_pixel_h) / 2

    draw_outline = "black" if size > 5 else "" 
    show_icon = True if size > 20 else False

    if n > 80:
          canvas.create_text(500, 400, text="Rendering large grid...", fill="yellow", font=("Arial", 20))
          app.update()

    if n <= 150:
        for r in range(n):
            cur_y = start_y + r * size
            for c in range(n):
                status = board_state[r][c]
                
                x1 = start_x + c * size
                x2 = x1 + size
                y2 = cur_y + size
                
                if status == "safe":

                    fill_color = "#eeeed2" if (r + c) % 2 == 0 else "#769656"
                elif status == "bishop":
                    fill_color = "#F0D9B5" 
                else:
                    fill_color = "#ff4d4d" 

                line_w = 1 if size > 5 else 0
                canvas.create_rectangle(x1, cur_y, x2, y2, fill=fill_color, outline=draw_outline, width=line_w)

                if status == "bishop":
                    if show_icon:
                        font_s = int(size * 0.7)
                        canvas.create_text(x1+size/2, cur_y+size/2, text="♛", fill="black", font=("Arial", font_s))
                    elif size > 4:
                        pad = size * 0.2
                        canvas.create_oval(x1+pad, cur_y+pad, x2-pad, y2-pad, fill="black")
    else:
        canvas.create_text(500, 400, text=f"Grid is too large to draw ({n}x{n})", fill="white", font=("Arial", 20))

    res_color = "#00FF00" if safe_squares > 0 else "red"
    canvas.create_text(500, 730, text=f"NUMBER OF SAFETY PARKING SPACES: {safe_squares}", fill=res_color, font=("Arial", 28, "bold"))

    canvas.create_text(500, 770, text=f"Order placed {len(bishops)} valid bishops", fill="gray", font=("Arial", 12, "italic"))

    btn_back = ctk.CTkButton(app, text="Return to data entry", command=setup_input_screen, fg_color="blue", height=40)
    canvas.create_window(500, 810, window=btn_back)

def process_input():
    global n, bishops

    try:
        n_txt = entry_n.get()
        if not n_txt:
            messagebox.showerror("Error", "Please enter size N!")
            return
        input_n = int(n_txt)
        if input_n <= 0: raise ValueError
        n = input_n
    except:
        messagebox.showerror("Error", "The size N must be a positive integer!")

    raw_text = txt_coords.get("1.0", "end").strip()
    valid_bishops = []

    numbers = re.findall(r'-?\d+', raw_text) 
    
    if len(numbers) % 2 != 0:
        messagebox.showerror("Input error", "Coordinates must be in pairs (Row, Column)!")
        return

    for i in range(0, len(numbers), 2):
        r = int(numbers[i])
        c = int(numbers[i+1])
        
        valid_bishops.append((r, c))

    bishops = valid_bishops
    setup_result_screen()

def setup_input_screen():
    set_background(is_dark=True)
    
    canvas.create_text(500, 60, text="DATA ENTRY", fill="white", font=("Arial", 28, "bold"))
    canvas.create_text(400, 140, text="Enter size N:", fill="white", font=("Arial", 16))
    global entry_n
    entry_n = ctk.CTkEntry(app, width=100, justify="center")
    entry_n.insert(0, "") 
    canvas.create_window(550, 140, window=entry_n)
    
    canvas.create_text(500, 220, text="Bishops Coordinates List:", fill="white", font=("Arial", 16, "bold"))
    canvas.create_text(500, 245, text="Example: Piece A (2,3). Enter 2 3. Add coordinates and press Enter to continue entering.", fill="yellow", font=("Arial", 13, "italic"))
    
    global txt_coords
    txt_coords = ctk.CTkTextbox(app, width=500, height=250, corner_radius=10, font=("Consolas", 14))

    default_text = ""
    txt_coords.insert("1.0", default_text)
    canvas.create_window(500, 380, window=txt_coords)

    btn_process = ctk.CTkButton(
        app, text="CALCULATE & DRAW",
        command=process_input,
        width=250, height=50,
        font=("Arial", 16, "bold"),
        fg_color="red", hover_color="#cc0000"
    )
    canvas.create_window(500, 580, window=btn_process)

def setup_main_screen():
    set_background(is_dark=False)
    
    create_outlined_text(
        canvas, 
        500, 100, 
        "Safe Squares Not Threatened by Bishops", 
        font=("Times New Roman", 30, "bold"), 
        text_color="white", 
        outline_color="black", 
        outline_width=2
    )
    
    create_rounded_button_on_canvas(
        canvas=canvas,
        x=500, y=250,            
        width=200, height=60,   
        corner_radius=30,       
        text="START",
        text_font=("Arial", 20, "bold"),
        command=setup_input_screen, 
        fg_color="green",        
        hover_color="#006400",  
        border_color="white",    
        border_width=3          
    )

if __name__ == "__main__":
    setup_main_screen()
    app.mainloop()
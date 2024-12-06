import mysql.connector
from PIL import Image, ImageDraw, ImageFont
import io
import webbrowser
import time
import pyautogui as auto
import os

def get_birthday_teachers():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="whatsapp_db"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT name, date_of_birth, time, photopath FROM data_of_birth WHERE MONTH(date_of_birth) = MONTH(CURDATE()) AND DAY(date_of_birth) = DAY(CURDATE())")
    rows = cursor.fetchall()
    connection.close()
    return rows

def create_birthday_card(template_path, name, photopath):
    """
    Create a birthday card with the teacher's photo and name.
    """
    template = Image.open(template_path)
    template_width, template_height = template.size
    
    teacher_photo = Image.open(photopath)
    teacher_photo = teacher_photo.resize((512, 520))
    
    # Paste the teacher's photo onto the template
    teacher_photo_x =57 # Center horizontally
    teacher_photo_y = 220  # Adjust vertical position
    template.paste(teacher_photo, (teacher_photo_x, teacher_photo_y))
    

    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("arial.ttf", 40)
    text_width, text_height = font.getbbox(name)[2:]

    text_x = teacher_photo_x + (teacher_photo.width - text_width) // 2  # Center the text below the photo
    text_y = teacher_photo_y + teacher_photo.height + 20

    draw.text((text_x, text_y), name, fill="black", font=font)
    

    output = io.BytesIO()
    template.save(output, format="PNG")
    output.seek(0)
    
    return output

def send_birthday_greetings(rows):
    """
    Fetch teachers, generate birthday cards, and send greetings.
    """
    template_path = "template.png"  
    
    for row in rows:
        name = row[0]
        photopath = row[3]
        
        
        card_image = create_birthday_card(template_path, name, photopath)
        
        message = f"🎉 Happy Birthday, {name}! 🎂"
        time.sleep(1)
        auto.press('enter')
        time.sleep(3)
        auto.write(message)
        auto.press('enter')
        time.sleep(2)
        

        output_directory = os.path.expanduser("C:/whatsapp/Downloads")
        os.makedirs(output_directory, exist_ok=True)

        output_path = os.path.join(output_directory, f"{name}_birthday_card.png")

        with open(output_path, "wb") as f:
            f.write(card_image.read())
            f.flush()

        if not os.path.exists(output_path):
            print(f"Error: The file {output_path} does not exist.")
        else:
            print(f"File saved successfully at {output_path}")

        time.sleep(2)  
        auto.click(x=614, y=914) 
        time.sleep(1)
        auto.click(x=654, y=656) 
        time.sleep(2)
        auto.write(os.path.abspath(output_path))  
        auto.press('enter') 
        time.sleep(6)
        auto.press('enter') 

        

def schedule_whatsapp_message(groupName, rows):
    webbrowser.open('https://web.whatsapp.com')
    time.sleep(10)
    auto.press('esc')
    time.sleep(1)
    auto.press('tab')
    time.sleep(1)
    auto.write(groupName)
    auto.press('enter')
    time.sleep(3)
    auto.moveTo(185, 181)
    auto.click()
    time.sleep(6)
    auto.write(groupName)
    auto.press('enter')
    auto.moveTo(728, 929)
    auto.click()


rows = get_birthday_teachers()
groupName = "Scheduler"
schedule_whatsapp_message(groupName, rows) 
send_birthday_greetings(rows)

time.sleep(5)

auto.hotkey('alt', 'f4')

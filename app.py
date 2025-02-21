import mysql.connector
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import webbrowser
import time
import pyautogui as auto
import os
from moviepy.editor import ImageSequenceClip, concatenate_videoclips, AudioFileClip
from itertools import groupby
import random

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

def create_birthday_card(template_paths, name, photopath):
    template = Image.open(template_paths)
    template_width, template_height = template.size

    if template_paths.endswith("template1.png"):
        teacher_photo = Image.open(photopath).resize((560, 580))
        teacher_photo_x, teacher_photo_y = 30, 180

    elif template_paths.endswith("template2.png"):
        teacher_photo = Image.open(photopath).resize((512, 530))
        teacher_photo_x, teacher_photo_y = 50, 190

    elif template_paths.endswith("template3.png"):
        teacher_photo = Image.open(photopath).resize((450, 450))
        teacher_photo_x = (template_width - teacher_photo.width) // 2  
        teacher_photo_y = 400

    elif template_paths.endswith("template4.png"):
        teacher_photo = Image.open(photopath).resize((400, 400))
        teacher_photo_x = (template_width - teacher_photo.width) // 2  
        teacher_photo_y = 360

    elif template_paths.endswith("template5.png"):
        teacher_photo = Image.open(photopath).resize((530, 560))
        teacher_photo_x = (template_width - teacher_photo.width) // 2  
        teacher_photo_y = 355

    elif template_paths.endswith("template6.png"):
        teacher_photo = Image.open(photopath).resize((700, 500))
        teacher_photo_x = (template_width - teacher_photo.width) // 2  
        teacher_photo_y = 550

    elif template_paths.endswith("template7.png"):
        teacher_photo = Image.open(photopath).resize((650, 520))
        teacher_photo_x, teacher_photo_y = 1090, 368

    elif template_paths.endswith("template8.png"):
        teacher_photo = Image.open(photopath).resize((530, 560))
        teacher_photo_x, teacher_photo_y = 1130, 400

    elif template_paths.endswith("template9.png"):
        teacher_photo = Image.open(photopath).resize((550, 590))
        teacher_photo_x = (template_width - teacher_photo.width) // 2  
        teacher_photo_y = 545

    elif template_paths.endswith("template10.png"):
        teacher_photo = Image.open(photopath).resize((770, 520))
        teacher_photo_x, teacher_photo_y = 1132, 468

    elif template_paths.endswith("template11.png"):
        teacher_photo = Image.open(photopath).resize((590, 600))
        teacher_photo_x, teacher_photo_y = 215, 320
    else:
        raise ValueError(f"Unknown template: {template_paths}")
    template.paste(teacher_photo, (teacher_photo_x, teacher_photo_y)) 

    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("arial.ttf", 40)
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = teacher_photo_x + (teacher_photo.width - text_width) // 2
    text_y = teacher_photo_y + teacher_photo.height + 20
    draw.text((text_x, text_y), name, fill="black", font=font)

    output = io.BytesIO()
    template.save(output, format="PNG")
    output.seek(0)
    
    return output

def create_birthday_video(image_paths, music_file):
    audio = AudioFileClip(music_file)
    audio_duration = audio.duration

    image_duration = audio_duration / len(image_paths)
    clips = []
    for i in image_paths:
        img_clip = ImageSequenceClip([i], fps=1)
        img_clip = img_clip.set_duration(image_duration)
        clips.append(img_clip)
    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_audio(audio)

    output_path = 'birthday_video.mp4'
    final_clip.write_videofile(output_path, codec='libx264')
    print(f"Video created successfully at {output_path}")
    
    return output_path

def send_birthday_greetings(rows):
    if not rows:
        return
    temp = [
        # r"C:\whatsapp\templates\template1.png",
        # r"C:\whatsapp\templates\template2.png",
        # r"C:\whatsapp\templates\template3.png",
        # r"C:\whatsapp\templates\template4.png",
        # r"C:\whatsapp\templates\template5.png",
        # r"C:\whatsapp\templates\template6.png",
        # r"C:\whatsapp\templates\template7.png",
        # r"C:\whatsapp\templates\template8.png",
        r"C:\whatsapp\templates\template9.png",
        # r"C:\whatsapp\templates\template10.png",
        # r"C:\whatsapp\templates\template11.png"
    ]
    rand_idx = random.randint(0, len(temp)-1)
    template_paths=temp[rand_idx]
    music_file = "Neenda-Neenda-Kaalam.mp3"
    
    rows_sorted = sorted(rows, key=lambda x: x[1])
    output_directory = os.path.expanduser("C:/whatsapp/Downloads")
    os.makedirs(output_directory, exist_ok=True)

    image_paths = []

    for (date), group in groupby(rows_sorted, key=lambda x: x[1]):
        group_list = list(group)

        template_index = len(image_paths) % len(template_paths)
        for row in group_list:
            name = row[0]
            photopath = row[3]
            
            card_image = create_birthday_card(template_paths, name, photopath)
            card_output_path = os.path.join(output_directory, f"{name}_birthday_card.png")
            with open(card_output_path, "wb") as f:
                f.write(card_image.read())
                f.flush()
            
            image_paths.append(card_output_path)

    message = f"🎉 Happy Birthday! 🎂"
    time.sleep(1)
    auto.press('enter')
    time.sleep(3)
    auto.write(message)
    auto.press('enter')
    time.sleep(2)
    video_path = create_birthday_video(image_paths, music_file)
    time.sleep(2)  
    auto.click(x=571, y=914)
    time.sleep(1)
    auto.click(x=675, y=649)
    time.sleep(2)
    auto.write(os.path.abspath(video_path))
    auto.press('enter') 
    time.sleep(6)
    auto.press('enter')
    for i in image_paths:
        if os.path.exists(i):
            os.remove(i)
    if os.path.exists("birthday_video.mp4"):
        with open("birthday_video.mp4", "wb") as f:
            pass 

def schedule_whatsapp_message(groupName):
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
schedule_whatsapp_message(groupName) 
send_birthday_greetings(rows)

time.sleep(10)
auto.hotkey('alt', 'f4')
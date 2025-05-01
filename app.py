import mysql.connector
from PIL import Image, ImageDraw, ImageFont
import io
import webbrowser
import time
import pyautogui as auto
import pyperclip
import os
from moviepy.editor import *
import random
import numpy as np

def get_birthday_teachers():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="whatsapp_db"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT name, phone_number, date_of_birth, photopath FROM data_of_birth WHERE MONTH(date_of_birth) = MONTH(CURDATE()) AND DAY(date_of_birth) = DAY(CURDATE())")
    rows = cursor.fetchall()
    connection.close()
    return rows

def create_birthday_card(template_paths, name, photopath):
    template = Image.open(template_paths)
    template_width, template_height = template.size

    if not os.path.exists(photopath):
        print(f"Photo not found: {photopath}")
        return None

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
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = teacher_photo_x + (teacher_photo.width - text_width) // 2
    text_y = teacher_photo_y + teacher_photo.height + 20
    draw.text((text_x, text_y), name, fill="black", font=font)

    output = io.BytesIO()
    template.save(output, format="PNG")
    output.seek(0)
    return output

def create_birthday_video(image_path, music_file, output_path):
    audio = AudioFileClip(music_file)
    image_clip = ImageSequenceClip([image_path], fps=1).set_duration(audio.duration)
    final_clip = image_clip.set_audio(audio)
    final_clip.write_videofile(output_path, codec='libx264')
    print(f"Video created successfully at {output_path}")
    return output_path

def create_text_image(text, width=1280, height=100, font_size=40, bg_color=(0, 0, 0, 0), text_color="white"):
    image = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), text, font=font, fill=text_color)
    return image

def add_confetti_with_chairman(base_video_path, confetti_path, chairman_img_path, final_output_path):
    base_video = VideoFileClip(base_video_path)
    confetti_clip = VideoFileClip(confetti_path).resize(base_video.size).subclip(0, 5)
    chairman_img = (ImageClip(chairman_img_path)
                    .set_duration(confetti_clip.duration)
                    .resize(height=500)
                    .set_position("center")
                    .fadein(1)
                    .fadeout(1))

    text_img1 = create_text_image("With best wishes from our Chairman", width=base_video.size[0])
    text_clip1 = (ImageClip(np.array(text_img1))
                 .set_duration(confetti_clip.duration)
                 .set_position(("center", base_video.size[1] - 180))
                 .fadein(1)
                 .fadeout(1))

    text_img2 = create_text_image("Wishing you a day filled with happiness and a year filled with joy!", width=base_video.size[0], font_size=35)
    text_clip2 = (ImageClip(np.array(text_img2))
                 .set_duration(confetti_clip.duration)
                 .set_position(("center", base_video.size[1] - 100))
                 .fadein(1)
                 .fadeout(1))

    chairman_scene = CompositeVideoClip([confetti_clip, chairman_img, text_clip1, text_clip2])
    final_video = concatenate_videoclips([base_video, chairman_scene])
    final_video.write_videofile(final_output_path, codec='libx264', fps=24)
    print(f"Final video created: {final_output_path}")

def send_to_phone_number(phone_number, message, video_path):
    url = f"https://wa.me/{phone_number}"
    print(f"Opening chat for {phone_number}")
    webbrowser.open(url)
    time.sleep(10)
    auto.press('enter')
    time.sleep(5)
    print(f"Sending message to {phone_number}")
    auto.write(message)
    auto.press('enter')
    time.sleep(2)
    print(f"Sending video to {phone_number}")
    try:
        attach_button = auto.locateCenterOnScreen('attach.png', confidence=0.9)
        auto.click(attach_button)
        time.sleep(3)
        button_location = auto.locateCenterOnScreen('photos_videos.png', confidence=0.8)
        if button_location is None:
            print("Photos & Videos button not found!")
        else:
            print(f"Found Photos & Videos button at: {button_location}")
            auto.moveTo(button_location)
            time.sleep(1)
            auto.click()
        auto.click()
        time.sleep(3)
        video_path_abs = os.path.abspath(video_path)
        pyperclip.copy(video_path_abs)
        time.sleep(1)
        auto.hotkey('ctrl', 'v')
        time.sleep(2)
        auto.press('enter')
        time.sleep(6)
        auto.press('enter')
        time.sleep(3)
    except Exception as e:
        print(f"Error during sending video: {e}")
    auto.hotkey('ctrl', 'w')
    time.sleep(3)

def send_birthday_greetings(rows):
    if not rows:
        return
    template_paths_list = [
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template1.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template2.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template3.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template4.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template5.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template6.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template7.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template8.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template9.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template10.png",
        r"C:\\Users\\keren\\OneDrive\\Desktop\\whatsapp\\templates\\template11.png",
    ]
    music_file = "Neenda-Neenda-Kaalam.mp3"
    output_directory = os.path.expanduser("C:/whatsapp/Downloads")
    os.makedirs(output_directory, exist_ok=True)
    for idx, row in enumerate(rows):
        name = row[0]
        phone_number = row[1]
        photopath = row[3]
        template_path = random.choice(template_paths_list)
        card_image = create_birthday_card(template_path, name, photopath)
        if card_image is None:
            continue
        card_output_path = os.path.join(output_directory, f"{name}_birthday_card.png")
        with open(card_output_path, "wb") as f:
            f.write(card_image.read())
            f.flush()
        raw_video_path = os.path.join(output_directory, f"{name}_birthday_video.mp4")
        final_video_path = os.path.join(output_directory, f"{name}_final_video.mp4")
        create_birthday_video(card_output_path, music_file, raw_video_path)
        add_confetti_with_chairman(
            base_video_path=raw_video_path,
            confetti_path="confetti.mp4",
            chairman_img_path="chairman.jpg",
            final_output_path=final_video_path
        )
        message = f"Happy Birthday {name}!"
        send_to_phone_number(phone_number, message, final_video_path)
        for path in [card_output_path, raw_video_path, final_video_path]:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    rows = get_birthday_teachers()
    send_birthday_greetings(rows)
    time.sleep(10)
    auto.hotkey('alt', 'f4')

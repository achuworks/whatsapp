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
from PIL import UnidentifiedImageError

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
    try:
        template = Image.open(template_paths)
        template_width, template_height = template.size

        print(f"Looking for photo at: {photopath}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Get base filename without extension
        base_name = os.path.splitext(os.path.basename(photopath))[0]
        
        # Try both .jpg and .png extensions
        possible_paths = []
        for ext in ['.jpg', '.png']:
            filename = base_name + ext
            possible_paths.extend([
                os.path.join(os.getcwd(), "photouploads", "Students", filename),
                os.path.join(os.getcwd(), "photouploads", "Faculty", filename),
                os.path.join(os.getcwd(), "photouploadsStudents", filename),
                os.path.join(os.getcwd(), "photouploadsFaculty", filename),
                os.path.join("photouploads", "Students", filename),
                os.path.join("photouploads", "Faculty", filename),
                os.path.join("photouploadsStudents", filename),
                os.path.join("photouploadsFaculty", filename),
                os.path.join(os.getcwd(), filename),
                filename
            ])
        
        found_photo = None
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with Image.open(path) as img:
                        img.verify()  # Verify image integrity
                    # If verification passes, open again for actual use
                    with Image.open(path) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        # Make a copy to ensure the image is fully loaded
                        img_copy = img.copy()
                    found_photo = path
                    print(f"Found valid photo at: {path}")
                    break
                except Exception as e:
                    print(f"Found file at {path} but it appears to be corrupted: {str(e)}")
                    continue
        
        if not found_photo:
            print(f"Photo not found or all photos corrupted in these locations: {possible_paths}")
            return None

        # Open and process the found photo
        try:
            teacher_photo = Image.open(found_photo)
            if teacher_photo.mode in ('RGBA', 'P'):
                teacher_photo = teacher_photo.convert('RGB')
                
            # Resize based on template with improved quality settings
            if template_paths.endswith("template1.png"):
                teacher_photo = teacher_photo.resize((560, 580), Image.Resampling.BICUBIC)
                teacher_photo_x, teacher_photo_y = 30, 180
            elif template_paths.endswith("template2.png"):
                teacher_photo = teacher_photo.resize((512, 530), Image.Resampling.BICUBIC)
                teacher_photo_x, teacher_photo_y = 50, 190
            elif template_paths.endswith("template3.png"):
                target_size = (450, 450)
                aspect_ratio = teacher_photo.width / teacher_photo.height
                if aspect_ratio > 1:
                    new_width = target_size[0]
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = target_size[1]
                    new_width = int(new_height * aspect_ratio)
                teacher_photo = teacher_photo.resize((new_width, new_height), Image.Resampling.BICUBIC)
                teacher_photo_x = (template_width - teacher_photo.width) // 2
                teacher_photo_y = 400
            elif template_paths.endswith("template4.png"):
                teacher_photo = teacher_photo.resize((400, 400), Image.Resampling.BICUBIC)
                teacher_photo_x = (template_width - teacher_photo.width) // 2
                teacher_photo_y = 360
            elif template_paths.endswith("template5.png"):
                teacher_photo = teacher_photo.resize((530, 560), Image.Resampling.BICUBIC)
                teacher_photo_x = (template_width - teacher_photo.width) // 2
                teacher_photo_y = 355
            elif template_paths.endswith("template6.png"):
                teacher_photo = teacher_photo.resize((700, 500), Image.Resampling.BICUBIC)
                teacher_photo_x = (template_width - teacher_photo.width) // 2
                teacher_photo_y = 550
            elif template_paths.endswith("template7.png"):
                teacher_photo = teacher_photo.resize((650, 520), Image.Resampling.BICUBIC)
                teacher_photo_x, teacher_photo_y = 1090, 368
            elif template_paths.endswith("template8.png"):
                teacher_photo = teacher_photo.resize((530, 560), Image.Resampling.BICUBIC)
                teacher_photo_x, teacher_photo_y = 1130, 400
            elif template_paths.endswith("template9.png"):
                teacher_photo = teacher_photo.resize((550, 590), Image.Resampling.BICUBIC)
                teacher_photo_x = (template_width - teacher_photo.width) // 2
                teacher_photo_y = 545
            elif template_paths.endswith("template10.png"):
                teacher_photo = teacher_photo.resize((770, 520), Image.Resampling.BICUBIC)
                teacher_photo_x, teacher_photo_y = 1132, 468
            elif template_paths.endswith("template11.png"):
                teacher_photo = teacher_photo.resize((590, 600), Image.Resampling.BICUBIC)
                teacher_photo_x, teacher_photo_y = 215, 320
            else:
                raise ValueError(f"Unknown template: {template_paths}")

            # Create a copy of the template to avoid modifying the original
            template_copy = template.copy()
            
            # Create a mask for smooth edges if needed
            mask = Image.new('L', teacher_photo.size, 255)
            
            # Paste the photo with the mask for smooth edges
            template_copy.paste(teacher_photo, (teacher_photo_x, teacher_photo_y), mask)
            
            # Add name with improved font rendering
            draw = ImageDraw.Draw(template_copy)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                font = ImageFont.load_default()
                
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = teacher_photo_x + (teacher_photo.width - text_width) // 2
            text_y = teacher_photo_y + teacher_photo.height + 20
            
            # Draw text with anti-aliasing
            draw.text((text_x, text_y), name, fill="black", font=font)

            # Save to BytesIO with high quality
            output = io.BytesIO()
            template_copy.save(output, format="PNG", quality=100)
            output.seek(0)
            return output
            
        except Exception as e:
            print(f"Error processing photo {found_photo}: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Error in create_birthday_card: {str(e)}")
        return None

def create_birthday_video(image_paths, music_file, output_path, duration_per_person):
    audio = AudioFileClip(music_file)
    total_duration = len(image_paths) * duration_per_person
    
    clips = []
    temp_files = []
    for idx, image_path in enumerate(image_paths):
        print(f"\nProcessing image {idx + 1}/{len(image_paths)}: {image_path}")
        try:
            print(f"Opening image: {image_path}")
            img = Image.open(image_path)
            print(f"Original format: {img.format}, Mode: {img.mode}, Size: {img.size}")
            
            # Convert to RGB first
            if img.mode != 'RGB':
                print(f"Converting {img.mode} to RGB")
                img = img.convert('RGB')
            
            # Ensure image is at least 1280x720
            if img.width < 1280 or img.height < 720:
                print(f"Resizing image from {img.size} to (1280, 720)")
                img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                temp_path = os.path.join(os.path.dirname(image_path), f"temp_resized_{idx}.png")
                print(f"Saving resized image to: {temp_path}")
                img.save(temp_path, format='PNG', quality=95)
                temp_files.append(temp_path)
                used_path = temp_path
            else:
                used_path = image_path
            
            print(f"Creating video clip from: {used_path}")
            clip = ImageClip(used_path).set_duration(duration_per_person)
            clips.append(clip)
            print(f"Successfully processed image {idx + 1}")
            
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            continue

    if not clips:
        print("No valid clips were created!")
        return None

    print("\nConcatenating clips...")
    final_clip = concatenate_videoclips(clips)
    
    print("Adding audio...")
    final_clip = final_clip.set_audio(audio.subclip(0, total_duration))
    
    print(f"Writing final video to: {output_path}")
    final_clip.write_videofile(output_path, codec='libx264', fps=24, bitrate="8000k")
    print("Video creation completed")

    print("\nCleaning up temporary files...")
    for temp_path in temp_files:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"Removed temporary file: {temp_path}")
    
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

def resize_with_lanczos(clip, newsize):
    from PIL import Image
    import numpy as np
    
    def resizer(pic):
        if isinstance(pic, np.ndarray):
            pilim = Image.fromarray(pic.astype('uint8'))
            resized_pil = pilim.resize(newsize[::-1], Image.Resampling.LANCZOS)
            return np.array(resized_pil)
        return pic
    
    return clip.fl_image(resizer)

def add_confetti_with_chairman(base_video_path, confetti_path, chairman_img_path, final_output_path):
    try:
        base_video = VideoFileClip(base_video_path)
        base_width, base_height = base_video.size
        
        confetti_clip = VideoFileClip(confetti_path)
        confetti_clip = resize_with_lanczos(confetti_clip, (base_width, base_height)).subclip(0, 5)
        
        chairman_img = ImageClip(chairman_img_path)
        chairman_img = chairman_img.set_duration(confetti_clip.duration)
        target_height = 500
        aspect_ratio = chairman_img.size[0] / chairman_img.size[1]
        target_width = int(target_height * aspect_ratio)
        chairman_img = resize_with_lanczos(chairman_img, (target_width, target_height))
        chairman_img = chairman_img.set_position(("center", "center")).fadein(1).fadeout(1)

        text_img1 = create_text_image("With best wishes from our Chairman", width=base_width)
        text_clip1 = (ImageClip(np.array(text_img1))
                     .set_duration(confetti_clip.duration)
                     .set_position(("center", base_height - 180))
                     .fadein(1)
                     .fadeout(1))

        text_img2 = create_text_image("Wishing you a day filled with happiness and a year filled with joy!", 
                                    width=base_width, font_size=35)
        text_clip2 = (ImageClip(np.array(text_img2))
                     .set_duration(confetti_clip.duration)
                     .set_position(("center", base_height - 100))
                     .fadein(1)
                     .fadeout(1))

        chairman_scene = CompositeVideoClip([confetti_clip, chairman_img, text_clip1, text_clip2], 
                                          size=(base_width, base_height))
        final_video = concatenate_videoclips([base_video, chairman_scene])
        
        try:
            final_video.write_videofile(final_output_path, 
                                      codec='libx264', 
                                      fps=24,
                                      threads=4,
                                      preset='ultrafast',
                                      ffmpeg_params=['-pix_fmt', 'yuv420p'])
            print(f"Final video created: {final_output_path}")
        except Exception as e:
            print(f"Error writing video file: {str(e)}")
            raise
    except Exception as e:
        print(f"Error in add_confetti_with_chairman: {str(e)}")
        raise
    finally:
        if 'base_video' in locals():
            base_video.close()
        if 'confetti_clip' in locals():
            confetti_clip.close()
        if 'final_video' in locals():
            final_video.close()

def send_to_whatsapp_group(group_name, video_path):
    # Open WhatsApp Web
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(30)  # Wait for WhatsApp Web to load
    
    try:
        # Click on search box
        auto.click(300, 200)  # Adjust these coordinates based on your screen
        time.sleep(2)
        
        # Type group name
        pyperclip.copy(group_name)
        auto.hotkey('ctrl', 'v')
        time.sleep(2)
        
        # Click on the group
        auto.click(274, 440)  # Adjust these coordinates based on your screen
        time.sleep(2)
        
        # Click attachment button
        auto.click(706, 967)  # Adjust these coordinates based on your screen
        time.sleep(2)
        
        # Click document button
        auto.click(683, 585)  # Adjust these coordinates based on your screen
        time.sleep(2)
        
        # Paste video path
        video_path_abs = os.path.abspath(video_path)
        pyperclip.copy(video_path_abs)
        time.sleep(1)
        auto.hotkey('ctrl', 'v')
        auto.press('enter')
        
        # Wait for upload and send
        time.sleep(8)
        auto.click(711, 956)
        time.sleep(5)
        auto.press('enter')
        time.sleep(10)
        
    except Exception as e:
        print(f"Error during sending video: {e}")
    finally:
        time.sleep(2)
        auto.hotkey('ctrl', 'w')

def create_combined_birthday_video(rows):
    if not rows:
        return
    
    # Define available templates
    template_dir = r"C:\Users\AchuAbu\Downloads\whatsapp\templates"
    template_files = [f"template{i}.png" for i in range(1, 12)]
    template_paths = [os.path.join(template_dir, template_file) for template_file in template_files]
    
    # Select a random template for the day
    selected_template = random.choice(template_paths)
    print(f"Selected template for today: {selected_template}")
    
    music_file = "Neenda-Neenda-Kaalam.mp3"
    output_directory = os.path.join(os.getcwd(), "output")
    os.makedirs(output_directory, exist_ok=True)
    
    # Get total song duration and calculate per-person duration
    audio = AudioFileClip(music_file)
    total_duration = audio.duration
    num_people = len(rows)
    duration_per_person = total_duration / num_people
    
    # Create individual birthday cards
    card_paths = []
    temp_files = []  # Keep track of temporary files
    
    for idx, row in enumerate(rows):
        name = row[0]
        photopath = row[3]
        
        print(f"\nProcessing birthday card for {name}")
        # Create birthday card using the same random template for all cards
        card_image = create_birthday_card(selected_template, name, photopath)
        if card_image is None:
            print(f"Failed to create birthday card for {name}")
            continue
            
        # Save BytesIO to a temporary file
        temp_path = os.path.join(output_directory, f"temp_card_{idx}.png")
        try:
            with open(temp_path, 'wb') as f:
                f.write(card_image.getvalue())
            print(f"Saved temporary card to: {temp_path}")
            card_paths.append(temp_path)
            temp_files.append(temp_path)  # Add to temp files list
        except Exception as e:
            print(f"Error saving temporary card for {name}: {str(e)}")
            continue
    
    if not card_paths:
        print("No valid birthday cards were created!")
        return
    
    print("\nCreating video from birthday cards...")
    # Create combined video with equal duration for each person
    raw_video_path = os.path.join(output_directory, "combined_birthday_video.mp4")
    final_video_path = os.path.join(output_directory, "final_combined_birthday_video.mp4")
    
    try:
        create_birthday_video(card_paths, music_file, raw_video_path, duration_per_person)
        
        # Add confetti and chairman's message
        add_confetti_with_chairman(
            base_video_path=raw_video_path,
            confetti_path="confetti.mp4",
            chairman_img_path="chairman.jpg",
            final_output_path=final_video_path
        )
        
        # Send to WhatsApp group
        send_to_whatsapp_group("Scheduler", final_video_path)
    except Exception as e:
        print(f"Error creating video: {str(e)}")
    finally:
        # Clean up all temporary files
        print("\nCleaning up temporary files...")
        for temp_path in temp_files:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    print(f"Removed temporary file: {temp_path}")
            except Exception as e:
                print(f"Error removing temporary file {temp_path}: {str(e)}")
        
        # Clean up intermediate video file
        if os.path.exists(raw_video_path):
            try:
                os.remove(raw_video_path)
                print("Removed intermediate video file")
            except Exception as e:
                print(f"Error removing intermediate video: {str(e)}")

if __name__ == "__main__":
    rows = get_birthday_teachers()
    create_combined_birthday_video(rows)
    time.sleep(10)
    auto.hotkey('alt', 'f4')
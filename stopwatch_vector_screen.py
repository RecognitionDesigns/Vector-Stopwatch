import anki_vector
from anki_vector.util import degrees
import time
from PIL import Image, ImageDraw, ImageFont
import sys

def make_text_image(text_to_draw, x, y, font=None):
    dimensions = (184, 96)
    text_image = Image.new('RGBA', dimensions, (0, 0, 0, 255))
    dc = ImageDraw.Draw(text_image)
    dc.text((x, y), text_to_draw, fill=(0, 255, 0, 255), font=font)
    return text_image

try:
    font_file = ImageFont.truetype("Arial.ttf", 30)
except IOError:
    try:
        font_file = ImageFont.truetype("Arial.ttf", 27)
    except IOError:
        pass

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60

    if mins == 0 and hours == 0:
        print("Time Lapsed = {:0.1f} seconds".format(sec))
        robot.behavior.say_text("{:0.1f} seconds have elapsed".format(sec))
        screen_1 = ("{:0.1f} seconds".format(sec))
        
    if mins == 1 and hours == 0:
        print("Time Lapsed = {:0.0f} minute and {:1.1f} seconds".format(int(mins),sec))
        robot.behavior.say_text("{:0.0f} minute and {:1.1f} seconds have elapsed".format(int(mins),sec))
        screen_1 = ("0{:0.0f}:{:1.1f}".format(int(mins),sec))
        
    if mins > 1 and hours == 0:
        print("Time Lapsed = {:0.0f} minutes and {:1.1f} seconds".format(int(mins),sec))
        robot.behavior.say_text("{:0.0f} minutes and {:1.1f} seconds have elapsed".format(int(mins),sec))
        screen_1 = ("{:0.0f}:{:1.1f}".format(int(mins),sec))

    if mins != 0 and hours != 0:
        print("Time Lapsed = {:0.0f} hours, {:1.0f} minutes and {:2.1f} seconds".format(int(hours),int(mins),sec))
        robot.behavior.say_text("{:0.0f} hours, {:0.0f} minutes and {:1.1f} seconds have elapsed".format(int(hours),int(mins),sec))
        screen_1 = ("{:0.0f}:{:0.0f}:{:1.1f}".format(int(hours),int(mins),sec))
        
    else:
        face_sum = (screen_1)
        text_to_draw = face_sum
        face_image = make_text_image(text_to_draw, 0, 25, font_file)

        print("Display image on Vector's face...")
        duration_s = 4.0
        screen_data = anki_vector.screen.convert_image_to_screen_data(face_image)
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(4)
        sys.exit()

with anki_vector.Robot() as robot:
    robot.behavior.say_text("Tap my back sensor to start the stop watch, tap it again to stop it")
    print("Ready!")
    
    while True:
        if (robot.touch.last_sensor_reading.is_being_touched):
            start_time = time.time()
            robot.behavior.set_eye_color(0.0, 1.0)
            robot.audio.stream_wav_file("Robot_blip.wav", 85)
            time.sleep(0.5)
            
            while True:
                if (robot.touch.last_sensor_reading.is_being_touched):
                    end_time = time.time()
                    robot.audio.stream_wav_file("Robot_blip.wav", 85)
                    robot.behavior.set_head_angle(degrees(30.0))
                    robot.behavior.set_lift_height(0.0)
                
                    time_lapsed = end_time - start_time
                    time_convert(time_lapsed)
            break

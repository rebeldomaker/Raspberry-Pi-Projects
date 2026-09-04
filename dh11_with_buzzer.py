import Adafruit_DHT
import RPi.GPIO as GPIO
import schedule
import time
from datetime import datetime

# Setup
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 7  # GPIO7 (physical pin 26)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO4 (physical pin 7)

# Define the frequency for the chimes
NOTE_G = 784   # G5
NOTE_C = 523   # C5
NOTE_D = 587   # D5
NOTE_E = 659   # E5

# Define the duration for each note
DURATION = 0.3   # Duration in seconds for each note

# Function to play a beep on the buzzer
def play_beep(frequency, duration):
    pwm = GPIO.PWM(BUZZER_PIN, frequency)
    pwm.start(50)  # 50% duty cycle
    time.sleep(duration)
    pwm.stop()
    time.sleep(0.05)  # Short pause between notes

# Function to play Westminster Chime
def play_westminster_chime():
    current_time = datetime.now().strftime("%H:%M")
    print(f"Playing Westminster Chime at {current_time}...")

    # First quarter
    play_beep(NOTE_G, DURATION)
    play_beep(NOTE_E, DURATION)
    play_beep(NOTE_D, DURATION)
    play_beep(NOTE_G, DURATION)

    time.sleep(1)  # Pause before the next quarter

    # Second quarter
    play_beep(NOTE_D, DURATION)
    play_beep(NOTE_C, DURATION)
    play_beep(NOTE_D, DURATION)
    play_beep(NOTE_G, DURATION)

    time.sleep(1)  # Pause before the next quarter

    # Third quarter
    play_beep(NOTE_E, DURATION)
    play_beep(NOTE_D, DURATION)
    play_beep(NOTE_E, DURATION)
    play_beep(NOTE_G, DURATION)

    time.sleep(1)  # Pause before the next quarter

    # Fourth quarter
    play_beep(NOTE_G, DURATION)
    play_beep(NOTE_E, DURATION)
    play_beep(NOTE_D, DURATION)
    play_beep(NOTE_G, DURATION)

    print("Chime Completed.")

# Function to check whether it is sleep time
def is_sleep_time():
    current_hour = datetime.now().hour
    # Assuming sleep time is from 22:00 to 07:00
    if current_hour >= 22 or current_hour < 7:
        return True
    return False

# Read Temperature
def read_temperature():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    current_time = datetime.now().strftime("%d %B %H:%M")
    if temperature is None:
        print(f"{current_time} - Temperature: Error")
    else:
        print(f"{current_time} - Temperature: {temperature}°C")
    return temperature

# Read Humidity
def read_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    current_time = datetime.now().strftime("%d %B %H:%M")
    if humidity is None:
        print(f"{current_time} - Humidity: Error")
    else:
        print(f"{current_time} - Humidity: {humidity}%")
    return humidity

# Function to play the hourly chime if not sleep time
def hourly_chime():
    if not is_sleep_time():
        play_westminster_chime()

# Function to play the morning alarm chime
def morning_alarm():
    if not is_sleep_time():
        print("Morning alarm triggered!")
        play_westminster_chime()

# Daily Runtime
def daily_runtime():
    current_time = datetime.now()
    runtime = current_time - start_time
    days = runtime.days
    print(f"This Raspberry Pi's been running for {days} Days.")

# Cleanup GPIO on exit
def stop_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

# Initialize start time
start_time = datetime.now()

# Scheduling tasks
schedule.every(20).minutes.do(read_temperature)
schedule.every(20).minutes.do(read_humidity)
schedule.every().hour.do(hourly_chime)
schedule.every().day.at("07:00").do(morning_alarm)
schedule.every().day.at("00:00").do(daily_runtime)

# Run initial functions
read_temperature()
read_humidity()

# Main loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    stop_buzzer()
    GPIO.cleanup()
    print("Program terminated and buzzer stopped.")

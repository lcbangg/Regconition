import os
import playsound
import speech_recognition as sr
import time
import random
import sys
import ctypes
import speech_recognition
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import openai
import cv2
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
from datetime import date
from datetime import datetime
from unidecode import unidecode


# Khúc này là khai báo các biến cho quá trình làm con Alex
wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()
robot_ear = speech_recognition.Recognizer()
openai.api_key = ""


# Text - to - speech: Chuyển đổi văn bản thành giọng nói
def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", block=True)
    os.remove("sound.mp3")


# Speech - to - text: Chuyển đổi giọng nói bạn yêu cầu vào thành văn bản hiện ra khi máy trả lại kết quả đã nghe
def get_audio():
    time.sleep(1)
    print("\nBot: \tĐang nghe \t *__^ \n")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=8)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text.lower()
        except:
            print("...")
            return 0


# Ở dòng này, Bot sẽ chào tạm biệt bạn khi bạn tạm biệt nó ^^
def stop():
    speak("Hẹn gặp lại bạn sau!")


# Khúc này Alex sẽ hỏi lại những gì mà bạn nói vào nhưng Alex không nghe rõ do bị dính tạp âm
def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Máy không nghe rõ. Bạn nói lại được không!")
    stop()
    return 0


# Ở đây là bước chào hỏi. Alex sẽ phân vùng thời gian để trò chuyện với bạn cho hợp lý nha ^^
def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
    else:
        speak("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name))


# Alex đang trả lời bạn về thời gian và ngày tháng nè.
def get_time(text):
    now = datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút %d giây' % (now.hour, now.minute, now.second))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")


# Ai mà lười kích đúp chuột để mở ứng dụng thì gọi Alex lên nhoa :3
def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        webbrowser.open('https://www.google.com')  # Trong ngoặc là đường dẫn đến ứng dụng trong máy mình, các bạn tự tìm trong máy mình sao cho đúng nha
    elif "word" in text:
        speak("Mở Microsoft Word")
        time.sleep(2)
        os.startfile('C:\Program Files\Microsoft Office\Office15\WINWORD.EXE')  # Ở đây cũng như ở trên
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk')  # Ở trển cũng giống dưới này =))
    elif "Sublime Text" in text:
        speak("Sublime Text đang được mở, bạn chờ xíu nha Ihihi")
        os.startfile('C:\Program Files\Sublime Text 3\sublime_text.exe')
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")


# Alex mở web cho bạn được luôn nè
def open_website():
    speak("Bạn muốn mở website nào")
    with open('website.json', encoding='utf-8') as f:
        data = json.load(f)
        # Get input from user
        user_input = get_text()
        # Look for a matching question in the data
        for question in data.keys():
            if question in user_input.lower():
                answer = data[question]
                break
        else:
            # If no matching question is found, use a default response
            speak("Tôi xin lỗi, tôi không hiểu ý của bạn")
    if answer:
        # domain = reg_ex.group(1)
        # url = 'https://www.' + domain + '.com'
        webbrowser.open(answer)
        speak("Trang web bạn yêu cầu đã được mở.")
        return True
    else:
        return False


# Muốn kiếm chị Google mà ngại tiếp xúc với chị ấy thì nhờ Alex nói giùm ha ^^
def open_google_and_search():
    speak('Bạn muốn tìm kiếm gì nào')
    search_for = get_text()
    # search_for = text.split("kiếm", 1)[1]
    speak('Okay!')
    driver = webdriver.Chrome(path)
    driver.get("http://www.google.com")
    que = driver.find_element_by_xpath("//input[@name='q']")
    que.send_keys(str(search_for))
    que.send_keys(Keys.RETURN)


# Alex còn biết gửi mail mà không cần bật gmail á, thấy giỏi hôn nè ^^
def send_email(text):
    with open('conversation.json', encoding='utf-8') as f:
        data = json.load(f)
    speak('Bạn gửi email cho ai nhỉ')
    recipient = get_text()
    for name in data:
        if name in recipient:  # 'anh' ở đây là keywords để máy tiếp tục gửi email cho bạn. Bạn có thể thay cái keywords này
            speak('Nội dung bạn muốn gửi là gì')
            time.sleep(2)
            content = get_text()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('lachibang20@gmail.com',
                       '')  # 'xyz' ở đây là địa chỉ email của bạn (địa chỉ email gửi), 'abc' là mật khẩu của email đó
            mail.sendmail('lachibang20@gmail.com',
                          data["name"], content.encode(
                    'utf-8'))  # 'xyz' ở đây cũng như bên trên, nhưng '123' là địa chỉ email nhận (email được bạn gửi thư)
            mail.close()
            speak('Email của bạn vùa được gửi. Bạn check lại email nhé hihi.')
            time.sleep(3)
        else:
            speak('Bot không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không')


# Muốn đi chơi mà sợ trời mưa thì hãy xem dự báo thời tiết nha, nhớ gọi Alex đó
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = unidecode(get_text())
    if not city:
        pass
    api_key = "ccb589d834be546ec2981a90002bfebf"
    call_url = ow_url + "&q=" + city.lower() + "&units=metric" + "&appid=" + api_key
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
                                                                            """.format(day=now.day, month=now.month, year=now.year,
                                                                           hourrise=sunrise.hour,
                                                                           minrise=sunrise.minute,
                                                                           hourset=sunset.hour, minset=sunset.minute,
                                                                           temp=current_temperature,
                                                                           pressure=current_pressure,
                                                                           humidity=current_humidity)
        speak(content)
    else:
        speak("Không tìm thấy địa chỉ của bạn")


# Relax hôn, nghe nhạc trên Youtube nè ^^
def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    time.sleep(1)
    mysong = get_text()
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    speak("Bài hát bạn yêu cầu đã được mở.")
    time.sleep(3)


# Không biết dạo này tình hình Cô Vy như thế nào rồi nhỉ, đọc báo phát xem thử nào :)
def read_news():
    speak("Bạn muốn đọc báo về gì")

    queue = get_text()
    params = {
        'apiKey': '30d02d187f7140faacf9ccd27a1441ad',
        "q": queue,
    }
    api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
    api_response = api_result.json()
    print("Tin tức")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"""Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}
    """)
        if number <= 3:
            webbrowser.open(result['url'])


# Hình nền máy tính bạn liệu có quá nhàm chán, hãy đổi ngay với Alex nhá
def change_wallpaper():
    api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
    url = 'https://api.unsplash.com/photos/random?client_id=' + \
          api_key
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json['urls']['full']
    # Nhớ đưa cái đường dẫn của mấy tấm ảnh nền mà bạn muốn thay đổi vào nha ^^
    urllib2.urlretrieve(photo, "C:\\Users\\PC\\b.jpg")
    image = os.path.join("C:\\Users\\PC\\b.jpg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
    speak('Hình nền máy tính vừa được thay đổi')


# Bật mí là con Bot này rất rất là "nhiều chuyện". Nên hổng biết cái gì cứ hỏi nó nha ^^
def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        time.sleep(2)
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0].split(".")[0])
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không")
            time.sleep(2)
            ans = get_text()
            if "có" not in ans:
                break
            speak(content)
        speak('Cảm ơn bạn đã lắng nghe!!!')
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")


# Khúc này là tự bạch của Alex. Bạn có thể thay đổi cái nội dung bên trong tùy theo ý thích của bạn nha
def introduce():
    speak(
        "Xin chào bạn. Rất hân hạnh được phục vụ bạn. Tôi là Alex. Tôi là trợ lý ảo được tạo ra dựa trên ngôn ngữ lập trình Python kết hợp với AI. Tôi sinh ra vào ngày 1/3/2023 và được sáng lập bởi Lê Phước Nghĩa. Hiện tại bạn đang sử dụng phiên bản Alex 2.1 (cập nhật lần gần nhất ngày 1/3/2023) và cũng đang là phiên bản mới nhất.")


# Ở đây là những gì mà Alex có thể làm và đang show cái list ra cho bạn xem nè
def help_me():
    speak("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    0. Giới thiệu bản thân
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Gửi email
    6. Dự báo thời tiết
    7. Mở video nhạc
    8. Thay đổi hình nền máy tính
    9. Đọc báo hôm nay
    10. Kể bạn biết về thế giới
    11. Hẹn giờ tắt máy
    12. Hỏi đáp nhanh""")


# Nếu như bạn không thích tắt máy ngay thì hãy dụng bộ cài đặt hẹn giờ sau đây nè
def shutdown():
    h = int(speak("Nhập giờ: "))
    m = int(speak("Nhập phút: "))
    s = int(speak("Nhập giây: "))
    while True:
        t = speak("Mời bạn chọn chế độ (ShutDown = s, Restart = r ): ")
        if t == "s" or t == "r":
            break

    h = h * 60 * 60
    m = m * 60
    s = s + m + h
    print("Bắt đầu hẹn giờ")
    os.system(f"ShutDown -{t} -t {s}")  # Lệnh thực hiện dòng lệnh
    print("Gõ lệnh ShutDown -a để hủy hẹn giờ")
    speak("Nhớ tắt hết ứng dụng trước khi tắt máy nhoa, ihihi ^^")


# Hỏi đáp nhanh với Alex nha
def Q_and_A():
    # Load data from JSON file
    with open('conversation.json', encoding='utf-8') as f:
        data = json.load(f)
    # Start conversation loop
    while True:
        # Get input from user
        user_input = get_text()
        # Look for a matching question in the data
        for question in data.keys():
            if question in user_input.lower():
                # Select a random answer from the matching question's list
                answer = random.choice(data[question])
                speak(answer)
                break
        else:
            # If no matching question is found, use a default response
            speak("Tôi xin lỗi, tôi không hiểu ý của bạn")
        if "tạm biệt" in user_input:
            break


def chatgpt():
    while True:
        speak('Bạn cần hỏi gì')
        time.sleep(1)
        content = get_text()
        if "dừng" in content or "kết thúc" in content:
            break;
        message = generate_text(content)
        speak(message)


def generate_text(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003", # chọn một trong các engine của GPT để sử dụng
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions["choices"][0]["text"]
    return message


def take_picture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    time.sleep(6)
    cv2.imwrite('picture.jpg', frame)
    cap.release()
    cv2.destroyAllWindows()
    speak('Chụp ảnh thành công')


# Liên kết chúng lại để tạo thành con Bot Alex hoàn chỉnh thôi nào ^_^
def assistant():
    speak("Xin chào, bạn tên là gì nhỉ?")
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        while True:
            speak("Bạn cần Bot Alex có thể giúp gì ạ?")
            text = get_text()
            if not text:
                break
            elif "dừng" in text or "tạm biệt" in text or "ngủ thôi" in text:
                stop()
                break
            elif "có thể làm gì" in text:
                help_me()
            elif "chào Alex" in text:
                hello(name)
            elif "giờ" in text or "ngày" in text:
                get_time(text)
            elif "google và tìm kiếm" in text:
                open_google_and_search()
            elif "mở website" in text:
                open_website()
            elif "ứng dụng" in text:
                speak("Tên ứng dụng bạn muốn mở là ")
                text1 = get_text()
                open_application(text1)
            elif "email" in text or "mail" in text or "gmail" in text:
                send_email(text)
            elif "thời tiết" in text:
                current_weather()
            elif "chơi nhạc" in text:
                play_song()
            elif "hình nền" in text:
                change_wallpaper()
            elif "đọc báo" in text:
                read_news()
            elif "định nghĩa" in text:
                tell_me_about()
            elif "giới thiệu" in text:
                introduce()
            elif "tắt máy" in text or "shutdown" in text:
                shutdown()
            elif "hỏi đáp" in text:
                Q_and_A()
            elif "chatgpt" in text or "chat" in text or "gpt" in text:
                chatgpt()
            elif "chụp ảnh" in text or "chụp" in text:
                take_picture()
            else:
                speak("Bot không hiểu bạn nói gì ạ")


assistant()
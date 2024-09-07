eng2tur = {'person': 'kişi', 'bicycle': 'bisiklet', 'car': 'araba', 'motorcycle': 'motosiklet', 'airplane': 'uçak', 'bus': 'otobüs', 'train': 'tren', 'truck': 'kamyon', 'boat': 'tekne', 'traffic light': 'trafik ışığı', 'fire hydrant': 'yangın musluğu', 'stop sign': 'dur işareti ', 'parking meter': 'parkmetre', 'bench': 'bank', 'bird': 'kuş', 'cat': 'kedi', 'dog': 'köpek', 'horse': 'at', 'sheep': 'koyun', 'cow': 'inek', 'elephant': 'fil', 'bear': 'ayı', 'zebra': 'zebra', 'giraffe': 'zürafa', 'backpack': 'sırt çantası', 'umbrella': 'şemsiye', 'handbag': 'el çantası', 'tie': 'kravat', 'suitcase': 'valiz', 'frisbee': 'frizbi', 'skis': 'kayak', 'snowboard': 'snowboard', 'sports ball': 'spor topu', 'kite': 'uçurtma', 'baseball bat': 'beyzbol sopası', 'baseball glove': 'beyzbol eldiveni ', 'skateboard': 'kaykay', 'surfboard': 'sörf tahtası', 'tennis racket': 'tenis raketi', 'bottle': 'şişe', 'wine glass': 'şarap kadehi', 'cup': 'fincan', 'fork': 'çatal', 'knife': 'bıçak', 'spoon': 'kaşık', 'bowl': 'kase', 'banana': 'muz', 'apple': 'elma ', 'sandwich': 'sandviç', 'orange': 'portakal', 'broccoli': 'brokoli', 'carrot': 'havuç', 'hot dog': 'sosisli sandviç', 'pizza': 'pizza', 'donut': 'çörek', 'cake': 'kek', 'chair': 'sandalye', 'couch': 'kanepe', 'potted plant': 'saksı bitkisi', 'bed': 'yatak ', 'dining table': 'masa', 'toilet': 'tuvalet', 'tv': 'tv', 'laptop': 'dizüstü bilgisayar', 'mouse': 'fare', 'remote': 'uzaktan kumanda', 'keyboard': 'klavye', 'cell phone': 'cep telefonu', 'microwave': 'mikrodalga', 'oven': 'fırın', 'toaster': 'ekmek kızartma makinesi', 'sink': 'lavabo ', 'refrigerator': 'buzdolabı', 'book': 'kitap', 'clock': 'saat', 'vase': 'vazo', 'scissors': 'makas', 'teddy bear': 'oyuncak ayı', 'hair drier': 'saç kurutma makinesi', 'toothbrush': 'diş fırçası', 'left': 'sol', 'right': 'sağ', 'center': 'orta'}
import cv2
import json
import random
import datetime

# JSON Schema Açıklamaları
def save_json_to_file(json_data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_data)

def generate_feedback_schema(interaction_id, user_id, input_prompt, response, rating, feedback_text, preferred_response, device, location, session_duration):
    feedback_schema = {
        "interaction_id": interaction_id,
        "user_id": user_id,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",  # Current time in ISO 8601 format
        "content_generated": {
            "input_prompt": input_prompt,
            "response": response
        },
        "user_feedback": {
            "rating": rating,  # Options: "like", "dislike"
            "feedback_text": feedback_text,
            "preferred_response": preferred_response
        },
        "feedback_metadata": {
            "device": device,
            "location": location,
            "session_duration": session_duration  # in seconds
        }
    }
    json_data = json.dumps(feedback_schema, indent=4, ensure_ascii=False)
    
    # JSON verisini bir dosyaya kaydet
    file = open("number.txt", "r")
    number = int(file.read())
    file.close()
    file = open("number.txt", "w")
    file.write(str(number + 1))
    file.close()
    save_json_to_file(json_data, "feedback_data" + str(number) + ".json")
    
    return json_data

import json
import requests
import json
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from gtts import gTTS
import pygame
import easyocr
import uuid
import numpy as np
from gradio_client import Client, handle_file
import threading
def convert_to_special_format(json_data):
    output = "<|begin_of_text|>"
    for entry in json_data:
        if entry["role"] == "system":
            output += f'<|start_header_id|>system<|end_header_id|>\n\n{entry["content"]}<|eot_id|>'
        elif entry["role"] == "user":
            output += f'\n<|start_header_id|>{entry["role"]}<|end_header_id|>\n\n{entry["content"]}<|eot_id|>'
            if json_data.index(entry) != len(json_data) - 1:
                output += ""
        elif entry["role"] == "assistant":
            output += f'\n<|start_header_id|>{entry["role"]}<|end_header_id|>\n\n{entry["content"]}<|eot_id|>'

    output += "\n<|start_header_id|>assistant<|end_header_id|>"
    return output

url = "https://inference2.t3ai.org/v1/completions"

# Başlangıç ayarları
pygame.mixer.init()
reader = easyocr.Reader(['tr'])

# Pencere boyutları ve tema
ctk.set_appearance_mode("dark")  # Başlangıçta koyu mod
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("700x600")
root.minsize(700, 600)
root.title("aiRehberim")

cap = cv2.VideoCapture(0)

def speak_text(text):
    tts = gTTS(text=text, lang='tr')
    tts.save("temp_output.mp3")
    pygame.mixer.music.load("temp_output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()

speak_text("Rehber'e hoşgeldiniz")

# OCR ve TTS işlemini iş parçacığında çalıştırmak için fonksiyon
def ocr_and_tts():
    global cap
    ret, frame = cap.read()
    if ret:
        filename = 'captured_image.png'
        cv2.imwrite(filename, frame)
        print(f"Resim kaydedildi: {filename}")
        results = reader.readtext(filename)
        for result in results:
            if result[1].strip() == "":
                continue
            print(result[1])
            speak_text(result[1].lower())

# "Oku" butonuna basıldığında iş parçacığı oluştur
def on_button_press():
    speak_text("Oku butonuna basıldı. Lütfen bekleyiniz")
    threading.Thread(target=ocr_and_tts).start()

# "Çevre Yardımı Başlat" butonuna basıldığında iş parçacığını oluştur ve butonu devre dışı bırak
def buton2_event():
    speak_text("Çevre Yardımı Başlat butonuna basıldı. Lütfen bekleyiniz")
    buton2.configure(state=tk.DISABLED)
    capture_and_send_image()

# Ana ekran
canvas_frame = ctk.CTkFrame(root)
canvas_frame.pack(pady=20, padx=50, expand=True)

# Uygulama adı
app_label = ctk.CTkLabel(canvas_frame, text="aiRehberim", font=ctk.CTkFont(size=30, weight="bold"))
app_label.grid(row=0, column=0, pady=(0, 10))

# Webcam görüntüsünü gösteren tuval
canvas = ctk.CTkCanvas(canvas_frame, width=600, height=400, bg='black', highlightthickness=0)
canvas.grid(row=1, column=0, pady=10)

# 'Oku' butonu
buton = ctk.CTkButton(canvas_frame, text="Oku", fg_color="red", hover_color="#ff1919", height=50, width=120,
                      font=ctk.CTkFont(size=20), command=on_button_press)
buton.grid(row=2, column=0, pady=10)

# Kamera güncelleme fonksiyonu
def update_frame():
    global canvas
    global cap
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)

        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk

    root.after(20, update_frame)

update_frame()

# API istemcilerini oluşturma
client = Client("depth-anything/Depth-Anything-V2")
client2 = Client("kedimestan/yolov8-segmentation-deneme")

# API çağrısını iş parçacığında çalıştırmak için fonksiyon
def api_processing():
    global cap
    ret, frame = cap.read()
    if ret:
        filename = 'captured_image.png'
        cv2.imwrite(filename, frame)
        print(f"Resim kaydedildi: {filename}")
    
    # Derinlik haritasını elde etme
    result = client.predict(
        image=handle_file(filename),
        api_name="/on_submit"
    )
    img = Image.open(result[1])

    depth_map = np.array(img)
    depth_map = 255 - depth_map
    biggest = depth_map.max()
    scaled_map = depth_map / biggest
    last_map = scaled_map * 89.28

    # Nesne tespiti
    objects = client2.predict(
        image=handle_file(filename),
        model_name="yolov8m.pt",
        image_size=640,
        conf_threshold=0.25,
        iou_threshold=0.45,
        api_name="/predict"
    )

    # Sonuçları işleme
    def process_objects_and_last_map(objects, last_map):
        results = []
        map_height, map_width = last_map.shape

        for obj in objects:
            label = obj['label']
            bbox_coords = obj['bbox_coords']
            box_coords = bbox_coords.replace("tensor", "").replace("([", "").replace("])", "").split(",")
            for i in range(len(box_coords)):
                box_coords[i] = float(box_coords[i][1:])

            x_min, y_min, x_max, y_max = box_coords
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2

            # Resmin ortasında mı, sağında mı, solunda mı olduğunu belirle
            if x_center < map_width / 3:
                position = 'left'
            elif x_center > 2 * map_width / 3:
                position = 'right'
            else:
                position = 'center'

            x_min = int(max(0, x_min))
            y_min = int(max(0, y_min))
            x_max = int(min(map_width, x_max))
            y_max = int(min(map_height, y_max))

            region = last_map[y_min:y_max, x_min:x_max]
            min_value = np.min(region)

            results.append({
                'label': eng2tur[label],
                'position': eng2tur[position],
                'min_value': min_value*100
            })

        return results




    processed_results = process_objects_and_last_map(objects, last_map)
    temp_string=";"
    for i in processed_results:
        temp_string += str(i["label"])+", "+str(int(i["min_value"]))+", "+str(i["position"])+";"
    json_data = [
    {"role": "system", "content": "Sen yardımcı bir asistansın ve sana verilen talimatlar doğrultusunda en iyi cevabı üretmeye çalışacaksın. Türkçe cevap vereceksin. Kullanıcıların sorularına Türkçe olarak doğru ve etkili yanıtlar vermek için tasarlandım. Girdinin tamamını türkçeye çevirerek düşüneceğim. Her iki noktalı virgül karakteri arasındaki birinci değer tespit edilen cismin türünü, ikinci değer ise cisim ile kullanıcı arasında cm cinsinden mesafe, üçüncü değer ise cismin sağda, solda ya da ortada olduğunu söylüyecek. Hiç bir yeri göremeyen engelli ya da yaşlı birey için bütün bu cisimleri, bütün bilgilerini ve somutsal özelliklerini söyleyecek bir uyarı metni yazmalıyım. Bilmiyorum demem yasak. Bütün cisimler için bu işlemi yapacağım."},
    {"role": "user", "content":  temp_string }]
    special_format_output = convert_to_special_format(json_data)
    payload = json.dumps({
        "model": "/home/ubuntu/hackathon_model_2/",
        "prompt": special_format_output,
        "temperature": 1,
        "top_p": 0.95,
        "max_tokens": 3000,
        "repetition_penalty": 1.1,
        "stop_token_ids": [
            128001,
            128009
    ],
    "skip_special_tokens": True
    })

    headers = {
    'Content-Type': 'application/json',
    }


    response = requests.post(url, headers=headers, data=payload)
    pretty_response = json.loads(response.text)
    print("LLM Cevap:", pretty_response['choices'][0]['text'])
    speak_text(pretty_response['choices'][0]['text'])

    rating = "Like"
    def get_rating(var):
        global rating
        rating = var

    fb_text_res = ""
    preffered_response_res = ""
    def feedback_page():
        global fb_text_res
        global preffered_response_res
        feedback_window = ctk.CTk()
        feedback_window.title("Geri Bildirim")
        feedback_window.geometry("600x800")

        label = ctk.CTkLabel(feedback_window, text = "Feedback Sayfası", font=ctk.CTkFont(size = 15))
        label.place(relx = 0.5, rely = 0.1, anchor = "center")
        rating_comb = ctk.CTkComboBox(feedback_window, values = ["Like", "Dislike"],
                                      fg_color=("#90CAF9","#1976D2"), border_color="#4FC3F7", border_width=2, command = get_rating)
        rating_comb.place(relx = 0.5, rely = 0.3, anchor = "center")

        fb_text = ctk.CTkEntry(feedback_window, height=90, width=150, placeholder_text="Feedback")
        fb_text.place(relx = 0.5, rely = 0.5, anchor = "center")

        preffered_response = ctk.CTkEntry(feedback_window, height=90, width=150, placeholder_text="Önerilen Cevap")
        preffered_response.place(relx = 0.5, rely = 0.6, anchor = "center")

        def gonder_buton():
            global fb_text_res
            global preffered_response_res
            fb_text_res = fb_text.get()
            print(fb_text_res)
            preffered_response_res = preffered_response.get()
            print(preffered_response_res)
        ans_btn = ctk.CTkButton(feedback_window, text = "Gönder", width= 50, height=30, 
                                corner_radius=20, command = gonder_buton)
        ans_btn.place(relx = 0.5, rely = 0.8, anchor = "center")


        feedback_window.mainloop()
    feedback_page()

    user = "user" + str(random.randint(1,100000000))

    generate_feedback_schema(rating=rating, preferred_response=preffered_response_res, 
                             feedback_text=fb_text_res, response=pretty_response['choices'][0]['text'],
                             input_prompt=temp_string, location="Antalya, Türkiye", device = "masaüstü",
                             session_duration="30 sec", interaction_id=str(uuid.uuid4()), user_id=user)

    root.after(30000, capture_and_send_image)

def capture_and_send_image():
    threading.Thread(target=api_processing).start()

# Koyu/Açık mod switchi
def switch_event():
    if switch_var.get():
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

switch_var = tk.BooleanVar(value=False)
mode_switch = ctk.CTkSwitch(root, text="Koyu/Açık Mod", command=switch_event, variable=switch_var, onvalue=True, offvalue=False)
mode_switch.place(relx=0.05, rely=0.95, anchor=tk.SW)

# Info Page butonu
def open_info_page():
    info_window = ctk.CTkToplevel(root)
    info_window.title("Info Page")
    info_window.geometry("500x200")
    info_window.minsize(500,200)
    info_label = ctk.CTkLabel(info_window, text="aiRehberim, görme engelli ve yaşlı bireylerin etrafındaki\ncisimler hakkında bilgi edinmesini amaçlayan bir uygulamadır.\n\nYapımcılar (Abra Muhara):\nŞuayp Talha Kocabay\nMehmet Kağan Albayrak\nFatih Kürşat Cansu (Danışman)", font=ctk.CTkFont(size=16))
    info_label.pack(pady=20)
    speak_text(info_label.cget("text"))

info_button = ctk.CTkButton(root, text="Info Page", fg_color="green", hover_color = "#83f28f",width = 100,command=open_info_page)
info_button.place(relx=0.95, rely=0.95, anchor=tk.SE)

# "Çevre Yardımı Başlat" butonu
buton2 = ctk.CTkButton(canvas_frame, text="Çevre Yardımı Başlat", fg_color="blue", height=50, width=200,font=ctk.CTkFont(size=20), command=buton2_event)
buton2.grid(row=3, column=0, pady=10)

root.mainloop()

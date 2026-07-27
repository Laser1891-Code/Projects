# This file provides the function to create the arduino sketch, and then upload it using upload_sketch_function_file.py

import customtkinter as ctk
from upload_sketch_function_file import upload
import os

def upload_program(app,progress_bar):
    os.chdir(app.save_dir)
    sketch = os.path.join(app.save_dir,"sketches","PLD","pld.ino")
    with open(app.program,"r") as f:
        data = f.read()

    split_data = list(data.replace("|", "").replace("-",""))
    split_data.reverse()

    with open(sketch, "w") as f:
        f.write("""
#define clear 8
#define data 4
#define clk 6                

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(clear, OUTPUT);
    pinMode(data, OUTPUT);
    pinMode(clk, OUTPUT);
                
    digitalWrite(data, LOW);
    digitalWrite(clk, HIGH);
    digitalWrite(clear, LOW);
    delay(50);
    digitalWrite(clear, HIGH);
                
    
    int data_values[] = """+str(split_data).replace("[","{").replace("]","}").replace("'","").replace(" ","")+""";
    
    for (int i=0; i<=48; i++) {
        digitalWrite(data,data_values[i]);
        digitalWrite(clk, LOW);
        digitalWrite(LED_BUILTIN, LOW);
        delay(50);
        digitalWrite(clk, HIGH);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(50);
    }
    //digitalWrite(clk,LOW);
    //digitalWrite(data,LOW);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}
""")

    upload(app, progress_bar)
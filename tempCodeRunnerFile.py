import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# 这是一个“假仪器”类，用来模仿示波器
class MockOscilloscope:
    def __init__(self,address):
        print(f"connecting to the device:{address}...connected!")

    def write(self,command):
        print(f"[send command]->{command}")
        if command == '*RST':
            print("(the device is reseting...)")
            time.sleep(1)   

    def query(self,command):
        print(f"[query command]->{command}")

        if command == '*IDN?':
            return "Marvell_Virtual_scope_2026"
        
        elif command == 'MEAS:VOLT?':
            fake_voltage = round(random.uniform(0,0.5),3)
            return str(fake_voltage)
        
        else:
            return "Error:Unknown Command"

scope = MockOscilloscope("USB0::0x1234::FAKE::INSTR")

# reset the device
scope.write('*RST')

datalist = []

print("\nStar Testing...")
for i in range(5):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    voltage = scope.query("MEAS:VOLT?")
    print(f"[{current_time} measurement #{i+1}] Voltage:{voltage}V")
    
    datalist.append(
        {
            "Timestamp":current_time,
            "Mesurement ID":i + 1,
            "Voltage(V)":voltage
        }
    )
    time.sleep(0.5)
    
print("\nSaving data to CSV...")

df = pd.DataFrame(datalist)  
df.to_csv("test_result.csv", index=False) 

print("Done! Check 'test_result.csv' in your folder.")
print("\nTest End!")

# 读取数据并绘图
data = pd.read_csv("test_result.csv")
print(data)

plt.figure(figsize=(10,5))

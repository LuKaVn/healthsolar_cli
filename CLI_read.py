#this page read data from IVT and export to CLI
#do not show in grafic
#do not write and read data from database
# do not use _VAR to defind 
'''
444 No Response
404 Not Found
400 Bad Request
'''
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
from CLI_data import *
import time
_SIGNAL=0
VAR=''
RESULT=[]
_CYCLE=10
BUFF_LIST_ISSUE=[]
FINAL_LIST_ISSUE=[]
WRITE_LIST_ISSUE=[]
class FloatModbusClient(ModbusClient):
    def read_float(self , address, number=1):
        reg_l = self.read_holding_registers(address,number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f  in utils.word_list_to_long(reg_l)]
        else:
            _SIGNAL = 444
            print(_SIGNAL)
c = FloatModbusClient()
def Connect_MbTCP(ip,func,reg_addr,reg_nb): #data=Connect_MbTCP("192.168.1.151",3,1,15)
    SERVER_HOST = ip
    SERVER_PORT = 502
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)
    if not c.is_open():
        _SIGNAL = 400
        print(_SIGNAL)
    else:
        if func==3:
            regs_data = c.read_float(reg_addr,reg_nb)
            return regs_data
        if func==4:
            regs_data=c.read_input_registers(reg_addr,reg_nb)
            return regs_data

def read_data():
    for i in range(len(KEYIVT)):
        _CONDITON_WEATHER=read_weather()
        while(_CONDITON_WEATHER==False): # đo dữ liệu thời tiết
            _CONDITON_WEATHER=read_weather() 
# mục đích code đoạn trên là để giữu không cho địa chỉ IP Inverter nó bị nhảy
        if(_CONDITON_WEATHER==True): # có thể không cần sử dụng IF trong trường hợp này
            time.sleep(1)
            for y in range(_CYCLE):# số lần đọc lặp lại
                VAR=IP_CONFIG[KEYIVT[i]] # địa chỉ Inverter 
                RESULT=Connect_MbTCP(VAR,3,1,15)
                
                VALUE_SCB=STRING_COUNT[KEYIVT[i]].values() # lấy số string trong mỗi COB
                compare_data(RESULT,VALUE_SCB)# đưa vào hàm cha giá trị 
                ############################
                #                          #
                #         RESULT           #
                #                          #
                ############################
                if len(BUFF_LIST_ISSUE)>0: # CÓ SỰ CHÊNH LỆCH GIÁ TRỊ
                    for z in range(len(BUFF_LIST_ISSUE)):
                        _VAR_REUSE=BUFF_LIST_ISSUE[z]
                        FINAL_LIST_ISSUE.append(list(STRING_COUNT[KEYIVT[i]].keys())[_VAR_REUSE]) # đưa giá trị vào trong list final
                        # DICT KEY KHÔNG SỬ DỤNG ĐƯỢC VỚI [VAR] ----------YÊU CẦU CHUYỂN QUA list
            #sau khi chạy 10 vòng lặp thì bắt đầu tính tổng số lỗi đã xảy ra trong lần đo.
            if len(FINAL_LIST_ISSUE)>0:
                for y in range(len(FINAL_LIST_ISSUE)): 
                    _COUNT=0 
                    for z in range(len(FINAL_LIST_ISSUE)):
                        if FINAL_LIST_ISSUE[y]==FINAL_LIST_ISSUE[z]:
                            _COUNT=_COUNT+1
                    if _COUNT>8:
                        print(FINAL_LIST_ISSUE[y])# IN GIÁ TRỊ BỊ LỖI NHIỀU NHẤT
                        WRITE_LIST_ISSUE.append(FINAL_LIST_ISSUE[y])# ----------------------------------------------------------------> EXPORT DATA       
            print(FINAL_LIST_ISSUE)       
                    
def compare_data( data1,data2):# DATA 1 LÀ KẾT QUẢ SAU KHI ĐO -----DATA2 LÀ SỐ TRING MẶC ĐỊNH TRONG NHÀ MÁY
    BUFF_RESULT=[] # CHỨA BIẾN TẠM KẾT QUẢ CHIA CHO SỐ TRING
    BUFF_LIST_ISSUE=[] # CHỨA BIẾN TẠM SỰ CỐ XẢY RA
    
    for z in range(len(data1)):
        BUFF_RESULT.append(data1[z]/data2[z]) # KẾT QUẢ SAU KHI CHIA CHO SỐ STRING
    _VAR_COMPARE = max(BUFF_RESULT)-(max(BUFF_RESULT)*0.1)
         
    for z in range(len(BUFF_RESULT)):
        if BUFF_RESULT[z]<_VAR_COMPARE:
            BUFF_LIST_ISSUE.append(z) # KẾT QUẢ SAU KHI SO SÁNH GIÁ TRỊ

def read_weather():
    data_weather1=Connect_MbTCP(IP_WEATHER[0],4,1,1)
    data_weather2=Connect_MbTCP(IP_WEATHER[1],4,1,1)
    if data_weather1 > 500 and data_weather2 > 500:
        return True
    else:
        return False
    
def main():
    # 2 condition to read data is: time from 9h30 to 14h30 AND   radiation no less than  500W
    _HOUR=time.localtime().tm_hour
    _CONDITION=(_HOUR>9 and _HOUR<15 and read_wearther())
    if _CONDITION==True:
        #START READ DATA
        read_data()
    else:
        print("time end")

'''       
def test_do():
    for i in range(10):
        _time=time.localtime().tm_min
        #time.struct_time(tm_year=2022, tm_mon=3, tm_mday=9, tm_hour=15, tm_min=15, tm_sec=40, tm_wday=2, tm_yday=68, tm_isdst=0)
        condition_time= _time>12 and _time<14
        while(condition_time==False):
            
            _time=time.localtime().tm_min
            condition_time= _time>12 and _time<14
            
        if(condition_time==True):
            print(i)
            _time=time.localtime().tm_min
            print(time.localtime().tm_sec)
            time.sleep(5)
        else:
            {}
        print(i)
'''

while(1):
    main()
    


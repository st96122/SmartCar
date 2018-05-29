## DBC File

+ 37     STEER_ANGLE_SENSOR  8byte

   - mode : 23 (8)**待驗證狀態**
   - 01 : 31 (8)*固定為1*
   - check : 63 (8)
   - wheel_angle : 15 (8) *signed*
   - rotation_count : 7 (8)

+ 180    SPEED  8byte

   + ENCODER : 39 (8)
   + CHECKSUM : 63 (8)
   + SPEED : 47 (16) 速度

+ 288    GEAR 8byte

   - gear_1 : 47  (8) *32為P檔, 34為N檔, 35為D檔*
   - gear_2 : 63  (8) **待驗證狀態**

+ 560    BRAKE_MODULE2  7byte

   + brake_LI : 26 (1)  *1為輕踩*
   + brake_H : 29 (1) *1為重踩*
   + handcrat : 24 (1) *1為腳煞車*  **待驗證狀態**

+ 1407     Headlamps  7byte

   + LIGHT_SMALL : 12 (1) *1為小燈*
   + LIGHT_BIG : 13 (1) *1為大燈*
   + LIGHT_FLASH : 11 (1) *1為閃*
   + pause : 7  (8) *燈改變狀態時動作*

+ 1462    DOOR  8byte

   - doorpause : 7 (8)*門狀態改變時動作*
   - door_lock : 7 (8) *0x00關 0x80開 0x81駕駛控制開 0x01駕駛控制開後手動關*

   

## Firebase Database

**Data: **

- 車速(int): 0~255
- 方向盤(float): -900~900度
- 油門踏板(gas_pedal): bool    **目前還缺少**
- 手煞車踏版(foot_brake_pedal): bool   **待驗證狀態**
- 車鎖(door lock): bool
- 煞車踏板(brake_pedal): 四個狀態無動作(0)、輕踩(1)、重踩(2)
- 檔位(gear): 四個狀態P(0)、N(1)、D(2)、R(3)
- 車燈(light): 四個狀態沒開(0)、小燈(1)、大燈(2)、閃燈(3)

   
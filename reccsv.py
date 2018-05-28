import csv
import cv2
import numpy as np
import time
import thread
def f0x25(j,frame,kj):
    global tt2
    if (tt2 == 0 or tt2 != kj):

        v=int(j[3][3:6],16)
        v=bin(v)
        v=v[2:len(v)].zfill(12)
        v=str(v)
        if(v[0]=='0'):
            v=int(v,2)
            cv2.putText(frame, str(v), (550, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
        else:
            nk=nott(v,len(v))
            nk=int(nk,2)
            cv2.putText(frame, '-'+str(nk), (550, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
        tt2=kj
def f0x230(j,frame):

    v = (int(j[3], 16))
    v = bin(v)
    v = v[2:len(v)].zfill(56)
    if (v[24] == '1'):
        print(j[3] + ' handcrat')
        cv2.putText(frame, ' handcrat', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    elif (v[29] == '1'):
        print(j[3] + ' brake_H')
        cv2.putText(frame, 'brake_H', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    elif (v[26] == '1'):
        print(j[3] + ' brake_L')
        cv2.putText(frame, 'brake_L', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    else:
        print(j[3] + ' no_brake')
        cv2.putText(frame, 'no_brake', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)

def f0x5b6(j,frame):

    if(j[3][4:5]=='8'):
        print(j[3]+'  lock')
        cv2.putText(frame, 'door lock', (550, 150), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    if (j[3][4:5] == '0'):
        print(j[3] + '  open')
        cv2.putText(frame, 'door open', (550, 150), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)

def f0x57f(j,frame):
    v=(int(j[3],16))
    v=bin(v)
    v=v[2:len(v)].zfill(56)
    if(v[11]=='1'):
        print(j[3]+' high')
        cv2.putText(frame, 'high', (0, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    elif(v[13]=='1'):
        print(j[3]+' big light')
        cv2.putText(frame, 'big light', (0, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    elif(v[12]=='1'):
        print(j[3]+' small light')
        cv2.putText(frame, 'small light', (0, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    else:
        print(j[3]+' light off')
        cv2.putText(frame, 'light off', (0, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)

def f0x120(j,frame):

    {
        '23': lambda:pr('d',j[3][12:14]),
        '20': lambda:pr('p',j[3][12:14]),
        '22': lambda:pr('n',j[3][12:14])
    }.get(j[3][12:14], lambda:pr('',j[3][12:14]))()
def f0xb4(j,frame,kj):
    v=int(j[3][12:16],16)*0.011
    global tt
    if(tt == 0 or tt!=kj):
        cv2.putText(frame, str(v), (0, 400), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
        tt=kj
def pr(k,j):
    print(j+'  '+k)
    cv2.putText(frame, k, (0, 500), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
def prvideo(frame):

    cv2.putText(frame, lk[kj][1], (0, 150), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    cv2.imshow('frame', frame)
    print('lk=   ' + str(lk[kj]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
def primg(kk):
    img = cv2.imread('car_logger/' + kk)
    cv2.putText(img, lk[kj][1], (0, 150), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 6)
    cv2.imshow('frame', img)
    print('lk=   ' + str(lk[kj]))


    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
def nott(v,le):
    k=''
    for i in range(0,le):
        if v[i]=='0':
            k=k+'1'
        else:
            k=k+'0'
    return k
tt=0
tt2=0
cap=cv2.VideoCapture('0524.avi')
ret,frame=cap.read()
with open('canbus_output2.csv','r') as csvf:
    with open('img_output2.csv','r') as  csvf2:

        k2=csv.reader(csvf2)
        k=csv.reader(csvf)
        lk=[]
        kj=1
        for i in k2:
            lk.append(i)
        np.asanyarray(lk)
        for j in k:

            kji = kj
            if(j[0]!='Time' and kj<1054):
                if(float(j[0])>=float(lk[kj][0])):
                    kj+=1
                '''
                while(float(j[0])>=float(lk[kj][0])):
                    print('kj='+str(kj))
                    kj+=1
                    if(kj>=1053):
                        kj=1053
                        break
                '''
            if(kji!=kj):
                time.sleep(0.03)
                prvideo(frame)
                ret, frame = cap.read()
            {

                '0x25': lambda: f0x25(j,frame,kj),
                '0x230': lambda: f0x230(j,frame),
                '0x5b6': lambda: f0x5b6(j,frame),
                '0x57f': lambda: f0x57f(j,frame),
                '0x120': lambda: f0x120(j,frame),
                '0xb4': lambda: f0xb4(j,frame,kj)
            }.get(j[2], lambda: None)()

                #primg(lk[kj][1])



import cv2
import numpy as np
import time
import math
from tkinter import *
from PIL import Image, ImageTk
import random
import PoseModule as pm
from cvzone.HandTrackingModule import HandDetector

# OpenCV 설정
cap = cv2.VideoCapture(0)
hand_detector = HandDetector(maxHands=1, detectionCon=0.5, minTrackCon=0.5)
pose_detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

# tkinter 설정
win = Tk()
win.title("Game")
win_w, win_h = (1000, 800)  # 창 크기를 넓혀서 게임 공간 확보
win.geometry(f"{win_w}x{win_h}")

previous_fingers_up_count = None


def press(fingers_up_count):
    global up_go, down_go, space_go, stage
    print(f"Press function called with {fingers_up_count} fingers up")  # 디버깅

    if fingers_up_count is None:
        print("Invalid fingers_up_count")
        return

    if stage == 1:
        if fingers_up_count == 1:
            up_go = True
            print("Up activated")
        elif fingers_up_count == 2:
            down_go = True
            print("Down activated")
        elif fingers_up_count == 3:
            space_go = True
            print("Space activated")
            stage = 2
            print("Stage changed to 2")

    elif stage == 2:
        if fingers_up_count == 3:
            space_go = True
            print("Space activated in stage 2")


def release(fingers_up_count):
    global up_go, down_go, space_go, bomb_cx, bomb_cy, bomb_vx, bomb_vy, bomb, stage
    print(f"Release function called with {fingers_up_count} fingers up")  # 디버깅

    if fingers_up_count is None:
        print("Invalid fingers_up_count")
        return

    if stage == 1:
        if fingers_up_count == 1:
            up_go = False
        elif fingers_up_count == 2:
            down_go = False

    elif stage == 2:
        if fingers_up_count == 3:
            space_go = False
            print("Space deactivated in release")
            bomb_cx = round(tank_cx + tank_w / 2 * math.cos(angle_now))
            bomb_cy = round(tank_cy - tank_w / 2 * math.sin(angle_now))
            bomb_vx = round(bomb_v_max * power / 100 * math.cos(angle_now))
            bomb_vy = round(-bomb_v_max * power / 100 * math.sin(angle_now))
            bomb = cvs.create_oval((bomb_cx - bomb_r, bomb_cy - bomb_r), (bomb_cx + bomb_r, bomb_cy + bomb_r),
                                   fill="red")
            stage = 3
            print("Bomb created and stage changed to 3")

# 초기화 부분
up_go, down_go, space_go = (False, False, False)
stage = 1
hit = False
# previous_fingers_up_count = 0
power = 0

cvs = Canvas(win)
cvs.config(width=win_w, height=win_h, bd=0, highlightthickness=0)
cvs.pack()

# Background
bot_h = round(win_h * 1 / 5)
bot_c = "#a6a6a6"
cvs.create_rectangle((0, win_h - bot_h), (win_w, win_h), fill=bot_c, outline=bot_c)
mid_h = round((win_h - bot_h) / 8)
mid_c = "#994d00"
cvs.create_rectangle((0, win_h - bot_h - mid_h), (win_w, win_h - bot_h), fill=mid_c, outline=mid_c)
top_h = win_h - bot_h - mid_h
top_c = "#b5b5fd"
cvs.create_rectangle((0, 0), (win_w, top_h), fill=top_c, outline=top_c)

# Angle
angle_r = round(bot_h / 2)
angle_mx = round(win_w / 20)
angle_my = round(bot_h / 4)
angle_ctr = (angle_r + angle_mx, win_h - bot_h + angle_my + angle_r)
cvs.create_arc((angle_ctr[0] - angle_r, angle_ctr[1] - angle_r), (angle_ctr[0] + angle_r, angle_ctr[1] + angle_r),
               fill="#6666ff", extent=180)
angle_min = 30 * math.pi / 180
angle_max = 90 * math.pi / 180
cvs.create_line(angle_ctr, (angle_ctr[0] + angle_r * math.cos(angle_min), angle_ctr[1] - angle_r * math.sin(angle_min)),
                width=2)
cvs.create_line(angle_ctr, (angle_ctr[0] + angle_r * math.cos(angle_max), angle_ctr[1] - angle_r * math.sin(angle_max)),
                width=2)
cvs.create_arc((angle_ctr[0] - round(angle_r / 5), angle_ctr[1] - round(angle_r / 5)),
               (angle_ctr[0] + round(angle_r / 5), angle_ctr[1] + round(angle_r / 5)), fill="#ffcccc", extent=180)
angle_now = 45 * math.pi / 180
angle_line = cvs.create_line(angle_ctr, (
    angle_ctr[0] + angle_r * math.cos(angle_now), angle_ctr[1] - angle_r * math.sin(angle_now)), fill="red", width=3)

# Tank
tank_w, tank_h = (round(min(win_w, win_h) / 10), round(min(win_w, win_h) / 10))
tank_cx = round(win_w / 40 + tank_w / 2)
tank_cy = top_h - round(tank_h / 2)
tank_img = Image.open("canon.png")
tank_img = tank_img.resize((tank_w, tank_h), Image.LANCZOS)
tank_img = tank_img.rotate(angle_now * 180 / math.pi - 10)
tank_img = ImageTk.PhotoImage(tank_img, master=win)
tank = cvs.create_image(tank_cx, tank_cy, image=tank_img)

# Gauge bar
gbar_mx = angle_mx
gbar_my = angle_my
gbar_w = win_w - angle_mx - gbar_mx * 2 - angle_r * 2
gbar_h = bot_h - gbar_my * 2
gbar_x = angle_mx + angle_r * 2 + gbar_mx
gbar_y = win_h - gbar_my - gbar_h
cvs.create_rectangle((gbar_x, gbar_y), (gbar_x + gbar_w, gbar_y + gbar_h), fill="white")
rbar_mx = round(gbar_h / 8)
rbar_my = rbar_mx
rbar_x = gbar_x + rbar_mx
rbar_y = gbar_y + rbar_my
power = 0
rbar_w = (gbar_w - rbar_mx * 2) * power / 100
rbar_h = gbar_h - rbar_my * 2
rbar = cvs.create_rectangle((rbar_x, rbar_y), (rbar_x + rbar_w, rbar_y + rbar_h), width=0, fill="red")

# Bomb
bomb_r = 10
bomb_v_max = 50
bomb_ay = 1

# Windbar
wbar_mx = gbar_mx
wbar_my = wbar_mx
wbar_w = wbar_mx * 8
wbar_h = wbar_my * 2
wbar_x = win_w - wbar_mx - wbar_w
wbar_y = wbar_my
cvs.create_rectangle((wbar_x, wbar_y), (wbar_x + wbar_w, wbar_y + wbar_h), width=2, fill="white")
cvs.create_line((round(wbar_x + wbar_w / 2), wbar_y), (round(wbar_x + wbar_w / 2), wbar_y + wbar_h), width=2)
wind = 0
wind_ax_max = 0.2
wind_ax = wind_ax_max * wind / 100
bbar_mx = round(wbar_h / 10)
bbar_my = bbar_mx
if wind >= 0:
    bbar_x = round(wbar_x + wbar_w / 2) + bbar_mx
else:
    bbar_x = round(wbar_x + wbar_w / 2) - bbar_mx
bbar_y = wbar_y + bbar_my
bbar_w = (wbar_w / 2 - 2 * bbar_mx) * wind / 100
bbar_h = wbar_h - 2 * bbar_my
bbar = cvs.create_rectangle((bbar_x, bbar_y), (bbar_x + bbar_w, bbar_y + bbar_h), width=0, fill="blue")

# Target
t_r = 40
t_range_x = (round(win_w / 3), win_w - t_r)
t_range_y = (wbar_y + wbar_h + t_r, top_h - t_r)
t_cx = random.randrange(t_range_x[0], t_range_x[1])
t_cy = random.randrange(t_range_y[0], t_range_y[1])
t_img = Image.open("apple.png")
t_img = t_img.resize((t_r * 4, t_r * 4), Image.LANCZOS)
t_img = ImageTk.PhotoImage(t_img, master=win)
target = cvs.create_image(t_cx, t_cy, image=t_img)

# Count box
cbox_x = wbar_mx
cbox_y = wbar_my
cbox_w = cbox_x * 3
cbox_h = wbar_h
cvs.create_rectangle((cbox_x, cbox_y), (cbox_x + cbox_w, cbox_y + cbox_h), fill="black", outline="red", width=2)
count = 0
c_box = cvs.create_text((round(cbox_x + cbox_w / 2), round(cbox_y + cbox_h / 2)), fill="white", font=("Arial", 30),
                        text=count)

win.update()

# OpenCV 윈도우 설정
cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)

while True:
    success, img = cap.read()
    if not success:
        print("웹캠을 읽을 수 없습니다.")
        break
    img = cv2.resize(img, (640, 480))

    # 손 추적 결과를 얻습니다
    hands, img = hand_detector.findHands(img, draw=True, flipType=True)

    # 포즈 추적을 위해 손이 감지된 경우에만 작업 수행
    if hands:
        hand = hands[0]
        hand_type = hand.get('type', None)
        img_hand = hand.get('image', img)
        if hand_type == 'Left':
            pose_points = (12, 14, 16)
        elif hand_type == 'Right':
            pose_points = (11, 13, 15)
        else:
            pose_points = (12, 14, 16)  # 기본값

        # 포즈 추적
        try:
            img_pose = pose_detector.findPose(img_hand, draw=False)
            lmList = pose_detector.findPosition(img_pose, draw=False)

            if len(lmList) > 0:
                # 각도 계산 (손의 종류에 따라 다른 포인트 사용)
                angle = pose_detector.findAngle(img_pose, *pose_points)

                if hand_type == 'Right':
                    angle = 360 - angle  # 오른손일 때 각도를 반전시킵니다

                per = np.interp(angle, (210, 310), (0, 100))
                power = per

                # 비율을 화면에 표시
                cv2.putText(img_pose, f'Power: {int(power)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)
        except Exception as e:
            print(f"포즈 추적 오류: {e}")  # 예외를 출력하고 계속 진행합니다

        # 손가락 펴진 상태 확인
        fingers_up = hand_detector.fingersUp(hand)
        fingers_up_count = fingers_up.count(1)  # 펴진 손가락 수 계산

        # 손가락 수를 화면에 표시
        cv2.putText(img, f'Fingers Up: {fingers_up_count}', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        # 손가락 수가 변경된 경우만 press 및 release 호출
        if previous_fingers_up_count != fingers_up_count:
            if fingers_up_count in [1, 2, 3]:
                press(fingers_up_count)
            elif fingers_up_count == 3 and stage == 2:
                # 게이지가 채워졌고 손가락이 3일 때 발사
                print("발사 조건 충족됨: power =", power)  # 디버깅
                space_go = True
            release(previous_fingers_up_count)
            previous_fingers_up_count = fingers_up_count
    else:
        # 손이 감지되지 않았을 때 손가락 수를 표시하지 않음
        cv2.putText(img, 'No hands detected', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # 결과 이미지를 표시합니다
    cv2.imshow("Webcam Feed", img)

    # 'q' 키를 눌러 창을 닫음
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.01)

    # 기존의 Tkinter 관련 코드 (게임 로직)
    cvs.delete(angle_line)
    cvs.delete(tank)
    cvs.delete(rbar)
    cvs.delete(bbar)
    try:
        cvs.delete(bomb)
    except:
        pass

    if stage == 1:
        if up_go and not down_go and angle_now <= angle_max:
            angle_now += 0.01
        elif down_go and not up_go and angle_now >= angle_min:
            angle_now -= 0.01
    if stage == 2:
        if space_go and power < 100:
            power += 1

    if stage == 3:
        wind_ax = wind_ax_max * wind / 100
        bomb_vx += wind_ax
        bomb_vy += bomb_ay
        bomb_cx += bomb_vx
        bomb_cy += bomb_vy
        dist = ((bomb_cx - t_cx) ** 2 + (bomb_cy - t_cy) ** 2) ** 0.5
        if dist <= bomb_r + t_r:
            hit = True
        if bomb_cy >= top_h or hit:
            stage = 1
            power = 0
            wind += random.randrange(-100, 101)
            if wind < -100:
                wind = -100
            elif wind > 100:
                wind = 100
            if hit:
                cvs.delete(target)
                cvs.delete(c_box)
                t_cx = random.randrange(t_range_x[0], t_range_x[1])
                t_cy = random.randrange(t_range_y[0], t_range_y[1])
                target = cvs.create_image(t_cx, t_cy, image=t_img)
                count += 1
                c_box = cvs.create_text((round(cbox_x + cbox_w / 2), round(cbox_y + cbox_h / 2)), fill="white",
                                        font=("Arial", 30), text=count)
                hit = False

    angle_line = cvs.create_line(angle_ctr, (angle_ctr[0] + angle_r * math.cos(angle_now), angle_ctr[1] - angle_r * math.sin(angle_now)), fill="red", width=3)
    tank_img = Image.open("canon.png")
    tank_img = tank_img.resize((tank_w, tank_h), Image.LANCZOS)
    tank_img = tank_img.rotate(angle_now * 180 / math.pi - 10)
    tank_img = ImageTk.PhotoImage(tank_img, master=win)
    tank = cvs.create_image(tank_cx, tank_cy, image=tank_img)
    rbar_w = (gbar_w - rbar_mx * 2) * power / 100
    if wind >= 0:
        bbar_x = round(wbar_x + wbar_w / 2) + bbar_mx
    else:
        bbar_x = round(wbar_x + wbar_w / 2) - bbar_mx
    bbar_w = (wbar_w / 2 - 2 * bbar_mx) * wind / 100
    if wind != 0:
        bbar = cvs.create_rectangle((bbar_x, bbar_y), (bbar_x + bbar_w, bbar_y + bbar_h), width=0, fill="blue")
    if power > 0:
        rbar = cvs.create_rectangle((rbar_x, rbar_y), (rbar_x + rbar_w, rbar_y + rbar_h), width=0, fill="red")
    if stage == 3:
        bomb = cvs.create_oval((bomb_cx - bomb_r, bomb_cy - bomb_r), (bomb_cx + bomb_r, bomb_cy + bomb_r), fill="red")

    win.update()

cap.release()
cv2.destroyAllWindows()

#该文件pic.py 与script.py互不干扰，纯纯打开摄像头的文件代码，作用是得到最新的摄像头图片，设置了3秒读取一张
#需要自己更改一下保存图片的路径save_path，否则不能运行
import cv2
import os
import time

# 设置保存图片的相对路径
save_path = "images"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 打开摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()
    
# 设置时间间隔（3秒）
interval = 3
last_saved_time = time.time()

while True:
    # 逐帧捕获
    ret, frame = cap.read()

    # 如果正确读取帧，ret为True
    if not ret:
        print("无法读取摄像头帧")
        break

    # 显示结果帧
    cv2.imshow('摄像头实时画面', frame)
    # 检查是否已过3秒
    if time.time() - last_saved_time > interval:
        cv2.imwrite(os.path.join(save_path, "1.jpg"), frame)
        last_saved_time = time.time()  # 更新最后保存时间

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 释放摄像头
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()

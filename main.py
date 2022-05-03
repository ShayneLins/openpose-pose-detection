#coding=utf-8
import pyopenpose as op
import math
import matplotlib.pyplot as plt
import cv2

import numpy
from PIL import Image, ImageDraw, ImageFont
 
def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, numpy.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)

def set_params():

    params = dict()
    params["logging_level"] = 3
    params["output_resolution"] = "-1x-1"
    params["net_resolution"] = "-1x368"
    params["model_pose"] = "BODY_25"
    params["alpha_pose"] = 0.6
    params["scale_gap"] = 0.3
    params["scale_number"] = 1
    params["render_threshold"] = 0.05
    params["num_gpu_start"] = 0
    params["disable_blending"] = False
    params["model_folder"] = "models/"
    return params

def main():

    time_begin = 20
    time_end = 54

    params = set_params()
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    stream = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    time_begin_flag = time_begin
    time_end_flag = time_end
    time_case_flag = 0
    time_youbaochi_flag = 0
    time_kaishi_flag = 0
    time_jieshu_flag = 0

    while True:

            datum = op.Datum()
            ret, img = stream.read()
            img_height = len(img)
            img_width = len(img[0])
            datum.cvInputData = img
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
#               print("Body keypoints: \n" + str(datum.poseKeypoints))
            
            try:

                people_num = len(datum.poseKeypoints)
                people_index = 0
                if people_num > 1:
                    people_flag1 = 10000
                    for i_people in range(0, people_num):
                        people_flag2 = abs((datum.poseKeypoints[i_people][1][0] -   img_width / 2) + (datum.poseKeypoints[i_people][1][1] - 1 * img_height / 3))
                        if people_flag2 < people_flag1:
                            people_flag1 = people_flag2
                            people_index = i_people

                point = datum.poseKeypoints[people_index]
                point_1x = point[1][0]
                point_1y = point[1][1]
                point_2x = point[8][0]
                point_2y = point[8][1]
                point_3x = point[0][0]
                point_3y = point[0][0]
                point_4x = point[0][0]
                point_4y = point[0][0]
                point_5x = point[1][0]
                point_5y = point[1][1]
                point_6x = point[17][0]
                point_6y = point[17][1]
                point_7x = point[0][0]
                point_7y = point[0][0]
                point_8x = point[0][0]
                point_8y = point[0][0]

                vector_12x = point_1x - point_2x
                vector_12y = point_1y - point_2y
                vector_34x = 1
                vector_34y = 0
                vector_56x = point_5x - point_6x
                vector_56y = point_5y - point_6y
                vector_78x = 1
                vector_78y = 0
                
                angle1 = math.atan2(vector_12y, vector_12x)
                angle1 = int(angle1 * 180 / math.pi)
                angle2 = math.atan2(vector_34y, vector_34x)
                angle2 = int(angle2 * 180 / math.pi)
                if angle1*angle2 >= 0:
                    included_angle1 = abs(angle1-angle2)
                else:
                    included_angle1 = abs(angle1) + abs(angle2)
                if included_angle1 > 180:
                    included_angle1 = 360 - included_angle1
                if (point_1x == 0.0 and point_1y == 0.0) or (point_2x == 0.0 and point_2y == 0.0):
                    included_angle1 = -1

                angle3 = math.atan2(vector_56y, vector_56x)
                angle3 = int(angle3 * 180 / math.pi)
                angle4 = math.atan2(vector_78y, vector_78x)
                angle4 = int(angle4 * 180 / math.pi)
                if angle3*angle4 >= 0:
                    included_angle2 = abs(angle3-angle4)
                else:
                    included_angle2 = abs(angle3) + abs(angle4)
                if included_angle2 > 180:
                    included_angle2 = 360 - included_angle2
                included_angle2 = included_angle2 + 0
                if (point_5x == 0.0 and point_5y == 0.0) or (point_6x == 0.0 and point_6y == 0.0):
                    included_angle2 = -1

#                text2 = '脊柱角度:' + str(included_angle1) + '°'
#                text3 = '头脖角度:' + str(included_angle2) + '°'
                text1 = ''
                text2 = ''
                text3 = ''

                if (point[7][1] < point[0][1] and point[7][1] > 0) or (point[4][1] < point[0][1] and point[4][1] > 0) or (point[6][1] < point[1][1] and point[6][1] > 0) or (point[3][1] < point[1][1] and point[3][1] > 0 ) and time_case_flag == 0:
                    time_begin_flag = time_begin_flag - 1
                else:
                    time_begin_flag = time_begin_flag + 1
                    if time_begin_flag > time_begin:
                        time_begin_flag = time_begin
                if time_begin_flag < 0:
                    time_begin_flag = 0
                    time_case_flag = 1
                    time_youbaochi_flag = 15
                if time_youbaochi_flag < 0:
                    time_case_flag = 2
                if time_youbaochi_flag > 15:
                    time_youbaochi_flag = 15
                if time_case_flag == 2:
                    time_end_flag = time_end_flag - 1
                    if time_end_flag < 0:
                        time_end_flag = 0

                if time_begin_flag >= time_begin and time_case_flag == 0:
                    text1 = ''
                    text2 = ''
                    text3 = '请举手三秒'
                elif time_begin - time_begin_flag < int(time_begin/3) and time_case_flag == 0:
                    text1 = ''
                    text2 = '3'
                    text3 = ''
                elif time_begin - time_begin_flag < int(2*time_begin/3) and time_begin - time_begin_flag >= int(time_begin/3) and time_case_flag == 0:
                    text1 = ''
                    text2 = '2'
                    text3 = ''
                elif time_begin - time_begin_flag < int(time_begin) and time_begin - time_begin_flag >= int(2*time_begin/3) and time_case_flag == 0:
                    text1 = ''
                    text2 = '1'
                    text3 = ''
                    time_kaishi_flag = int(2 * time_begin / 3)
                elif time_kaishi_flag > 0 and time_case_flag == 0:
                    text1 = ''
                    text2 = ''
                    text3 = '开始检测了'
                    time_kaishi_flag = time_kaishi_flag - 1

                elif (included_angle1 < 0 or included_angle2 < 0) and time_case_flag == 1:
                    text1 = '未检测到'
                    text2 = ''
                    text3 = ''
                elif included_angle1 <= 95 and included_angle1 >= 85 and included_angle2 <= 96 and included_angle2 >= 84 and time_case_flag == 1:
                    text1 = '姿势成绩：优'
                    text2 = ''
                    text3 = '请继续保持'
                    time_youbaochi_flag = time_youbaochi_flag - 1
                elif included_angle1 <= 105 and included_angle1 >= 75 and included_angle2 <= 106 and included_angle2 >= 74 and time_case_flag == 1:
                    time_youbaochi_flag = time_youbaochi_flag + 1
                    text1 = '姿势成绩：良'
                    text2 = ''
                    if included_angle2 > 96 or included_angle2 < 84:
                        text3 = '请挺直腰板'
                    if included_angle1 > 95:
                        text3 = '请不要后仰'
                    if included_angle1 < 85:
                        text3 = '请不要前倾'
                elif time_case_flag == 1:
                    time_youbaochi_flag = time_youbaochi_flag + 1
                    text1 = '姿势错误'
                    text2 = ''
                    if included_angle2 > 96 or included_angle2 < 84:
                        text3 = '请挺直腰板'
                    if included_angle1 > 95:
                        text3 = '请不要后仰'
                    if included_angle1 < 85:
                        text3 = '请不要前倾'

                elif time_end-time_end_flag < int(time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '9'
                    text3 = ''
                elif time_end-time_end_flag < int(2*time_end/9) and time_end-time_end_flag >= int(time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '8'
                    text3 = ''
                elif time_end-time_end_flag < int(3*time_end/9) and time_end-time_end_flag >= int(2*time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '7'
                    text3 = ''
                elif time_end-time_end_flag < int(4*time_end/9) and time_end-time_end_flag >= int(3*time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '6'
                    text3 = ''
                elif time_end-time_end_flag < int(5*time_end/9) and time_end-time_end_flag >= int(4*time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '5'
                    text3 = ''
                elif time_end-time_end_flag < int(6*time_end/9) and time_end-time_end_flag >= int(5*time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '4'
                    text3 = ''
                elif time_end-time_end_flag < int(7*time_end/9) and time_end-time_end_flag >= int(6*time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '3'
                    text3 = ''
                elif time_end-time_end_flag < int(8*time_end/9) and time_end-time_end_flag >= int(7*time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '2'
                    text3 = ''
                elif time_end-time_end_flag < int(time_end) and time_end-time_end_flag >= int(8*time_end/9) and time_case_flag == 2:
                    text1 = ''
                    text2 = '1'
                    text3 = ''
                    time_jieshu_flag = int(5*time_begin/9)
                elif time_jieshu_flag > 0 and time_case_flag == 2:
                    text1 = ''
                    text2 = ''
                    text3 = '你太棒了！'
                    time_jieshu_flag = time_jieshu_flag - 1
                    if time_jieshu_flag <= 0:
                        time_begin_flag = time_begin
                        time_end_flag = time_end
                        time_case_flag = 0
                        time_youbaochi_flag = 0
                        time_kaishi_flag = 0
                        time_jieshu_flag = 0

                out_win = "By Wang J.Y."
                out_pic = datum.cvOutputData
                cv2.namedWindow(out_win, cv2.WINDOW_NORMAL)
                cv2.setWindowProperty(out_win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                
#                    cv2.putText(out_pic, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                out_pic2 = cv2ImgAddText(out_pic, text1, 10, 10, (255, 0, 0), 50)
                out_pic3 = cv2ImgAddText(out_pic2, text2, int(img_width/2-10), int(img_height/2-40), (255, 0, 0), 60)
                out = cv2ImgAddText(out_pic3, text3, int(img_width/2)-100, int(img_height/2)-30, (255, 0, 0), 40)
                cv2.imshow(out_win, out)

                key = cv2.waitKey(1)
                if key==27:
                        break
                        
            except TypeError:
                continue
    stream.release()
    cv2.destroyAllWindows()

main()

import os
import sys

from PyQt5 import QtWidgets

import FaceDetect
import face_train
from ui import FaceIdentification
import Face_recognition


# 训练
def train_faceData():
    dataset = face_train.Dataset('./data/')
    dataset.load()
    model = face_train.Model()
    model.build_model(dataset)
    # 先前添加的测试build_model()函数的代码
    model.build_model(dataset)
    # 测试训练函数的代码
    model.train(dataset)
    # 储存训练模型
    model.save_model(file_path='./model/all.face.model.h5')
    # 评估模型
    model.load_model(file_path='./model/all.face.model.h5')
    model.evaluate(dataset)
    # os.system('python face_train.py')


# 识别
def identify():
    Face_recognition.execute_faceID()
    # os.system('python Face_recognition.py')


# 窗口
class my_window(QtWidgets.QMainWindow, FaceIdentification.Ui_FaceIdentification):
    def __init__(self):
        super(my_window, self).__init__()
        self.setupUi(self)
        # 将push button 和事件绑定
        self.identifyStart.clicked.connect(identify)
        self.recordStart.clicked.connect(self.pick_face)
        self.viewFaceData.clicked.connect(self.view_faceData)
        self.trainStart.clicked.connect(train_faceData)

    # 记录人脸数据信息
    def pick_face(self):
        try:
            name = self.faceNameEdit.text()
            face_num = eval(self.faceNumEdit.text())
            for i in name:
                if 256 < ord(i) or ord(i) < 0:
                    fail_result = r'名称只能是英文'
                    self.successTips.setText(fail_result)
                    return
            if 0 < face_num <= 1000:
                pathname = "./data\\" + name
                FaceDetect.mkdir(pathname)
                print(pathname)
                if len(sys.argv) != 1:
                    print("Usage:%s camera_id face_num_mapx path_name\r\n" % (sys.argv[0]))
                else:
                    FaceDetect.CatchPICFromVideo("Catch Your Face", 0, face_num, pathname)
                    success_result = r'当前面部信息记录成功！'
                    self.successTips.setText(success_result)
            else:
                fail_result = r'采集数越界！'
                self.successTips.setText(fail_result)
                return
        except:
            fail_result = '采集出错！\n注意信息不可为空！'
            self.successTips.setText(fail_result)

    # C:\Anaconda3\Lib\site - packages
    # 查看当前已经记录的人脸名称
    def view_faceData(self):
        face_data_path = './data'
        face_files = os.listdir(face_data_path)
        all_face = ""
        for face_file in face_files:
            all_face += face_file
            all_face += "  "
        self.allFaceData.setText(all_face)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = my_window()
    ui.show()
    sys.exit(app.exec_())

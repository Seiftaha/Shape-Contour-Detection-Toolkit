from PyQt5.QtWidgets import (QRadioButton, QMainWindow, QVBoxLayout, QWidget,QLabel,QFileDialog,
                             QHBoxLayout,QGridLayout,QPushButton,QLineEdit,QSlider,QGroupBox, 
                             QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import cv2






class Contour(QMainWindow):
    def __init__(self,main_window):
        super().__init__()
        self.setWindowTitle("Signal viewer")
        self.setGeometry(200,200,1500,1200)
        self.main_window=main_window
        self.image = None  # To store the loaded image
        self.equalized_image = None  # To store the loaded image



        self.initUI()

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QGridLayout()
        controls_layout = QVBoxLayout()

        group_box = QGroupBox()
        box_layout=QVBoxLayout()
        images_layout=QHBoxLayout()
        buttons_layout=QHBoxLayout()

        # Labels for images
        input_image_layout=QVBoxLayout()
        self.input_label = QLabel("Original Image")
        self.input_label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_label.setFixedSize(500, 500)
        self.color_mode = QRadioButton("Color")
        self.gray_mode = QRadioButton("Grayscale")
        self.color_mode.setChecked(True)  # Default mode is Color
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.color_mode)
        mode_layout.addWidget(self.gray_mode)
        input_image_layout.addWidget(self.input_label)
        input_image_layout.addLayout(mode_layout)

        self.output_label = QLabel("Equalized Image")
        self.output_label.setStyleSheet("background-color: black; border: 1px solid black;")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setFixedSize(500, 500)


        images_layout.addLayout(input_image_layout)
        images_layout.addWidget(self.output_label)

        self.upload_button = QPushButton("Upload Image")
        self.upload_button.setFixedWidth(150)
        self.reset_button=QPushButton("Reset")
        self.reset_button.setFixedWidth(150)
        self.save_button=QPushButton("Save")
        self.save_button.setFixedWidth(150)
        buttons_layout.addWidget(self.upload_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.reset_button)

        # Next pages buttons
        next_pages_buttons_layout=QHBoxLayout()
        self.home_page_button=QPushButton("Home page")
        self.home_page_button.clicked.connect(self.switch_to_home_page)
        self.home_page_button.setFixedWidth(150)
        next_pages_buttons_layout.addWidget(self.home_page_button)
        next_pages_buttons_layout.addStretch(1)

        box_layout.addLayout(next_pages_buttons_layout)
        box_layout.addStretch(1)
        box_layout.addLayout(images_layout)
        box_layout.addStretch(1)
        box_layout.addLayout(buttons_layout)
        box_layout.addStretch(1)
        group_box.setLayout(box_layout)




        # Mask selection 
        noise_menu_label=QLabel("Edge Detectors menu")
        noise_menu_label.setObjectName("menu")

        #  Sobel mask
        self.apply_sobel_button=QPushButton("Apply Sobel mask")

        # Prewitt mask
        self.apply_prewitt_button=QPushButton("Apply Prewitt mask")

        # Robert mask
        self.apply_robert_button=QPushButton("Apply Robert mask")

        # Canny mask
        high_layout=QHBoxLayout()
        high_layout.addWidget(QLabel("High threshold: "))
        self.high_input=QLineEdit()
        high_layout.addWidget(self.high_input)
        low_layout=QHBoxLayout()
        low_layout.addWidget(QLabel("Low threshold: "))
        self.low_input=QLineEdit()
        low_layout.addWidget(self.low_input)
        self.apply_canny_button=QPushButton("Apply Canny mask")

        self.histogram_CDF_button=QPushButton("Histogram and CDF")






        controls_layout.addWidget(noise_menu_label)
        controls_layout.addStretch(1)
        controls_layout.addWidget(QLabel("Sobel mask: "))
        controls_layout.addWidget(self.apply_sobel_button)
        controls_layout.addStretch(1)
        controls_layout.addStretch(1)
        controls_layout.addWidget(QLabel("Prewitt mask: "))
        controls_layout.addWidget(self.apply_prewitt_button)
        controls_layout.addStretch(1)
        controls_layout.addStretch(1)
        controls_layout.addWidget(QLabel("Robert mask: "))
        controls_layout.addWidget(self.apply_robert_button)
        controls_layout.addStretch(1)
        controls_layout.addStretch(1)
        controls_layout.addWidget(QLabel("Canny mask: "))
        controls_layout.addLayout(high_layout)
        controls_layout.addLayout(low_layout)
        controls_layout.addWidget(self.apply_canny_button)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.histogram_CDF_button)
        controls_layout.addStretch(1)

        # Connect buttons
        self.upload_button.clicked.connect(self.load_image)
        self.reset_button.clicked.connect(self.reset_images)
        self.save_button.clicked.connect(self.save_output_image)


        main_layout.addLayout(controls_layout,0,0)
        main_layout.addWidget(group_box,0,1)
        main_layout.setColumnStretch(1,2)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


        self.setStyleSheet("""
             QLabel{
                font-size:20px;
                color:black;     
                    }
            QLabel#menu{
                font-size:29px;
                color:black;
                           }
            QPushButton{
                    font-size:18px;
                    padding:10px;
                    border:white 1px solid;
                    border-radius:15px;
                    background-color:white;
                    color:black;         
                        }
        """)

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.tiff);;All Files (*)", options=options
        )

        if file_path:
            # Check which mode is selected
            if self.gray_mode.isChecked():
                self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
            else:
                self.image = cv2.imread(file_path, cv2.IMREAD_COLOR)  # Load as color (default)

            self.display_image(self.image, self.input_label)  # Display in input label

    def display_image(self, img, label):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img).scaled(label.width(), label.height(), Qt.KeepAspectRatio)
        label.setPixmap(pixmap)

    def reset_images(self):
        self.input_label.clear()  # Clear input image label
        self.output_label.clear()  # Clear output image label
        self.image = None  # Remove stored image
        self.equalized_image = None  # Remove stored output

    def save_output_image(self):
        if self.equalized_image is None:
            return  # No image to save
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options
        )
        
        if file_path:
            cv2.imwrite(file_path, self.equalized_image)  # Save using OpenCV

    def switch_to_home_page(self):
        self.main_window.stacked_widget.setCurrentIndex(0)




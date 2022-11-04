# import sys and os modules
import sys
import os
import re
from os import path
import urllib.request
import pafy # For YouTube Downloads
import humanize # For convert file size to human Readable


# import PyQt5 modules
from PyQt5.QtGui import *
# from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont
from PyQt5.QtCore import *
# from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QBoxLayout, QTextEdit, QCompleter
from PyQt5.uic import loadUiType


# For Fix SSL Error its important 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# For load on save Gui
FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"Download Videos.ui"))

# Intiate Ui File
class MainApp(QMainWindow , FORM_CLASS):
  def __init__(self, parent=None):
    # pafy.set_api_key("AIzaSyBVMRM6hTFiSJL5K5yCSpovgn82g2W55FU")
    super().__init__(parent)
    QMainWindow.__init__(self)
    self.setupUi(self)
    self.Handle_Ui()
    self.Handle_Buttons()
    

  def Handle_Ui(self):
    self.setWindowTitle("PyDownloader")
    self.setFixedSize(800, 411)
    
    

  def Handle_Buttons(self):
    # For Download Files 
    self.pushButton.clicked.connect(self.Download)
    self.pushButton_2.clicked.connect(self.Handle_Browse)
    # For YouTube Single Video
    self.pushButton_3.clicked.connect(self.Browse_File_location)
    self.pushButton_7.clicked.connect(self.Get_YouTube_Video_or_Details)
    self.pushButton_4.clicked.connect(self.Download_Video_or_Sound)
    # For Download youtube playlist
    self.pushButton_6.clicked.connect(self.Download_YouTube_Playlist)
    self.pushButton_5.clicked.connect(self.Browse_playlist_location)
    
    

  def Handle_Browse(self):
    save_place = QFileDialog.getSaveFileName(self, "Save As", "", "All(*)")
    if save_place is not None:
      self.lineEdit_2.setText(save_place[0])

# when push button is pressed, this method is called
  def Handle_Progress(self, blocknum, blocksize, totalsize):

      ## calculate the progress
      readed_data = blocknum * blocksize

      if totalsize > 0:
          download_percentage = readed_data * 100 / totalsize
          self.progressBar.setValue(download_percentage)
          QApplication.processEvents() # to fix not responding
    
  # For Download Files 
  def Download(self):
    url = self.lineEdit.text()
    file_name = self.lineEdit_2.text()
    try:
      urllib.request.urlretrieve(url, file_name, self.Handle_Progress)
      QMessageBox.information(self, "Download Status", "Download Complated .......")
        
    except Exception:
      QMessageBox.warning(self, "Error", "Download Faild")
    
    self.progressBar.setValue(0)
    self.lineEdit.setText("")
    self.lineEdit_2.setText("")
    
  # For YouTube Single Video
  
  def Browse_File_location(self):
    file_location = QFileDialog.getExistingDirectory(self, "Select Download Directory", "")
    if file_location is not None:
      self.lineEdit_4.setText(file_location)
  
  def Get_YouTube_Video_or_Details(self):
    url = self.lineEdit_3.text()
    video = pafy.new(url)
    streams = video.allstreams
    for s in streams:
      humanSize = humanize.naturalsize(s.get_filesize())
      data = "-- {} ,  {} ,  {} ,  {}".format(s.mediatype, s.extension, s.quality, humanSize)
      self.comboBox_2.addItem(data)
    
  def Download_Video_or_Sound(self):
    vid_or_sou_link = self.lineEdit_3.text()
    vid_or_sou_location = self.lineEdit_4.text()
    video_or_sound = pafy.new(vid_or_sou_link)
    quality = self.comboBox_2.currentIndex()
    
    chosen_stream = video_or_sound.allstreams[quality]
    chosen_stream.download(vid_or_sou_location)
    
  # For Download youtube playlist
  def Browse_playlist_location(self):
    file_location = QFileDialog.getExistingDirectory(self, "Select Download Directory", "")
    if file_location is not None:
      self.lineEdit_6.setText(file_location)
  
  def Download_YouTube_Playlist(self):
    playlist_url = self.lineEdit_5.text()
    playlist_location = self.lineEdit_6.text()
    get_playlist = pafy.get_playlist(playlist_url)
    videos = get_playlist["items"]
    
    os.chdir(str(playlist_location))
    if os.path.exists(str(get_playlist["title"])):
      os.chdir(str(get_playlist["title"]))
    else:
      os.mkdir(str(get_playlist["title"]))
      os.chdir(str(get_playlist["title"]))
    
    
    for video in videos:
      p = video["pafy"]
      best = p.getbest(preftype="mp4")
      best.download()

      
# main method to call our app
if __name__ == '__main__':
 
    # create app
    App = QApplication(sys.argv)
 
    # create the instance of our window
    window = MainApp()
 
    window.show()
    
    # start the app
    sys.exit(App.exec())
    
    
# def main():
#   app=QApplication(sys.argv)
#   window = MainApp()
#   window.show()
#   app.exec_()  # infinte loop


# if __name__ == "__main__":
#   main()

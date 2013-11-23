#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from content import *
from torrent import Torrent

__version__ ="1.0.1"

class MainWindow(QMainWindow):
    ''' Основное окно '''
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.setup()
        self.setWindowTitle(u"Видео-торрент")

    def setup(self):
        # работа с БД
        #db = QSqlDatabase.addDatabase("QSQLITE")
        #db.setDatabaseName("video.db")
        #if not db.open():
            #QMessageBox.warning(None, u"Видео",
                                #QString(u"Ошибка базы данных: %1").arg(db.lastError().text()))
            #sys.exit(1)

        # создание основного содержимого
        #self.content = Content(self)
        #self.content.setDB(db)
        self.setCentralWidget(self.content)
        
    def set_torrent(self, torrent):
        self.content = Content(self)
        self.content.set_torrent(torrent)
        self.connect(self.content.url.readButton, SIGNAL("clicked()"), self.read_torrent)
        self.connect(self.content.url.saveButton, SIGNAL("clicked()"), self.save_torrent)
    
    def read_torrent(self):
        if self.content.url.edit.text():
            url = self.content.url.edit.text()
            # прочитаем новое содержимое
            self.content.update(url)
            self.content.url.saveButton.setEnabled(True)
            
    def save_torrent(self):
        print "save torrent"
        self.content.save_db()
            

def main():
    #url = "pervyj-mstitel_captain-america-the-first-avenger-2011-bdrip-1080p-ot-youtracker-licenzija"
    #url = "virtuoznost_virtuosity-1995-hdrip-ot-rulya74"
    url = "http://rutor.org/torrent/318589/kolonija_dvojnaja-komanda_double-team-1997-bdrip-by-msltel-p-p2-a"
    #url = "chelovek-bez-proshlogo_mies-vailla-menneisyytt&auml"
    #url = "seksualnye-hroniki-francuzskoj-semi_chroniques-sexuelles-dune-famille-daujourdhui-2012-bdrip-1080p-uncut"
    
    app = QApplication(sys.argv)
    app.setApplicationName("Video torrent")
    torrent = Torrent()
    torrent.get_source(url)
    
    #print torrent.get_sql_insert()
    
    form = MainWindow()
    form.set_torrent(torrent.info)
    form.setup()
    form.setMinimumSize(800, 600)
    form.show()
    
    #torrent.save()
    torrent.close()
    
    sys.exit(app.exec_())

main()

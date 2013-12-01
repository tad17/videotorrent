#!/usr/bin/python
# -*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from torrent import Torrent

# основное содержимое

class Info():
    ''' список отдельных значений '''
    def __init__(self):
        self.content = {
            "title": u"<b>Название фильма<b>",
            "original": u"(оригинальное название)",}

    def label(self, name):
        value = self.content[name]
        label = QLabel(value)
        label.setAlignment(Qt.AlignCenter)
        return label


class Item(QWidget):

    '''одно значение'''
    def __init__(self, parent, label, value=None):
        QWidget.__init__(self, parent)
        self.lb = QLabel(label)
        self.ed = QLineEdit(value)

    def add(self, grid, nom):
        grid.addWidget(self.lb, nom, 0)
        grid.addWidget(self.ed, nom, 1)

    def setText(self, text):
        self.ed.setText(text)
        self.ed.setCursorPosition(0)

    def clear(self):
        self.ed.clear()

class URL(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)
        label = QLabel(u"URL:")
        self.edit = QLineEdit()
        self.readButton = QPushButton(u"Считать")
        self.saveButton = QPushButton(u"Сохранить")
        self.saveButton.setEnabled(False)

        # размещаем
        self.addWidget(label)
        self.addWidget(self.edit)
        self.addWidget(self.readButton)
        self.addWidget(self.saveButton)


class Content(QWidget):
    '''Детальная информация по фильму'''

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        info = Info()
        self.Title = info.label("title")
        self.Original = info.label("original")

        self.iCountry = Item(self, u"Страна")
        self.iYear = Item(self, u"Год выпуска:")
        self.iGenre = Item(self, u"Жанр:")
        self.iDuration = Item(self, u"Время фильма:")
        self.iTranslation = Item(self, u"Перевод:")
        self.iSubtitle = Item(self, u"Субтитры:")
        self.iDirector = Item(self, u"Режиссер:")
        self.iRoles = Item(self, u"В ролях:")
        self.iStudio = Item(self, u"Киностудия:")
        self.iQuantity = Item(self, u"Качество:")
        self.iVideo = Item(self, u"Видео:")
        self.iAudio = Item(self, u"Аудио:")

        layout = QVBoxLayout()
        layout.addWidget(self.Title)
        layout.addWidget(self.Original)
        hline = QLabel("<hr>")
        layout.addWidget(hline)

        # для детальной информации и картинки
        hlayout = QHBoxLayout()

        # для детальной информации
        grid = QGridLayout()
        self.iCountry.add(grid, 0)
        self.iYear.add(grid, 1)
        self.iGenre.add(grid, 2)
        self.iDuration.add(grid, 3)
        self.iTranslation.add(grid, 4)
        self.iSubtitle.add(grid, 5)
        self.iDirector.add(grid, 6)
        self.iRoles.add(grid, 7)
        self.iStudio.add(grid, 8)
        self.iQuantity.add(grid, 9)
        self.iVideo.add(grid, 10)
        self.iAudio.add(grid, 11)

        self.Description = QTextEdit()
        grid.addWidget(self.Description, 12, 0, 1, 2)

        self.Image = QImage()
        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)

        hlayout.addLayout(grid)
        hlayout.addWidget(self.imageLabel)

        layout.addLayout(hlayout)
        hline = QLabel("<hr>")
        layout.addWidget(hline)

        # url
        self.url = URL()
        layout.addLayout(self.url)

        # кнопки
        #buttonbox = QDialogButtonBox(QDialogButtonBox.Save |
                                        #QDialogButtonBox.Cancel)
        #buttonbox.button(QDialogButtonBox.Save).setDefault(True)
        #layout.addWidget(buttonbox)

        self.setLayout(layout)

    def setDB(self, db):
        self.db = db

        query = QSqlQuery()
        sql = '''
        SELECT
            id, title, original ,country, genre,
            year, duration, translation, director,
            subtitle, roles, description, studio,
            quantity, video, audio, img
        FROM video
        '''
        query.exec_(sql)
        query.next()
        #query.next()
        #query.next()
        if query.next():
            id = query.value(0).toInt()[0]
            title = unicode(query.value(1).toString())
            original = unicode(query.value(2).toString())
            country = unicode(query.value(3).toString())
            genre = unicode(query.value(4).toString())
            year = unicode(query.value(5).toString())
            duration = unicode(query.value(6).toString())
            translation = unicode(query.value(7).toString())
            director = unicode(query.value(8).toString())
            subtitle = unicode(query.value(9).toString())
            roles = unicode(query.value(10).toString())
            description = unicode(query.value(11).toString())
            studio = unicode(query.value(12).toString())
            quantity = unicode(query.value(13).toString())
            video = unicode(query.value(14).toString())
            audio = unicode(query.value(15).toString())
            img = unicode(query.value(16).toString())

            self.Title.setText("<b>%s</b>" % title)
            self.Original.setText(original)
            self.iCountry.setText(country)
            self.iGenre.setText(genre)
            self.iYear.setText(year)
            self.iDuration.setText(duration)
            self.iTranslation.setText(translation)
            self.iDirector.setText(director)
            self.iSubtitle.setText(subtitle)
            self.iRoles.setText(roles)
            self.Description.setText(description)
            self.iStudio.setText(studio)
            self.iQuantity.setText(quantity)
            self.iVideo.setText(video)
            self.iAudio.setText(audio)

            self.Image = QImage("images/%s" % img)
            width = 400
            height = 600
            self.Image.scaled(width, height, Qt.KeepAspectRatio)
            self.imageLabel.setPixmap(QPixmap.fromImage(self.Image))

    def save_db(self):
        "пока картинки не сохраняются ((("
        query = QSqlQuery()
        query.prepare("INSERT INTO video"
                      "(title, original, img, torrent, country, genre, year, duration, "
                      "translation, subtitle, director, roles, description, studio, "
                      "quantity, video, audio) "
                      "VALUES"
                      "(:title, :original, :img, :torrent, :country, :genre, :year, :duration, "
                      ":translation, :subtitle, :director, :roles, :description, :studio, "
                      ":quantity, :video, :audio) ")
        query.bindValue(":title", QVariant(QString(u"пока не сделано")))
        query.bindValue(":original", QVariant(QString(u"пока не сделано")))
        query.bindValue(":img", QVariant(QString(u"пока не сделано")))
        query.bindValue(":torrent", QVariant(QString(u"пока не сделано")))
        query.bindValue(":contry", QVariant(self.iCountry.ed.text()))
        query.bindValue(":genre", QVariant(self.iGenre.ed.text()))
        query.bindValue(":year", QVariant(self.iYear.ed.text()))
        query.bindValue(":duration", QVariant(self.iDuration.ed.text()))
        query.bindValue(":translation", QVariant(self.iTranslation.ed.text()))
        query.bindValue(":subtitle", QVariant(self.iSubtitle.ed.text()))
        query.bindValue(":director", QVariant(self.iDirector.ed.text()))
        query.bindValue(":roles", QVariant(self.iRoles.ed.text()))
        query.bindValue(":description", QVariant(self.iDirector.ed.text()))
        query.bindValue(":studio", QVariant(self.iStudio.ed.text()))
        query.bindValue(":quantity", QVariant(self.iQuantity.ed.text()))
        query.bindValue(":video", QVariant(self.iVideo.ed.text()))
        query.bindValue(":audio", QVariant(self.iAudio.ed.text()))
        query.exec_()


    def clear(self):
        self.Title.clear()
        self.Original.clear()
        self.iCountry.clear()
        self.iGenre.clear()
        self.iYear.clear()
        self.iDuration.clear()
        self.iTranslation.clear()
        self.iDirector.clear()
        self.iSubtitle.clear()
        self.iRoles.clear()
        self.Description.clear()
        self.iStudio.clear()
        self.iQuantity.clear()
        self.iVideo.clear()
        self.iAudio.clear()

    def set_torrent(self, torrent):
        self.Title.setText("<b>%s</b>" % QString(torrent["title"]))
        self.Original.setText(QString(torrent["original"]))
        self.iCountry.setText(torrent["country"])
        self.iGenre.setText(torrent["genre"])
        self.iYear.setText(torrent["year"])
        self.iDuration.setText(torrent["duration"])
        self.iTranslation.setText(torrent["translation"])
        self.iDirector.setText(torrent["director"])
        self.iSubtitle.setText(torrent["subtitle"])
        self.iRoles.setText(torrent["roles"])
        self.Description.setText(torrent["description"])
        self.iStudio.setText(torrent["studio"])
        self.iQuantity.setText(torrent["quantity"])
        self.iVideo.setText(torrent["video"])
        self.iAudio.setText(torrent["audio"])

        self.Image = QImage("./images/%s" % torrent["img"])
        width = 800
        height = 600
        self.Image.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.Image))

    def update(self, url):
        # сначала очистим содержимое
        self.clear()
        torrent = Torrent()
        torrent.get_source(url)
        self.set_torrent(torrent.info)

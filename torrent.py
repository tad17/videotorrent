#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import shutil
from lxml import html
import urllib

from PyQt4.QtSql import *

CREATE_TABLE = '''
	create table if not exists video (
		id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                url VARCHAR(255) NOT NULL,
		title VARCHAR(255) NOT NULL,
		original VARCHAR(255),
		img VARCHAR(255),
		torrent VARCHAR(255),
		country VARCHAR(255),
		genre VARCHAR(255),
		year INTEGER,
		duration VARCHAR(20),
		translation VARCHAR(255),
		subtitle VARCHAR(255),
		director VARCHAR(255),
		roles VARCHAR(255),
		description VARCHAR(255),
		studio VARCHAR(255),
		quantity VARCHAR(50),
		video VARCHAR(100),
		audio VARCHAR(100));'''


class Torrent():
    ''' основная работа с торрентом'''
    
    def __init__(self):
        #proxy = {'http': 'http://127.0.0.1:5865'}
        #url = "http://rutor.org/torrent/311342/seksualnye-hroniki-francuzskoj-semi_chroniques-sexuelles-dune-famille-daujourdhui-2012-bdrip-1080p-uncut"
        #page = urllib.urlopen(url, proxies=proxy).read().decode('utf-8')
        
        self.info = {
            'id': "",
            'url': "",
            'title': "",
            'original': "",
            'country': "",
            'genre': "",
            'year': "",
            'duration': "",
            'translation': "",
            'subtitle': "",
            'director': "",
            'roles': "",
            'description': "",
            'studio': "",
            'quantity': "",
            'video': "",
            'audio': "",
            'img': "",
            'torrent': "",
        }
        
        self.params = {
            'title': [u'Название'],
            'original': [u'Оригинальное название'],
            'country': [u'Страна'],
            'genre': [u'Жанр'],
            'year': [u'Год выпуска', u'Год выхода'],
            'duration': [u'Продолжительность'],
            'translation': [u'Перевод'],
            'subtitle': [u'Субтитры'],
            'director': [u'Режиссер'],
            'roles': [u'В ролях'],
            'description': [u'Описание', u'О фильме'],
            'studio': [u'Выпущено'],
            'quantity': [u'Качество видео', u'Качество'],
            'video': [u'Формат видео', u'Формат', u'Видео', u'Кодек'],
            'audio': [u'Озвучивание', u'Аудио', u'Звук']}
        
        self.open_database()
        
    def open_database(self, db_name="video.db"):
        # =========== Откроем базу данных ==================
        self.db_name = db_name
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)
        if not self.db.open():
            print "Database error %s" % self.db.lastError().text()
            sys.exit(1)
            
        # создадим таблицу, если еще нет такой
        #print "создание таблицы"
        sql = CREATE_TABLE
        query = QSqlQuery()
        if not query.exec_(sql):
            print query.lastError().text()
            sys.exit(1)

    def get_source(self, url):
        # ========== получение данных =================
        self.url = url
        page = open(self.url).read().decode('utf-8')
        self.xmldata = html.document_fromstring(page)
        
        self.get_title()
        self.get_torrent()
        self.get_detail()
        self.get_img()

    def get_title(self):
        #================== определение названия =================
        title_all = self.xmldata.xpath('//h1/text()')[0].split('/')
        self.info['title'] = title_all[0].strip()
        self.info['original'] = title_all[-1].strip()

    def get_torrent(self):
        #=================== загрузка торрента ====================
        hrefs = self.xmldata.xpath('//div[@id="download"]/a')
        for href in hrefs:
            torrent = href.get('href').strip()
            if "/download/" in torrent:
                #print "[torrent]: %s" % torrent
                if torrent:
                        filename, headers = urllib.urlretrieve(torrent)
                        shutil.copy(filename, './torrent')
                        self.info['torrent'] = os.path.basename(filename)

    def get_detail(self):
        #=================== детальная информация =================
        # Выборка всех строк таблицы
        rows = self.xmldata.xpath('//table[@id="details"]/tr')
        
        # Выбираем только текст, без учета внутренних тэгов
        # типа <b></br>  и т.п.
        # Пока обрабатываем только первую строку таблицы
        alltext = rows[0].xpath('descendant-or-self::text()')
        is_value = False
        param = ''
        for item in alltext:
            text = item.strip().strip(':').strip()
            # интересуют только непустые строки
            if text:
                if is_value:
                    # значение параметра
                    is_value, value = False, text
                    # готово для дальнейшей обработки
                    #print "[%s]: %s" % (param, value)
                    self.info[param] = value
        
                # просматриваем все параметры
                for key in self.params:
                    # проверяем все возможные альтернативы написания
                    if text in self.params[key]:
                        # есть такой параметр
                        is_value, param = True, key
                        break
        
    def get_img(self):
        # =========== Выбираем url изображения (постер) =================
        img = self.xmldata.xpath('//table[@id="details"]/tr/td/img')[0].get('src')
        self.info['img'] = img
        print "url изображения: %s" % img
        if img:
                filename, headers = urllib.urlretrieve(img)
                shutil.copy(filename, './images')
                #self.info['img'] = os.path.basename(filename)
                self.info['img'] = "tmp79QsXW.jpg"
                
    def get_sql_insert(self):
        #=========== печатаем, что получилось ============================
        keys = ''
        values = ''
        for key, value in self.info.items():
            print "[%s] = %s" % (key, value)
            try:
                #print type(value)
                if type(value) == unicode:
                    #print "------------- unicode ---------------"
                    values += ', "%s"' % value
                else:
                    values += ', "%s"' % value.decode('utf-8', errors='replace')
                keys += ', %s' % key
            except:
                print "ошибка кодировки строки %s" % value.__repr__()
                
        d1 = ",".join(self.info.keys())
        d2 = ",".join('"%s"' % f for f in self.info.values())
        sql = "insert into video (%s) values (%s)" % (d1, d2)
        return sql

    def save(self):
        query = QSqlQuery()
        # выполним вставку записи
        if not query.exec_(self.get_sql_insert()):
            print query.lastError().text()
            
    def close(self):
        self.db.close()


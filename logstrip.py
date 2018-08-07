#!/usr/bin/python
# coding: utf-8
#创建时间：2018年8月6日
#auther:韩世勤


# -------------------------------------------------------------------------------
# Filename:    logstrip.py
# Revision:    v1.1
# Create Date:        2018/08/06
# -------------------------------------------------------------------------------
# Copyright:   2018 (c) hanshiqin
# License:     GPL
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# you should have received a copy of the GNU General Public License
# along with this program (or with Nagios);
#
# Credits go to Ethan Galstad for coding Nagios
# If any changes are made to this script, please mail me a copy of the changes
# -------------------------------------------------------------------------------
#Version 1.0 2018年8月6日


import logging, logging.handlers
import os,sys,datetime,time,re,shutil

workhome='/data/works'
logpath='/tmp/jarlog/mylog.log'
yesterday=(datetime.datetime.now()-datetime.timedelta(days = 1)).date().strftime("%Y-%m-%d")


def comdate(str):
    #匹配日期
    re1=re.compile('\d{4}-\d{1,2}-\d{1,2}')
    if re.findall(re1, str):
        return 'ok'
    else:
        return 'no'


def test_TimedRotatingFileHandler(filepath):
    if not os.path.isfile(filepath):
        try:
            os.makedirs(os.path.dirname(filepath))
        except Exception as e:
            file=open(filepath,'w')
            file.close()

    # 定义日志输出格式
    fmt_str = '%(asctime)s[level-%(levelname)s][%(name)s]:%(message)s'
    # 初始化
    logging.basicConfig(level=logging.DEBUG)

    # 创建TimedRotatingFileHandler处理对象
    # 间隔5(S)创建新的名称为myLog%Y%m%d_%H%M%S.log的文件，并一直占用myLog文件。
    fileshandle = logging.handlers.TimedRotatingFileHandler(filepath, when='D', interval=7, backupCount=7)
    # 设置日志文件后缀，以当前时间作为日志文件后缀名。
    fileshandle.suffix = "%Y%m%d_%H%M%S.log"
    # 设置日志输出级别和格式
    fileshandle.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt_str)
    fileshandle.setFormatter(formatter)
    # 添加到日志处理对象集合
    logging.getLogger('').addHandler(fileshandle)


def shelp():
    print('''
            本脚本的用途：实现某一目录下的多个文件中的日志分割
            本脚本有2个自定义变量 workhome logpath
            workhome 指定一个或多个jar包放置的上级目录位置
            logpath  指定日志分割日志的位置
            配置好后使用crontab 定时实现日志分割

        ''')

def comdate(str):
    re1=re.compile('\d{4}-\d{1,2}-\d{1,2}')
    if re.findall(re1, str):
        return 'ok'
    else:
        return 'no'



def listdir_nohidden(path,format):
    #传入路径和格式，格式为文件file或目录dir
    for i in os.listdir(path):
        if format=='dir':
            if os.path.isdir(i) and not i.startswith('.'):
                yield i
        elif format=='file':
            if os.path.isfile(i) and not i.startswith('.'):
                yield i
        else:
            shelp()


def movefile(srcfile,dstfile):
    #从源文件中复制内容到新文件中，并清空默认文件
    if not os.path.isfile(srcfile):
        logging.info("%s not exist!"%(srcfile))
    else:
        if os.path.isfile(dstfile):
            logging.info('{0}已经创建过了'.format(dstfile))
        else:
            shutil.copy(srcfile,dstfile)
            logging.info("copy %s -> %s"%( srcfile,dstfile))
            os.system(">{0}".format(srcfile))





if __name__=='__main__':
    test_TimedRotatingFileHandler(logpath)
    os.chdir(workhome)
    iterdir=listdir_nohidden(workhome,'dir')
    for i in iterdir:
        os.chdir(i+'/logs')
        for i in listdir_nohidden('.','file'):
            logging.info('----{0}-------'.format(i))
            if comdate(i)=='ok':
                pass
            elif comdate(i)=='no':
                logging.info('to copy the file {0} to {1}'.format(i,i.rstrip('.log')+yesterday+'.log\n'))
                if os.path.getsize(i):
                    movefile(i,i.rstrip('.log')+'_'+yesterday+'.log')
                else:
                    logging.info('{0} is empty'.format(i))
            else:
                logging.info('{0}文件名称不符合'.format(i))
        os.chdir(workhome)
    shelp()



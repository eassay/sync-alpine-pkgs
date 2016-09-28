# -*- coding: utf-8 -*-
"""
@auth: chenping
@desc: 用于下载alpine apk文件，建立和本地镜像
"""

import urllib2, re, logging, os, threading
import argparse
import traceback

download_err_pkgs=[]

def main(pkg_url, threadnum, timeout, downloadroot):
    """主函数"""
    init_logging()
    
    logging.info("下载仓库URL：%s" % pkg_url)
    logging.info("下载线程数：%d" % threadnum)
    logging.info("下载超时时间：%d" % timeout)
    logging.info("下载到本地目录：%s" % downloadroot)
    logging.info(u"开始下载alpine安装包...")
    
    if not os.path.exists(downloadroot):
        os.makedirs(downloadroot)

    packages = get_all_pkgs(pkg_url)
    download_in_threads(threadnum, timeout, packages, downloadroot)

    if len(download_err_pkgs) != 0:
        logging.info(u"进行第二次下载安装包...")
        download_in_threads(threadnum, timeout, download_err_pkgs, downloadroot)
    
    logging.info(u"下载任务结束!")
    
def init_logging():
    """"""
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename = 'run.log', level = logging.DEBUG, format = formatter)
    
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter(formatter))
    
    rootlogger = logging.getLogger()
    rootlogger.addHandler(sh)
    
def get_all_pkgs(pkg_url):
    """根据仓库地址,获取所有的安装包URL"""
    _data = urllib2.urlopen(pkg_url)
    
    html_content = None
    req_code = _data.getcode()
    if req_code == 200:
        html_content = _data.fp.read()
    else:
        logging.error(u"打开URL:[%s]失败! HTTP Response code is: %s" % (pkg_url, req_code))
        return []
        
    a_tags = re.findall('<a href=".+">[a-zA-Z0-9\.\-_+]+</a>', html_content)

    packages = []
    for _a_tag in a_tags:
        tag_val = re.search('>[a-zA-Z0-9\.\-_+]+</a>', _a_tag).group(0)
        pkg_name = tag_val.replace(">", "").replace("</a", "")
        temp = _a_tag.replace(tag_val, "")
        href = temp.replace("<a href=", "").strip('"')

        _package = Package()
        _package.Url = pkg_url + href
        _package.PackageName = pkg_name
        
        packages.append(_package)
    
    logging.info(u"共抓取到安装包数目为:%d" % len(packages))
    return packages

def download_pkg(package, timeout, pkgroot):
    """"""
    pkgfilepath = os.path.join(pkgroot, package.PackageName)
    if os.path.exists(pkgfilepath):
        logging.info(u"%s 已经存在!" % package.PackageName)
        return

    logging.info(u"开始下载 [%s] --> [%s]" %(package.Url, pkgfilepath))
    
    _data = urllib2.urlopen(package.Url, timeout=timeout)
    retCode = _data.getcode()
    if retCode == 200:
        try:
            with open(pkgfilepath, "wb") as downloadfileobj:
                downloadfileobj.write(_data.fp.read())
                logging.info(u"下载安装包 %s 成功!" % package.PackageName)
        except Exception, e:
            logging.error(u"下载安装包 %s 失败!\n%s" % (package.PackageName, traceback.format_exc()))
            download_err_pkgs.append(package)
            os.remove(pkgfilepath)
    else:
        logging.error(u"下载安装包 %s 失败!HTTP 返回码是:%d" %(package.PackageName, retCode))

def download_in_threads(threadnum, timeout, packages, downloadroot):
    """"""
    logging.info(u"准备在线程池中执行安装包下载任务...")
    
    threadlist = []
    for _pkg in packages:
        downloadthread = threading.Thread(target=download_pkg, args=(_pkg, timeout, downloadroot))
        downloadthread.start()
        
        threadlist.append(downloadthread)
        if len(threadlist) > threadnum:
            wait_one_thread_exit(threadlist)
    
    wait_all_thread_exit(threadlist)
    logging.info(u"全部下载线程均已经退出!")        
        
def wait_one_thread_exit(threadlist):
    """"""
    import time
    while(True):
        for _thread in threadlist:
            if _thread.isAlive() == False:
                threadlist.remove(_thread)
                logging.debug(u"检测到一个线程退出!")
                return
        time.sleep(1)

def wait_all_thread_exit(threadlist):
    """"""
    for _thread in threadlist:
        if _thread.isAlive() == True:
            _thread.join()

class Package:
    def __init__(self):
        self.Url = None
        self.PackageName = None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pkgurl', dest="pkg_url", help=u"输入需要下载的安装包仓库地址")
    parser.add_argument('--threadnum', type=int, dest="threadnum", help=u"设置下载线程数")
    parser.add_argument('--timeout', type=int, dest="timeout", help=u'设置下载超时时间')
    parser.add_argument('--downloadroot', dest="downloadroot",  help=u"设置下载文件的存放路径")
    
    args = parser.parse_args()
    
    main(args.pkg_url, 
         args.threadnum,
         args.timeout, 
         args.downloadroot)
    pass
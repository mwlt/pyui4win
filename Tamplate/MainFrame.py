# __author__ = 'generated by py-ui4win'
import sys
import string, os, time
import threading
from ctypes import *

# from PyUI import *
from PyFrameBase import *
from CommonUtil import *
import win32con


class COPYDATASTRUCT(Structure):
    _fields_ = [('dwData', POINTER(c_uint)),
                ('cbData', c_uint),
                ('lpData', c_char_p)]


PCOPYDATASTRUCT = POINTER(COPYDATASTRUCT)

def addsxx(a:int, b:int) -> int:
    return a+b

class MainFrame(PyFrameBase):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.clsName = self.__class__.__name__  # 不要改动
        self.skinFileName = self.__class__.__name__ + '.xml'  # 不要改动

    # 准备显示前的处理
    def OnPrepare(self, sendor, wParam, lParam):
        self.minbtn = self.PyFindButton("minbtn")
        self.maxbtn = self.PyFindButton("maxbtn")
        self.restorebtn = self.PyFindButton("restorebtn")
        self.closebtn = self.PyFindButton("closebtn")
        self.btnOpenLog = self.PyFindButton("btnOpenLog")
        self.btnClearLog = self.PyFindButton("btnClearLog")
        self.btnExcute = self.PyFindButton("btnExcute")
        self.OU_home = self.PyFindOption("OU_home")
        self.OU_back = self.PyFindOption("OU_back")
        self.OU_forward = self.PyFindOption("OU_forward")
        self.OU_genPwd3 = self.PyFindOption("OU_genPwd3")
        self.OU_genPwd4 = self.PyFindOption("OU_genPwd4")
        self.OU_genPwd5 = self.PyFindOption("OU_genPwd5")
        self.OU_genPwd6 = self.PyFindOption("OU_genPwd6")
        self.OU_enableProxy = self.PyFindOption("OU_enableProxy")
        self.OU_disableProxy = self.PyFindOption("OU_disableProxy")
        self.txtDiagnose = self.PyFindRichEdit("txtDiagnose")
        self.AnimationJuhua1 = self.PyFindAnimation("AnimationJuhua1")
        self.HLU_caption = self.PyFindHorizontalLayout("HLU_caption")
        self.DriverDiagnoseTab = self.PyFindVerticalLayout("DriverDiagnoseTab")
        self.TLU_client = self.PyFindTabLayout("TLU_client")

    # 退出处理
    def OnClose(self, uMsg, wParam, lParam):
        ctypes.windll.kernel32.ExitProcess(0)
        return 0

    def minbtn_click(self, sendor, sType, wParam, lParam):
        self.MinimizeWindow()

    def maxbtn_click(self, sendor, sType, wParam, lParam):
        self.MaximizeWindow()

    def btnOpenLog_click(self, sendor, sType, wParam, lParam):
        print(PyWin32Util.GetExeDirectory())
        applog = PyWin32Util.GetExeDirectory() + '\\applog\\applog.ini'
        print(applog)
        if os.path.isfile(applog):
            windll.Shell32.ShellExecuteW(0, 'open',applog, None, None, 1)

    def restorebtn_click(self, sendor, sType, wParam, lParam):
        self.RestoreWindow()

    def closebtn_click(self, sendor, sType, wParam, lParam):
        self.CloseWindow()

    def btnClearLog_click(self, sendor, sType, wParam, lParam):
        self.txtDiagnose.SetText('')
        applog = PyWin32Util.GetExeDirectory() + '\\applog\\applog.ini'
        if os.path.isfile(applog):
            os.remove(applog)

    def btnExcute_click(self, sendor, sType, wParam, lParam):
        def PyThreadPythonExecute():
            try:
                self._StartAnimation()
                self._ExecutePython()
            except Exception as e:
                PyLog().LogText(str(traceback.format_exc()))
            self._StopAnimation()
            PyLog().LogText('PyThreadExecute exit')

        # 多线程测试
        t = threading.Thread(target=PyThreadPythonExecute)
        t.start()

        # ctypes测试
        windll.user32.MessageBoxW(0, "中文", "Your title", win32con.MB_YESNO)
        windll.user32.MessageBoxA(0, "中文".encode('gbk'), "Your title".encode('gbk'), win32con.MB_YESNO)

        # win32gui测试
        import win32gui
        win32gui.MessageBox(self.GetHWnd(),
                '中文', 'Your title',
                win32con.MB_YESNO | win32con.MB_ICONINFORMATION |
                win32con.MB_SYSTEMMODAL)

        (a, b, c) = win32gui.GetOpenFileNameW()
        print(a, b, c)
        win32gui.MessageBox(self.GetHWnd(),
                a, str(b),
                win32con.MB_YESNO | win32con.MB_ICONINFORMATION |
                win32con.MB_SYSTEMMODAL)


        # 进程间消息测试
        hwnd = windll.user32.FindWindowW(None, '计算器')
        if windll.user32.IsWindow(hwnd):
            msgstr = '计算器' + '\0'
            print(len(msgstr))

            msgbytes = msgstr.encode('utf-8')
            copydata = COPYDATASTRUCT(None, len(msgbytes), msgbytes)
            for i in range(1, 2):
                # time.sleep(1)
                PyLog().LogText('%d'%i)
                windll.user32.SendMessageA(hwnd, 0x4a, None, byref(copydata))

    # 界面事件处理
    def OnNotifyInternal(self, sendor, sType, wParam, lParam):
        # 用户点击事件
        if sType == DUI_MSGTYPE_CLICK:
            if hasattr(self, '{}_click'.format(sendor)):
                getattr(self, '{}_click'.format(sendor))(sendor, sType, wParam, lParam)
            
        # 用户选择事件
        if sType == DUI_MSGTYPE_ITEMSELECT:
            pass

    def _StopAnimation(self):
        self.AnimationJuhua1.StopAnimation()

    def _StartAnimation(self):
        self.AnimationJuhua1.StartAnimation()

    def AppendAndLog(self, line):
        PyLog().LogText( line)
        msg = self.txtDiagnose.GetText()
        print(type(msg))
        print(msg)
        print(G2U(msg))
        self.txtDiagnose.SetText(U2G(G2U(msg) + '\n' + line))

    def ShowAndLog(self, line):
        PyLog().LogText( line)
        self.txtDiagnose.SetText(line)

    def _ExecutePython(self):
        CommonUtils.ReverseToExePath()
        ISOTIMEFORMAT='%Y-%m-%d %X'
        self.ShowAndLog(time.strftime( ISOTIMEFORMAT, time.localtime() ))

        i = 0
        while i < 50:

            hwnd = windll.user32.FindWindowW(None, '计算器')
            if windll.user32.IsWindow(hwnd):
                msgstr = '计算器' + '\0'
                # print(len(msgstr))

                msgbytes = msgstr.encode('utf-8')
                copydata = COPYDATASTRUCT(None, len(msgbytes), msgbytes)
                for j in range(1, 200):
                    # PyLog().LogText('%d'%i)
                    
                    windll.user32.SendMessageA(hwnd, 0x4a, None, byref(copydata))

            self.AppendAndLog('等待 %d 秒' % i)
            time.sleep(1)
            i = i + 1

        self.AppendAndLog('python线程运行结束')

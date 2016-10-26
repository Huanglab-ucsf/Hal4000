import numpy as np
import ctypes
from ctypes import windll, cdll, create_string_buffer

libLocation = 'C:\\Users\\Public\\Documents\\PI\\E-709\\Samples\\C++\\First_steps\\'

pidll = windll.LoadLibrary(libLocation+'PI_GCS2_DLL.dll')

#Functions:
connectUSB = pidll.__getattr__('PI_ConnectUSB') #Arg: char* szDescription
connectRS232 = pidll.__getattr__('PI_ConnectRS232') #Args: int iPortNum, int Baudrate
closeConnection = pidll.__getattr__('PI_CloseConnection') #Arg: int ID
enumerateUSB = pidll.__getattr__('PI_EnumerateUSB') #Args: char* szBuffer, int iBufferSize, char* szFilter
getError = pidll.__getattr__('PI_GetError') #Arg: int ID
isConnected = pidll.__getattr__('PI_IsConnected') #Arg: int ID
gcsCommandset = pidll.__getattr__('PI_GcsCommandset')
gcsGetAnswer = pidll.__getattr__('PI_GcsGetAnswer')
gcsGetAnswerSize = pidll.__getattr__('PI_GcsGetAnswerSize')
translateError = pidll.__getattr__('PI_TranslateError') #Args: int iErrorNum, char* szErrorMesg, int buffsize

aos = pidll.__getattr__('PI_AOS') #Sets offset to analog input for given axis
atz = pidll.__getattr__('PI_ATZ') #Automatic zero-point calibration

isMoving = pidll.__getattr__('PI_IsMoving')

svo = pidll.__getattr__('PI_SVO') #Sets servo mode
qSVO = pidll.__getattr__('PI_qSVO') #(long ID, const char* szAxes, BOOL* pbValueArray)

qSai = pidll.__getattr__('PI_qSAI') #get name of connect axis

#Stop all motion
stp = pidll.__getattr__('PI_STP') # long ID, const char* szAxes

#Move
mov = pidll.__getattr__('PI_MOV') #Args: int ID, char* szAxes, double* pdValueArray

#Move relative
mvr = pidll.__getattr__('PI_MVR') #Same args as mov

qAOS = pidll.__getattr__('PI_qAOS') #get analog input offset

qONT = pidll.__getattr__('PI_qONT') #check if axes have reached the target

pos = pidll.__getattr__('PI_POS') #(long ID, const char* szAxes, const double* pdValueArray);
qPOS = pidll.__getattr__('PI_qPOS') #check current position

qTMN = pidll.__getattr__('PI_qTMN') #Get minimum travel range
qTMX = pidll.__getattr__('PI_qTMX') #Get maximum travel range

vel = pidll.__getattr__('PI_VEL') #Sets velocity during moves; only works in closed-loop (servo on)
qVEL = pidll.__getattr__('PI_qVEL') #(long ID, const char* szAxes, double* pdValueArray)

qHLP = pidll.__getattr__('PI_qHLP') #Args: int ID, char* szBuffer, int sizebuffer
qHPA = pidll.__getattr__('PI_qHPA') #same args as qHLP

def call_enumerateUSB():
    buff = create_string_buffer(30)
    return enumerateUSB(buff, ctypes.c_int(30), ""), buff.value
    

def call_connectRS232(port):
    portNum = ctypes.c_int(port)
    baudrate = ctypes.c_int(57600)
    return connectRS232(portNum, baudrate)

def call_getError(ID):
    iError = getError(ctypes.c_int(ID))
    szErrorMesg = create_string_buffer(1024)
    translateError(iError, szErrorMesg, ctypes.c_int(1024))
    return szErrorMesg.value
    
def call_qhlp(device): #gets help string
    szBuffer = create_string_buffer(4096)
    qHLP(device, szBuffer, ctypes.c_int(4096))
    return szBuffer.value
    
def call_qhla(device): #gets help string
    szBuffer = create_string_buffer(4096)
    qHLA(device, szBuffer, ctypes.c_int(4096))
    return szBuffer.value


def call_closeConnection(device):
    return closeConnection(ctypes.c_int(device))

def call_qsai(device):
    buff = create_string_buffer(17)
    return qSai(device, buff, 16), buff.value

def call_mov(device, position_value):
    position = (ctypes.c_double * 1)()
    position[0] = position_value
    axis = create_string_buffer('1\n')
    return mov(device, axis, position)

def call_mvr(device, position_value):
    position = (ctypes.c_double * 1)()
    position[0] = position_value
    axis = create_string_buffer('1\n')
    return mvr(device, axis, position)

def call_isMoving(device):
    axis = create_string_buffer('1\n')
    moving = (ctypes.c_bool * 1)()
    return isMoving(device, axis, moving), moving

def call_qont(device):
    axis = create_string_buffer('1\n')
    ontarget = (ctypes.c_bool * 1)()
    return qONT(device, axis, ontarget), ontarget
    
def call_qpos(device):
    pos = (ctypes.c_double * 1)()
    axis = create_string_buffer('1\n')
    return qPOS(device, axis, pos), pos

def call_qtmn(device):
    posmin = (ctypes.c_double * 1)()
    axis = create_string_buffer('1\n')
    return qTMN(device, axis, posmin), posmin

def call_qtmx(device):
    posmax = (ctypes.c_double * 1)()
    axis = create_string_buffer('1\n')
    return qTMN(device, axis, posmax), posmax

def call_vel(device, velocity_value):
    velocity = (ctypes.c_double * 1)()
    velocity[0] = velocity_value
    axis = create_string_buffer('1\n')
    return vel(device, axis, velocity)

def call_qvel(device):
    velocity = (ctypes.c_double * 1)()
    axis = create_string_buffer('1\n')
    return qVEL(device, axis, velocity), velocity

def call_svo(device, onoff):
    bFlags = (ctypes.c_bool * 1)()
    if onoff:
        bFlags[0] = True
    else:
        bFlags[0] = False
    axis = create_string_buffer('1\n')
    return svo(device, axis, bFlags)

def call_qsvo(device):
    axis = create_string_buffer('1\n')
    svo = (ctypes.c_bool * 1)()
    return qSVO(device, axis, svo), svo
    
def call_stp(device):
    axis = create_string_buffer('1\n')
    return stp(devce, axis)

    


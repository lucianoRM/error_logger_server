import json
import random
import string

import time
from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.words = ['zadgkxjeib', 'jfchhplzzx', 'nygcluenkm', 'abbnxolzrv', 'bxccgpngey', 'jntyrpelre', 'skadjdmeju', 'vhzrardblv', 'fexfqugplm', 'efjmqrxdtx', 'efodxywzog', 'mfhslgubzr', 'ysmxhijlrr', 'vncchikyol', 'jstkxyrxvr', 'wqwzrwoofd', 'vyvehdurbt', 'esvlnfvpkh', 'qxgtsntpfq', 'eflxadntvi', 'mzzvqfvcja', 'bhkngffnoa', 'lcnjbvipav', 'vvhbehknay', 'efdvscavob', 'ivdiygzzsm', 'ctmkiakkdh', 'yocwaxdimv', 'aoaedlukbc', 'wbemghvrcu', 'fgrdmyiehc', 'vkienffpzn', 'gzpqxajwdo', 'guhlrbaeds', 'okblntujfv', 'thjlwttefv', 'zpdslqfefq', 'vxofxlpcga', 'msmjmrfoyj', 'mvygongjlm', 'mvdehhfwix', 'wzxucmlnum', 'cnromdoffd', 'ghvuumnabp', 'mokmwczvmu', 'odnwcpehkt', 'sfhhuwrauy', 'bxzfnhgbkc', 'ohhffbuqbh', 'vfernuwysv', 'qjugxwlwic', 'godgfvxzep', 'waipjrtiic', 'ybbqumtaje', 'danhwzxmhl', 'oxxophxlim', 'todwopreup', 'edgfpdbbtx', 'vtwivmgefs', 'nvqgrogtmx', 'fwjrhodxxc', 'nhucqyazas', 'qohqzxtbwz', 'vyywvidwqo', 'ytaduascul', 'gcmesrpoxe', 'rfzvqglegg', 'oywmwjdwji', 'aawtluuquk', 'kekhgcylch', 'uxnvwpbaif', 'rhsohadufa', 'ewdkkerqkq', 'etfwaegjyz', 'rdhalrzvtz', 'tyvbstlfpe', 'tzeozjwcfs', 'kyqxpdcjry', 'amwfhwuzpv', 'rlyrcavyzs', 'yhoillbtar', 'xacqjjswxj', 'gplwrgitwm', 'chiitpgebp', 'vvmrkfdcbc', 'msrnefpozh', 'wvzbuluhzg', 'yzhavyoxtt', 'xbmhxwktxb', 'yqyuwfdjfi', 'juvfiozsha', 'tvxqmydhdo', 'dkprlbuwrl', 'qksfievmtm', 'sljolhnaqx', 'uahqufujjz', 'ypiyljrtya', 'zwiljfhyoe', 'snkrfhruus', 'rujlxdkksz', 'qpexcvkubl', 'cempddsuoz', 'decbsoecfw', 'mhajpjxjvs', 'hyqttqyqnp', 'kydprscdjo', 'ieweccvcgo', 'gxijeepymi', 'moktmjzncd', 'nsqvsyitxp', 'ycuaxooycg', 'eutslorvjh', 'dlgghuscdg', 'rqfxsjitwp', 'wrfoziptys', 'tjajgqeaqb', 'zzfcdcimpd', 'xfdtsxwtbu', 'qpuxhssglg', 'plvcjsazgo', 'zeltqdaynm', 'xtanlmshgd', 'vznoeonqwx', 'pukostfeyj', 'krgkafkhee', 'zieixjnqlb', 'ikeymeccpy', 'vzkhveqttx', 'lspfglurqb', 'jojcbissly', 'zufbwnwdex', 'tmiqcfbokf', 'ommcgxstsz', 'xiglosgczi', 'hvluqwaith', 'idzqoczssc', 'jpbuigpysi', 'yhsaoqbrji', 'fauvuahols', 'sfxxmbyvwi', 'vpqspjbugy', 'zopmylnlkz', 'bvjoejtkfe', 'yfumlubjky', 'jirelmqzhd', 'ddughqfjhd', 'rsxqccatum', 'xarroqeiqm', 'xszcierusk', 'jmgqysoxew', 'cddinkdwqo', 'jbnnophknz', 'rplhjuaglq', 'kwiausslys', 'izqwkjfrai', 'ygsegsyste', 'fcmwnwpybi', 'yheghgkcfm', 'ruwnqxqayx', 'jvhjlvupke', 'ltdmzsvhxk', 'fslkltclzt', 'zpkungozmn', 'gomhbqnszu', 'oxduvveqef', 'hpvmguriqw', 'zfagtodgnv', 'lfcglknmen', 'ograokvsvy', 'kzvdtdwoto', 'vjcfgpnxzq', 'ufaryqwnmm', 'agkuunwnbp', 'jfrafnenva', 'gmrlbjerjr', 'jzealvtxal', 'osqsrwdrik', 'axappajjqa', 'durvrettjv', 'vpuhbkknql', 'fcgmaitaua', 'lqvfazbdmt', 'fkokeipksf', 'wgeshemsbb', 'kieaxhjvbp', 'gfdmcljgjy', 'kkyitfjxfz', 'mwojdrmsol', 'akxtlauvad', 'clhzdrxamo', 'ewswhxbviq', 'ryxevpdfjn', 'miybwxnrch', 'pwhwbyxyno', 'cetlhvdyfi', 'qqvrkplwlr', 'tpocnfbmpy', 'vkfzaydnxx', 'juofspuhlk', 'mopkbzwlkf']

    def login(self):
        self.client.post("/login", {"username":"ellen_key", "password":"education"})


    @task(1)
    def sendError(self):
        dicc = {
            "userName" : "luciano",
            "appName" : random.choice(self.words),
            "timestamp" : int(time.time()),
            "os" : "Linux",
            "errorText" : "Error!"
        }
        self.client.post('/errors',json=json.dumps(dicc))

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 2000
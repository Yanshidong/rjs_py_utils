import time
from io import TextIOWrapper, BufferedReader

import chardet


class JsTransfer:
    def fun_utils(self):
        return 'window.rjs_blobToDataURI=function(blob,res_token){var reader=new FileReader();reader.readAsDataURL(blob);reader.onload=function(e){console.log(e.target.result);if(res_token!==undefined){window.RjsData[res_token]=e.target.result}}};window.rjs_dataURItoBlob=function(base64Data){var byteString;if(base64Data.split(",")[0].indexOf("base64")>=0){byteString=atob(base64Data.split(",")[1])}else{byteString=unescape(base64Data.split(",")[1])}var mimeString=base64Data.split(",")[0].split(":")[1].split(";")[0];var ia=new Uint8Array(byteString.length);for(var i=0;i<byteString.length;i++){ia[i]=byteString.charCodeAt(i)}var blob=new Blob([ia],{type:mimeString});return blob};window.rjs_any_beauty=function(obj,res_token){if(res_token===undefined){res_token=Math.random()+""}if(window.RjsData===undefined){window.RjsData={}}if(obj instanceof Blob){window.rjs_blobToDataURI(obj,res_token)}else{if(typeof obj==="number"){window.RjsData[res_token]=obj}else{if(typeof obj==="boolean"){window.RjsData[res_token]=obj}else{if(typeof obj==="string"){window.RjsData[res_token]=obj}}}}return res_token};window.rjs_beauty_any=function(obj){if(obj instanceof Blob){return obj}else{if(typeof obj==="number"){return obj}else{if(typeof obj==="boolean"){return obj}else{if(typeof obj==="string"){if(obj.indexOf("data:")===0){return window.rjs_dataURItoBlob(obj)}return obj}else{return obj}}}}};'
    def data_utils(self):
        return 'if(window.RjsTableUtils===undefined)window.RjsTableUtils=null;if(window.RjsDB===undefined)window.RjsDB=null;if(window.RjsData===undefined)window.RjsData={};'
    def back2hell(self,hell_key):
        while self.driver.execute_script('return window.RjsData["'+hell_key+'"]') is None:
            print('等待异步回调结果:'+hell_key)
            time.sleep(0.1)
        print('等待结束----获取到返回值----:'+hell_key)
        # 处理 undefined情况
        res = self.driver.execute_script('return window.RjsData["' + hell_key + '"]')
        if res == "rjsUndefined": return None
        return res
    def pv2jv(self,pv):
        if isinstance(pv, bool):
            return 'true' if pv else 'false'
        elif isinstance(pv, int):
            return str(pv)
        elif isinstance(pv, float):
            return str(pv)
        elif isinstance(pv, str):
            return '"' + (pv.replace('"', '\\"')) + '"'
        elif isinstance(pv, TextIOWrapper):
            file_str = ''
            type_f = pv.name.split('__rjs__').pop().replace('.', '/')
            if type_f is None or type_f == '': type_f = 'text/plain'
            for line_str in pv.readlines():
                line_str = line_str.replace('\n', '\\n')
                file_str += self.pv2jv(line_str) if file_str == '' else ',' + self.pv2jv(line_str)
            return 'new Blob([' + file_str + '],{"type":' + self.pv2jv(type_f) + '})'
        elif isinstance(pv, BufferedReader):
            file_str = ''
            type_f = pv.name.split('__rjs__').pop().replace('.', '/')
            if type_f is None or type_f == '': type_f = 'text/plain'
            encoding = None
            for line_str in pv.readlines():
                if encoding == None: encoding = chardet.detect(line_str)['encoding']
                if encoding == None: encoding = 'utf-8'
                line_str = str(line_str).lstrip('b').strip("'")
                file_str += self.pv2jv(line_str) if file_str == '' else ',' + self.pv2jv(line_str)
            return 'new Blob([' + file_str + '],{"type":' + self.pv2jv(type_f) + '})'
        elif isinstance(pv, set):
            return str(pv)
        elif isinstance(pv, tuple):
            return str(tuple)
        elif type(pv).__name__ == 'dict':
            return self.dic2str(pv)
        elif isinstance(pv, list):
            res = ''
            for v1 in pv:
                res = res +(self.pv2jv(v1) if res=='' else ','+self.pv2jv(v1))
            return '['+res+']'
    def dic2str(self, dic):
        res = '{'
        for key, value in dic.items():
            res = (res if res == '{' else res + ',') + self.pv2jv(key) + ':' + self.pv2jv(value)
        return res + '}'

    def __init__(self,driver) -> None:
        super().__init__()
        self.driver=driver

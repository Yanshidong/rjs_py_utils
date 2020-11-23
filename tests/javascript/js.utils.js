window.rjs_blobToDataURI = function (blob,res_token) {
   var reader = new FileReader();
   reader.readAsDataURL(blob);
   reader.onload = function (e) {
       console.log(e.target.result);
       if(res_token!==undefined)window.RjsData[res_token]=e.target.result;
   };
};

window.rjs_dataURItoBlob=function(base64Data) {
    var byteString;
    if(base64Data.split(",")[0].indexOf("base64") >= 0)
        byteString = atob(base64Data.split(",")[1])
    else{
        byteString = unescape(base64Data.split(",")[1]);
    };
    var mimeString = base64Data.split(",")[0].split(":")[1].split(";")[0];
    var ia = new Uint8Array(byteString.length);//¥¥Ω® ”Õº
    for(var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    };
    var blob = new Blob([ia], {
        type: mimeString
    });
    return blob;
};
window.rjs_any_beauty = function (obj,res_token){
    if(res_token===undefined)res_token=Math.random()+"";
    if(window.RjsData===undefined)window.RjsData={}
    if(obj instanceof Blob){
        window.rjs_blobToDataURI(obj,res_token);
    }else if(typeof obj ==="number"){
        window.RjsData[res_token]=obj
    }else if(typeof  obj ==="boolean"){
        window.RjsData[res_token]=obj
    }else if(typeof  obj ==="string"){
        window.RjsData[res_token]=obj
    }
    return res_token
};
window.rjs_any_beauty = function (obj,res_token){
    if(res_token===undefined)res_token=Math.random()+"";
    if(window.RjsData===undefined)window.RjsData={}
    if(obj instanceof Blob){
        window.rjs_blobToDataURI(obj,res_token);
    }else if(typeof obj ==="number"){
        window.RjsData[res_token]=obj
    }else if(typeof  obj ==="boolean"){
        window.RjsData[res_token]=obj
    }else if(typeof  obj ==="string"){
        window.RjsData[res_token]=obj
    }
    return res_token
};
window.rjs_beauty_any = function (obj){
    if(obj instanceof Blob){
        return obj;
    }else if(typeof obj ==="number"){
        return obj;
    }else if(typeof  obj ==="boolean"){
        return obj;
    }else if(typeof  obj ==="string"){
        if(obj.indexOf('data:')===0){
            return window.rjs_dataURItoBlob(obj);
        }
        return obj;
    }else {
        return obj;
    }
}
window.rjs_jv2pv=function (obj){
    var res ={"type":"any","value":obj}
    if(typeof obj ==="number"){
        if(~~obj===obj){
            res['type']='int'
        }else{
            res['type']='float'
        }
    }else if(typeof  obj ==="boolean"){
        res['type']='bool';
    }else if(typeof  obj ==="string"){
        if(obj.indexOf('data:')===0){
            res['type']='blob';
        }else{
            res['type']='str';
        }
    }else if(typeof obj ==='object') {
        res['type']='dict';
        res['value']=window.rjs_jv2pv()
    }
    return res
}
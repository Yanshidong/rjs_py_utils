var res=Math.random()+"";
var transaction=window.RjsTableUtils.transaction(["keyvaluepairs"],"readwrite");
transaction.onsuccess=function(event){console.log("[Transaction] 好了!")};
var studentsStore=transaction.objectStore("keyvaluepairs");
studentsStore.get("dic").onsuccess=function(event){window.rjs_any_beauty(event.target.result===undefined?"rjsUndefined":event.target.result,res);
window.RjsData[res]=event.target.result;
console.log("res:",event.target.result)};

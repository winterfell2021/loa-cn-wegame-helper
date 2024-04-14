# Tech
- 反编译
    - blackdex
    - dex修复
- jdax-gui打开，搜关键词Gh-Header找到函数`com.xx.xx.netscene.m9.j`
- 发现`com.xx.xx.netscene.base.i`这个类有个getUrl方法，直接上 frida hook 下
```
function showStacks() {
    console.log(
        Java.use("android.util.Log")
            .getStackTraceString(
                Java.use("java.lang.Throwable").$new()
            )
    );
}
function main() {
    Java.perform(function () {
        var m9 = Java.use("com.xx.xx.netscene.m9")
        m9.j.overload('com.xx.xx.netscene.base.j').implementation = function (iVar) {
             console.log(iVar.getUrl())
             showStacks()
             this.j(iVar)
        }
    })
}

setImmediate(main)
```

点一个item，结果发现确实是这里
```
-> https://xx.com/game/detailinfov2
[object Object]
java.lang.Throwable
        at com.xx.xx.netscene.m9.f(Native Method)
        at com.xx.xx.netscene.m9.h(SceneCenter.java:1)
        at com.xx.xx.netscene.m9.k(SceneCenter.java)
        at com.xx.xx.netscene.m9.a(SceneCenter.java)
        at com.xx.xx.netscene.m9$a.run(SceneCenter.java)
        at com.xx.bible.utils.thread.ThreadPool$i.run(ThreadPool.java:6)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1133)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:607)
        at java.lang.Thread.run(Thread.java:761)
        at com.xx.bible.utils.thread.d$a.run(PriorityThreadFactory.java:2)
```
- 整个函数是包在线程里run的，最终跟踪到`com.xx.xx.netscene.base.a.u1`，发现所有请求都会继承这个类，hook onParamBuilded函数能看到请求参数

```
function print_map(map) {
    var HashMap = Java.use('java.util.HashMap');
    console.log("map：" + Java.cast(map, HashMap).toString());
}
var u1 = Java.use("com.xx.xx.netscene.u1")
        u1.onParamBuilded.implementation = function (map) {
            console.log(this.getUrl())
            print_map(map)
            this.onParamBuilded(map)
}
```
- 回到`com.xx.xx.netscene.m9`，看到Content-Type的header以及控制加解密的头，完成
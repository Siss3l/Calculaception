"use strict";
try {
    const res = Memory.scanSync(Process.enumerateModulesSync()[0].base, Process.enumerateModulesSync()[0].size,
        "windows-feedback:?contextid=130&metadata=%7B%22Metadata%22:[%7B%22AppBuild%22:%22".split("").map(i => { return i.charCodeAt(0).toString(16); }).join(" 00 "));
    if (typeof JSON.stringify(res[0]) !== "undefined") {
        let pointer = ptr(res[0].address);
        if (!pointer.isNull()) {
            Memory.protect(pointer, 0x01, "rw-");
            pointer = ptr(res[0].address).writeByteArray([0x43, 0x00, 0x61, 0x00, 0x6c, 0x00, 0x63, 0x00, 0x75, 0x00, 0x6c, 0x00, 0x61, 0x00, 0x74, 0x00, 0x6f, 0x00, 0x72, 0x00, 0x3a]);
            console.info(hexdump(ptr(res[0].address), { offset: 0, length: res[0].size, header: true, ansi: false }));
        } else {
            send("Pointer is null.");
        }
    } else {
        send("Memory is undefined.");
    }
    new NativeFunction(Module.getExportByName("kernel32.dll", "FreeLibrary"), "bool", ["pointer"]);
    (Process.getModuleByName("frida-agent.dll").base);
} catch (err) {
    send(err);
}

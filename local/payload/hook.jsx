"use strict";
try {
    let proc  = Process.enumerateModulesSync().find(x => x.name.toLowerCase() === "calculator.exe" || x.name.toLowerCase() === "calculatorapp.dll");
    const res = Memory.scanSync(proc.base, proc.size, "77 00 69 00 6E 00 64 00 6F 00 77 00 73 00 2D 00 66 00 65 00" +
                                "65 00 64 00 62 00 61 00 63 00 6B 00 3A 00 3F 00 63 00 6F 00" +
                                "6E 00 74 00 65 00 78 00 74 00 69 00 64 00 3D 00 31 00 33 00" +
                                "30 00 26 00 6D 00 65 00 74 00 61 00 64 00 61 00 74 00 61 00" +
                                "3D 00 25 00 37 00 42 00 25 00 32 00 32 00 4D 00 65 00 74 00" +
                                "61 00 64 00 61 00 74 00 61 00 25 00 32 00 32 00 3A 00 5B 00" +
                                "25 00 37 00 42 00 25 00 32 00 32 00 41 00 70 00 70 00 42 00" +
                                "75 00 69 00 6C 00 64 00 25 00 32 00 32");
    if (typeof JSON.stringify(res[0]) !== "undefined") {
        let pointer = ptr(res[0].address);
        if (!pointer.isNull()) {
            Memory.protect(pointer, 0x01, "rw-");
            pointer = ptr(res[0].address).writeByteArray([0x43, 0x00, 0x61, 0x00, 0x6c, 0x00, 0x63, 0x00, 0x75, 0x00, 0x6c, 0x00, 0x61, 0x00, 0x74, 0x00, 0x6f, 0x00, 0x72, 0x00, 0x3a]);
            console.info(hexdump(ptr(res[0].address), { offset: 0, length: res[0].size, header: true, ansi: false }));
        } else {
            send("Pointer is null");
        }
    } else {
        send("Memory is down");
    }
    new NativeFunction(Module.getExportByName("kernel32.dll", "FreeLibrary"), "bool", ["pointer"]);
    (Process.getModuleByName("frida-agent.dll").base);
} catch (err) {
    send(err);
}

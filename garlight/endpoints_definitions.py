def create_definitions(devices: list[str]) -> str:
    functions = ["on-off", "set_timer", "set_warm", "set_color"]
    definitions = "- all, All\n" + "".join(
        f"-- {device.lower()},{device.capitalize()}\n" +
        "".join(f"--- {device}_{func},{func},{func.lower()}/{device.lower()}\n"
                for func in functions)
        for device in devices
    )
    return definitions

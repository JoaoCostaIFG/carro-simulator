import asyncio
from gui import GuiApp


def main():
    gui: GuiApp = GuiApp()

    asyncio.run(gui.async_run())


if __name__ == '__main__':
    asyncio.run(main())

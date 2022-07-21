from src import utility
from src import effectmanager
from src import audiomanager
from src import effectwindow
from src import mainwindow
import threading


class Effects:
    LOADED_EFFECTS = []
    ENABLED = []

    @staticmethod
    def addEffect(c, n):
        if not n in Effects.ENABLED:
            try:
                Effects.LOADED_EFFECTS.append({"name": n, "class": c()})
                Effects.ENABLED.append(n)
                print('Effect "' + n + '" has been loaded.')
            except Exception as e:
                print('Error while loading effect "' + n + '". An error has occurred: ' + str(e))


if __name__ == '__main__':

    #mainwindow.mainWindow().run()

    effectwindow.EffectWindow()
    effectmanager.EffectManager().loadEffects()

    audiomanager.Audio()
    audiomanager_thread = threading.Thread(target=audiomanager.Audio.audioReadStarter)
    audiomanager_thread.start()

    if len(effectmanager.EffectManager.effects.ENABLED) > 0:
        effectmanager.EffectManager().startEffect(input(str(effectmanager.EffectManager.effects.ENABLED) + " » "))
    else:
        utility.mprint("There is no effect loaded!")

    while True:
        effectwindow.EffectWindow.updateWindow()

    audiomanager.Audio.stopStream()

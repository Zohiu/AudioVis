from src import utility
from src import audiomanager
from src import effectwindow
import importlib
import os


class Effects:
    utility.mprint("Effects class is being loaded.")
    LOADED_EFFECTS = []
    ENABLED = []

    @staticmethod
    def addEffect(c, n):
        if n not in Effects.ENABLED:
            try:
                for i in ["start", "update", "stop"]:
                    test = getattr(c, i, None)
                    if not callable(test):
                        raise Exception('Invalid effect! The "Effect" class is missing the function "' + i + '"')

                Effects.LOADED_EFFECTS.append({"name": n, "class": c()})
                Effects.ENABLED.append(n)
                utility.mprint('Effect "' + n + '" has been loaded.')
            except Exception as e:
                try:
                    Effects.LOADED_EFFECTS.remove({"name": n, "class": c()})
                    Effects.ENABLED.remove(n)
                except:
                    pass

                utility.mprint('Error while loading effect "' + n + '".\nAn error has occurred: ' + str(e))


class EffectManager:
    utility.mprint("EffectManager class is being loaded.")
    effects = Effects()
    current_effect = None

    @staticmethod
    def loadEffects():
        for root, dirs, files in os.walk("Effects"):
            for file in files:
                # append the file name to the list
                if file.split(".")[1] == "py" and file.split(".")[0] != "__init__":
                    root = root.replace("/", ".").replace("\\", ".")
                    effect = root + "." + file.split(".")[0]
                    name = file.split(".")[0]

                    try:
                        globals()[effect] = importlib.import_module(effect)
                        EffectManager.effects.addEffect(globals()[effect].Effect, name[0].upper() + name[1:])
                    except Exception as e:
                        utility.mprint('Error while loading effect "' + name + '".\nAn error has occurred: The effect is missing the "Effect" class')

    @staticmethod
    def startEffect(effect):
        if effect in EffectManager.effects.ENABLED:
            try:
                for i in EffectManager.effects.LOADED_EFFECTS:
                    if i["name"] == effect:
                        EffectManager.current_effect = i
                        EffectManager.current_effect["class"].start(effectwindow.EffectWindow.wn,
                                                             effectwindow.EffectWindow.WIDTH,
                                                             effectwindow.EffectWindow.HEIGHT,)
                        utility.mprint("Started effect " + '"' + EffectManager.current_effect["name"] + '"')
                        break

                if EffectManager.current_effect == None:
                    utility.mprint('Error while starting effect "' + effect + '".\nAn error has occurred: Effect was not found!')
                    return

            except Exception as e:
                utility.mprint('Error while starting effect "' + effect + '".\nAn error has occurred: ' + str(e))
        else:
            utility.mprint(
                'Error while starting effect "' + effect + '".\nAn error has occurred: Effect does not exist!')

    @staticmethod
    def loopEffect(screen):
        if EffectManager.current_effect["name"] is not None:
            try:
                EffectManager.current_effect["class"].update(screen,
                                                             effectwindow.EffectWindow.WIDTH,
                                                             effectwindow.EffectWindow.HEIGHT,
                                                             audiomanager.Audio.OUTPUT["RAW"],
                                                             audiomanager.Audio.OUTPUT["FREQ"],
                                                             audiomanager.Audio.OUTPUT["VOL"],
                                                             audiomanager.Audio.OUTPUT["PEAK"],
                                                             audiomanager.Audio.OUTPUT["BASS"],
                                                             audiomanager.Audio.OUTPUT["MID"],
                                                             audiomanager.Audio.OUTPUT["HIGH"],)
            except Exception as e:
                utility.mprint('Error while running effect "' + EffectManager.current_effect["name"] + '".\nAn error has occurred: ' + str(e))
                raise e
                EffectManager.stopEffect()

    @staticmethod
    def stopEffect():
        if EffectManager.current_effect["name"] is not None:
            EffectManager.current_effect["class"].stop(effectwindow.EffectWindow.wn,
                                                             effectwindow.EffectWindow.WIDTH,
                                                             effectwindow.EffectWindow.HEIGHT,)
            utility.mprint("Stopped effect " + '"' + EffectManager.current_effect["name"] + '"')
            EffectManager.current_effect = None
from random import randint, choice
from tkinter import Canvas, Tk, mainloop
import numpy as np


class Terrain:

    def __init__(self, master=None):
        self.terr = np.array([
                           [0]*4
                           ]*4)
        self.master = master
        self.canvas = Canvas(self.master)
        sq_0 = Square()
        nsq = [
            choice(np.where(self.terr == 0)[0]),
            choice(np.where(self.terr == 0)[0])
            ]
        self.terr[nsq[0], nsq[1]] = sq_0.value

    def display(self):
        color = {
            0: 'white', 2: "#%02x%02x%02x" % (238, 228, 219),
            4: "#%02x%02x%02x" % (238, 223, 200),
            8: "#%02x%02x%02x" % (242, 177, 121),
            16: "#%02x%02x%02x" % (236, 141, 85),
            32: "#%02x%02x%02x" % (247, 123, 95),
            64: "#%02x%02x%02x" % (234, 90, 56),
            128: "#%02x%02x%02x" % (238, 206, 105),
            256: "#%02x%02x%02x" % (242, 208, 75),
            512: "#%02x%02x%02x" % (242, 208, 75),
            1024: "#%02x%02x%02x" % (227, 186, 20),
            2048: "#%02x%02x%02x" % (236, 196, 2),
            4096: "#%02x%02x%02x" % (96, 217, 146)
        }
        for i in range(4):
            for j in range(4):
                self.rectangle = self.canvas.create_rectangle(
                            i*50, j*50, (i+1)*50, (j+1)*50,
                            fill=color[self.terr[j, i]]
                            )
                if self.terr[j, i] == 0:
                    fil = "white"
                else:
                    fil = "black"
                self.label = self.canvas.create_text(
                            i*50 + 25, j*50 + 25,
                            text=self.terr[j, i],
                            fill=fil)
        self.canvas.pack(padx=50, pady=50)

    def swip(self, serie):
        # pdv swip droite
        non_nul = serie[serie > 0]
        if len(non_nul) > 1:
            for i in range(-1, -len(non_nul), -1):
                if non_nul[i] == non_nul[i-1]:
                    non_nul[i] = 2 * non_nul[i]
                    non_nul[i-1] = 0
        serie = np.concatenate((
                        serie[serie == 0],
                        non_nul[non_nul == 0],
                        non_nul[non_nul > 0]
                    ), axis=None)
        return serie

    def move_up(self, event):
        print(event.keysym)
        check = 0
        # SWIP INVERSE
        for col in range(4):
            terr_ini = np.flipud(self.terr[:, col])
            if all(self.swip(terr_ini) == terr_ini):
                pass
            else:
                self.terr[:, col] = np.flipud(self.swip(terr_ini))
                check += 1
        # AJOUT CARRE
        if check != 0:
            sq = Square()
            rand = randint(0, len(np.where(self.terr == 0)[0])-1)
            nsq = [
                np.where(self.terr == 0)[0][rand],
                np.where(self.terr == 0)[1][rand]
                ]
            self.terr[nsq[0], nsq[1]] = sq.value
        else:
            pass
        return self.display()

    def move_down(self, event):
        print(event.keysym)
        check = 0
        # SWIP EQUIVALENT RIGHT
        for col in range(4):
            terr_ini = self.terr[:, col]
            if all(self.swip(terr_ini) == terr_ini):
                pass
            else:
                self.terr[:, col] = self.swip(terr_ini)
                check += 1
        # AJOUT CARRE
        if check != 0:
            print("CHECK", check)
            sq = Square()
            rand = randint(0, len(np.where(self.terr == 0)[0])-1)
            nsq = [
                np.where(self.terr == 0)[0][rand],
                np.where(self.terr == 0)[1][rand]
                ]
            self.terr[nsq[0], nsq[1]] = sq.value
        else:
            pass
        return self.display()

    def move_left(self, event):
        print(event.keysym)
        check = 0
        # SWIP INVERSE
        for row in range(4):
            terr_ini = np.flipud(self.terr[row, :])
            if all(self.swip(terr_ini) == terr_ini):
                pass
            else:
                self.terr[row, :] = np.flipud(self.swip(terr_ini))
                check += 1
        if check != 0:
            sq = Square()
            rand = randint(0, len(np.where(self.terr == 0)[0])-1)
            nsq = [
                np.where(self.terr == 0)[0][rand],
                np.where(self.terr == 0)[1][rand]
                ]
            self.terr[nsq[0], nsq[1]] = sq.value
        else:
            pass
        return self.display()

    def move_right(self, event):
        print(event.keysym)
        check = 0
        # SWIP RIGHT
        for row in range(4):
            terr_ini = self.terr[row, :]
            if all(self.swip(terr_ini) == terr_ini):
                pass
            else:
                self.terr[row, :] = self.swip(terr_ini)
                check += 1
        # AJOUT CARRE
        if check != 0:
            sq = Square()
            rand = randint(0, len(np.where(self.terr == 0)[0])-1)
            nsq = [
                np.where(self.terr == 0)[0][rand],
                np.where(self.terr == 0)[1][rand]
                ]
            self.terr[nsq[0], nsq[1]] = sq.value
        else:
            pass
        return self.display()

    def re_initialize(self, event):
        self.canvas.destroy()
        self.__init__(master)
        return self.display()


class Square:
    def __init__(self):
        self.value = randint(1, 2)*2


if __name__ == "__main__":

    master = Tk()
    master.title("2048")
    master.geometry("300x300")
    terr = Terrain(master)
    terr.display()

    master.bind("<KeyPress-Left>", lambda e: terr.move_left(e))
    master.bind("<KeyPress-Right>", lambda e: terr.move_right(e))
    master.bind("<KeyPress-Up>", lambda e: terr.move_up(e))
    master.bind("<KeyPress-Down>", lambda e: terr.move_down(e))
    master.bind("<Escape>", lambda e: terr.re_initialize(e))
    mainloop()

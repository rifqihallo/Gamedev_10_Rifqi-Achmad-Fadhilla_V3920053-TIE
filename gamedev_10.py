from math import pi, sin, cos #untuk menghitung pergerakan kamera

from direct.showbase.ShowBase import ShowBase #untuk mengambil dan menampilkan image
from direct.task import Task #untuk manajemen fungsi
from direct.actor.Actor import Actor #meload kelas aktor yang digunakan.
from direct.interval.IntervalGlobal import Sequence #memanipulasi durasi movement 
from panda3d.core import Point3 #untuk mengatur koordinat aktor


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Nonaktifkan kontrol trackball kamera.
        self.disableMouse()

        # memuat environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Atur ulang model yang akan dirender.
        self.scene.reparentTo(self.render)
        # Terapkan transformasi scale dan posisi pada model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Tambahkan prosedur spinCameraTask ke pengelola tugas.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load dan ubah aktor panda.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop animasinya.
        self.pandaActor.loop("walk")

        # Buat empat interval lerp yang dibutuhkan panda untuk
        # berjalan bolak-balik.
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # Buat dan mainkan urutan yang mengoordinasikan interval.
        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

    # Tentukan prosedur untuk menggerakkan kamera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

#inisialisasi Function MyApp() ke variabel app
app = MyApp()
mySound = app.loader.loadSfx("Maidens-Longing.ogg")
#musik diputar
mySound.play()
#untuk mengulang musik
mySound.setLoop(True)
#mengatur volume
mySound.setVolume(10)
#untuk menjalankan aplikasi
app.run()

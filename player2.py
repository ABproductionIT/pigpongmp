from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
import socket
import asyncio

# client for ball position data
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

# client for player1 position data
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect(("127.0.0.1", 12346))

# server socket for send player2 position to player1
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12347))
server.listen()
user, addres = server.accept()


class PongPaddle(Widget):
    score = NumericProperty(0)  # очки игрока

    # Отскок мячика при коллизии с панелькой игрока
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1

            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    # Скорость движения нашего шарика по двум осям
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # Создаем условный вектор
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Заставим шарик двигаться
    def move(self):
        data = client.recv(1024)
        a = data.decode("utf-8")
        # data from player1 ball position socket
        try:
            b = list(map(float, a.split(", ")))
            self.pos = b
        except:
            pass


class PongGame(Widget):
    ball = ObjectProperty(None)  # это будет наша связь с объектом шарика
    player1 = ObjectProperty(None)  # Игрок 1
    player2 = ObjectProperty(None)  # Игрок 2

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()  # двигаем шарик в каждом обновлении экрана

        # проверка отскока шарика от панелек игроков
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # this is send data about player2 position to player1
        p = str(self.player2.center_y)
        user.send(p.encode("utf-8"))

        # data from player1  position socket
        datax = client1.recv(1024)
        t = datax.decode("utf-8")
        try:
            self.player1.center_y = float(t)
        except:
            pass
        # file1.close()

        # отскок шарика по оси Y
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1  # инверсируем текущую скорость по оси Y

        # отскок шарика по оси X
        # тут если шарик смог уйти за панельку игрока, то есть игрок не успел отбить шарик
        # то это значит что он проиграл и мы добавим +1 очко противнику
        if self.ball.x < self.x:
            # Первый игрок проиграл, добавляем 1 очко второму игроку
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))  # заново спавним шарик в центре

        if self.ball.x > self.width:
            # Второй игрок проиграл, добавляем 1 очко первому игроку
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))  # заново спавним шарик в центре

    # Событие прикосновения к экрану
    def on_touch_move(self, touch):
        # второй игрок может касаться только своей части экрана (правой)
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
            # k = str(self.player2.center_y)
            # client.send(k.encode("utf-8"))


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60)  # 60 FPS
        return game


if __name__ == '__main__':
    PongApp().run()

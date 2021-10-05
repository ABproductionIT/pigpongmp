from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
import socket
import json


ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
ClientSocket.connect((host, port))
jsoncode = {"code": '1234', "player": 'player1'}
jsoncode = json.dumps(jsoncode)
ClientSocket.send(str(jsoncode).encode('utf-8'))


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
        self.pos = Vector(*self.velocity) + self.pos



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

        # send player1, & ball position data to player2
        p1data = str(self.player1.center_y)
        sharik = str(self.ball.x) + ", " + str(self.ball.y)
        jsonResult = {"player1": p1data, "ballpos": sharik}
        jsonResult = json.dumps(jsonResult)
        ClientSocket.send(str(jsonResult).encode('utf-8'))

        # recv data from player2 about his position
        Response = ClientSocket.recv(1024)
        try:
            data = Response.decode('utf-8')
            y1 = json.loads(data)
            self.player2.center_y = float(y1['player2'])
        except:
            pass

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
        # первый игрок может касаться только своей части экрана (левой)
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60)  # 60 FPS
        return game


if __name__ == '__main__':
    PongApp().run()

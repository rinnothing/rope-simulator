import pygame

def draw(self, surface, color):
    tow = []
    bck = []

    tow.append(self.segments[0].top_right)
    bck.append(self.segments[0].bot_right)

    for i in range(len(self.segments)-1):
        x1, y1 = self.segments[i].top_right
        x2, y2 = self.segments[i].top_left
        x3, y3 = self.segments[i+1].top_right
        x4, y4 = self.segments[i+1].top_left

        if (y1-y2)*(x3-x4) - (y3-y4)*(x1-x2) != 0:
            x = ((x1-x2)*(x3*y4-x4*y3) - (x3-x4)*(x1*y2-x2*y1)) / ((y1-y2)*(x3-x4) - (y3-y4)*(x1-x2))
            if x1-x2 != 0:
                y = (x * (y1-y2) + x1*y2 - x2*y1) / (x1-x2)
            else:
                y = (x * (y3-y4) + x3*y4 - x4*y3) / (x3 - x4)

            tow.append((x, y))

        x1, y1 = self.segments[i].bot_right
        x2, y2 = self.segments[i].bot_left
        x3, y3 = self.segments[i+1].bot_right
        x4, y4 = self.segments[i+1].bot_left

        if (y1-y2)*(x3-x4) - (y3-y4)*(x1-x2) != 0:
            x = ((x1-x2)*(x3*y4-x4*y3) - (x3-x4)*(x1*y2-x2*y1)) / ((y1-y2)*(x3-x4) - (y3-y4)*(x1-x2))
            if x1-x2 != 0:
                y = (x * (y1-y2) + x1*y2 - x2*y1) / (x1-x2)
            else:
                y = (x * (y3-y4) + x3*y4 - x4*y3) / (x3 - x4)

            bck.append((x, y))


    tow.append(self.segments[len(self.segments)-1].top_left)
    bck.append(self.segments[len(self.segments)-1].bot_left)

    pygame.draw.polygon(surface, color, tow + bck[::-1])
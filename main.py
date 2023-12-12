# TEE PELI TÄHÄN
import pygame
import random

class PELI:
    def __init__(self) -> None:
        pygame.init()
        self.naytto = pygame.display.set_mode((1024,768))
        self.leveys = 1024
        self.korkeus = 768

        # onko peli aloitettu
        self.aloitettu = False

        # startti screen looppi
        while self.aloitettu == False:
            self.aloitus()
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RETURN:
                        self.aloitettu = True


        self.lataa_kuvat()

        self.kello = pygame.time.Clock()


        # robotin liikutus
        self.robo_x = 0
        self.robo_y = 0
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.alas = False


        # hirvio
        self.hirvio_x = 400
        self.hirvio_y = 400
        self.hirvio_x_nopeus = 2
        self.hirvio_y_nopeus = 2

        # kolikko
        self.kolikko_x = 100
        self.kolikko_y = 100
        self.kierros = 0

        # high score
        self.highscore = 0
        
        # varsinainen pelilooppi
        while True:
            self.naytto.fill((0, 0, 204))
            self.robotti()
            self.kolikko_funktio()
            self.hirvio_funktio()
            self.pistemaara()
            pygame.display.flip()
            if self.collision(self.robo_x, self.robo_y, self.robo, self.hirvio_x, self.hirvio_y, self.hirvio):
                while True:
                    self.lopetus()







    def lataa_kuvat(self):
        self.hirvio = pygame.image.load("hirvio.png")
        self.kolikko = pygame.image.load("kolikko.png")
        self.robo = pygame.image.load("robo.png")

    def aloitus(self):
        self.naytto.fill((0,0,0))
        fontti = pygame.font.SysFont("Arial", 24)
        teksti = fontti.render("Paina enter aloittaaksesi ja liikuta robottia nuolinäppäimillä ja väistele hirviöitä", True, (255,255,255))
        self.naytto.blit(teksti, (0, 0))
        teksti = fontti.render("Lycka till!", True, (255,255,255))
        self.naytto.blit(teksti, (0, 24))
        pygame.display.flip()

    def lopetus(self):
        if self.kierros > self.highscore:
            self.highscore = self.kierros
        self.naytto.fill((0,0,0))
        fontti = pygame.font.SysFont("Arial", 24)
        teksti = fontti.render("Hävisit!", True, (255,255,255))
        self.naytto.blit(teksti, (0, 0))
        teksti = fontti.render(f"Pisteesi: {self.kierros}", True, (255,255,255))
        self.naytto.blit(teksti, (0, 24))
        teksti = fontti.render(f"Voit nyt sulkea pelin, avaa peli uudestaan jos haluat pelata lisää.", True, (255,255,255))
        self.naytto.blit(teksti, (0, 50))

        pygame.display.flip()

    def pistemaara(self):
        fontti = pygame.font.SysFont("Arial", 24)
        teksti = fontti.render(f"Pisteet: {self.kierros}", True, (255,255,255))
        self.naytto.blit(teksti, (self.leveys /2, 0))

    def robotti(self):
        for tapahtuma in pygame.event.get():
            # näppäin painetaan self.alas
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True

            # näppäin nostetaan ylös
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False

        if self.oikealle == True:
            if self.robo_x != self.leveys - self.robo.get_width():
                self.robo_x += 2
        if self.vasemmalle == True:
            if self.robo_x != 0:
                self.robo_x -= 2
        if self.alas == True:
            if self.robo_y != self.korkeus - self.robo.get_height():
                self.robo_y += 2
        if self.ylos == True:
            if self.robo_y != 0:
                self.robo_y -= 2

        self.naytto.blit(self.robo, (self.robo_x,self.robo_y))

        self.kello.tick(60)


    def collision(self, obj1_x, obj1_y, obj1, obj2_x, obj2_y, obj2):
        #Rect(left, top, width, height)
        obj1_rect = pygame.Rect(obj1_x, obj1_y, obj1.get_width(), obj1.get_height())
        obj2_rect = pygame.Rect(obj2_x, obj2_y, obj2.get_width(), obj2.get_height())

        osuuko = obj1_rect.colliderect(obj2_rect)

        if osuuko == True:
            return True
        if osuuko == False:
            return False

    def kolikko_funktio(self):
        self.naytto.blit(self.kolikko, (self.kolikko_x, self.kolikko_y))
        if self.collision(self.robo_x, self.robo_y, self.robo, self.kolikko_x, self.kolikko_y, self.kolikko):
            self.kolikko_x = random.randint(0,1024 - self.kolikko.get_width())            
            self.kolikko_y = random.randint(0,768 - self.kolikko.get_height())
            self.kolikko_saatu()

    def hirvio_funktio(self):
        if self.hirvio_y + self.hirvio.get_height() >= self.korkeus:
            self.hirvio_y_nopeus = -self.hirvio_y_nopeus
        if self.hirvio_y <= 0:
            self.hirvio_y_nopeus = -self.hirvio_y_nopeus
        if self.hirvio_x + self.hirvio.get_width() >= self.leveys:
            self.hirvio_x_nopeus = -self.hirvio_x_nopeus        
        if self.hirvio_x <= 0:
            self.hirvio_x_nopeus = -self.hirvio_x_nopeus

        self.hirvio_x += self.hirvio_x_nopeus
        self.hirvio_y += self.hirvio_y_nopeus
        self.naytto.blit(self.hirvio, (self.hirvio_x, self.hirvio_y))






    def kolikko_saatu(self):
        self.kierros += 1
        if self.kierros % 5 == 0:
            self.hirvio_y_nopeus = self.hirvio_y_nopeus * 1.5
            self.hirvio_x_nopeus = self.hirvio_x_nopeus * 1.5
            self.hirvio_y_nopeus = self.hirvio_y_nopeus * 1.1
            self.hirvio_x_nopeus = self.hirvio_x_nopeus * 1.1













if __name__ == "__main__":
    peli = PELI()
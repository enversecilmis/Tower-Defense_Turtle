import turtle
from playsound import playsound

# Ekranı ayarla
wn = turtle.Screen()
wn.title("Tower Defense")
width = 900
height = 600
wn.setup(width,height)
wn.cv._rootwindow.resizable(False, False)
wn.colormode(255)


#global değişkenler
state = 0
money = 0
player_health = 100


# şekilleri kaydet
wn.register_shape("Images/enemy_knife.gif")
wn.register_shape("Images/enemy_pistol.gif")
wn.register_shape("Images/enemy_rifle.gif")
wn.register_shape("Images/enemy_shotgun.gif")
wn.register_shape("Images/space_tower.gif")
wn.register_shape("Images/tower_lvl2.gif")
wn.addshape("Images/level2_T.gif")
wn.addshape("Images/level1_T.gif")

wn.addshape("Images/tower_lvl2.gif")
wn.addshape("Images/space_tower.gif")
wn.addshape("Images/money_maker.gif")

# Kule tiplerini tutan turtlelar. Kule butonları için.
towerTypes = ["Images/tower_lvl2.gif","Images/space_tower.gif","Images/money_maker.gif"]




# Spriteları renderlayan turtle
pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.hideturtle()





# Bölüm
class Level():
	def __init__(self,bgimage,btnimage,difficulty,path):
		self.bgimage = bgimage
		self.difficulty = difficulty
		self.path = path
		self.btnimage = btnimage


# Kuleler ve düşmanlar için base class
class Sprite():
	def __init__(self,x,y,image,damage,health):
		self.x = x
		self.y = y
		self.image = image
		self.damage = damage/2
		self.health = health

	# objenin kordinatına spriteını çiz
	def render(self,pen):
		pen.goto(self.x,self.y)
		pen.shape(self.image)
		pen.stamp()



# Kule
class Tower(Sprite):
	towerCount = 0
	def __init__(self,x,y,image,damage,health,price,rangee):
		Sprite.__init__(self,x,y,image,damage,health)
		self.price = price
		self.range = rangee
		self.target = None

		self.laser = turtle.Turtle()
		self.laser.speed(0)
		self.laser.penup()
		self.laser.hideturtle()
		self.laser.goto(self.x,self.y)
		self.laser.color(0.05*damage+0.4,0.05*damage+0.4,0.02*damage+0.4)
		self.laser.pendown()
		self.laser.pensize(0.5*damage)
		Tower.towerCount += 1

	# Düşman menzilde mi
	def is_in_range(self,enemy):
		if abs(self.x - enemy.x) < self.range and abs(self.y - enemy.y) < self.range:
			return True
		else:
			return False

	# Menzilde olan ilk hedefe saldır
	def attack(self,enemies):
		self.laser.clear()
		# belirlenmiş hedef !var mı
		if self.target == None:
			for enemy in enemies:
				# düşmanlardan menzile giren varsa hedef olarak belirle
				if self.is_in_range(enemy):
					self.target = enemy
					break

		# belirlenmiş hedef varsa ve hala menzildeyse hasar ver
		elif self.is_in_range(self.target):
			self.laser.goto(self.target.x,self.target.y)
			self.laser.setposition(self.x,self.y)
			self.target.health -= self.damage
			if self.target.health < 0:
				self.target = None

		# hedef menzilden çıktıysa bırak
		else:
			self.target = None




# Düşman
class Enemy(Sprite):
	def __init__(self,x,y,image,damage,health,speed):
		Sprite.__init__(self,x,y,image,damage,health)
		self.speed = speed
		self.dx = 0
		self.dy = 0
		self.c_dest = 0



	def set_direction(self,path):

		if self.c_dest+1 < len(path):
			if path[self.c_dest][0] != path[self.c_dest+1][0]:
				self.dx = self.speed
				self.dy = 0
				self.c_dest += 1
			elif path[self.c_dest][1] > path[self.c_dest+1][1]:
				self.dy = -self.speed
				self.dx = 0
				self.c_dest += 1
			else:
				self.dy = self.speed
				self.dx = 0
				self.c_dest += 1

	def move(self):
		self.x += self.dx
		self.y += self.dy
		

	def follow_path(self, path):

		if self.dx > 0:
			if self.x > path[self.c_dest][0]:
				self.set_direction(path)
		elif self.dy > 0:
			if self.y > path[self.c_dest][1]:
				self.set_direction(path)
		elif self.dy < 0:
			if self.y < path[self.c_dest][1]:
				self.set_direction(path)

		self.move()






levels = []



# levellerı tanımla ve diziye at
lvl1_path = [[-440,-25],[-300,-25],[-300,145],[-120,145],[-120,-90],[120,-90],[120,25],[450,25]]
levels.append( Level("Images/level1.gif","Images/level1_T.gif",4,lvl1_path))

lvl2_path = [[-440,245],[-350,245],[-350,-110],[-220,-110],[-220,160],[0,160],[0,80],[80,80],[80,-30],[360,-30],[360,180],[450,180]]
levels.append( Level("Images/level2.gif","Images/level2_T.gif",100,lvl2_path))



# Kuleleri oluşturup diziye atacak metod
# Tıklanan kule butonunu parametre olarak alıyor
def makeTower(x,y,towerType):
	towers.append( Tower(x-width/2,-y+height/2,towerType.type,3*towerType.power,50*towerType.power,10*towerType.power/2,200))
	canvas = wn.getcanvas()
	playsound("Sound/button4.wav",False)
	canvas.bind('<Button-3>',lambda x: print(x))

	






# Seçilen levelde oyunu başlat
def startGame(level):
	playsound("Sound/launch_select2.wav",False)

	global player_health

	global money

	difficulty = level.difficulty
	money = 5+difficulty
	player_health = 100



	# Önceki ekrandakileri temizle
	wn.clear()
	# wn.update() kullandığımız için tracer(0) dedik
	wn.tracer(0)
	# Arkaplan ayarla
	wn.bgpic(level.bgimage)

	def updateHealth():
		health_turtle.clear()
		health_turtle.goto(250,-200)
		health_turtle.write("Health: ",font=('arial',20,'normal'))
		health_turtle.goto(330,-200)
		health_turtle.write(player_health,font=('arial',20,'normal'))

	health_turtle = turtle.Turtle()
	health_turtle.hideturtle()
	health_turtle.penup()
	health_turtle.color("green")
	updateHealth()


	# Kule satın alma butonlarını oluştur
	tower_buttons = []
	tower_button_position_x = -150
	for i in range(0,len(towerTypes)):
		tower_buttons.append( turtle.Turtle())
		tower_buttons[i].speed(0)
		tower_buttons[i].penup()
		tower_buttons[i].shape(towerTypes[i])
		tower_buttons[i].type = towerTypes[i]
		tower_buttons[i].power = i+1
		tower_buttons[i].setposition(tower_button_position_x,-220)
		#tower_buttons[i].onclick(lambda x,y: buy_tower(tower_buttons[i]))
		tower_buttons[i].onclick(lambda x,y, towerType = tower_buttons[i]: buy_tower(towerType))
		tower_buttons[i].color('yellow')
		tower_buttons[i].write(10*tower_buttons[i].power/2,align='right',font=('arial',13,'bold'))
		tower_button_position_x += 150


	global towers
	towers = []
	# Kule satın alma fonksiyonu
	def buy_tower(towerType):
		global money
		if(money >= 10*towerType.power/2):
			canvas = wn.getcanvas()
			canvas.bind('<Button-3>',lambda event: makeTower(event.x,event.y,towerType))
			money -= 10*towerType.power/2
			updateMoney()
			playsound("Sound/gunpickup2.wav",False)
		else:
			playsound("Sound/wpn_select.wav",False)
		
		



	# Geri fonksiyonu
	def back(x,y):
		global state
		state = 0
		playsound("Sound/launch_dnmenu1.wav",False)
		lvlMenu()

		
	# Geri butonu
	back2menu = turtle.Turtle()
	back2menu.speed(0)
	back2menu.penup()
	back2menu.setposition(420, -270)
	back2menu.shape("square")
	back2menu.shapesize(2)
	back2menu.color("red")
	back2menu.onclick(back)




	# Gösterilen para miktarını güncelle
	def updateMoney():
		money_turtle.clear()
		money_turtle.goto(250,-170)
		money_turtle.write("Para: ",font=('arial',20,'normal'))
		money_turtle.goto(320,-170)
		money_turtle.write(money,font=('arial',20,'normal'))




	# Para göstergesi
	money_turtle = turtle.Turtle()
	money_turtle.hideturtle()
	money_turtle.penup()
	money_turtle.color("yellow")
	updateMoney()


	
	playsound("Sound/alert.wav")
	playsound("Sound/intruder.wav")
	playsound("Sound/detected.wav")
	playsound("Sound/weaponselect_on.wav",False)
	playsound("Sound/siren.wav",False)

	# Düşmanları şu anki levelin zorluğuna göre oluştur
	enemies = []
	for x in range(0,level.difficulty*2):
		enemies.append( Enemy(level.path[0][0]-1000-x*1200/difficulty, level.path[0][1], "Images/enemy_knife.gif", 10, 600+difficulty*20, 0.3+0.05*difficulty))
		enemies[x].dx = enemies[x].speed

	global state
	state = 1
	wawe = 1
	# Oyun içi döngü
	while (state == 1):

		# Nedense ekranı yneileyince arkaplan siliniyor
		# Bu yüzden tekrar arkaplanı ayarlamak gerekiyor
		wn.bgpic(level.bgimage)

		
		# Düşmanları renderla ve yolu takip ettir
		for enemy in enemies:
			enemy.render(pen)
			enemy.follow_path(level.path)

		# Kuleleri renderla ve düşmanlara saldırt
		for tower in towers:
			tower.render(pen)
			tower.attack(enemies)

		# Canı 0'a düşen düşmanları sil
		for enemy in enemies:
			if enemy.health < 0:
				#playsound("ba_pain2.wav",False)
				enemies.remove(enemy)
				del enemy
				playsound("Sound/pl_pain6.wav",False)
				#update money
				money += 1
				updateMoney()
		for enemy in enemies:
			if enemy.x > 500:
				player_health -= enemy.damage
				updateHealth()
				enemies.remove(enemy)
				del enemy
				playsound("Sound/blip1.wav",False)
		if player_health < 0:
			playsound("Sound/failed.wav",False)
			state = 0
			mainMenu()
			




		# Ekranı yenile
		wn.update()



		# Tüm düşmanlar öldüyse sonraki dalgaya geç
		if len(enemies) == 0:
			difficulty += 2
			wawe += 1
			enemies = []
			for x in range(0,difficulty*2):
				enemies.append( Enemy(level.path[0][0]-1000-x*1200/difficulty, level.path[0][1], "Images/enemy_knife.gif", 10, 600+difficulty*20, 0.3+0.05*difficulty))
				enemies[x].dx = enemies[x].speed

			writeNext = turtle.Turtle()
			writeNext.hideturtle()
			writeNext.penup()
			writeNext.speed(0)
			writeNext.setposition(-110,230)
			writeNext.write(wawe,font=('arial',30,'normal'))
			writeNext.setposition(-90,230)
			writeNext.write(". Dalga Geliyor !!",font=('arial',30,'normal'))

			playsound("Sound/alert.wav")
			playsound("Sound/intruder.wav")
			playsound("Sound/detected.wav")
			playsound("Sound/siren.wav",False)
			writeNext.clear()


		# Önceden renderlanan imgeleri temizle
		pen.clear()





def lvlMenu():
	wn.clear()
	wn.bgcolor("gray")

	level_turtles = []

	lvl_image_position = -200
	for i in range(0,len(levels)):
		level_turtles.append( turtle.Turtle())
		level_turtles[i].speed(0)
		level_turtles[i].penup()
		level_turtles[i].setposition(lvl_image_position,0)
		level_turtles[i].shape(levels[i].btnimage)
		level_turtles[i].level = levels[i]
		level_turtles[i].onclick(lambda x,y,level = level_turtles[i].level: startGame(level))
		lvl_image_position += 300

		def back2Main_menu(x,y):
			playsound("Sound/launch_dnmenu1.wav",False)
			mainMenu()
	
		# Geri butonu.(Ana menüye)
		back2M_menu = turtle.Turtle()
		back2M_menu.speed(0)
		back2M_menu.penup()
		back2M_menu.setposition(420, -270)
		back2M_menu.shape("square")
		back2M_menu.shapesize(2)
		back2M_menu.color("red")
		back2M_menu.onclick(back2Main_menu)


def startLvlMenu():
	playsound("Sound/launch_select2.wav",False)
	lvlMenu()
def mainMenu():
	wn.clear()
	wn.bgcolor("gray")
	m_menu_btn = turtle.Turtle()
	m_menu_btn.speed(0)
	m_menu_btn.penup()
	m_menu_btn.shape("square")
	m_menu_btn.shapesize(3)
	m_menu_btn.color("orange")
	m_menu_btn.onclick(lambda x,y: startLvlMenu())

	m_menu_write = turtle.Turtle()
	m_menu_write.hideturtle()
	m_menu_write.speed(0)
	m_menu_write.penup()
	m_menu_write.color("white")
	m_menu_write.setposition(200,-20)
	m_menu_write.write(	"Bölümler",align="right",font=('arial',30,'normal'))
mainMenu()


wn.mainloop()
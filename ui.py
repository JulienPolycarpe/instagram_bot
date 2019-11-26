from appJar import gui

#http://appjar.info/pythonWidgets/#widgets

def validate():
	app.setFont(12)
	app.addMessage("mess", """You can put a lot of text in this widget.
	The text will be wrapped over mul	tiple lines.
	It's not possible to apply different styles to different words.""")
	pass



app=gui()

app.addEntry("username")
app.addSecretEntry("password")
app.addEntry("caption")
app.addEntry("delay_between_posts")
app.addButton("validate", validate)

app.setEntryDefault("username", "Username")
app.setEntryDefault("password", "Password")
app.setEntryDefault("caption", "Caption of your posts")
app.setEntryDefault("delay_between_posts", "Delay between posts(seconds)")

app.go()
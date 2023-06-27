socket := 0.0.0.0:$(port)

gunicorn:
	@echo socket $(socket)
	gunicorn --bind $(socket) foodgram_backend.wsgi

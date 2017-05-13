all:
	pyuic4 gui/camino.ui > main_window.py
	pyuic4 gui/settings.ui > settings_window.py
	pyuic4 gui/about.ui > about_window.py

clean:
	rm *.pyc 2>/dev/null


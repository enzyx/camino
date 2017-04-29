all:
	pyuic4 gui/camino.ui > design.py
	pyuic4 gui/settings.ui > settings_view.py
	pyuic4 gui/about.ui > about_view.py


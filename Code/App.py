from Config import config  # import z podfolderu configuration

# Tworzymy okno i interfejs
okno = config.create_app()

# Uruchamiamy aplikację
okno.mainloop()

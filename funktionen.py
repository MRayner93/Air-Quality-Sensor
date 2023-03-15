global ppm
#----------------------------- Funktionen ------------------------------
class funktionen():

    # Gute Luftqualität-Funktion
    def luft_gut():
    # Die grüne LED ist an, alle anderen aus und der Buzzer macht kein Geräusch
        led_gruen.on()
        led_gelb.off()
        led_rot.off()
        buzzer.off()
    # Auf dem Display wird die PPM und die Luftqualität angezeigt
        display.fill(0)
        display.text("-Luftqualitaet-", 7, 0)
        display.text("Gut", 43, 15)
        display.text(f"PPM: {ppm}", 0, 55)
        display.show()

    # Mittlere Luftqualität-Funktion
    def luft_mittel():
    # Die gelbe LED ist an, alle anderen aus und der Buzzer macht kein Geräusch
        led_gruen.off()
        led_gelb.on()
        led_rot.off()
        buzzer.off()
        display.fill(0)
    # Auf dem Display wird die PPM und die Luftqualität angezeigt
        display.text("-Luftqualitaet-", 2, 0)
        display.text("Mittel", 43, 15)
        display.text("!Bitte Lueften!", 5, 35)
        display.text(f"PPM: {ppm}", 0, 55)
        display.show()

    # Schlechte Luftqualität-Funktion
    def luft_schlecht():
    # Die rote ist LED an, alle anderen aus und der Buzzer macht ein Geräusch
        led_gruen.off()
        led_gelb.off()
        led_rot.on()
        buzzer.on()
    # Auf dem Display wird die PPM und die Luftqualität angezeigt
        display.fill(0)
        display.text("-Luftqualitaet-", 0, 0)
        display.text("Schlecht", 36, 15)
        display.text("!Sofort Lueften!", 0, 35)
        display.text(f"PPM: {ppm}", 0, 55)
        display.show()
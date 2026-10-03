import turtle

wn = turtle.Screen()
wn.title("Test pause")

def test():
    print("La touche P a bien été détectée !")

wn.listen()
wn.onkeypress(test, "p")
wn.onkeypress(test, "P")

wn.mainloop()
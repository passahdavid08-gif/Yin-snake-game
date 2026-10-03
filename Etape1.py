def tree(i):
    t = tree
    if i < 10:
        return
    else:
        t.forward(i)
        t.color('blue')
        t.circle(2)
        t.color('brown')

        t.left(20)
        tree(4 * i / 5)
        t.right(40)
        tree(4 * i / 5)
        t.left(20)

        t.backward(i)

tree(500)
import tetris_engine

t = tetris_engine.Tetris()

print(t.figure.type)
print(t.spoiler)

for i in range(20):
    t.new_figure()
    print(t.figure.type)
    print(t.spoiler)
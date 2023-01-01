> 警告：fastgame已经停止维护。请使用`opengame`来代替。

# 什么是fastgame
Fastgame是一个帮助你快速构建游戏或简单的GUI界面的python第三方库。  
内部封装pygame2复杂的API。

# 为什么使用fastgame
下面是同样在`pygame`和`fastgame`中显示文字的对比  
使用`pygame`:
```python
import sys
import pygame as pg
pg.init()
screen = pg.display.set_mode((400, 400))
pg.display.set_caption('Hello World')
font = pg.font.Font(None, 16)
text = font.render('hello world', True, (0, 0, 0))
while True:
    screen.blit(text, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
```
使用`fastgame`:
```python
import fastgame as fg
game = fg.FastGame(title='Hello World', size=(400, 400))
text = fg.Label('hello world')
@game.update
def update():
    text.update()
game.mainloop()
```

# 在哪里查看fastgame
github网址: [https://github.com/stripepython/fastgame](https://github.com/stripepython/fastgame)  
文档: [https://stripepython.github.io/fastgame-document/document.html](https://stripepython.github.io/fastgame-document/)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from PIL import Image, ImageSequence, ImageDraw, ImageFont


def txtlayer(base, text="Hello World!", xy=(0, 0), color="#FFFFFF"):
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
    font_size = 20
    print(xy)
    x, y = xy
    x = x - font_size * len(text) / 2
    y = y - font_size / 2
    xy = x, y
    print(xy)
    # get a font
    fnt = ImageFont.truetype(u'resources/文泉驿微米黑.ttf', font_size)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    # d.text(xy, text, font=fnt, fill=(255, 255, 255, 255))
    d.multiline_text(xy, text, font=fnt, fill=color, anchor=True, align="center")
    return txt



def convert(src='source.gif', xy=(10, 10), color="#FFFFFF"):

    os.system("gifsicle --colors=255 {src} -o cache/tmp.gif".format(src=src))
    os.system("gifsicle --unoptimize cache/tmp.gif -o {src}".format(src=src))

    with open(src + ".txt", encoding="utf8") as fpt:
        rules = fpt.readlines()
        rules = [rule.split("`") for rule in rules]

    with Image.open(src) as im:
        if im.is_animated:

            newframes = []
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                # get an image
                base = frame.copy().convert('RGBA')
                t = " "
                for start, end, text in rules:
                    start = int(start)
                    end = int(end)
                    if start <= i <= end:
                        t = " " + text.strip() + " "
                print(t)
                txt = txtlayer(base, t, xy, color)
                newframes.append(Image.alpha_composite(base, txt))

            newframes[0].save('%s.out.gif' % src.replace(".gif", ""), save_all=True, append_images=newframes[1:])


if __name__ == '__main__':
    from appJar import gui

    app = gui()
    # app.setFont(20)
    app.setGeometry("600x400")


    def select(f):
        a = app.openBox(title="aaa", dirName=None, fileTypes=[('images', '*.gif')], asFile=True, parent=None)
        app.setEntry(u"gif文件名", a.name)
        app.setEntry(u"rule文件名", a.name + ".txt")
        im = Image.open(a.name)
        x, y = im.size
        app.setEntry(u"gif文字坐标x", x // 2)
        app.setEntry(u"gif文字坐标y", y - 30)
        fs = [f for f in ImageSequence.Iterator(im)]
        app.setEntry(u"gif帧数", len(fs))
        print(len(fs))


    app.startLabelFrame("gif_group", hideTitle=True)
    app.addButton(u"选择gif", select)
    app.addLabelEntry(u"gif文件名")
    app.addLabelEntry(u"gif帧数")
    app.addLabelEntry(u"gif文字坐标x")
    app.addLabelEntry(u"gif文字坐标y")
    app.setEntry(u"gif文字坐标x", "10")
    app.setEntry(u"gif文字坐标y", "10")
    app.stopLabelFrame()


    def selectcolor(f):
        color = app.colourBox(colour="#FF0000")
        print(color)
        app.setEntry(u"color", color)


    app.startLabelFrame("color_group", hideTitle=True)
    app.addButton("选择color", selectcolor)

    app.addLabelEntry(u"color")
    app.setEntry(u"color", "#FFFFFF")
    app.stopLabelFrame()

    app.addLabelEntry(u"rule文件名")


    def gene(f):
        print(f)
        giffile = app.getEntry(u"gif文件名")
        x = app.getEntry(u"gif文字坐标x")
        y = app.getEntry(u"gif文字坐标y")
        xy = (int(x), int(y))
        color = app.getEntry(u"color")
        convert(giffile,  xy, color)
        app.infoBox("消息", "生成成功")


    app.addButton("生成", gene)

    app.go()

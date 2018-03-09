# facepy
表情包制作工具，支持mp4和gif



## mp4转gif

在mp4转gif的同时生成gif的帧文字序列，可以用于gif加文字


## gif加文字

将gif文件和同名的txt文件放在同一目录下
> 如：source.gif 和 source.gif.txt

1. 运行 face8gif.py
2. 点击 选择gif 按钮来选择gif，系统会自动读取同名txt文件

> 文件中规则 1\`5\`222 代表在第一帧到第五帧一直显示222

3. 可以设置文字在gif中显示的位置，xy

4. 可以设置文字颜色，点击 选择color

5. 点击 生成 按钮，生成同名.out.gif文件
> 如：source.out.gif


### 解压缩问题
由于压缩过的gif会将重复帧设为透明，重拼时会出现绿色花片，所以需要首先解压缩
> 参考 [浓缩的才是精华：浅析GIF格式图片的存储和压缩](https://www.cnblogs.com/qcloud1001/p/6647080.html)

```
gifsicle --colors=255 beauty.gif -o tmp.gif
gifsicle --unoptimize tmp.gif > beauty.unoptimize.gif
```
### 工具
- ffmpeg: mp4转gif，gif转gif，不过用到九牛之一毛
- gifsicle: gif解压缩

### 依赖
```
pip install fabric3 imageio pillow appJar
```
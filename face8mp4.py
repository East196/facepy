#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os
from subprocess import Popen, PIPE

from jinja2 import Template


def calculate_hash(src):
    m2 = hashlib.md5()
    m2.update(str(src).encode("utf8"))
    return m2.hexdigest()


def time2frame(t):
    hms, sub = t.split(".")
    h, m, s = hms.split(":")
    h, m, s, sub = (int(i) for i in (h, m, s, sub))
    num = (h * 3600 + m * 60 + s) * 100 + sub
    frame = num / (100 / 8)
    return int(frame // 1)


class MP4toGIF(object):
    def __init__(self, template_name, sentences=[]):
        self.template_name = template_name
        self.sentences = sentences
        self.video_path = "resources/" + template_name + ".mp4"
        self.ass_tpl_path = self.video_path + ".ass.tpl"
        if sentences:
            self.gif_path = "cache/" + self.template_name + "-" + calculate_hash(sentences) + ".gif"
        else:
            self.gif_path = "resources/" + self.template_name + ".gif"
        self.ass_path = self.gif_path + ".ass"
        self.txt_path = self.gif_path + ".txt"

    def render_ass(self):
        with open(self.ass_tpl_path) as fp:
            template = fp.read()
            ass_text = Template(template).render(sentences=sentences)
            with open(self.ass_path, "w", encoding="utf8") as fp:
                fp.write(ass_text)
        with open(self.ass_path, encoding="utf8") as fp:
            lines = [line.replace("Dialogue: ", "").split(",") for line in fp.readlines() if line.startswith("Dialogue: ")]
            with open(self.txt_path, "w", encoding="utf8") as fpt:
                for _, start_time, end_time, _, _, _, _, _, _, txt in lines:
                    print(start_time, end_time, txt)
                    start_frame = time2frame(start_time)
                    end_frame = time2frame(end_time)
                    fpt.write("%s`%s`%s\n" % (start_frame, end_frame, txt.strip() + " "))

        return self.ass_path

    def make_gif_with_ffmpeg(self):
        cmd = "ffmpeg -i {video_path} -r 8 -vf ass={ass_path},scale=300:-1 -y {gif_path}" \
            .format(video_path=self.video_path, ass_path=self.ass_path, gif_path=self.gif_path)
        print(cmd)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        p.wait()
        if p.returncode != 0:
            raise Exception("Error. ReturnCode is %s" % p.returncode)

    def render_gif(self):
        if os.path.exists(self.gif_path):
            return self.gif_path
        self.render_ass()
        self.make_gif_with_ffmpeg()
        return self.gif_path


if __name__ == '__main__':
    print(str(["hello"]))
    sentences = ["好啊", "就算你是一流工程师", "就算你出报告再完美", "我叫你改报告你就要改", "毕竟我是客户", "客户了不起啊", "sorry 客户真的了不起", "以后叫他天天改报告", "天天改 天天改"]
    template_name = "sorry"
    path = MP4toGIF(template_name, sentences)
    print(path.render_gif())

import os

import Dailynews
from PIL import Image, ImageDraw, ImageFont
import yaml

def draw_text_with_wrap(text, position, max_width, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont):
    # 分词
    words = []
    for t in text:
        words.append(t)
    lines = []
    current_line = words[0]
    for word in words[1:]:
        # 预测如果加入新词后的行宽
        test_line = f'{current_line}{word}'
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]  # 计算文本宽度
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill="black")
        bbox = draw.textbbox((position[0], y), line, font=font)
        y += bbox[3] - bbox[1]  # 行高


news = Dailynews.DailyNews()

news.get_news()
news.analyze()
news.touhou_get_fes()

image = Image.open("template.png")
draw = ImageDraw.Draw(image)

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path_absolute = os.path.join(script_dir, news.font_path)

font = ImageFont.truetype(font_path_absolute, 30)

# 历史上的今天：年份
x = 50
y = 575
loc = [(x, k) for k in range(y, y + 800, 160)]
for new, pos in zip(news.news_year, loc):
    draw_text_with_wrap(new, pos, 300, draw, font)

# 历史上的今天：内容
x = 60
y = 610
loc = [(x, k) for k in range(y, y + 800, 160)]
for content, pos in zip(news.news_content, loc):
    draw_text_with_wrap(content, pos, 400, draw, font)

font = ImageFont.truetype(news.font_path, 40)

# 农历、阳历、节日

# 阳历
x = 225
y = 120
draw_text_with_wrap(news.today_content[0], (x, y), max_width=500, draw=draw, font=font)

# 阳历节日
# news.today_lunar_fes = ['Test']
if len(news.today_lunar_fes) != 0:
    font = ImageFont.truetype(news.font_path, 30)
    x = 400
    y = 180
    for item in news.today_lunar_fes:
        draw_text_with_wrap(item, (x, y), max_width=500, draw=draw, font=font)
        x += 40

font = ImageFont.truetype(news.font_path, 40)

# 农历
x = 225
y = 230
draw_text_with_wrap(news.today_content[1], (x, y), max_width=500, draw=draw, font=font)

# 农历节日
# news.today_solar_fes = ['Test']
if len(news.today_solar_fes) != 0:
    font = ImageFont.truetype(news.font_path, 30)
    x = 400
    y = 290
    for item in news.today_solar_fes:
        draw_text_with_wrap(item, (x, y), max_width=500, draw=draw, font=font)
        x += 40

# 农历：宜

font = ImageFont.truetype(news.font_path, 40)
x = 150
y = 280
draw_text_with_wrap("宜", (x, y), max_width=500, draw=draw, font=font)

# 农历：忌
x = 750
y = 280
draw_text_with_wrap("忌", position=(x, y), max_width=500, draw=draw, font=font)

# 内容拼接
str_ = ""
for item in news.today_yi:
    str_ += item + " "

font = ImageFont.truetype(news.font_path, 25)
x = 50
y = 350
draw_text_with_wrap(str_, (x, y), max_width=300, draw=draw, font=font)

str_ = ""
for item in news.today_ji:
    str_ += item + " "
x = 650
y = 350
draw_text_with_wrap(str_, (x, y), max_width=300, draw=draw, font=font)


font = ImageFont.truetype(news.font_path, 40)
# 东方角色日
x = 600
y = 600
for char in news.touhou_festival:
    draw_text_with_wrap(char,(x, y), max_width=350, draw=draw, font=font)
    y += 100

with open("data.yml","w",encoding="UTF-8") as stream:
    data = {
                "character": news.touhou_festival,
                "news": [str(s) for s in news.news_content],
                "year":[str(s) for s in news.news_year],
                "today_yi":news.today_yi,
                "today_ji":news.today_ji,
                "today_solar_fes":news.today_solar_fes,
                "today_lunar_fes":news.today_lunar_fes,
            }
    yaml.dump(data, stream,allow_unicode=True)
image.save("output.png")



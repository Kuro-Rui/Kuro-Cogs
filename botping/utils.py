"""
MIT License

Copyright (c) 2021-present Kuro-Rui

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import random

ping_pong_gifs = [
    "https://i.pinimg.com/originals/ac/b8/8f/acb88f71e5ed54072a24f647e28a9c3f.gif",
    "https://4.bp.blogspot.com/-8XanbCQDxfg/WnJTaUeifYI/AAAAAAABEUo/5yv_KUlLV9cmJsuI8jeFRrGSXbtQMclngCKgBGAs/s1600/Omake%2BGif%2BAnime%2B-%2BShokugeki%2Bno%2BSoma%2BS2%2B-%2BOAD%2B1%2B%255BDVD%255D%2B-%2BMegumi%2Bvs%2BIsshiki.gif",
    "https://remyfool.files.wordpress.com/2016/11/agari-rally.gif?w=924",
    "https://i.imgur.com/LkdjWE6.gif",
    "https://i.gifer.com/6TaL.gif",
    "https://i.kym-cdn.com/photos/images/original/000/753/601/bc8.gif",
    "https://c.tenor.com/On7v3wlDxNUAAAAd/ping-pong-anime.gif",
    "https://imgur.com/1cnscjV.gif",
    "https://images.squarespace-cdn.com/content/v1/5b23e822f79392038cbd486c/1589129513917-X6QBWRXBHLCSFXT9INR2/b17c1b31e185d12aeca55b576c1ecaef.gif",
    "https://i1.wp.com/drunkenanimeblog.com/wp-content/uploads/2017/11/shakunetsu-no-takkyuu-musume-scorching-ping-pong-girls.gif?fit=540%2C303&ssl=1&resize=350%2C200https://media1.tenor.com/images/2b27c6e7747d319f76fd98d2a226ab33/tenor.gif?itemid=15479836",
]


def ping_gifs_picker():
    pick = random.choice(ping_pong_gifs)
    return pick

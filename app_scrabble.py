from flask import Flask, render_template, url_for, redirect, request, flash, Markup
from config import Config
from forms import GameForm

app = Flask(__name__)
app.config.from_object(Config)

global X
global Y
global l
global h
global take
global letters
global cursors
global xy_id
global xy_move



X = 14
Y = 7
take = 0
letters = {'O1': {'abbr': 'abbr="O" ', 'coord': 'id=6.4', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/o_letter.png"}, 'D': {'abbr': 'abbr="D" ', 'coord': 'id=5.10', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/d_letter.png"}, 'L1': {'abbr': 'abbr="L" ', 'coord': 'id=1.8', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/l_letter.png"}, 'R': {'abbr': 'abbr="R" ', 'coord': 'id=4.5', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/r_letter.png"}, 'W': {'abbr': 'abbr="W" ', 'coord': 'id=2.13', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/w_letter.png"}, 'L2': {'abbr': 'abbr="L" ', 'coord': 'id=3.0', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/l_letter.png"}, 'L3': {'abbr': 'abbr="L" ', 'coord': 'id=6.7', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/l_letter.png"}, 'E': {'abbr': 'abbr="E" ', 'coord': 'id=0.2', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/e_letter.png"}, 'H': {'abbr': 'abbr="H" ', 'coord': 'id=4.12', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/h_letter.png"}, 'O2': {'abbr': 'abbr="O" ', 'coord': 'id=6.12', 'atr': 'background=', 'space': ' ', 'pic': "/static/img/o_letter.png"}}
cursors = {'abbr': 'abbr="cursor"', 'coord': 'id=6.13', 'bg': 'bgcolor=', 'color_reg': '"lightgrey"', 'color_take': '"lightgreen"', 'color_miss': '"red"', 'color_move': '"yellow"'}
xy_id = {}
xy_move = {}



@app.route('/')
def start():
    return render_template('index_game.html')


@app.route('/game',  methods=['GET', 'POST'])
def game():
    global X
    global Y
    global l
    global h
    global take
    global letters   # первичный словарь всех аттрибутов букв
    global cursors
    global xy_id   # промежуточный словарь координат букв
    global xy_move   # словарь букв в движении

    form = GameForm(request.form)

    if request.method == 'POST':
        if xy_id == {}:
            take = 0
            xy_id['cursor'] = cursors['coord']
            for key in letters:
                coords = letters[key].get('coord')
                xy_id[key] = coords
        elif xy_move != {}:
            take = 1

        if form.up.raw_data != []:
            old_y = xy_id['cursor']
            dot = old_y.index('.')
            part = old_y[3:dot]
            if part == '0':
                new_y = old_y
                xy_id['cursor'] = new_y
            else:
                new_part = str(int(old_y[3:dot]) - 1)
                new_y = old_y.replace(part, new_part, 1)
                if take == 1:
                    if new_y not in xy_id.values():
                        xy_id['cursor'] = new_y
                    else:
                        new_y = old_y
                        xy_id['cursor'] = new_y
                else:
                    xy_id['cursor'] = new_y

        elif form.down.raw_data != []:
            old_y = xy_id['cursor']
            dot = old_y.index('.')
            part = old_y[3:dot]
            if part == str(Y-1):
                xy_id['cursor'] = old_y
            else:
                new_part = str(int(old_y[3:dot]) + 1)
                new_y = old_y.replace(part, new_part, 1)
                if take == 1:
                    if new_y not in xy_id.values():
                        xy_id['cursor'] = new_y
                    else:
                        new_y = old_y
                        xy_id['cursor'] = new_y
                else:
                    xy_id['cursor'] = new_y

        elif form.left.raw_data != []:
            old_x = xy_id['cursor']
            dot = old_x.index('.')
            part = old_x[dot+1:]
            if part == '0':
                xy_id['cursor'] = old_x
            else:
                new_part = str(int(old_x[dot+1:]) - 1)
                new_x = old_x[:dot+1] + new_part
                if take == 1:
                    if new_x not in xy_id.values():
                        xy_id['cursor'] = new_x
                    else:
                        new_x = old_x
                        xy_id['cursor'] = new_x
                else:
                    xy_id['cursor'] = new_x

        elif form.right.raw_data != []:
            old_x = xy_id['cursor']
            dot = old_x.index('.')
            part = old_x[dot + 1:]
            if part == str(X-1):
                xy_id['cursor'] = old_x
            else:
                new_part = str(int(old_x[dot + 1:]) + 1)
                new_x = old_x[:dot + 1] + new_part
                if take == 1:
                    if new_x not in xy_id.values():
                        xy_id['cursor'] = new_x
                    else:
                        new_x = old_x
                        xy_id['cursor'] = new_x
                else:
                    xy_id['cursor'] = new_x

        elif form.take.raw_data != []:
            if take == 0:
                for key, value in xy_id.items():
                    if key != 'cursor':
                        if value == xy_id['cursor']:
                            take = 1
            else:
                take = 1

        elif form.drop.raw_data != []:
            if take == 1:
                take = 0
                for key, value in xy_id.items():
                    if key != 'cursor':
                        if value == xy_id['cursor']:
                            letters[key]['coord'] = xy_id['cursor']
            else:
                take = 0

        string_html = ''
        cell = '&nbsp;'
        tbl_o = '<table border = "1px" width = "' + str(l * 70) + 'px" height = "' + str(h * 70) + 'px">'
        tbl_c = '</table>'
        tr_o = '<tr>'
        tr_c = '</tr>'
        td_oo = '<td'
        td_oc = '>'
        td_c = '</td>'
        string_html += tbl_o
        for i in range(h):
                string_html += tr_o
                for j in range(l):
                    string_html += td_oo
                    string_html += ' '
                    id_add = 'id='+str(i)+'.'+str(j)
                    string_html += id_add
                    string_html += td_oc
                    string_html += cell
                    string_html += td_c
                string_html += tr_c
        string_html += tbl_c

        for key in xy_id:
            if key == 'cursor':
                coords = xy_id['cursor']
                bg = cursors['bg']
                spot = string_html.index(coords)
                if take == 0:
                    color = cursors['color_reg']
                    string_html = string_html[:spot] + bg + color + string_html[spot:]
                elif take == 1:
                    for key, value in xy_id.items():
                        if value == coords and key != 'cursor':
                            if key in xy_move:
                                color = cursors['color_miss'] # добавил
                            else:
                                xy_move[key] = value
                                color = cursors['color_take']
                        elif key in xy_move:
                            xy_move[key] = xy_id['cursor']
                            color = cursors['color_move']
                    string_html = string_html[:spot] + bg + color + string_html[spot:]
            else:
                abbr = letters[key].get('abbr')
                attr = letters[key].get('atr')
                space = letters[key].get('space')
                picture = letters[key].get('pic')
                if take == 0:
                    if key in xy_move:
                        letters[key]['coord'] = xy_move[key]
                        xy_id[key] = xy_move[key]
                        xy_move.pop(key)
                        coords = letters[key].get('coord')
                        spot = string_html.index(coords)
                        string_html = string_html[:spot] + abbr + attr + picture + space + string_html[spot:]
                    else:
                        coords = letters[key].get('coord')
                        spot = string_html.index(coords)
                        string_html = string_html[:spot]+abbr+attr+picture+space+string_html[spot:]
                elif take == 1:
                    if key in xy_move:
                        coords = xy_move[key]
                        xy_id[key] = coords # добавил
                        spot = string_html.index(coords)
                        string_html = string_html[:spot] + abbr + attr + picture + space + string_html[spot:]
                    else:
                        coords = xy_id[key]
                        spot = string_html.index(coords)
                        string_html = string_html[:spot] + abbr + attr + picture + space + string_html[spot:]

        message = Markup(string_html)
        flash(message)
        return redirect(url_for('game'))
    return render_template('game.html')


if __name__ == '__main__':
    l = X
    h = Y
    app.run(host='127.0.0.1', port=5000)
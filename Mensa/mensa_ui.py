import ui, appex
from datetime import datetime
from mensa import load_mensa_data


class TableViewDataSource(object):
    def __init__(self):
        today = lambda row: datetime.now().strftime("%d.%m.%Y") == row.date
        data = load_mensa_data(filter_expr=lambda row: today(row))
        self.data = sorted(list(data), key=lambda row: len(row.kind), reverse=True)
	
    def tableview_number_of_sections(self, tableview):
        return 1

    def tableview_number_of_rows(self, tableview, section):
        return len(self.data)

    def tableview_cell_for_row(self, tableview, section, row):
        entry = self.data[row]
        cell = ui.TableViewCell(style="subtitle")
        cell.text_label.text = entry.food
        cell.detail_text_label.text = str(entry.location) + " - " + str(entry.price)
        img = 'emj:Cow_Face'
        if "vegan" in entry.kind.lower():
        	img = 'emj:Leaves_1'
        elif "veggi" in entry.kind.lower():
        	img = 'emj:Leaves_2'
        cell.image_view.image = ui.Image(img)
        return cell

    def tableview_title_for_header(self, tableview, section):
        return None

    def tableview_can_delete(self, tableview, section, row):
        return False

    def tableview_can_move(self, tableview, section, row):
        return False


def scroll(px):
	off = tableview.content_offset
	off.y = min(max(off.y+px, 0), (len(tableview.data_source.data)-1)*tableview.row_height)
	tableview.content_offset = off
	
def scroll_down(bt):
	scroll(tableview.row_height)

def scroll_up(bt):
	scroll(-tableview.row_height)


v = ui.load_view()
v.background_color = "clear"
tableview = v["tableview"]
tableview.touch_enabled = False
tableview.data_source = TableViewDataSource()
tableview.delegate = None
#tableview.reload_data()

appex.set_widget_view(v)

# Copyright (C) weslowskij
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
# Note the special nature of indentation in the adapter declaration, where
# the adapter: is on one line, then the value side must be given at one level
# of indentation.

Builder.load_string("""
#:import lv listview8
#:import la kivy.adapters.dictadapter

<ListViewModal>:
    list_view8: list_view_id
    size_hint: None,None
    size: 400,400
    ListView8:
        id: list_view_id
        size_hint: .8,.8
        adapter:
            la.DictAdapter(
            data=dict([(i, str(i)) for i in xrange(1000)]),
            selection_mode='single',
            allow_empty_selection=False,
            cls=lv.ListItemButton)
""")

class ListViewModal(ModalView):
    selected_item = StringProperty('no selection')

    def __init__(self, **kwargs):
        super(ListViewModal, self).__init__(**kwargs)
        self.list_view8.adapter.bind(on_selection_change=self.selection_changed)

    # This is for the binding set up at instantiation, to the list adapter's
    # special on_selection_change (bind to it, not to adapter.seleciton).
    def selection_changed(self, *args):
        print '    args when selection changes gets you the adapter', args
        self.selected_item = args[0].selection[0].text

    # This is to illustrate another type of binding. This time it is to this
    # class's selected_item StringProperty (where the selected item text is set).
    # See other examples of how bindings are set up between things. This one
    # works because if you put on_ in front of a Kivy property name, a binding
    # is set up for you automatically.
    def on_selected_item(self, *args):
        print '    args when a list property changes gets you the list property, and the changed item', args
        print 'selected item text', args[1]

class MainView(GridLayout):
    """
    Implementation of a ListView using the kv language.
    """

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        kwargs['size_hint'] = (1.0, 1.0)
        super(MainView, self).__init__(**kwargs)

        listview_modal = ListViewModal()

        self.add_widget(listview_modal)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=800))
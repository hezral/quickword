# utils.py
#
# Copyright 2021 adi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class HelperUtils:

    @staticmethod
    def run_async(func):
        '''
        https://github.com/learningequality/ka-lite-gtk/blob/341813092ec7a6665cfbfb890aa293602fb0e92f/kalite_gtk/mainwindow.py
        http://code.activestate.com/recipes/576683-simple-threading-decorator/
        run_async(func): 
        function decorator, intended to make "func" run in a separate thread (asynchronously).
        Returns the created Thread object
        Example:
            @run_async
            def task1():
                do_something
            @run_async
            def task2():
                do_something_too
        '''
        from threading import Thread
        from functools import wraps

        @wraps(func)
        def async_func(*args, **kwargs):
            func_hl = Thread(target=func, args=args, kwargs=kwargs)
            func_hl.start()
            # Never return anything, idle_add will think it should re-run the
            # function because it's a non-False value.
            return None

        return async_func

    @staticmethod
    def get_active_window_xlib():
        ''' Function to get active window '''
        import Xlib
        import Xlib.display

        display = Xlib.display.Display()
        root = display.screen().root

        NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')
        GTK_APPLICATION_ID = display.intern_atom('_GTK_APPLICATION_ID')

        root.change_attributes(event_mask=Xlib.X.FocusChangeMask)
        try:
            window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
            window = display.create_resource_object('window', window_id)
            try:
                return window.get_full_property(GTK_APPLICATION_ID, 0).value.replace(b'\x00',b' ').decode("utf-8").lower()
            except:
                return None
        except Xlib.error.XError: #simplify dealing with BadWindow
            return None
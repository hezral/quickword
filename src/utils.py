# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

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
    def get_active_window_wm_class():
        ''' Function to get active window '''
        import Xlib
        import Xlib.display

        display = Xlib.display.Display()
        root = display.screen().root

        NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')
        WM_CLASS = display.intern_atom('WM_CLASS')

        root.change_attributes(event_mask=Xlib.X.FocusChangeMask)
        try:
            window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
            window = display.create_resource_object('window', window_id)
            try:
                return window.get_full_property(WM_CLASS, 0).value.replace(b'\x00',b' ').decode("utf-8").lower()
            except:
                return None
        except Xlib.error.XError: #simplify dealing with BadWindow
            return None
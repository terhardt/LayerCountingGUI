"""Simple matplotlib based GUI to mark annual layer boundaries
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.facecolor'] = 'None'
mpl.rcParams['lines.linewidth'] = 0.5
mpl.rcParams['figure.autolayout'] = True
mpl.rcParams['keymap.grid'] = ''


class LayerPlot(object):

    def __init__(self, data, cursors=None):
        self._figure = None
        self._axes = None
        self._line = None
        self._cursors = dict()
        self._working_cursor = list()
        self._dragging_cursor = None
        self._data = data
        self._init_plot()
        if cursors is not None:
            for x in cursors:
                self._add_cursor(x)
        plt.show()

    def get_cursors(self):
        cursors = list(sorted(self._cursors.keys()))
        return cursors

    def _init_plot(self):
        nax = len(self._data.columns)
        figsize = (15, nax * 1.5)
        self._figure, self._axes = plt.subplots(figsize=figsize,
                                                nrows=nax,
                                                sharex=True,
                                                )
        x = np.mean(data.index)
        for ax, (c, d) in zip(self._axes, self._data.iteritems()):
            ax.plot(self._data.index, d, 'k-')
            ax.set_ylabel(c)
            ax.set_xlim(self._data.index.min(),
                        self._data.index.max())
            self._working_cursor.append(ax.axvline(x, lw=2,
                                                   ls='dashed',
                                                   zorder=-100))
        self._figure.canvas.mpl_connect('button_press_event',
                                        self._on_click)
        self._figure.canvas.mpl_connect('button_release_event',
                                        self._on_release)
        self._figure.canvas.mpl_connect('motion_notify_event',
                                        self._on_motion)
        self._figure.canvas.mpl_connect('key_press_event',
                                        self._on_keypress)

    def _update_plot(self):
        nlayers = len(self._cursors)
        print('Number of layers: %u' % nlayers)
        self._figure.canvas.draw()

    def _on_keypress(self, event):
        if event.key == 'b':
            x = self._working_cursor[0].get_xdata()
            x = np.clip(x, 0, len(self._data))
            self._add_cursor(x)
        self._update_plot()

    def _add_cursor(self, x):
        lines = list()
        for ax in self._axes:
            lines.append(ax.axvline(x, lw=1, alpha=0.9, color='C1',
                                    zorder=-100, pickradius=2))
        self._cursors[x] = lines

    def _update_working(self, event):
        x = np.clip(event.xdata, 0, len(self._data))
        for c in self._working_cursor:
            c.set_xdata(x)
        self._figure.canvas.draw()

    def _remove_cursor(self, x):
        if x in self._cursors:
            lines = self._cursors.pop(x)
            for line in lines:
                line.axes.lines.remove(line)
        self._update_plot()

    def _find_closest_cursor(self, event):
        for cursor_loc, lines in self._cursors.items():
            for line in lines:
                contains, details = line.contains(event)
                if contains:
                    return cursor_loc
        return None

    def _on_click(self, event):
        # left click
        if event.button == 1 and event.inaxes in self._axes:
            on_cursor = self._find_closest_cursor(event)
            if on_cursor:
                self._dragging_cursor = on_cursor
            else:
                self._update_working(event)
        if event.button == 3 and event.inaxes in self._axes:
            on_cursor = self._find_closest_cursor(event)
            if on_cursor:
                self._remove_cursor(on_cursor)

    def _on_release(self, event):
        in_axis = event.inaxes in self._axes
        if event.button == 1 and in_axis and self._dragging_cursor:
            self._dragging_cursor = None
            self._update_plot()

    def _update_cursor(self, cursor, x):
        lines = self._cursors.pop(cursor)
        x = np.clip(x, 0, len(self._data))
        for line in lines:
            line.set_xdata(x)
        self._cursors[x] = lines
        return x

    def _on_motion(self, event):
        if event.inaxes not in self._axes:
            return
        if not self._dragging_cursor:
            return
        if event.xdata is None or event.ydata is None:
            return
        self._dragging_cursor = self._update_cursor(self._dragging_cursor,
                                                    event.xdata)
        self._update_plot()


if __name__ == '__main__':
    data = pd.DataFrame(data=np.cumsum(np.random.randn(200, 2), axis=0),
                        index=np.linspace(0, 20, 200))
    plot = LayerPlot(data, cursors=None)
    cursors = pd.Series(plot.get_cursors())
    cursors.to_csv('cursours.csv')
    plt.close()

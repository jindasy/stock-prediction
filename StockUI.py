import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import PhotoImage
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry
from stock import *
from company import Company
from threading import Thread
from datetime import date
import sv_ttk


class StockUI(tk.Tk):
    """User interface for stock prediction."""

    def __init__(self):
        super().__init__()
        self.title('Stock Prediction')
        sv_ttk.set_theme('light')
        style = ttk.Style()
        style.configure('TLabelframe.Label', font=('MS Sans Serif', 14, 'italic'))
        # initialize for DataFrame
        self.df = Microsoft()
        self.company = 'Microsoft'
        self.init_component()
        self.init_component_tab1()
        self.init_component_tab2()

    def init_component(self):
        """Create components for main window."""
        self.options = {'padx': 2, 'pady': 2, 'sticky': 'NSEW'}
        self.font = ('MS Sans Serif', 16)

        label = ttk.Label(self, text='Stock Prediction', font=('MS Sans Serif', 30, 'bold'))
        label.grid(row=0, column=0, sticky='NS')

        # create button for change theme
        self.light_photo = PhotoImage(file='pic/light.png')
        self.btn_light = ttk.Button(self, image=self.light_photo)
        self.btn_light.grid(row=0, column=0, padx=60, sticky='NE')
        self.btn_light.bind('<Button-1>', self.change_theme)

        self.dark_photo = PhotoImage(file='pic/dark.png')
        self.btn_dark = ttk.Button(self, image=self.dark_photo)
        self.btn_dark.grid(row=0, column=0, padx=10, sticky='NE')
        self.btn_dark.bind('<Button-1>', self.change_theme)

        # create notebook for contains pages
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky='NSEW')

        self.btn_quit = ttk.Button(self, text='Quit', command=self.destroy)
        self.btn_quit.grid(row=2, column=0, padx=10, pady=5, sticky='E')

        columns, rows = self.grid_size()
        for row in range(rows):
            self.rowconfigure(row, weight=1)
        for col in range(columns):
            self.columnconfigure(col, weight=1)

    def change_theme(self, ev):
        """ Event handler for change theme."""
        if ev.widget == self.btn_light:
            sv_ttk.use_light_theme()
        elif ev.widget == self.btn_dark:
            sv_ttk.use_dark_theme()

    def init_component_tab1(self):
        """Create components and layout for tab1 in notebook."""
        self.frame1 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1, text='Stock')

        # tab 1
        self.filter1 = ttk.LabelFrame(self.frame1, text='Filters', style="TLabelframe")
        self.filter1.grid(row=0, column=2, **self.options)

        # create Combobox from company name
        company1_label = ttk.Label(self.filter1, text='Select Company', font=self.font)
        company1_label.grid(row=1, column=2, **self.options)
        self.company1_filter = ttk.Combobox(self.filter1, state='readonly')
        self.company1_filter['values'] = [company for company, cls in Company()]
        self.company1_filter.set(self.company1_filter['values'][0])
        self.company1_filter.grid(row=2, column=2, **self.options)

        # select data label
        data1_label = ttk.Label(self.filter1, text='Select Data', font=self.font)
        data1_label.grid(row=3, column=2, **self.options)

        # create checkbutton from columns name
        self.data_list = self.df.all_columns()
        self.var1 = {}
        self.btn_data = {}
        row_num = 3

        for data in self.data_list:
            self.var1[data] = tk.IntVar()
            row_num += 1
            self.btn_data[data] = ttk.Checkbutton(self.filter1, text=data, variable=self.var1[data],
                                                  onvalue=1, offvalue=0)
            self.btn_data[data].grid(row=row_num, column=2, **self.options)

        # crate date filter component
        date1_label = ttk.Label(self.filter1, text='Select Date', font=self.font)
        date1_label.grid(row=10, column=2, **self.options)

        date1_from_label = ttk.Label(self.filter1, text='From')
        date1_from_label.grid(row=11, column=2, padx=2, pady=2, sticky='W')
        self.date1_from = DateEntry(self.filter1, selectmode='day')
        self.date1_from.grid(row=11, column=2, padx=10, pady=2, sticky='E')

        date1_to_label = ttk.Label(self.filter1, text='To')
        date1_to_label.grid(row=12, column=2, padx=2, pady=2, sticky='W')
        self.date1_to = DateEntry(self.filter1, selectmode='day')
        self.date1_to.grid(row=12, column=2, padx=10, pady=2, sticky='E')

        # create select filter button to show graph
        self.btn_select1 = ttk.Button(self.filter1, text='Select')
        self.btn_select1.grid(row=13, column=2, padx=5, pady=2, sticky='NS')
        self.btn_select1.bind('<Button-1>', lambda ev: self.progressbar_running(self.update_filters_tab1))

        # create clear filter button
        self.btn_clear1 = ttk.Button(self.filter1, text='Clear')
        self.btn_clear1.grid(row=14, column=2, padx=5, pady=2, sticky='NS')
        self.btn_clear1.bind('<Button-1>', self.clear)

        # create Matplotlib figure and plotting axes
        self.figure1 = Figure()
        self.fig1 = FigureCanvasTkAgg(self.figure1, master=self.frame1)
        self.fig1_axes = self.figure1.add_subplot()
        self.fig1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10,
                                       sticky='NSEW')

        columns, rows = self.grid_size()
        for row in range(rows):
            self.frame1.rowconfigure(row, weight=1)
        for col in range(columns):
            self.frame1.columnconfigure(col, weight=1)

    def init_component_tab2(self):
        """Create components and layout for tab2 in notebook."""
        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2, text='Compare')

        # tab 2
        self.filter2 = ttk.LabelFrame(self.frame2, text='Filters', style="TLabelframe")
        self.filter2.grid(row=0, column=2, **self.options)

        # create Combobox from columns name
        stock_data_label = ttk.Label(self.filter2, text='Select Stock Data', font=self.font)
        stock_data_label.grid(row=1, column=2, **self.options)
        self.stock_data_filter = ttk.Combobox(self.filter2, state='readonly')
        self.stock_data_filter['values'] = [data for data in self.df.all_columns()]
        self.stock_data_filter.set(self.stock_data_filter['values'][0])
        self.stock_data_filter.grid(row=2, column=2, **self.options)

        # select company label
        company_label = ttk.Label(self.filter2, text='Select Company', font=self.font)
        company_label.grid(row=3, column=2, **self.options)

        # create checkbutton from company name
        self.var2 = {}
        self.btn_company = {}
        row_num = 3

        for company, cls in Company():
            self.var2[company] = tk.IntVar()
            row_num += 1
            self.btn_company[company] = ttk.Checkbutton(self.filter2, text=company, variable=self.var2[company],
                                                        onvalue=1, offvalue=0)
            self.btn_company[company].grid(row=row_num, column=2, **self.options)

        # crate date filter component
        date2_label = ttk.Label(self.filter2, text='Select Date', font=self.font)
        date2_label.grid(row=15, column=2, **self.options)

        date2_from_label = ttk.Label(self.filter2, text='From')
        date2_from_label.grid(row=16, column=2, padx=2, pady=2, sticky='W')
        self.date2_from = DateEntry(self.filter2, selectmode='day')
        self.date2_from.grid(row=16, column=2, padx=10, pady=2, sticky='E')

        date2_to_label = ttk.Label(self.filter2, text='To')
        date2_to_label.grid(row=17, column=2, padx=2, pady=2, sticky='W')
        self.date2_to = DateEntry(self.filter2, selectmode='day')
        self.date2_to.grid(row=17, column=2, padx=10, pady=2, sticky='E')

        # create select filter button to show graph
        self.btn_select2 = ttk.Button(self.filter2, text='Select')
        self.btn_select2.grid(row=18, column=2, padx=5, pady=2, sticky='NS')
        self.btn_select2.bind('<Button-1>', lambda ev: self.progressbar_running(self.update_filters_tab2))

        # create clear filter button
        self.btn_clear2 = ttk.Button(self.filter2, text='Clear')
        self.btn_clear2.grid(row=19, column=2, padx=5, pady=2, sticky='NS')
        self.btn_clear2.bind('<Button-1>', self.clear)

        # create Matplotlib figure and plotting axes
        self.figure2 = Figure()
        self.fig2 = FigureCanvasTkAgg(self.figure2, master=self.frame2)
        self.fig2_axes = self.figure2.add_subplot()
        self.fig2.get_tk_widget().grid(row=0, column=0, padx=10, pady=10,
                                       sticky='NEWS')

        columns, rows = self.grid_size()
        for row in range(rows):
            self.frame2.rowconfigure(row, weight=1)
        for col in range(columns):
            self.frame2.columnconfigure(col, weight=1)

    def progressbar(self):
        """Create progressbar components."""
        self.top = tk.Toplevel(self)
        self.top.title('loading')
        self.top.grid()
        self.pgbar = ttk.Progressbar(self.top, length=500, mode='indeterminate')
        self.pgbar.grid(row=0, column=1, sticky='SEW', padx=10)

    def progressbar_running(self, func):
        """ Create thread for running task.

        :param func: str
        """
        self.progressbar()
        self.tab_thread = Thread(target=func())
        self.tab_thread.start()
        self.pgbar.start()
        self.after(10, self.check_task)

    def check_task(self):
        """Checking for update filters and plot graph."""
        self.btn_select1.config(state='disabled')
        self.btn_select2.config(state='disabled')
        if self.tab_thread.is_alive():
            self.after(10, self.check_task)
        else:
            self.pgbar.stop()
            self.top.destroy()
        self.btn_select1.config(state='enabled')
        self.btn_select2.config(state='enabled')

    def update_filters_tab1(self):
        """Get data from filters and plot the graph."""
        self.selected_data_list = []
        for data in self.data_list:
            if self.var1[data].get() == 1:
                self.selected_data_list.append(data)
        # change dataframe
        for company, cls in Company():
            if company == self.company1_filter.get():
                self.df = cls

        self.company = self.company1_filter.get()
        self.plot_one_company()

    def update_filters_tab2(self):
        """Get data from filters and plot the graph."""
        self.selected_company_list = {}
        for company, cls in Company():
            if self.var2[company].get() == 1:
                self.selected_company_list[company] = cls
        self.plot_multi_company()

    def clear(self, ev):
        """Clear all selected data from widget."""
        # clear tab 1
        today = date.today()
        if ev.widget == self.btn_clear1:
            for data in self.data_list:
                self.var1[data].set(0)
            self.fig1_axes.clear()
            self.fig1.draw()
            self.date1_from.set_date(today)
            self.date1_to.set_date(today)
            self.company1_filter.set(self.company1_filter['values'][0])
        # clear tab 2
        elif ev.widget == self.btn_clear2:
            for data in self.var2.keys():
                self.var2[data].set(0)
            self.fig2_axes.clear()
            self.fig2.draw()
            self.date2_from.set_date(today)
            self.date2_to.set_date(today)
            self.stock_data_filter.set(self.stock_data_filter['values'][0])

    def plot_one_company(self):
        """Plot the graph in tab 1 from selected data."""
        self.fig1_axes.clear()
        date_from = self.date1_from.get_date()
        date_to = self.date1_to.get_date()
        df = self.df.get_date(date_from, date_to)
        try:
            df[self.selected_data_list].plot(ax=self.fig1_axes, title=f'{self.company} Stock Prediction',
                                             ylabel='USD')
            self.fig1.draw()
        except TypeError:
            self.error_window('data of stock')

    def plot_multi_company(self):
        """Plot the graph in tab 2 from selected data."""
        self.fig2_axes.clear()
        date_from = self.date2_from.get_date()
        date_to = self.date2_to.get_date()
        data = self.stock_data_filter.get()
        if self.selected_company_list == {}:
            self.error_window('company')
        else:
            for company, cls in self.selected_company_list.items():
                df = cls
                df = df.get_date(date_from, date_to)
                df[data].plot(ax=self.fig2_axes, ylabel='USD', title='Stock Comparison', label=company)
                self.fig2_axes.legend(loc='best')
                self.fig2.draw()

    def error_window(self, word):
        """Messagebox show error when user did not select data."""
        messagebox.showerror(title='Error', message=f'Please select at least 1 {word}!')

    def run(self):
        """Running application."""
        self.mainloop()

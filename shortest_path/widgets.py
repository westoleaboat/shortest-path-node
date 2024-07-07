""" 
shortest-path/widgets.py: file containing the widgets of our app
"""

import tkinter as tk
from tkinter import ttk

from .constants import FieldTypes as FT


class BoundText(tk.Text):
    """A Text widget with a bound variable.

       Add the following to Text widget:
           -pass in a StringVar, which it will be bound to
           -update widget contents whenever the variable is updated;
           for example if loaded in from file or changed by other widget
           -update variable contents whenever widget is updated;
           for example when user types or pastes content into widget

       Override initializer to allow a control variable to be passed in,
       use textvariable argument to pass in a StringVar object

    """

    def __init__(self, *args, textvariable=None, **kwargs):

        super().__init__(*args, **kwargs)
        self._variable = textvariable
        if self._variable:
            # insert any default value
            self.insert('1.0', self._variable.get())
            self._variable.trace_add('write', self._set_content)
            self.bind('<<Modified>>', self._set_var)

    def _set_var(self, *_):
        """Set the variable to the text contents"""
        if self.edit_modified():
            content = self.get('1.0', 'end-1chars')
            self._variable.set(content)
            self.edit_modified(False)

    def _set_content(self, *_):
        """Set the text contents to the variable"""
        self.delete('1.0', tk.END)
        self.insert('1.0', self._variable.get())


class LabelInput(tk.Frame):
    """A widget containing a label and input together.

    Minimal set of arguments may be:

           -parent widget
           -text for the label
           -type of input widget to use
           -dictionary of arguments to pass to input widget

       Call superclass initializer so Frame widget can be constructed.
       Pass parent argument, since that will be the parent widget of
       the Frame itsel, the parent widget for the Label and input
       widget is self, that is, the LabelInput object itself.

       It requires a variable to be bound to each widget (since each
       widget can be bound to one) and an extra dict arg to pass to 
       label widget, in case needed.
       Defaults input_class to ttk.Entry for being the most common case.

       demo:

            AdvancedLabelInput(
                frame, 'Notes',
                input_class=BoundText, var=self._vars['Notes'],
                input_args={"width": 75, "height": 10}
            ).grid(sticky=tk.W + tk.E)

        **Default arguments are evaluated when the function definition is first run. 
        This means that a dictionary object created in the function signature will 
        be the same object every time the function is run, rather than a fresh, 
        empty dictionary each time. 
        Since we want a fresh, empty dictionary each time, we create the dictionaries 
        inside the function body rather than the argument list.

        To use RadioButton widgets with LabelInput, we need to pass in a
        list of values to the input arguments, just as for Combobox.
    """

    # this dictonary act as a key to translate our model's
    # field types into an appropiate widget type
    field_types = {
        FT.long_string: BoundText
    }

    def __init__(
        self, parent, label, var, input_class=ttk.Entry,
        input_args=None, label_args=None, field_spec=None,
        disable_var=None, **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        # save input_var to an instance variable
        self.variable = var
        # save label as property of the variable object
        # to avoid references to LabelInput objects;
        # can access them through variable object if needed.
        self.variable.label_widget = self

        # active disable_var
        self.disable_var = disable_var

        ######################
        # setup the variable #
        ######################
        if input_class in (
            # button classes use variable as the argument name
            ttk.Checkbutton, ttk.Button, ttk.Radiobutton
        ):
            input_args["variable"] = self.variable
        else:
            # others use textvariable
            input_args["textvariable"] = self.variable

        if field_spec:
            field_type = field_spec.get('type', FT.string)
            input_class = input_class or self.field_types.get(field_type)

            if 'min' in field_spec and 'from_' not in input_args:
                input_args['from_'] = field_spec.get('min')
            if 'max' in field_spec and 'to' not in input_args:
                input_args['to'] = field_spec.get('max')
            if 'inc' in field_spec and 'increment' not in input_args:
                input_args['increment'] = field_spec.get('inc')
            if 'values' in field_spec and 'values' not in input_args:
                input_args['values'] = field_spec.get('values')

        ###################
        # setup the label #
        ###################
        if input_class in (ttk.Checkbutton, ttk.Button):
            # Buttons don't need labels, they're built-in
            input_args["text"] = label
        else:
            # add Label widget to first row and column of LabelInput
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=tk.W + tk.E)

        ###################
        # setup the input #
        ###################
        if input_class == ttk.Radiobutton:
            # for Radiobutton, create one input per value
            self.input = tk.Frame(self)  # frame to hold buttons
            # for each value passed add Radiobutton to Frame layout
            for v in input_args.pop('values', []):
                button = ttk.Radiobutton(
                    self.input, value=v, text=v, **input_args
                )
                button.pack(
                    side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x'
                )
        else:
            self.input = input_class(self, **input_args)

        # with self.input created, add to layout
        self.input.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.columnconfigure(0, weight=1)  # fill entire width with column 0

        if disable_var:  # p.154
            self.disable_var = disable_var
            self.disable_var.trace_add('write', self._check_disable)

    def _check_disable(self, *_):
        if not hasattr(self, 'disable_var'):
            return

        if self.disable_var.get():
            self.input.configure(state=tk.DISABLED)
            self.variable.set('')
        else:
            self.input.configure(state=tk.NORMAL)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """override geometry layout default grid"""
        # widget to stick to the left and right sides of container w/ max width possible.
        # rather than passing sticky=(tk.E + tk.W) every time
        super().grid(sticky=sticky, **kwargs)

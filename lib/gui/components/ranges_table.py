from lib.controller.validator import Validator
from lib.gui.components.editable_tree_view import EditableTreeView
from lib.utils import rreal_size


class RangesTable(EditableTreeView):
    INDEX_COL_NAME = 'Ext. Var. No.'
    COLS = {
        'ranges': 'Ranges',
    }
    FROM_TO = 'from-to'
    DEFAULT_VALUE = ['1', '1-9']
    NUM_RANGES = 10

    def __init__(self, master, **kw):
        columns = list(self.COLS.values()) + [f"{i} {self.FROM_TO}" for i in
                                              range(1, self.NUM_RANGES + 1)]
        super().__init__(master, columns=columns, disable_sub_menu=True,
                         index_col_name=self.INDEX_COL_NAME,
                         add_check_box=False,
                         validation_callback=self.validate,
                         **kw)
        for col in columns:
            self.heading(col, text=col, anchor="w")
            self.column(col, width=rreal_size(60), anchor='w')
            self.column(col, stretch=False)
        self.heading('Ranges', anchor='center')

    @staticmethod
    def get_new_row(values_=None):
        if not values_:
            values = RangesTable.DEFAULT_VALUE.copy()
            [values.append('') for _ in range(RangesTable.NUM_RANGES)]
        else:
            values = values_.copy()
            if len(values) <= (RangesTable.NUM_RANGES + 1):
                values += [''] * ((RangesTable.NUM_RANGES + 1) - len(values))
            else:
                raise ValueError(f"Too many ranges for variables")
        return values

    def set_default(self):
        for i in range(len(self)):
            self.set_range(i, self.DEFAULT_VALUE)

    def set_range(self, i: int, values_: list):
        values = self.get_new_row(values_)
        self.set_row(i, values)

    def validate(self, value, col_index, row_values):
        """
        :param value:
        :param col_index: 1 -> n
        :param row_values:
        :return:
        """

        # validate that the value is in the format of %d-%d
        if not value: return True
        if col_index == 1:
            try:
                int(value)
            except:
                return False
            if int(value) > self.NUM_RANGES:
                return False
            non_empty_ranges = [x for x in row_values[1:] if x]
            return len(non_empty_ranges) <= int(value)
        return Validator.validate_range_string(value, col_index - 1,
                                               row_values)

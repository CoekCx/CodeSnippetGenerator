from prompt_toolkit import Application
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.widgets import Frame

from config.prompts import (
    style,
)
from core.benchmark_parser import parse_benchmark_table
from models.benchmark_table import BenchmarkTable, BenchmarkRow, BenchmarkCell


def format_cell(cell: BenchmarkCell) -> str:
    """Formats a cell value with underline indicator if needed."""
    return f"<u>{cell.value}</u>" if cell.is_underlined else cell.value


def select_cells_for_underline(benchmark_table: BenchmarkTable) -> BenchmarkTable:
    """
    Allows user to select which cells should be underlined in the benchmark table.
    Uses keyboard navigation and displays a formatted table.
    """
    current_row = 0
    current_col = 0
    kb = KeyBindings()

    def get_column_widths(table):
        """Calculate optimal column widths for the table"""
        widths = [len(str(header)) for header in table.headers]

        for row in table.rows:
            for i, cell in enumerate(row.sorted_cells(table.headers)[:len(table.headers)]):
                cell_str = str(cell.value) if cell.value is not None else ""
                if i < len(widths):
                    widths[i] = max(widths[i], len(cell_str))

        return widths

    def format_table():
        """Format the entire table with proper alignment and highlighting"""
        widths = get_column_widths(benchmark_table)
        output = []

        header_line = " | ".join(
            str(header).ljust(widths[i])
            for i, header in enumerate(benchmark_table.headers)
        )
        output.append(f"<b>{header_line}</b>")

        separator = "-+-".join("-" * width for width in widths)
        output.append(separator)

        for row_idx, row in enumerate(benchmark_table.rows):
            row_cells = []
            for col_idx, cell in enumerate(row.sorted_cells(benchmark_table.headers)):
                if col_idx >= len(widths):
                    break

                cell_value = str(cell.value if cell.value is not None else "").ljust(widths[col_idx])
                if row_idx == current_row and col_idx == current_col:
                    cell_text = f"<reverse>{cell_value}</reverse>"
                elif cell.is_underlined:
                    cell_text = f"<u>{cell_value}</u>"
                else:
                    cell_text = cell_value
                row_cells.append(cell_text)
            output.append(" | ".join(row_cells))

        return "\n".join(output)

    @kb.add('left')
    def _(event):
        nonlocal current_col
        if current_col > 0:
            current_col -= 1
        event.app.invalidate()

    @kb.add('right')
    def _(event):
        nonlocal current_col
        if current_col < len(benchmark_table.headers) - 1:
            current_col += 1
        event.app.invalidate()

    @kb.add('up')
    def _(event):
        nonlocal current_row
        if current_row > 0:
            current_row -= 1
        event.app.invalidate()

    @kb.add('down')
    def _(event):
        nonlocal current_row
        if current_row < len(benchmark_table.rows) - 1:
            current_row += 1
        event.app.invalidate()

    @kb.add('space')
    def _(event):
        current_cell = benchmark_table.rows[current_row].get_cell_by_header(
            benchmark_table.headers[current_col]
        )
        if current_cell:
            current_cell.is_underlined = not current_cell.is_underlined
        event.app.invalidate()

    @kb.add('enter')
    def _(event):
        event.app.exit()

    layout = Layout(
        HSplit([
            Frame(
                Window(
                    FormattedTextControl(
                        lambda: HTML(format_table())
                    ),
                    wrap_lines=False
                ),
            ),
            Window(
                FormattedTextControl(
                    'Use arrow keys to navigate | SPACE to toggle underline | ENTER to finish'
                ),
                height=1
            ),
        ])
    )

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True,
        mouse_support=True
    )
    app.run()

    return benchmark_table


def select_benchmark_columns(benchmark_table: BenchmarkTable) -> BenchmarkTable:
    """
    Allows user to select which columns to include in the benchmark table.

    Args:
        benchmark_table (BenchmarkTable): The original benchmark table with all columns

    Returns:
        BenchmarkTable: A new benchmark table with only the selected columns
    """
    columns = [(header, header) for header in benchmark_table.headers]

    selected_columns = checkboxlist_dialog(
        title="Select Columns",
        text="Choose which columns to include in the table:",
        values=columns,
        style=style,
        default_values=[header for header in benchmark_table.headers if header not in ("RatioSD", "Alloc Ratio")],
    ).run()

    if not selected_columns:
        return benchmark_table

    new_rows = []
    for row in benchmark_table.rows:
        column_values = {
            "Method": row.method,
            "Mean": row.mean,
            "Error": row.error,
            "StdDev": row.std_dev,
            "Ratio": row.ratio,
            "RatioSD": row.ratio_sd,
            "Allocated": row.allocated,
            "Alloc Ratio": row.alloc_ratio
        }

        new_row = BenchmarkRow(
            method=column_values["Method"],
            mean=column_values["Mean"],
            error=column_values["Error"],
            std_dev=column_values["StdDev"],
            ratio=column_values["Ratio"],
            ratio_sd=column_values["RatioSD"] if "RatioSD" in selected_columns else None,
            allocated=column_values["Allocated"] if "Allocated" in selected_columns else None,
            alloc_ratio=column_values["Alloc Ratio"] if "Alloc Ratio" in selected_columns else None
        )
        new_rows.append(new_row)

    return BenchmarkTable(headers=selected_columns, rows=new_rows)


def process_benchmark_table(benchmark_text: str) -> BenchmarkTable:
    """
    Processes a benchmark table from raw text through a series of transformations.
    
    This function parses the raw benchmark text into a structured table, then allows
    the user to select which columns to include and which cells to underline for emphasis.
    
    Args:
        benchmark_text (str): The raw benchmark results text
        
    Returns:
        BenchmarkTable: A fully processed benchmark table ready for display or export
    """
    benchmark_table = parse_benchmark_table(benchmark_text)
    benchmark_table = select_benchmark_columns(benchmark_table)
    benchmark_table = select_cells_for_underline(benchmark_table)
    return benchmark_table

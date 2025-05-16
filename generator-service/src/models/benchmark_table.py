from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BenchmarkCell:
    """A class representing a single cell in a benchmark table.
    
    This class handles the formatting and display of individual cells, including special
    formatting for underlined values and method names.
    
    Attributes:
        value (str): The content of the cell.
        column_name (str): The name of the column this cell belongs to.
        is_underlined (bool): Whether the cell should be displayed with underlining.
        is_method (bool): Whether the cell contains a method name.
    """
    value: str
    column_name: str
    is_underlined: bool = False
    is_method: bool = False

    def print_cell(self) -> str:
        """Formats the cell content with appropriate HTML styling.
        
        Returns:
            str: HTML-formatted string representation of the cell content.
                If the cell is underlined, it will be wrapped in <u> tags.
                Method cells get an additional class="method" attribute.
        """
        if self.is_underlined:
            if self.is_method:
                return f"<u class=\"method\">{self.value}</u>"
            return f"<u>{self.value}</u>"
        return self.value


@dataclass
class BenchmarkRow:
    """A class representing a row in a benchmark table.
    
    Contains cells for various benchmark metrics including method name, mean,
    error, standard deviation, ratios, and allocation information.
    
    Attributes:
        method (Optional[BenchmarkCell]): Cell containing the method name.
        runtime (Optional[BenchmarkCell]): Cell containing the runtime value.
        mean (Optional[BenchmarkCell]): Cell containing the mean value.
        error (Optional[BenchmarkCell]): Cell containing the error value.
        std_dev (Optional[BenchmarkCell]): Cell containing the standard deviation.
        median (Optional[BenchmarkCell]): Cell containing the median value.
        ratio (Optional[BenchmarkCell]): Cell containing the ratio value.
        ratio_sd (Optional[BenchmarkCell]): Cell containing the ratio standard deviation.
        gen0 (Optional[BenchmarkCell]): Cell containing the gen0 value.
        allocated (Optional[BenchmarkCell]): Cell containing allocation information.
        alloc_ratio (Optional[BenchmarkCell]): Cell containing allocation ratio.
    """
    method: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Method", is_method=True))
    runtime: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Runtime"))
    mean: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Mean"))
    error: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Error"))
    std_dev: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "StdDev"))
    median: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Median"))
    ratio: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Ratio"))
    ratio_sd: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "RatioSD"))
    gen0: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Gen0"))
    allocated: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Allocated"))
    alloc_ratio: Optional[BenchmarkCell] = field(default_factory=lambda: BenchmarkCell(None, "Alloc Ratio"))
    header_not_found: str = "Header not found"

    def get_cell_by_header(self, header: str) -> Optional[BenchmarkCell]:
        """Retrieves a cell based on its header name.
        
        Args:
            header (str): The header name to look up.
            
        Returns:
            Optional[BenchmarkCell]: The corresponding cell if found, None otherwise.
        """
        cell = [cell for cell in self.all_cells if cell.column_name == header]
        return cell[0] if cell else self.header_not_found

    @property
    def all_cells(self) -> List[BenchmarkCell]:
        """Returns a list of all cells in the row.
        
        Returns:
            List[BenchmarkCell]: List of all cells that have values.
        """
        return [cell for cell in [
            self.method,
            self.runtime,
            self.mean,
            self.error,
            self.std_dev,
            self.median,
            self.ratio,
            self.ratio_sd,
            self.gen0,
            self.allocated,
            self.alloc_ratio
        ] if cell is not None]

    @property
    def cells(self) -> List[BenchmarkCell]:
        """Returns a list of all non-None cells in the row.

        Returns:
            List[BenchmarkCell]: List of all cells that have values.
        """
        return [cell for cell in self.all_cells if cell.value is not None]

    def sorted_cells(self, headers: List[str]) -> List[BenchmarkCell]:
        """Returns cells sorted according to the order specified in headers.
        
        Args:
            headers (List[str]): List of header names defining the sort order.
            
        Returns:
            List[BenchmarkCell]: Sorted list of cells based on their column names.
        """
        return sorted(self.cells, key=lambda x: headers.index(x.column_name))


@dataclass
class BenchmarkTable:
    """A class representing a complete benchmark table.
    
    Contains the table headers and rows of benchmark data.
    
    Attributes:
        headers (List[str]): List of column headers for the table.
        rows (List[BenchmarkRow]): List of benchmark rows containing the data.
    """
    headers: List[str]
    rows: List[BenchmarkRow]

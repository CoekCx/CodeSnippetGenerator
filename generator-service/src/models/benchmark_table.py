from dataclasses import dataclass
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
        mean (Optional[BenchmarkCell]): Cell containing the mean value.
        error (Optional[BenchmarkCell]): Cell containing the error value.
        std_dev (Optional[BenchmarkCell]): Cell containing the standard deviation.
        ratio (Optional[BenchmarkCell]): Cell containing the ratio value.
        ratio_sd (Optional[BenchmarkCell]): Cell containing the ratio standard deviation.
        allocated (Optional[BenchmarkCell]): Cell containing allocation information.
        alloc_ratio (Optional[BenchmarkCell]): Cell containing allocation ratio.
    """
    method: Optional[BenchmarkCell] = None
    mean: Optional[BenchmarkCell] = None
    error: Optional[BenchmarkCell] = None
    std_dev: Optional[BenchmarkCell] = None
    ratio: Optional[BenchmarkCell] = None
    ratio_sd: Optional[BenchmarkCell] = None
    allocated: Optional[BenchmarkCell] = None
    alloc_ratio: Optional[BenchmarkCell] = None

    def get_cell_by_header(self, header: str) -> Optional[BenchmarkCell]:
        """Retrieves a cell based on its header name.
        
        Args:
            header (str): The header name to look up.
            
        Returns:
            Optional[BenchmarkCell]: The corresponding cell if found, None otherwise.
        """
        header_to_cell = {
            'Method': self.method,
            'Mean': self.mean,
            'Error': self.error,
            'StdDev': self.std_dev,
            'Ratio': self.ratio,
            'Ratio SD': self.ratio_sd,
            'Allocated': self.allocated,
            'Alloc Ratio': self.alloc_ratio
        }
        return header_to_cell.get(header)

    @property
    def cells(self) -> List[BenchmarkCell]:
        """Returns a list of all non-None cells in the row.
        
        Returns:
            List[BenchmarkCell]: List of all cells that have values.
        """
        return [cell for cell in [
            self.method,
            self.mean,
            self.error,
            self.std_dev,
            self.ratio,
            self.ratio_sd,
            self.allocated,
            self.alloc_ratio
        ] if cell is not None]

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

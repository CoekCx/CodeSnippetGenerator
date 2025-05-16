from typing import List

from models.benchmark_table import BenchmarkRow, BenchmarkTable


def parse_benchmark_table(content: str) -> BenchmarkTable:
    """
    Parses benchmark results from a text file into a BenchmarkTable model.
    
    Args:
        content (str): The raw benchmark results text
        
    Returns:
        BenchmarkTable: A structured representation of the benchmark results
    """
    lines = [line.strip().replace('Â', '') for line in content.strip().split('\n') if line.strip()]

    lines = [line for line in lines if not all(c in '-|' for c in line)]

    headers = [h.strip().replace('Â', '') for h in lines[0].split('|')[1:-1]]

    rows: List[BenchmarkRow] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.split('|')[1:-1]]

        row = BenchmarkRow()
        for cell, header in zip(cells, headers):
            row_cell = row.get_cell_by_header(header)
            if row_cell != BenchmarkRow.header_not_found:
                row_cell.value = cell

        rows.append(row)

    return BenchmarkTable(headers=headers, rows=rows)

from typing import List

from models.benchmark_table import BenchmarkCell, BenchmarkRow, BenchmarkTable


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

        method = BenchmarkCell(value=cells[0], column_name=headers[0], is_method=True)
        mean = BenchmarkCell(value=cells[1], column_name=headers[1])
        error = BenchmarkCell(value=cells[2], column_name=headers[2])
        std_dev = BenchmarkCell(value=cells[3], column_name=headers[3])
        ratio = BenchmarkCell(value=cells[4], column_name=headers[4])
        ratio_sd = BenchmarkCell(value=cells[5], column_name=headers[5])
        allocated = BenchmarkCell(value=cells[6], column_name=headers[6])
        alloc_ratio = BenchmarkCell(value=cells[7], column_name=headers[7])

        row = BenchmarkRow(
            method=method,
            mean=mean,
            error=error,
            std_dev=std_dev,
            ratio=ratio,
            ratio_sd=ratio_sd,
            allocated=allocated,
            alloc_ratio=alloc_ratio
        )
        rows.append(row)

    return BenchmarkTable(headers=headers, rows=rows)

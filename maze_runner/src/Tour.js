import { WALL, START, END, DIRECTIONS } from './Constants';

function isValidCell(matrix, visited, row, col, totalRows, totalCols) {
  return (
    0 <= row &&
    row < totalRows &&
    0 <= col &&
    col < totalCols &&
    matrix[row][col] !== WALL &&
    !visited[row][col]
  );
}

export function visit(matrix, totalRows, totalCols, row, col, visited, depth=0, memo={}) {
  const key = `${row}${col}`;
  if (key in memo && matrix[row][col] !== END) {
    return memo[key];
  }
  memo[key] = null;
  visited[row][col] = true;

  if (matrix[row][col] === END) {
    memo[key] = [true, [[row, col]], depth];
    visited[row][col] = false;
    return memo[key];
  }

  const foundPaths = [];
  const depths = [];

  for (const [dr, dc] of DIRECTIONS) {
    const nextRow = row + dr;
    const nextCol = col + dc;

    if (isValidCell(matrix, visited, nextRow, nextCol, totalRows, totalCols)) {
      const [found, path, maxDepth] = visit(
        matrix,
        totalRows,
        totalCols,
        nextRow,
        nextCol,
        visited,
        depth + 1
      );

      if (found) {
        foundPaths.push([[row, col], ...path]);
        depths.push(maxDepth);
      }
    }
  }

  visited[row][col] = false;

  if (foundPaths.length > 0) {
    const minDepthIdx = depths.indexOf(Math.min(...depths));
    memo[key] = [
      true,
      foundPaths[minDepthIdx],
      depths[minDepthIdx]
    ];
    return memo[key];
  }

  memo[key] = [false, null, null];
  return memo[key];
}

export function findStartCell(matrix) {
    for (let rowIdx = 0; rowIdx < matrix.length; rowIdx++) {
      for (let colIdx = 0; colIdx < matrix[rowIdx].length; colIdx++) {
        if (matrix[rowIdx][colIdx] === START) {
          return [rowIdx, colIdx];
        }
      }
    }
    return [null, null];
  }

// const visited = new Array(totalRows);
// const matrix = [["S", ".", "E"]];

// for (let i = 0; i < totalRows; i++) {
//   visited[i] = new Array(totalCols).fill(false);
// }

// const [startRow, startCol] = findStartCell(matrix);
// const [found, path, depth] = visit(matrix, startRow, startCol, visited);
// console.log(found, path);
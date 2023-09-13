export const WALL = "#";
export const START = "Start";
export const END = "End";
export const ANIMAL = "ANIMAL";
export const MAZES = [
    {
        rows: 1,
        columns: 3,
        matrix: [["Start", ".", "End"]],
        width: 18.3,
        height: 15
    },
    {
        rows: 4,
        columns: 2,
        matrix: [
            [".", "End"],
            ["#", "."], 
            ["#", "#"], 
            [".", "Start"]
        ],
        width: 14.3,
        height: 15
    },
    {
        rows: 3,
        columns: 3,
        matrix: [
                    ["Start", ".", "#"],
                    ["#", ".", "."],
                    ["#", ".", "End"]
                ],
        width: 18.3,
        height: 10
    }
]

export const baseWidth = 6.3;
export const baseHeight = 15;
export const baseUnits = 'rem';
export const SUCCESS = 'Yayy!! Reached the END!';
export const DOOMED = "DOOMED!! Could not find path!!";
export const DIRECTIONS = [
    [0, 1],
    [0, -1],
    [-1, 0],
    [1, 0]
  ];
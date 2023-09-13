export const WALL = "X";
export const START = "Start";
export const END = "End";
export const ANIMAL = "ANIMAL";
export const MAZES = [
    {
        rows: 1,
        columns: 3,
        matrix: [["S", ".", "E"]],
        width: 18.3,
        height: 15
    },
    {
        rows: 4,
        columns: 2,
        matrix: [
            [".", "E"],
            ["#", "."], 
            ["#", "#"], 
            [".", "S"]
        ],
        width: 14.3,
        height: 15
    },
    {
        rows: 3,
        columns: 3,
        matrix: [
                    ["S", ".", "#"],
                    ["#", ".", "."],
                    ["#", ".", "E"]
                ],
        width: 18.3,
        height: 10
    }
]

export const TOURS = [
    ['00', '01', '02'],
    ['31'],
    ['00', '01', '11', '21', '22'],
]

export const baseWidth = 6.3;
export const baseHeight = 15;
export const baseUnits = 'rem';
export const SUCCESS = 'Yayy!! Reached the END!';
export const DOOMED = "DOOMED!! Could not find path!!";
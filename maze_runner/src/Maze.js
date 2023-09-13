import { useEffect, useState, useRef } from 'react';
import Box from './Box';
import { START, END, WALL, ANIMAL, DOOMED, SUCCESS} from './Constants';
import { visit, findStartCell } from './Tour.js';
import audioFile from './jump.mp3';

function Maze({rows, columns, matrix, width, height, nextButtonStateHandler, handleMessage}) {
    const [widthState, setWidthState] = useState(width);
    const [heightState, setHeightState] = useState(height);
    const [rowsState, setRowsState] = useState(rows);
    const [columnsState, setColumns] = useState(columns);
    const [matrixState, setMatrixState] = useState(matrix);
    const [isStartButtonClicked, setStartButtonClicked] = useState(false);
    const [isTourComplete, setTourComplete] = useState(false);
    const [initialBoxValues, setInitialBoxValues] = useState([]);
    const [boxValues, setBoxValues] = useState([]);
    const [tourState, setTourState] = useState(null);

    const computeVisitedMatrix = () => {
      let visited = [];
      for (let i = 0; i < rowsState; i++) {
        visited[i] = new Array(columnsState).fill(false);
      }
      return visited;
    }
    const [visited, setVisited] = useState(null);


    const [style, setStyle] = useState({
        width: `${widthState}rem`,
    });

    const playAudio = () => {
      const audio = new Audio(audioFile);
      audio.play();
    };

    useEffect(() => {
        setStyle({
            width: `${widthState}rem`,
        });
    }, [widthState, heightState]);

    useEffect(() => {
        if(width !== widthState) {
            setWidthState(width);
            
        }
        if(height !== heightState) {
            setHeightState(height);
        }
        if(rows !== rowsState) {
            setRowsState(rows);
        }
        if(columns !== columnsState) {
            setColumns(columns);
        }

        if(matrix !== matrixState) {
            setMatrixState(matrix);
        }

    }, [rows, columns, matrix, width, height]);
    
    useEffect(() => {
      let values = []
      for (let row = 0; row < rowsState; row++) {
        for (let col = 0; col < columnsState; col++) {
          const matrix_val = matrixState[row][col];
          values.push(
            matrix_val === 'S' ? START : (matrix_val === 'E') ? END : (matrix_val === "#") ? WALL : matrix_val
          );
        }
    }
      setInitialBoxValues(values);
    }, [rowsState, columnsState, matrixState]);
  
    useEffect(() => {
        setBoxValues(initialBoxValues);
    }, [initialBoxValues]);

    const doTour = () => {
        let tour = tourState;
        let counter = 0;
        let interval = setInterval(() => {
          if(tour === null) {
            clearInterval(interval);
            return;
          }
          if (tour.length === 0) {
            clearInterval(interval);
            setTourComplete(true);
            handleMessage(DOOMED);
            return;
          }
          if(counter >= tour.length) {
            clearInterval(interval);
            setTourComplete(true);
            handleMessage(SUCCESS);
            return;
          }
          playAudio();
          handleBoxClick(tour[counter]);
          counter += 1;
        }, 1000);
        
      };
  
    const findTour = () => {
      const [startRow, startCol] = findStartCell(matrixState);
      console.log(startRow, startCol, visited, matrix);
      const [found, path, depth] = visit(matrix, rowsState, columnsState, startRow, startCol, visited);
      if(found) {
        let pth = [];
        for(let i=0; i<path.length; i++) {
          let stop = path[i];
          pth.push(`${stop[0]}${stop[1]}`);
        }
        setTourState(pth);
      } else {
        setTourState([]);
      }
    };

    useEffect(() => {
      console.log("After finding tour", tourState);
      doTour();
    },[tourState]);

    useEffect(() => {
      console.log(visited);
      if(visited !== null) {
        console.log("Calling find tour");
        findTour();
      }else {
        console.log("Visited is null");
      }
      
    }, [visited]);

    useEffect(() => { 
      if(isTourComplete) {
        setStartButtonClicked(false);
        nextButtonStateHandler(false);
      }
  
      if(isStartButtonClicked && !isTourComplete) {
        let vst = computeVisitedMatrix();
        console.log("Before find tour", vst);
        setVisited(vst);
      }
    }, [isStartButtonClicked, isTourComplete]);
  
    const handleBoxClick = (pos) => {
      let [r, c] = pos
      let index = parseInt(r)*rowsState + c%columnsState;
  
      const newBoxValues = boxValues.map((value, idx) => {
        if (index === idx && value !== ANIMAL) {
          return ANIMAL;
        }
        return initialBoxValues[idx];
      });
      setBoxValues(newBoxValues);
    };
  
    const handleButtonClick = () => {
      console.log("Button clicked");
      setTourComplete(false);
      setStartButtonClicked(true);
      nextButtonStateHandler(true);
      setBoxValues(initialBoxValues);
    };

    const audioStyle = {
      display: 'none'
    };

    return (
      <>
        <div className="maze" style={style}>
          {boxValues.map((value, index) => (
            <Box
                key={index}
                pos={index}
                width={Math.floor(widthState/(columnsState))}
                height={Math.floor(heightState/(rowsState))}
                value={value}
                handleBoxClick={handleBoxClick}
            />
            ))}
        </div>
        <button id="startButton" disabled={isStartButtonClicked} onClick={handleButtonClick}>GO</button>
        </>
    );
  }
export default Maze;
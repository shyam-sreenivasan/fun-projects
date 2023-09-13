import { useEffect, useState } from 'react';
import Box from './Box';
import { START, END, WALL, ANIMAL, DOOMED, SUCCESS} from './Constants';

function Maze({rows, columns, matrix, width, height, tour, nextButtonStateHandler, handleMessage}) {
    const [widthState, setWidthState] = useState(width);
    const [heightState, setHeightState] = useState(height);
    const [rowsState, setRowsState] = useState(rows);
    const [columnsState, setColumns] = useState(columns);
    const [matrixState, setMatrixState] = useState(matrix);
    const [isStartButtonClicked, setStartButtonClicked] = useState(false);
    const [isTourComplete, setTourComplete] = useState(false);
    const [initialBoxValues, setInitialBoxValues] = useState([]);
    const [boxValues, setBoxValues] = useState([]);
    const [tourState, setTourState] = useState(tour);

    const [style, setStyle] = useState({
        width: `${widthState}rem`,
    });

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

        if(tour !== tourState) {
            setTourState(tour);
        }

    }, [rows, columns, matrix, width, height, tour]);
    
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
          if (tour === null || tour.length === 0) {
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
          
          handleBoxClick(tour[counter]);
          counter += 1;
        }, 1000);
        
      };
  
    useEffect(() => { 
      if(isTourComplete) {
        setStartButtonClicked(false);
        nextButtonStateHandler(false);
      }
  
      if(isStartButtonClicked && !isTourComplete) {
        doTour();
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
      setTourComplete(false);
      setStartButtonClicked(true);
      nextButtonStateHandler(true);
      setBoxValues(initialBoxValues);
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
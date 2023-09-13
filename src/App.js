import logo from './logo.svg';
import './App.css';
import Maze from './Maze';
import { MAZES, TOURS, baseHeight, baseWidth} from './Constants';
import { useState, useEffect } from 'react';

function App() {
  const [mazeCounter, setMazeCounter] = useState(0);
  const [nextButtonDisabled, setNextButtonDisabled] = useState(false);
  const [rows, setRows] = useState(MAZES[0].rows);
  const [columns, setColumns] = useState(MAZES[0].columns);
  const [matrix, setMatrix] = useState(MAZES[0].matrix);
  const [mazeWidth, setMazeWidth] = useState(MAZES[0].columns*baseWidth);
  const [mazeHeight, setMazeHeight] = useState(MAZES[0].rows*baseHeight);
  const [tour, setTour] = useState(TOURS[0]);
  const [isGameOver, setGameOver] = useState(false);
  const [restartButtonDisabled, setRestartButtonDisabled] = useState(true);
  const [message, setMessage] = useState("");

  const handleMessage = (msg) => {
    setMessage(msg);
  };

  useEffect(() => {
    if(mazeCounter >= 0 && mazeCounter < MAZES.length) {
      let maze = MAZES[mazeCounter];
      let curr_tour = TOURS[mazeCounter];
      setRows(maze.rows);
      setColumns(maze.columns);
      setMazeHeight(maze.rows*baseHeight);
      setMazeWidth(maze.columns*baseWidth);
      setMatrix(maze.matrix);
      setTour(curr_tour);
    } else {
      setGameOver(true);
      setRestartButtonDisabled(false);
    }
  }, [mazeCounter]);

  const handleNextButtonClick = () => {
    let mz = mazeCounter + 1;
    setMazeCounter(mz);
    setMessage("");
  };

  const handleNextButtonClickForStartButtonState = (disabled) => {
    setNextButtonDisabled(disabled);
  }

  const maze = <Maze rows={rows} columns={columns} matrix={matrix} width={mazeWidth} height={mazeHeight} tour={tour} nextButtonStateHandler={handleNextButtonClickForStartButtonState} key="maze" handleMessage={handleMessage} />;

  const handleRestartButton = () => {
    setGameOver(false);
    setMazeCounter(0);
    setRestartButtonDisabled(true);
  };

  const getGameState = () => {
    let res = []
    let msgdiv = <h3 id="msg" key="msg">{message}</h3>
    if(!isGameOver) { 
      res.push(maze);
      res.push(<button id="nextButton" disabled={nextButtonDisabled} onClick={handleNextButtonClick} key="nextButton">NEXT</button>);
      res.push(msgdiv)
      return res;
    } 
    res.push(<p key="gameover">Game Over</p>);
    res.push(<p key="restart"><button id="restartButton" disabled={restartButtonDisabled} onClick={handleRestartButton}>RESTART</button></p>);
    return res;
  }
  return (
    <>
      <h2 id="header">The Ultimate Maze Test</h2>
      {getGameState()}
    </>
    
  );
}

export default App;

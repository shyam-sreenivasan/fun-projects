import ANIMALIMAGE from './images/animal.png';
import { ANIMAL } from './Constants';

function Box({width, height, pos, value}) {
    const boxStyle = {
      width: `${width}rem`,
      height: `${height}vh`
    }
  
  function getBoxContent(value) {
    if(value === ANIMAL) {
        return <img className="animalImage" src={ANIMALIMAGE}  alt={value}/>;
    }
    return value;
  }
  
    return (
      <div id={pos} className="box" style={boxStyle}> 
        <div className="boxposition">{pos}</div>
        <div className="boxcontent">{getBoxContent(value)}</div>
        <div className="boxposition hop"></div>
      </div>
    );
  }

export default Box;
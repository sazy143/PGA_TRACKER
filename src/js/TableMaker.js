import React, {Component} from "react";
import ReactDOM from "react-dom";

class TableMaker extends Component {
    constructor(props) {
        super(props)
        this.state = {
            players: props.data.players
        }
    }

    componentDidMount() {
    }

    render() {
        let table;
        if(this.state.players != null){
            let keys = Object.keys(this.state.players);
            let players = this.state.players;
            keys.sort((a,b) => {
                return players[a].rank - players[b].rank;
            });
            table = keys.map( (key,index) => {
                //console.log(key);
                return <tr className='player-row' key={index}>
                            <td>{players[key].position}</td>
                            <td>{key.toUpperCase()}</td>
                            <td>{players[key].score}</td>
                            <td>{players[key].round1}</td>
                            <td>{players[key].round2}</td>
                            <td>{players[key].round3}</td>
                            <td>{players[key].round4}</td>
                            <td>{(parseInt(players[key].round1) | 0)  + (parseInt(players[key].round2) | 0) + (parseInt(players[key].round3) | 0) + (parseInt(players[key].round4) | 0)} </td>
                        </tr>
            });
            console.log();
        }
        
        return(
            <table className='player-table'>
                    <tbody>
                        <tr className='header-row'>
                            <th>Position</th>
                            <th>Name</th>
                            <th>Score</th>
                            <th>Round 1</th>
                            <th>Round 2</th>
                            <th>Round 3</th>
                            <th>Round 4</th>
                            <th>Strokes</th>
                        </tr>
                        {table}
                    </tbody>
                </table>
            
        )
    }

}
export default TableMaker
import React, {Component} from "react";
import ReactDOM from "react-dom";
import fedex from "../jsonFiles/fedex.json"

class LeaderBoard extends Component {
    constructor(){
        super();

        this.state = {
            players: fedex.players
        }
    }
    
    
    render(){
        let table;
        let players = this.state.players;
        let keys = Object.keys(players);
        table = keys.map( (key,index) => {
            return <tr className='player-row' key={index}>
                <td>{players[key].position}</td>
                <td>{key}</td>
                <td>{players[key].points}</td>
                <td>{players[key].events}</td>
            </tr>
        });
        return(
            <div className='page-content'>
                <h1>FedEx Cup Leaderboard</h1>
                <table className='player-table'>
                    <tbody>
                        <tr className='header-row'>
                            <th>Rank</th>
                            <th>Name</th>
                            <th>Points</th>
                            <th>Events Played</th>
                        </tr>
                        {table}
                    </tbody>
             </table>
         
            </div>
        );
    }
}

export default LeaderBoard;
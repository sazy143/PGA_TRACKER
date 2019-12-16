import React, {Component} from "react";
import ReactDOM from "react-dom";
import schedule from "../jsonFiles/schedule.json"

class Future extends Component {
    constructor(){
        super();
        this.state = {
            schedule: schedule
        }
    }
    
    render(){

        let table;
        let schedule = this.state.schedule;
        let keys = Object.keys(schedule);
        table = keys.map( (key,index) => {
            return <tr className='player-row' key={index}>
                <td>{schedule[key].date}</td>
                <td>{key}</td>
                <td>{schedule[key].purse ? '$'+schedule[key].purse : 'purse not listed yet'}</td>
                <td>{schedule[key].points ? schedule[key].points : '0'}</td>
            </tr>
        });
        
        return(
            <div className='page-content'>
                <h1>Future Tournaments</h1>
                <table className='player-table'>
                    <tbody>
                        <tr className='header-row'>
                            <th>date</th>
                            <th>Tournament</th>
                            <th>Purse</th>
                            <th>FedEx points</th>
                        </tr>
                        {table}
                    </tbody>
                </table>
            </div>
        );
        
    }
    
}

export default Future;